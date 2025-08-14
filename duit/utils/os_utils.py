import functools
import platform
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any, TypeVar


class OSType(Enum):
    """
    Enum representing supported operating systems.
    """
    WINDOWS = "Windows"
    LINUX = "Linux"
    MACOS = "macOS"
    UNKNOWN = "Unknown"


class OSArchitecture(Enum):
    """
    Enum representing common OS architectures.
    """
    X86_64 = "x86_64"
    ARM = "ARM"
    ARM64 = "ARM64"
    X86 = "x86"
    UNKNOWN = "Unknown"


@dataclass
class OperatingSystem:
    """
    Dataclass to hold information about the operating system.

    :param os_type: The type of operating system (e.g., Windows, Linux, macOS, etc.)
    :param architecture: The architecture of the operating system (e.g., x86_64, ARM, etc.)
    :param version: The version string of the operating system.
    """
    os_type: OSType
    architecture: OSArchitecture
    version: str


def get_operating_system() -> OperatingSystem:
    """
    Detects and returns the current operating system information as a dataclass.

    :return: OperatingSystem object containing OS type, architecture, and version.
    """
    system = platform.system()
    machine = platform.machine().lower()
    version = platform.version()

    if system == "Darwin":
        os_type = OSType.MACOS
    elif system == "Linux":
        os_type = OSType.LINUX
    elif system == "Windows":
        os_type = OSType.WINDOWS
    else:
        os_type = OSType.UNKNOWN

    if machine in ("x86_64", "amd64"):
        architecture = OSArchitecture.X86_64
    elif machine in ("arm", "armv7l"):
        architecture = OSArchitecture.ARM
    elif machine in ("aarch64", "arm64"):
        architecture = OSArchitecture.ARM64
    elif machine in ("i386", "i686"):
        architecture = OSArchitecture.X86
    else:
        architecture = OSArchitecture.UNKNOWN

    return OperatingSystem(
        os_type=os_type,
        architecture=architecture,
        version=version
    )


def is_macos() -> bool:
    """
    Check if the current operating system is macOS.

    :return: True if macOS, False otherwise.
    """
    return get_operating_system().os_type == OSType.MACOS


def is_linux() -> bool:
    """
    Check if the current operating system is Linux.

    :return: True if Linux, False otherwise.
    """
    return get_operating_system().os_type == OSType.LINUX


def is_windows() -> bool:
    """
    Check if the current operating system is Windows.

    :return: True if Windows, False otherwise.
    """
    return get_operating_system().os_type == OSType.WINDOWS


F = TypeVar("F", bound=Callable[..., Any])


def require_os(*allowed_os: OSType) -> Callable[[F], F]:
    """
    Decorator that runs the function only if the current OS is in allowed_os.
    Works with normal, class, and static methods.

    :param allowed_os: One or more OSType values that are allowed to execute the function.

    :return: A decorator that conditionally executes the function based on the OS.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_os = get_operating_system().os_type
            if current_os in allowed_os:
                return func(*args, **kwargs)
            return None

        return wrapper  # type: ignore

    return decorator


def require_windows(func: F) -> F:
    """
    Decorator to ensure the function only runs on Windows.

    :param func: The function to decorate.

    :return: The decorated function if the OS is Windows; otherwise, None.
    """
    return require_os(OSType.WINDOWS)(func)


def require_linux(func: F) -> F:
    """
    Decorator to ensure the function only runs on Linux.

    :param func: The function to decorate.

    :return: The decorated function if the OS is Linux; otherwise, None.
    """
    return require_os(OSType.LINUX)(func)


def require_macos(func: F) -> F:
    """
    Decorator to ensure the function only runs on macOS.

    :param func: The function to decorate.

    :return: The decorated function if the OS is macOS; otherwise, None.
    """
    return require_os(OSType.MACOS)(func)
