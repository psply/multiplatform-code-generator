"""
Multiplatform Code Generator

A powerful MCP tool for generating cross-platform code from C++ interfaces.
"""

__version__ = "1.0.0"
__author__ = "Multiplatform Code Generator Team"
__license__ = "MIT"

from .main import main
from .server import MultiplatformCodeGeneratorServer
from .parsers.cpp_parser import CppInterfaceParser
from .generators.android_jni import AndroidJniGenerator
from .generators.ios_oc import IosOcGenerator
from .generators.harmony_napi import HarmonyNapiGenerator
from .utils.file_manager import FileManager

__all__ = [
    "main",
    "MultiplatformCodeGeneratorServer",
    "CppInterfaceParser",
    "AndroidJniGenerator", 
    "IosOcGenerator",
    "HarmonyNapiGenerator",
    "FileManager",
]
