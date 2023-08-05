import random
from .common.colors import *

from dataclasses import dataclass
from pathlib import Path
from dataclasses import dataclass
from .common.files import Read, Write
import typing as t
import random

# ------------------ CONFIGURATION --------------------------------------------
#
DEFAULT_START_VERSION = "0.0.0.0"


# ------------------------------------------- (Class) VersionParts
@dataclass
class VersionParts:
    major: int
    minor: int
    patch: int
    patch2: int
    extra: int = 0
    pre_release: bool = True
    version = ""

    def make_int(self, item: t.Union[str, int]):
        if isinstance(item, str):
            return int(item)
        return item

    def __post_init__(self):
        items = ("major", "minor", "patch", "patch2", "extra")
        for item in items:
            setattr(self, item, self.make_int(getattr(self, item)))
        self.combine()

    def combine(self):
        if self.pre_release:
            pre = "rc"
            self.version = f"{self.major}.{self.minor}.{self.patch}.{self.patch2}{pre}{self.extra}"
            return
        self.version = f"{self.major}.{self.minor}.{self.patch}.{self.patch2}"

    def __str__(self):
        return self.version


# ------------------------------------------- (Class) Project
@dataclass
class Project():
    """Project"""
    package_name: str = "XYZ"
    default_version: str = DEFAULT_START_VERSION
    version_file_path: t.Union[str, Path] = None
    now_testing: bool = False
    version: VersionParts = None
    next_version: VersionParts = None
    """
    Project (Class)
    @attrs
        package_name: str => package name  
        ------------
        default_version: str  => 
        ------------
            if there is not a version file yet this will be used to start a version number 
            default is : 0.0.0.0    
                    (when incremented with function below it will be 0.0.0.1 or 0.0.0.1rc1 )
            
        version_file_path: Union[str, Path] => 
        ------------
            Version file address : this will be used to read current version  
          
        now_testing: bool => default : False 
        ------------
            this will be set True while testing development 
    
    """

    def __post_init__(self):
        if isinstance(self.version_file_path, str):
            self.version_file_path = Path(self.version_file_path)


# ------------------------------------------- () mock_versions

# test = False
mock_versions = {
    0: "1.0.17.2",
    1: "1.0.17.3rc2",
    2: "1.0.17.8rc6",
    3: "1.0.17.7",
    4: "1.0.17.9rc2",
    5: "1.0.17.9rc8",
}


# ------------------------------------------- (fnc) mock_read

def mock_read(*args, **kwargs) -> str:
    x = random.choice(tuple(mock_versions.keys()))
    return mock_versions[x]


def increment(next_status: bool, prev_instance: VersionParts) -> VersionParts:
    major = prev_instance.major
    minor = prev_instance.minor
    patch = prev_instance.patch
    patch2 = prev_instance.patch2
    extra = prev_instance.extra
    if next_status and prev_instance.pre_release:
        # 1.3rc3<=#1.3rc2
        extra = extra + 1
    if next_status and not prev_instance.pre_release:
        # 1.4rc1<=#1.3
        patch2 = patch2 + 1
        extra = 1
    if not next_status and not prev_instance.pre_release:
        # 1.4<=#1.3
        patch2 = patch2 + 1
        extra = 0
    if not next_status and prev_instance.pre_release:
        # 1.3<=#1.3rc2
        patch2 = patch2 + 0
        extra = 0
    new_element = VersionParts(major, minor, patch, patch2, extra, next_status)
    return new_element


# ------------------------------------------- (fnc) create_version_instance

def create_version_instance(version: str, project: Project = Project()) -> VersionParts:
    """creates versionParts instance from string  """
    if not len(version.split(".")) > 3:
        print_with_failure_style(
            f"version : {version} does not fit to PEP. Continues with default start.{DEFAULT_START_VERSION}")
        version = DEFAULT_START_VERSION
    version = version.lower().replace("#", "").strip().replace("'", "")
    if "rc" in version.lower():
        status_pre = True
        # 1.0.17.6rc2
        major, minor, patch, e = version.split(".")
        sp = e.split("rc")
        patch2 = int(sp[0])
        extra = int(sp[1])
    else:
        # 1.0.17.6
        status_pre = False
        try:
            major, minor, patch, patch2 = version.split(".")
        except Exception as exc:
            print(exc)
            print(version)
            major, minor, patch, patch2 = project.default_version.split(".")
        extra = 0
    instance = VersionParts(major, minor, patch, patch2, extra=extra, pre_release=status_pre)
    return instance


class VersionNotFound(BaseException):
    """Version file not found """

    def __int__(self, *args):
        self.msg = f"Could find a proper version file, path may be given incorrectly path:  {', '.join(args)}"
        self.args = args

    def __str__(self):
        return self.msg


def get_previous(project):
    def local_read_fn(x: any = None):
        if project.now_testing:
            """ for pytest """
            return lambda x: mock_read(x)
        """for production"""
        return lambda x: Read(x)

    if not project.version_file_path:
        project.version_file_path = Path() / project.package_name / "__version__.py"
    if project.version_file_path.is_file():
        c = local_read_fn()(project.version_file_path)
        c = c.replace("version", "")
        c = c.replace("=", "").strip()
        print(c, "xx")
    else:
        if not project.now_testing:
            print(project.version_file_path, "not a file ")
            return project.default_version
            # raise VersionNotFound(project.version_file_path)
    return c


def get_prev_version_instance(project):
    previous_version = project.default_version
    try:
        previous_version = get_previous(project)
    except  VersionNotFound:
        ...
        previous_version = project.default_version
        # raise "could not read"
        # previous_version = project.default_version
    except Exception as exc:
        print(exc)
        previous_version = project.default_version
    return create_version_instance(previous_version, project)


def check_and_write(project: Project, version: VersionParts):
    """check_and_write create version file __version__.py"""
    try:
        Write(project.version_file_path, f"#{version}")
        print(f"version file was created...\n  {project.version_file_path} : project.next_version")
    except:
        print(f"version file was not created...\n  {project.version_file_path} : project.next_version")


# ---------------------------------------------------------------------
#               M A I N
# ---------------------------------------------------------------------
def get_next_version(project: Project = Project(),
                     increment_=True,
                     pre_release=True,
                     verbose=True,
                     write_version_file=True,
                     now_testing=False,
                     ) -> VersionParts:
    """
    gets current version of the project and increments depending on arguments given by developer...
        @params
            project : Project => see Project class which takes path to version file
            ------------
            increment_ : bool => it may increment or return same version
            ------------
                if True => depending on pre_release parameter creates new version number
                if False => ignores pre_release parameter and just returns current version
            pre_release : bool => creates next version by incrementin and adding "rc" text to the version
            ------------
                    (lets suppose current version is 0.0.1.2)
                if True => creates a version like 0.0.1.3rc1
                if False =>  creates a version like 0.0.1.3
            verbose : bool
            ------------
                verbose or silent while doing process
            write_version_file :  pathlib.Path  or str
            ------------
                if True : writes new version to given path
                if False : does not write any file
            now_testing: bool => default : False
            ------------
                for testing purposes it plays with fake versions
                this will be set True while testing development
    """
    if now_testing:
        project.now_testing = now_testing
    if project.now_testing:
        now_testing = project.now_testing
    prev_instance = get_prev_version_instance(project)
    project.version = prev_instance
    if not increment_:
        next_instance = prev_instance
    else:
        next_instance = increment(pre_release, prev_instance)
    if verbose:
        print("-" * 15)
        print("CURRENT VERSION", prev_instance)
        print(f"increment : {increment_}")
        print(f"pre_release : {pre_release}")
        if prev_instance.version != next_instance:
            print("VERSION number was incremented...")
        print("NEW VERSION", next_instance)
    project.next_version = next_instance
    if write_version_file:
        """ write new version"""
        check_and_write(project, project.next_version)
    return next_instance


def get_current_version(project: Project = Project(),
                        verbose=True,
                        write_version_file=True,
                        now_testing=False,
                        ) -> VersionParts:
    """
    get_current_version
    Read-only function
        tries to find out current version of the file and returns.
        @params
            project : Project => see Project class which takes path to version file
            verbose : bool
                verbose or silent while doing process
            write_version_file :  pathlib.Path  or str
                if True : writes new version to given path
                if False : does not write any file
            test :
                for testing purposes it plays with fake versions
    """
    prev_instance = get_prev_version_instance(project)
    project.version = prev_instance
    if verbose:
        print(project.version)
    if write_version_file:
        """ write current version"""
        check_and_write(project, project.version)

    return prev_instance
