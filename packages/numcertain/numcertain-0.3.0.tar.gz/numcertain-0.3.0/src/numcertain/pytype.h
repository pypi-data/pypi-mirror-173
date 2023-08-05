#pragma once

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

#include "ctype.h"

void set_overflow(void);

typedef struct PyUncertain {
  PyObject_HEAD Uncertain_t u;
} PyUncertain_t;

extern PyTypeObject PyUncertain_Type;

int PyUncertain_Check(PyObject *object);
PyObject *PyUncertain_from_Uncertain(Uncertain_t u);
PyObject *PyUncertain_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
PyObject *PyUncertain_repr(PyObject *self);

#define UNCERTAIN_BINOP(name)                                                  \
  PyObject *PyUncertain_##name(PyObject *pya, PyObject *pyb);

UNCERTAIN_BINOP(add)
UNCERTAIN_BINOP(subtract)
UNCERTAIN_BINOP(multiply)
UNCERTAIN_BINOP(divide)

PyObject *PyUncertain_int(PyObject *self);
PyObject *PyUncertain_float(PyObject *self);

#undef UNCERTAIN_BINOP

Py_hash_t PyUncertain_hash(PyObject *self);
PyObject *PyUncertain_str(PyObject *self);
PyObject *PyUncertain_nominal(PyObject *self, void *closure);
PyObject *PyUncertain_uncertainty(PyObject *self, void *closure);
PyTypeObject *PyUncertain_richcompare(PyObject *self, PyObject *other, int op);
