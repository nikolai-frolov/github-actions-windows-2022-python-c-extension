#include <Python.h>

static PyModuleDef moduledef = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "foo",
    .m_size = -1
};

PyMODINIT_FUNC PyInit_foo(void)
{
    PyObject *module = PyModule_Create(&moduledef);
    return module;
}
