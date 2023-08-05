import fnmatch
import os
import re
import shutil
import subprocess
import sys

import docutils.core
from setuptools import Extension, find_packages
from setuptools.command.build_ext import build_ext

# Convert distutils Windows platform specifiers to CMake -A arguments
PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}


# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def __init__(self, dist):
        self.distribution = None
        super().__init__(dist)

    def build_extension(self, ext):  # noqa: C901
        ext_dir = self.get_ext_fullpath(ext.name)
        ext_dir = os.path.dirname(ext_dir)
        ext_dir = os.path.abspath(ext_dir)

        # required for auto-detection & inclusion of auxiliary "native" libs
        if not ext_dir.endswith(os.path.sep):
            ext_dir += os.path.sep

        debug = self.debug or int(os.environ.get("DEBUG", 0))
        cfg = "Debug" if debug else "Release"

        # CMake lets you override the generator - we need to check this.
        # Can be set with Conda-Build, for example.
        cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

        # Set Python_EXECUTABLE instead if you use PYBIND11_FINDPYTHON
        # EXAMPLE_VERSION_INFO shows you how to pass a value into the C++ code
        # from Python.
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={ext_dir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",  # not used on MSVC, but no harm
        ]
        build_args = []
        # Adding CMake arguments set as environment variable
        # (needed e.g. to build for ARM OSx on conda-forge)
        if "CMAKE_ARGS" in os.environ:
            cmake_args += [item for item in os.environ["CMAKE_ARGS"].split(" ") if item]

        # In this example, we pass in the version to C++. You might not need to.
        cmake_args += [f"-DVERSION_INFO={self.distribution.get_version()}"]

        if self.compiler.compiler_type == "msvc":

            # Single config generators are handled "normally"
            single_config = any(x in cmake_generator for x in {"NMake", "Ninja"})

            if not single_config:
                # CMake allows an arch-in-generator style for backward compatibility
                contains_arch = any(x in cmake_generator for x in {"ARM", "Win64"})

                if not contains_arch:
                    cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name]]

                cmake_args += [f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={ext_dir}"]
                build_args += ["--config", cfg]

        elif not cmake_generator:
            try:
                import ninja  # noqa: F401

                cmake_args += ["-GNinja"]
            except ImportError:
                pass

        if sys.platform.startswith("darwin"):
            if archs := re.findall(r"-arch (\S+)", os.environ.get("ARCHFLAGS", "")):
                cmake_args += [f'-DCMAKE_OSX_ARCHITECTURES={";".join(archs)}']

        # Set CMAKE_BUILD_PARALLEL_LEVEL to control the parallel build level
        # across all generators.
        if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ and hasattr(self, "parallel") and self.parallel:
            # CMake 3.12+ only.
            build_args += [f"-j{self.parallel}"]

        build_temp = os.path.join(self.build_temp, ext.name)
        if not os.path.exists(build_temp):
            os.makedirs(build_temp)

        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=build_temp)
        subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=build_temp)


# Setuptools bug causes collision between pypy and cpython artifacts
# if os.path.exists("build"):
#     shutil.rmtree("build")

docutils.core.publish_file(source_path="README.rst", destination_path="README.html", writer_name="html")

with open("README.html") as fh:
    long_description = fh.read()


def build(setup_kwargs):
    ext_modules = [CMakeExtension("_cornflakes", "inst/_cornflakes")]
    setup_kwargs.update(
        {
            "ext_modules": ext_modules,
            "cmdclass": {"build_ext": CMakeBuild},
            "zip_safe": False,
            "long_description": long_description,
            "long_description_content_type": "text/html",
            # "packages": find_packages("src"),
            # "package_dir": {"": "src"},
        }
    )
