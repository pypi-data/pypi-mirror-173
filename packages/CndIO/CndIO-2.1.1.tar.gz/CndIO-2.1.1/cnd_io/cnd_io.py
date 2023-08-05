from cnd_io.__version__ import (
    __version__,
)
import yaml


class CndIO:
    def __init__(self, provider, print):
        self._print = print
        self._print.info_v(f"CndIO Version {__version__}")
        self._provider = provider
        self._cached_file = {}
        self._files = {}

    def _uuid(self, source_name, file_name, branch='main'):
        return f"{source_name}:{file_name}:{branch}"

    def pull_file(self, source_name, file_name, branch='main'):
        if self._uuid(source_name, file_name, branch=branch) not in self._cached_file:
            if self._provider.file_exist(source_name, file_name, branch=branch) is False:
                return False
            self._cached_file[self._uuid(source_name, file_name, branch=branch)] = self._provider.pull_file(source_name, file_name, branch=branch)
        return self._cached_file[self._uuid(source_name, file_name, branch=branch)]

    def commit_file(self, source_name, file_name, content, branch='main'):
        if source_name not in self._files:
            self._files[source_name] = {}
        if branch not in self._files[source_name]:
            self._files[source_name][branch] = {}
        self._files[source_name][branch][file_name] = content
        return len(self._files[source_name][branch])

    def commit_yaml_file(self, source_name, file_name, content, branch='main'):
        return self.commit_file(source_name, file_name, yaml.dump(content), branch='main')

    def push_files(self, source_name, branch='main', commit_message="It's a so nice day today"):
        if source_name not in self._files:
            return None
        if branch not in self._files[source_name]:
            return None            
        return self._provider.push_files(source_name, self._files[source_name][branch], commit_message=commit_message)

    def push_file(self, source_name, file_name, content, branch='main', commit_message="It's a so nice day today"):
        if self._provider.push_file(source_name, file_name, content, branch=branch, commit_message=commit_message) is True:
            self._cached_file[self._uuid(source_name, file_name, branch=branch)] = content
            return True
        else:
            return False

    def pull_yaml_file(self, source_name, file_name, branch='main'):
        content = self.pull_file(source_name, file_name, branch=branch)
        if content is False:
            return False
        return yaml.safe_load(content)

    def push_yaml_file(self, source_name, file_name, content, branch='main'):
        return self.push_file(source_name, file_name, yaml.dump(content), branch=branch)
