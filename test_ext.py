import glob
import sys

pytest_plugins = ['pytester']


def test_foo(testdir):
    testdir.makepyfile(setup="""
        from setuptools import setup, Extension
        ext = Extension('foo', sources=['foo.c'])
        setup(name='foo', py_modules=['test_foo'], ext_modules=[ext])
        """,
        test_foo="""
        import foo

        def test_bar():
            assert foo.bar() == "Hello world"
        """)
    testdir.makefile('.c', foo=r"""
        #include <Python.h>

        static PyObject *bar(PyObject *self, PyObject *args)
        {
            return PyUnicode_FromString("Hello world");
        }

        static PyMethodDef methods[] = {
            {.ml_name = "bar", .ml_meth = bar, .ml_flags = METH_VARARGS, .ml_doc = "no docstring"},
            {/* terminal element, all NULL */}
        };

        static PyModuleDef moduledef = {
            .m_base = PyModuleDef_HEAD_INIT,
            .m_methods = methods,
            .m_name = "foo",
            .m_size = -1
        };

        PyMODINIT_FUNC PyInit_foo(void)
        {
            return PyModule_Create(&moduledef);
        }
        """)
    testdir.run(sys.executable, 'setup.py', 'build')
    build_dir, = glob.glob(str(testdir.tmpdir / 'build/lib.*'))

    result = testdir.inline_run(build_dir)
    result.assertoutcome(passed=1, failed=0)
