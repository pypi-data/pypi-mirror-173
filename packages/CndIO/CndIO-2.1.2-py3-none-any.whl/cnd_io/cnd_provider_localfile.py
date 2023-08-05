from os.path import exists
from cnd_io.cnd_provider import CndProvider


class CndProviderLocalfile(CndProvider):
    def _full_path(selft, source_name, file_name):
        return f"{source_name}/{file_name}"

    def pull_file(self, source_name, file_name, **kwargs):
        self._print_me("trace_c", f"Opening file {self._full_path(source_name, file_name)} now")
        f = open(self._full_path(source_name, file_name), "r")
        return f.read()

    def push_file(self, source_name, file_name, content, **kwargs):
        self._print_me("trace_c", f"Creation file {self._full_path(source_name, file_name)} now")
        with open(self._full_path(source_name, file_name), 'w') as f:
            f.write(content)
        return True

    def push_files(self, source_name, files, **kwargs):
        for file_name in files:
            self.push_file(source_name, file_name, files[file_name])
        return True

    def file_exist(self, source_name, file_name, **kwargs):
        self._print_me("trace_c", f"Checking file {self._full_path(source_name, file_name)} now")
        return exists(self._full_path(source_name, file_name))
