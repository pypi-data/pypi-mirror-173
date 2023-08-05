# import verser
from verserLocal.verser_ import *

n = get_next_version(verbose=True,
                     project=Project(package_name="verser",
                                     version_file_path=Path("verserLocal\__version__.py")
                                     )

                     )
print(n)
