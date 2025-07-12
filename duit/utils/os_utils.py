"""
A basic Python script with type hints to determine the current operating system
and its architecture, returning a dataclass containing all relevant OS information.
"""

import platform
from dataclasses import dataclass
from enum import Enum


class OSType(Enum):
    """Enum representing supported operating systems."""
    WINDOWS = "Windows"
    LINUX = "Linux"
    MACOS = "macOS"
    UNKNOWN = "Unknown"


class OSArchitecture(Enum):
    """Enum representing common OS architectures."""
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

    # Determine OS type
    if system == "Darwin":
        os_type = OSType.MACOS
    elif system == "Linux":
        os_type = OSType.LINUX
    elif system == "Windows":
        os_type = OSType.WINDOWS
    else:
        os_type = OSType.UNKNOWN

    # Determine architecture
    # Common values for platform.machine():
    #  - "x86_64", "AMD64" => x86_64
    #  - "arm", "armv7l"   => ARM
    #  - "aarch64"         => ARM64
    #  - "i386", "i686"    => x86
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


def disable_app_nap_on_macos():
    """
    Disables App Nap on macOS to prevent the application from being throttled
    when it is not in the foreground.

    This function checks if the operating system is macOS and uses the
    `appnope` module to disable App Nap for the current process.
    """
    if is_macos():
        import appnope

        # disable App Nap for the rest of your process
        appnope.nope()
