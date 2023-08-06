from dataclasses import dataclass


@dataclass
class PyPI:
    
    path_repository: str = None
    path_setup_file: str = None
    path_init_file: str = None
    path_distribution_folder: str = None
    path_egg_folder: str = None
    first_run: bool = None
    _old_version: str = None
    _new_version: str = None
    
    
    def print_file(self, path_file):
        
        with open(path_file, 'r') as file:
            print(file.read())
    
    
    def _generate_versions(self):
        
        with open(self.path_setup_file, 'r') as file:
            list_lines = [line.strip('\n') for line in file.readlines()]
            version = [line for line in list_lines if 'version' in line][0]
            self._old_version = version.strip('version = ')
            version = int(self._old_version.replace('.', ''))
            version = (version if self.first_run else version + 1)
            list_version = [f'.{v}' for v in str(version)]
            new_version = '0.0' + ''.join(list_version)
            self._new_version = new_version[-5:]
    
    
    def _update_version(self, path):
        
        with open(path, 'r') as file_read:
            content = (
                file_read
                .read()
                .replace(self._old_version, self._new_version)
            )
            with open(path, 'w') as file_write:
                file_write.write(content)
    
    
    def update_version_in_files(self):
        
        self._generate_versions()
        self._update_version(self.path_setup_file)
        self._update_version(self.path_init_file)

