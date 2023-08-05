#include "numcertain.h"

static PyMethodDef module_methods[] = {{0}};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT, // m_base
    "numcertain",          // m_name
    NULL,                  // m_doc
    -1,                    // m_size
    module_methods,        // m_methods
    NULL,                  // m_slots
    NULL,                  // m_traverse
    NULL,                  // m_clear
    NULL                   // m_free
};

PyMODINIT_FUNC PyInit__numcertain(void) {
  PyObject *module = PyModule_Create(&moduledef);
  if (!module)
    return NULL;

  if (add_numpy_functionality(module) < 0)
    return NULL;

  if (PyType_Ready(&PyUncertain_Type) < 0)
    return NULL;

  Py_IncRef(&PyUncertain_Type);
  PyModule_AddObject(module, "uncertain", (PyObject *)&PyUncertain_Type);

  return module;
}
