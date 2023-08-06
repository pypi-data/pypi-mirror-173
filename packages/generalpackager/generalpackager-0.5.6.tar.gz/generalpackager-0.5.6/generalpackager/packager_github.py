from generallibrary import deco_cache
from git import Git

from github import Github

from generalpackager import PACKAGER_GITHUB_API


class _PackagerGitHub:
    """ Sync metadata. """
    def sync_github_metadata(self):
        """ Sync GitHub with local metadata.

            :param generalpackager.Packager self: """
        assert self.github.set_website(self.pypi.url).ok
        assert self.github.set_description(self.localrepo.metadata.description).ok
        assert self.github.set_topics(*self.get_topics()).ok

    @property
    @deco_cache()
    def remote(self):
        """ :param generalpackager.Packager self: """
        remote = self.localrepo.repo.remote()
        remote.set_url(f"https://Mandera:{PACKAGER_GITHUB_API}@github.com/{self.github.owner}/{self.name}.git")
        return remote

    def push(self, tag=None):
        """ Might want to catch OSError - # Just suppressing weird invalid handle error

            :param generalpackager.Packager self: """
        if tag:
            tag = self.localrepo.repo.create_tag(f"v{self.localrepo.metadata.version}", force=True)
        else:
            tag = None
        return self.remote.push(refspec=tag)

    def commit_and_push(self, message=None, tag=None):
        """ Commit and push this local repo to GitHub.
            Return short sha1 of pushed commit.

            Todo: commit-hook failed for auto commit "not a valid Win32 application"

            :param generalpackager.Packager self: """
        # Bad hard-coded quick fix
        if "Sync" in message and tag:
            message = message.replace("Sync", "Publish")

        self.localrepo.commit(message=message)
        self.push(tag=tag)

    def enable_vcs_operations(self):
        """ :param generalpackager.Packager self: """
        Git(str(self.path)).init()
        # self.localrepo.get_repo().git.add(A=True)
        # repo = self.localrepo.get_repo()

    def create_github_repo(self):
        """ :param generalpackager.Packager self: """
        g = Github(PACKAGER_GITHUB_API.value)

        manderageneral = g.get_organization("ManderaGeneral")

        repo = manderageneral.create_repo(
            name=self.name,
            private=self.localrepo.metadata.private,
        )
        repo = manderageneral.get_repo(self.name)
        # repo.create_git_ref()
        # print(repo.master_branch)
        # print(list(repo.get_branches()))

    def create_master_branch(self):
        """ :param generalpackager.Packager self: """
        repo = self.localrepo.repo
        # Create remote somehow first
        print(repo.remote().push("head"))

    # Todo: Setup env vars for project.






