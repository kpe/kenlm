import glob
import platform
import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

#Does gcc compile with this header and library?
def compile_test(header, library):
    dummy_path = os.path.join(os.path.dirname(__file__), "dummy")
    command = "bash -c \"g++ -include " + header + " -l" + library + " -x c++ - <<<'int main() {}' -o " + dummy_path + " >/dev/null 2>/dev/null && rm " + dummy_path + " 2>/dev/null\""
    return os.system(command) == 0


FILES = glob.glob('util/*.cc') + glob.glob('lm/*.cc') + glob.glob('util/double-conversion/*.cc')
FILES = [fn for fn in FILES if not (fn.endswith('main.cc') or fn.endswith('test.cc'))]

LIBS = ['stdc++']
if platform.system() != 'Darwin':
    LIBS.append('rt')

#We don't need -std=c++11 but python seems to be compiled with it now.  https://github.com/kpu/kenlm/issues/86
ARGS = ['-O3', '-DNDEBUG', '-DKENLM_MAX_ORDER=12', '-std=c++11']

if compile_test('zlib.h', 'z'):
    ARGS.append('-DHAVE_ZLIB')
    LIBS.append('z')

if compile_test('bzlib.h', 'bz2'):
    ARGS.append('-DHAVE_BZLIB')
    LIBS.append('bz2')

if compile_test('lzma.h', 'lzma'):
    ARGS.append('-DHAVE_XZLIB')
    LIBS.append('lzma')

extensions = [
    Extension('kenlm',
        ['python/kenlm.pyx']+FILES,
        language='C++',
        include_dirs=['.'],
        libraries=LIBS,
        extra_compile_args=ARGS)
]

setup(
    name='kenlm',
    version='0.1.0',
    ext_modules=cythonize(extensions),
    include_package_data=True
)
