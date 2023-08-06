
from generalfile import Path
from generallibrary import deco_cache, Timer


class _PackagerFiles:
    @classmethod
    def create_blank_locally_python(cls, path, install=True):
        """ Create a new general package locally only.
            Todo: Fix create_blank, it overwrites current projects pip install.

            :param generalpackager.Packager or Any cls:
            :param Path or str path:
            :param install: Whether to pip install. """
        path = Path(path)
        assert path.empty()
        packager = cls(name=path.name(), path=path, target=cls.Targets.python)

        packager.localrepo.metadata.write_config()
        packager.generate_localfiles()

        if install:
            packager.localrepo.pip_install_editable()
        # new_self = packager.get_new_packager()  # Reset caches to get updated files
        # new_self.generate_localfiles()
        return packager

    @deco_cache()
    def _compare_local(self, platform, aesthetic):
        """ :param generalpackager.Packager self: """
        def filt(path):
            """ Filter to return True for files we want to compare. """
            if path.match(*self.git_exclude_lines):
                return False
            if aesthetic is not None:
                file = self.get_file_from_path(path=path)
                if file is None:
                    return True  # Probably a python file
                return file.aesthetic is aesthetic
            return True

        unpack_target = Path.get_cache_dir() / "Python"
        package_path = platform.download(path=unpack_target, overwrite=True)
        return self.path.get_differing_files(target=package_path, filt=filt)

    def compare_local_to_github(self, aesthetic=None):
        """ Get a list of changed files compared to remote with optional aesthetic files.

            :param generalpackager.Packager self:
            :param aesthetic: """
        return self._compare_local(platform=self.github, aesthetic=aesthetic)

    def compare_local_to_pypi(self, aesthetic=None):
        """ Get a list of changed files compared to pypi with optional aesthetic files.

            :param generalpackager.Packager self:
            :param aesthetic: """
        return self._compare_local(platform=self.pypi, aesthetic=aesthetic)

    def _error_on_change(self, files):
        """ :param generalpackager.Packager self: """
        file_paths = {file.path for file in files}
        changed_files = {path.absolute() for path in self.localrepo.git_changed_files()}

        changed_generated_files = file_paths.intersection(changed_files)
        if changed_generated_files:
            raise EnvironmentError(f"Files changed: {changed_generated_files}")

    def generate_localfiles(self, include_aesthetic=True, print_out=False, error_on_change=False):
        """ Generate all local files.
            Returns True if any file is changed.

            :param generalpackager.Packager self: """
        with Timer(print_out=print_out):
            # Not in files because it writes with json not text, it's also a bit unique
            self.localrepo.metadata.name = self.name
            self.localrepo.metadata.write_config()

            files = [file for file in self.get_files() if include_aesthetic or not file.aesthetic]

            for file in files:
                file.generate()

        if error_on_change and "[CI SKIP]" not in self.localrepo.get_commit_message():
            self._error_on_change(files=files)

























