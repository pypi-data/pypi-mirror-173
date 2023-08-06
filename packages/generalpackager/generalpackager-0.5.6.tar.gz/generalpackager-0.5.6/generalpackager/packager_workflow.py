
from generalfile import Path
from generallibrary import EnvVar, Log


class _PackagerWorkflow:
    def run_ordered_methods(self, *funcs):
        """ :param generalpackager.Packager self: """
        order = self.get_ordered_packagers()
        for func in funcs:
            for packager in order:
                func(packager)

    def workflow_unittest(self):
        """ :param generalpackager.Packager self: """
        Log().debug("Working dir for workflow_unittest:", Path().absolute())

        self.run_ordered_methods(
            lambda packager: packager.generate_localfiles(include_aesthetic=False),
            lambda packager: packager.localrepo.unittest(),
        )

    def workflow_sync(self):
        """ Runs in workflow once Packagers have created each LocalRepo from the latest master commit.
            It can generate new workflow, compare, and then stop workflow after commiting and pushing.

            :param generalpackager.Packager self: """
        trigger_repo = str(EnvVar('GITHUB_REPOSITORY')).split('/')[1]
        msg1 = f"[CI AUTO] For commit sha reference"
        msg2 = f"[CI AUTO] Sync triggered by {trigger_repo}"

        any_bumped = any(self.general_bumped_set())

        self.run_ordered_methods(
            lambda packager: packager.if_publish_bump(any_bumped=any_bumped),
            lambda packager: packager.generate_localfiles(include_aesthetic=False),
            lambda packager: packager.localrepo.unittest(),  # Will set coverage percentage
            lambda packager, msg=msg1: packager.localrepo.commit(message=msg),  # Will update commit_sha
            lambda packager: packager.generate_localfiles(include_aesthetic=True),  # With coverage number and commit_sha
            lambda packager, msg=msg2: packager.commit_and_push(message=msg, tag=packager.is_bumped()),
            lambda packager: packager.if_publish_upload(),
            lambda packager: packager.sync_github_metadata(),
        )

        for summary_packager in self.summary_packagers():
            summary_packager.upload_package_summary(msg=msg1)

    def upload_package_summary(self, msg):
        """ :param generalpackager.Packager self: """
        self.org_readme_file.generate()
        self.commit_and_push(message=msg)

    def if_publish_bump(self, any_bumped):
        """ Bump if updated and any other Packager is bumped.

            :param generalpackager.Packager self: """
        if any_bumped and not self.is_bumped() and self.compare_local_to_pypi(aesthetic=False):
            self.localrepo.bump_version()

    def if_publish_upload(self):
        """ Only does anything if bumped.
            Upload to PyPI unless private.
            Upload exe if exetarget.py exists.

            :param generalpackager.Packager self: """
        if self.is_bumped() and not self.localrepo.metadata.private:
            self.localrepo.upload()

        # if self.localrepo.get_exetarget_path().exists():
        #     self.localrepo.generate_exe()
        #     MainframeClient().upload_exe(exe_path=self.localrepo.get_exeproduct_path(), name=self.name, version=self.localrepo.metadata.version)








