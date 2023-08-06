from generallibrary import CodeLine

from generalpackager.api.shared.files.file import File


class RandomtestingFile(File):
    _relative_path = "randomtesting.py"
    aesthetic = True
    overwrite = False

    def _generate(self):
        codeline = CodeLine(f"from {self.packager.name} import *", space_before=1, space_after=50)
        return codeline

