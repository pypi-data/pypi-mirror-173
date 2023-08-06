from logging import getLogger

from generalfile import Path
from generallibrary import deco_cache

from generalpackager.api.localrepo.base.targets import Targets


class DynamicRelativePath:
    def __get__(self, instance, owner):
        if instance:
            return Path(instance._relative_path)
        else:
            assert not instance.requires_instance(), f"Only an instantialized Packager can access '{owner.__name__}'."
            return Path(owner._relative_path)


class File:
    """ Instantiated if its owner is. """
    targets = Targets

    _relative_path = ...
    aesthetic = ...

    remove = False
    overwrite = True
    is_file = True
    target = Targets.python  # Should probably default to None, and then I put python on most files

    def _generate(self):
        return ""

    def __init__(self, owner):
        """ :param generalpackager.Packager or generalpackager.LocalRepo owner: """
        self.owner = owner
        self.packager = owner if type(owner).__name__ == "Packager" else None
        self.localrepo = self.packager.localrepo if self.packager else owner

    relative_path = DynamicRelativePath()

    @classmethod
    def requires_instance(cls):
        return hasattr(cls._relative_path, "fget")

    @property
    @deco_cache()
    def path(self):
        return self.owner.path / self._relative_path

    def can_write(self):
        return (
            self.is_file and
            not self.remove and
            type(self)._generate is not File._generate and
            self.target == self.owner.target and
            (self.overwrite is True or not self.path.exists())
        )

    def generate(self):
        logger = getLogger(__name__)
        if self.can_write():
            logger.info(f"Writing to '{self.relative_path}' for '{self.owner.name}'")
            return self.path.text.write(text=f"{self._generate()}\n", overwrite=self.overwrite)
        elif self.remove:
            logger.info(f"Deleting '{self.relative_path}' for '{self.owner.name}'")
            self.path.delete()

    def __str__(self):
        return f"<File: {self.owner.name} - {self.relative_path}>"
