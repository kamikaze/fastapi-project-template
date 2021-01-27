// This definition is needed for future-proofing your code
// see https://docs.python.org/3/c-api/arg.html#:~:text=Note%20For%20all,always%20define%20PY_SSIZE_T_CLEAN.
#define PY_SSIZE_T_CLEAN
// The actual Python API
#include <Python.h>

// pure C function that will be called recursively
int fib(int n)
{
  if (n <= 1)
    return n;

  return fib(n-1) + fib(n-2);
}

// function that will be called from Python code
// wraps around the pure C fib function
PyObject* c_fib(PyObject* self, PyObject* args)
{
  int n;
  PyArg_ParseTuple(args, "i", &n);
  n = fib(n);

  return PyLong_FromLong(n);
}

// array containing the module's methods' definitions
// put here the methods to export
// the array must end with a {NULL} struct
PyMethodDef module_methods[] =
{
    {"c_fib", c_fib, METH_VARARGS, "Method description"},
    {NULL} // this struct signals the end of the array
};

// struct representing the module
struct PyModuleDef extmod =
{
    PyModuleDef_HEAD_INIT, // Always initialize this member to PyModuleDef_HEAD_INIT
    "extmod", // module name
    "Module description", // module description
    -1, // module size (more on this later)
    module_methods // methods associated with the module
};

// function that initializes the module
PyMODINIT_FUNC PyInit_extmod()
{
    return PyModule_Create(&extmod);
}
