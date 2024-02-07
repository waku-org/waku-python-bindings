from setuptools import setup, Extension
from Cython.Build import cythonize

# Define the Extension object
my_extension = Extension(
    'waku.waku', # Module name in Python (resulting in my_package.my_module.so)
    sources=[''],
    include_dirs=['include/'],  # Directories to search for header files
    libraries=['waku'],  # Names of libraries to link against (without 'lib' prefix or file extension)
    library_dirs=['lib/'],  # Directories to search for libraries
    runtime_library_dirs=['lib/'],  # Directories to search for shared libraries at runtime
    # extra_compile_args=['-O3'],  # Extra compiler options
    # extra_link_args=['-L/path/to/lib', '-Wl,-rpath=/path/to/lib'],  # Extra linker options
)

setup(
    name='waku',
    version='0.1',
    packages=['waku'],
    ext_modules=cythonize([my_extension]),
)

# [project.urls]
# Homepage = "https://github.com/pypa/sampleproject"
# Issues = "https://github.com/pypa/sampleproject/issues"
