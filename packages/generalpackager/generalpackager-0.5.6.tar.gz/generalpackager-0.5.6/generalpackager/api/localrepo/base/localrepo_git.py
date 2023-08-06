
from generallibrary import deco_cache
from generalfile import Path
from git import Repo, InvalidGitRepositoryError, NoSuchPathError
import re


class _LocalRepo_Git:
    def get_commit_message(self):
        """ :param generalpackager.LocalRepo self: """
        return self.commit_editmsg_file.path.text.read()

    def init_repo(self):
        """ :param generalpackager.LocalRepo self: """
        return Repo.init(str(self.path))

    @property
    @deco_cache()
    def repo(self):
        """ Return existing or new repo.

            :param generalpackager.LocalRepo self: """
        try:
            return Repo(str(self.path))
        except (InvalidGitRepositoryError, NoSuchPathError):
            return self.init_repo()

    def commit(self, message=None):
        """ :param generalpackager.LocalRepo self: """
        self.repo.git.add(A=True)
        self.repo.index.commit(message=str(message) if message else "No commit message.")

    @property
    def commit_sha(self):
        """ Defaults to 'master' if missing.

            :param generalpackager.LocalRepo self: """
        try:
            return self.repo.head.object.hexsha
        except ValueError:
            return "master"

    @property
    def commit_sha_short(self):
        """ Defaults to 'master' if missing.

            :param generalpackager.LocalRepo self: """
        return self.commit_sha[0:8]

    def git_changed_files(self):
        """ Get a list of relative paths changed files using local .git folder.

            :param generalpackager.LocalRepo self: """
        return [Path(file) for file in re.findall("diff --git a/(.*) " + "b/", self.repo.git.diff())]






























