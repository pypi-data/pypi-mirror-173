from generallibrary import CodeLine, comma_and_and

from generalpackager.api.shared.files.file import File


class WorkflowFile(File):
    _relative_path = ".github/workflows/workflow.yml"
    aesthetic = True

    def _generate(self):
        workflow = CodeLine()
        workflow.indent_str = " " * 2

        workflow.add_node(self._get_name())
        workflow.add_node(self._get_triggers())
        workflow.add_node(self._get_defaults())

        jobs = workflow.add_node("jobs:")
        jobs.add_node(self._get_unittest_job())
        jobs.add_node(self._get_sync_job())

        return workflow

    PIP_NECESSARY_PACKAGES = (
        "setuptools",
        "wheel",
        "twine",
    )

    _commit_msg = "github.event.head_commit.message"
    _action_checkout = "actions/checkout@v2"
    _action_setup_python = "actions/setup-python@v2"
    _action_setup_ssh = "webfactory/ssh-agent@v0.5.3"
    _matrix_os = "matrix.os"
    _matrix_python_version = "matrix.python-version"

    @staticmethod
    def _var(string):
        return f"${{{{ {string} }}}}"

    @staticmethod
    def _commit_msg_if(*literals, **conditions):
        checks = [f"contains(github.event.head_commit.message, '[CI {key}]') == {str(value).lower()}" for key, value in conditions.items()]
        checks += list(literals)
        return f"if: {' && '.join(checks)}"

    def _get_name(self):
        name = CodeLine("name: workflow")
        return name

    def _get_triggers(self):
        on = CodeLine("on: push", space_after=1)
        return on

    def _get_defaults(self):
        defaults = CodeLine("defaults:")
        defaults.add_node("run:").add_node("working-directory: ../../main", space_after=1)
        return defaults

    def _get_step(self, name, *codelines):
        step = CodeLine(f"- name: {name}")
        for codeline in codelines:
            if codeline:
                step.add_node(codeline)
        return step

    def _step_make_workdir(self):
        step = CodeLine("- name: Create folder")
        step.add_node("working-directory: ../../")
        step.add_node("run: mkdir main")
        return step

    def _step_setup_ssh(self):
        with_ = CodeLine("with:")
        with_.add_node("ssh-private-key: ${{ secrets.GIT_SSH }}")
        return self._get_step(f"Set up Git SSH", f"uses: {self._action_setup_ssh}", with_)

    def _step_setup_python(self, version):
        with_ = CodeLine("with:")
        with_.add_node(f"python-version: '{version}'")
        return self._get_step(f"Set up python version {version}", f"uses: {self._action_setup_python}", with_)

    def _step_install_necessities(self):
        run = CodeLine("run: |")
        run.add_node("python -m pip install --upgrade pip")
        run.add_node(f"pip install {' '.join(self.PIP_NECESSARY_PACKAGES)}")
        return self._get_step(f"Install necessities pip, setuptools, wheel, twine", run)

    def _step_install_package_pip(self, *packagers):
        """ Supply Packagers to create pip install steps for. """
        names = [p.name for p in packagers]
        run = CodeLine(f"run: pip install {' '.join(names)}")
        return self._get_step(f"Install pip packages {comma_and_and(*names, period=False)}", run)

    def _step_clone_repos(self):
        """ Supply Packagers to create git install steps for. """
        packagers = self.packager.get_ordered_packagers(include_private=False, include_summary_packagers=True)

        step = CodeLine(f"- name: Clone {len(packagers)} repos")
        run = step.add_node(f"run: |")

        for packager in packagers:
            run.add_node(packager.github.git_clone_command)
        return step

    def _step_install_repos(self):
        """ Supply Packagers to create git install steps for. """
        packagers = self.packager.get_ordered_packagers(include_private=False)

        step = CodeLine(f"- name: Install {len(packagers)} repos")
        run = step.add_node(f"run: |")

        for packager in packagers:
            if packager.target == packager.Targets.python:
                run.add_node(f"pip install -e {packager.name}[full]")
        return step

    def _get_env(self):
        env = CodeLine("env:")
        for packager in self.packager.get_all():
            for env_var in packager.localmodule.get_env_vars(error=False):
                if env_var.actions_name and env_var.name not in str(env):  # Coupled to generallibrary.EnvVar
                    env.add_node(f"{env_var.name}: {env_var.actions_name}")
        if not env.get_children():
            return None
        return env

    def _steps_setup(self, python_version):
        steps = CodeLine("steps:")
        steps.add_node(self._step_make_workdir())
        steps.add_node(self._step_setup_ssh())
        steps.add_node(self._step_setup_python(version=python_version))
        steps.add_node(self._step_install_necessities())
        steps.add_node(self._step_clone_repos())
        steps.add_node(self._step_install_repos())
        return steps

    def _get_strategy(self):
        strategy = CodeLine("strategy:")
        matrix = strategy.add_node("matrix:")
        matrix.add_node(f"python-version: {list(self.packager.python)}")
        matrix.add_node(f"os: {[f'{os}-latest' for os in self.packager.os]}".replace("'", ""))
        return strategy

    def _get_unittest_job(self):
        job = CodeLine("unittest:")
        job.add_node(self._commit_msg_if("github.ref == 'refs/heads/master'", SKIP=False, AUTO=False))
        job.add_node(f"runs-on: {self._var(self._matrix_os)}")
        job.add_node(self._get_strategy())

        python_version = self._var(self._matrix_python_version)
        steps = job.add_node(self._steps_setup(python_version=python_version))
        steps.add_node(self._step_run_packager_method("workflow_unittest"))
        return job

    def _get_sync_job(self):
        job = CodeLine("sync:")
        job.add_node("needs: unittest")
        job.add_node(f"runs-on: ubuntu-latest")
        steps = job.add_node(self._steps_setup(python_version=self.packager.python[0]))
        steps.add_node(self._step_run_packager_method("workflow_sync"))
        return job

    def _step_run_packager_method(self, method):
        run = CodeLine(f'run: |')
        run.add_node(f'python -c "from generalpackager import Packager; Packager().{method}()"')
        return self._get_step(f"Run Packager method '{method}'", run, self._get_env())

