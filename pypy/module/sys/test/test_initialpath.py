import py
from pypy.module.sys.state import getinitialpath
from pypy.module.sys.version import PYPY_VERSION, CPYTHON_VERSION

def build_hierarchy(prefix):
    dirname = '%d.%d' % CPYTHON_VERSION[:2]
    a = prefix.join('lib_pypy').ensure(dir=1)
    b = prefix.join('lib-python', dirname).ensure(dir=1)
    return a, b


def test_stdlib_in_prefix(tmpdir):
    dirs = build_hierarchy(tmpdir)
    path = getinitialpath(None, str(tmpdir))
    # we get at least 'dirs', and maybe more (e.g. plat-linux2)
    assert path[:len(dirs)] == map(str, dirs)

def test_include_libtk(tmpdir):
    lib_pypy, lib_python = build_hierarchy(tmpdir)
    lib_tk = lib_python.join('lib-tk')
    path = getinitialpath(None, str(tmpdir))
    assert lib_tk in path
