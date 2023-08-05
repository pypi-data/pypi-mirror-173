# import verser
from verserLocal.verser_ import *

project = Project(package_name="verser",
                  version_file_path=Path() /  "__version2__.py",

                  )
n = get_next_version(verbose=True,
                     project=project

                     )
print(n)
print(project.version_file_path.absolute())
# assert project.version_file_path.is_file(), project.version_file_path
