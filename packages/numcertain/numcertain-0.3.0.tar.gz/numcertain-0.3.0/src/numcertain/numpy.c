#include "numpy.h"

PyObject *npyuncertain_getitem(void *data, void *arr) {
  Uncertain_t u;
  memcpy(&u, data, sizeof(Uncertain_t));
  return PyUncertain_from_Uncertain(u);
};

int npyuncertain_setitem(PyObject *item, void *data, void *arr) {
  Uncertain_t u;
  if (PyUncertain_Check(item))
    u = ((PyUncertain_t *)item)->u;
  else {
    long long n = PyLong_AsLongLong(item);
    PyObject *y = PyLong_FromLongLong(n);
    if (!y)
      return -1;
    int eq = PyObject_RichCompareBool(item, y, Py_EQ);
    Py_DECREF(y);
    if (eq < 0)
      return -1;
    if (!eq)
      PyErr_Format(PyExc_TypeError, "expected uncertain, got %s",
                   item->ob_type->tp_name);
    u = make_uncertain_long(n);
  }
  memcpy(data, &u, sizeof(Uncertain_t));
  return 0;
};

#define BYTESWAP(Type)                                                         \
  inline void byteswap_##Type(Type *x) {                                       \
    char *p = (char *)x;                                                       \
    size_t i;                                                                  \
    for (i = 0; i < sizeof(Type *) / 2; i++) {                                 \
      size_t j = sizeof(*x) - 1 - i;                                           \
      char t = p[i];                                                           \
      p[i] = p[j];                                                             \
      p[j] = t;                                                                \
    }                                                                          \
  };

BYTESWAP(double)

void npyuncertain_copyswapn(void *dst_, npy_intp dstride, void *src_,
                            npy_intp sstride, npy_intp n, int swap, void *arr) {
  char *dst = (char *)dst_, *src = (char *)src_;
  if (!src)
    return;
  if (swap) {
    for (npy_intp i = 0; i < n; i++) {
      Uncertain_t *u = (Uncertain_t *)(dst + dstride * i);
      memcpy(u, src + sstride * i, sizeof(Uncertain_t));
      byteswap_double(&u->nominal);
      byteswap_double(&u->uncertainity);
    }
  } else if (dstride == sizeof(Uncertain_t) && sstride == sizeof(Uncertain_t)) {
    memcpy(dst, src, n * sizeof(Uncertain_t));
  } else {
    for (npy_intp i = 0; i < n; i++) {
      memcpy(dst + dstride * i, src + sstride * i, sizeof(Uncertain_t));
    }
  }
};

void npyuncertain_copyswap(void *dst, void *src, int swap, void *arr) {
  if (!src)
    return;
  Uncertain_t *u = (Uncertain_t *)dst;
  memcpy(u, src, sizeof(Uncertain_t));
  if (swap) {
    byteswap_double(&u->nominal);
    byteswap_double(&u->uncertainity);
  }
};

npy_bool npyuncertain_nonzero(void *data, void *arr) {
  Uncertain_t u;
  memcpy(&u, data, sizeof(Uncertain_t));
  return uncertain_nonzero(u) ? NPY_TRUE : NPY_FALSE;
}

PyArray_ArrFuncs npyuncertain_arrfuncs;

PyArray_Descr npyuncertain_descr = {
    PyObject_HEAD_INIT(0) & PyUncertain_Type,            // typeobj
    'V',                                                 // kind
    'r',                                                 // type
    '=',                                                 // byteorder
    NPY_NEEDS_PYAPI | NPY_USE_GETITEM | NPY_USE_SETITEM, // hasobject
    0,                                                   // type_num
    sizeof(Uncertain_t),                                 // elsize
    offsetof(align_test, u),                             // alignment
    0,                                                   // subarray
    0,                                                   // fields
    0,                                                   // names
    &npyuncertain_arrfuncs};                             // f

#define DEFINE_CAST(From, To, statement)                                       \
  void npycast_##From##_##To(void *from_, void *to_, npy_intp n,               \
                             void *fromarr, void *toarr) {                     \
    const From *from = (From *)from_;                                          \
    To *to = (To *)to_;                                                        \
    for (npy_intp i = 0; i < n; i++) {                                         \
      From x = from[i];                                                        \
      statement;                                                               \
      to[i] = y;                                                               \
    }                                                                          \
  }

#define DEFINE_FLOAT_CAST(bits)                                                \
  DEFINE_CAST(npy_float##bits, Uncertain_t,                                    \
              Uncertain_t y = make_uncertain_double(x);)                       \
  DEFINE_CAST(Uncertain_t, npy_float##bits,                                    \
              npy_float##bits z = uncertain_double(x);                         \
              npy_float##bits y = z; if (y != z) set_overflow();)

#define DEFINE_INT_CAST(bits)                                                  \
  DEFINE_CAST(npy_int##bits, Uncertain_t,                                      \
              Uncertain_t y = make_uncertain_long(x);)                         \
  DEFINE_CAST(Uncertain_t, npy_int##bits, npy_int##bits z = uncertain_long(x); \
              npy_int##bits y = z; if (y != z) set_overflow();)

DEFINE_FLOAT_CAST(32)
DEFINE_FLOAT_CAST(64)

DEFINE_INT_CAST(8)
DEFINE_INT_CAST(16)
DEFINE_INT_CAST(32)
DEFINE_INT_CAST(64)

DEFINE_CAST(npy_bool, Uncertain_t, Uncertain_t y = make_uncertain_long(x);)
DEFINE_CAST(Uncertain_t, npy_bool, npy_bool y = uncertain_nonzero(x);)

#define UNCERTAIN_BINOP_UFUNC(name, outtype, exp)                              \
  void uncertain_ufunc_##name(char **args, npy_intp const *dimensions,         \
                              npy_intp const *steps, void *data) {             \
    npy_intp in_a_step = steps[0], in_b_step = steps[1], out_step = steps[2];  \
                                                                               \
    char *in_a = args[0], *in_b = args[1], *out = args[2];                     \
                                                                               \
    for (int i = 0; i < *dimensions; i++) {                                    \
      Uncertain_t a = *(Uncertain_t *)in_a;                                    \
      Uncertain_t b = *(Uncertain_t *)in_b;                                    \
      *(outtype *)out = exp(a, b);                                             \
      in_a += in_a_step;                                                       \
      in_b += in_b_step;                                                       \
      out += out_step;                                                         \
    }                                                                          \
  }

UNCERTAIN_BINOP_UFUNC(add, Uncertain_t, uncertain_add)
UNCERTAIN_BINOP_UFUNC(subtract, Uncertain_t, uncertain_subtract)
UNCERTAIN_BINOP_UFUNC(multiply, Uncertain_t, uncertain_multiply)
UNCERTAIN_BINOP_UFUNC(divide, Uncertain_t, uncertain_divide)

UNCERTAIN_BINOP_UFUNC(equal, bool, uncertain_eq)
UNCERTAIN_BINOP_UFUNC(not_equal, bool, uncertain_ne)

#define UNCERTAIN_UNARY_UFUNC(name, outtype, exp)                              \
  void uncertain_ufunc_##name(char **args, npy_intp const *dimensions,         \
                              npy_intp const *steps, void *data) {             \
    npy_intp in_step = steps[0], out_step = steps[1];                          \
    char *in = args[0], *out = args[1];                                        \
    for (int i = 0; i < *dimensions; i++) {                                    \
      Uncertain_t u = *(Uncertain_t *)in;                                      \
      *(outtype *)out = exp(u);                                                \
      in += in_step;                                                           \
      out += out_step;                                                         \
    }                                                                          \
  }

UNCERTAIN_UNARY_UFUNC(nominal, npy_float64, uncertain_nominal)
UNCERTAIN_UNARY_UFUNC(uncertainty, npy_float64, uncertain_uncertainty)

static PyMethodDef module_methods[] = {{0}};

static struct PyModuleDef moduledef = {PyModuleDef_HEAD_INIT,
                                       "numpy",
                                       NULL,
                                       -1,
                                       module_methods,
                                       NULL,
                                       NULL,
                                       NULL,
                                       NULL};

int add_numpy_functionality(PyObject *module) {

  import_array();
  import_umath();

  PyObject *numpy_str = PyUnicode_FromString("numpy");
  if (!numpy_str)
    return -1;
  PyObject *numpy = PyImport_Import(numpy_str);
  Py_DECREF(numpy_str);
  if (!numpy)
    return -1;

  PyUncertain_Type.tp_base = &PyGenericArrType_Type;

  if (PyType_Ready(&PyUncertain_Type) < 0)
    return -1;

  PyArray_InitArrFuncs(&npyuncertain_arrfuncs);
  npyuncertain_arrfuncs.getitem = npyuncertain_getitem;
  npyuncertain_arrfuncs.setitem = npyuncertain_setitem;
  npyuncertain_arrfuncs.copyswapn = npyuncertain_copyswapn;
  npyuncertain_arrfuncs.copyswap = npyuncertain_copyswap;
  npyuncertain_arrfuncs.nonzero = npyuncertain_nonzero;

  Py_SET_TYPE(&npyuncertain_descr, &PyArrayDescr_Type);

  int npy_uncertain = PyArray_RegisterDataType(&npyuncertain_descr);
  if (npy_uncertain < 0) {
    return -1;
  }

  if (PyDict_SetItemString(PyUncertain_Type.tp_dict, "dtype",
                           (PyObject *)&npyuncertain_descr) < 0)
    return -1;

#define REGISTER_CAST(From, To, from_descr, to_typenum, safe)                  \
  {                                                                            \
    if (PyArray_RegisterCastFunc((from_descr), (to_typenum),                   \
                                 npycast_##From##_##To) < 0)                   \
      return -1;                                                               \
    if (safe &&                                                                \
        PyArray_RegisterCanCast((from_descr), (to_typenum), NPY_NOSCALAR) < 0) \
      return -1;                                                               \
  };

#define REGISTER_FLOAT_CAST(bits)                                              \
  REGISTER_CAST(npy_float##bits, Uncertain_t,                                  \
                PyArray_DescrFromType(NPY_FLOAT##bits), npy_uncertain, 1)      \
  REGISTER_CAST(Uncertain_t, npy_float##bits, &npyuncertain_descr,             \
                NPY_FLOAT##bits, 0)

#define REGISTER_INT_CAST(bits)                                                \
  REGISTER_CAST(npy_int##bits, Uncertain_t,                                    \
                PyArray_DescrFromType(NPY_INT##bits), npy_uncertain, 1)        \
  REGISTER_CAST(Uncertain_t, npy_int##bits, &npyuncertain_descr,               \
                NPY_INT##bits, 0)

  REGISTER_FLOAT_CAST(32)
  REGISTER_FLOAT_CAST(64)

  REGISTER_INT_CAST(8)
  REGISTER_INT_CAST(16)
  REGISTER_INT_CAST(32)
  REGISTER_INT_CAST(64)

  REGISTER_CAST(npy_bool, Uncertain_t, PyArray_DescrFromType(NPY_BOOL),
                npy_uncertain, 1)
  REGISTER_CAST(Uncertain_t, npy_bool, &npyuncertain_descr, NPY_BOOL, 0)

#define REGISTER_UFUNC(name, ufuncmodule, ...)                                 \
  {                                                                            \
    PyUFuncObject *ufunc =                                                     \
        (PyUFuncObject *)PyObject_GetAttrString(ufuncmodule, #name);           \
    if (!ufunc) {                                                              \
      return -1;                                                               \
    }                                                                          \
    int arg_types[] = __VA_ARGS__;                                             \
    if (sizeof(arg_types) / sizeof(int) != ufunc->nargs) {                     \
      Py_DECREF(module);                                                       \
      return -1;                                                               \
    }                                                                          \
    if (PyUFunc_RegisterLoopForType((PyUFuncObject *)ufunc, npy_uncertain,     \
                                    uncertain_ufunc_##name, arg_types,         \
                                    0) < 0) {                                  \
      Py_DECREF(module);                                                       \
      return -1;                                                               \
    }                                                                          \
    Py_DECREF(ufunc);                                                          \
  }

#define REGISTER_NUMPY_UFUNC(name, ...) REGISTER_UFUNC(name, numpy, __VA_ARGS__)

#define REGISTER_NUMPY_UFUNC_BINOP_UNCERTAIN(name)                             \
  REGISTER_NUMPY_UFUNC(name, {npy_uncertain, npy_uncertain, npy_uncertain})
#define REGISTER_NUMPY_UFUNC_BINOP_BOOL(name)                                  \
  REGISTER_NUMPY_UFUNC(name, {npy_uncertain, npy_uncertain, NPY_BOOL})

  REGISTER_NUMPY_UFUNC_BINOP_UNCERTAIN(add)
  REGISTER_NUMPY_UFUNC_BINOP_UNCERTAIN(subtract)
  REGISTER_NUMPY_UFUNC_BINOP_UNCERTAIN(multiply)
  REGISTER_NUMPY_UFUNC_BINOP_UNCERTAIN(divide)

  REGISTER_NUMPY_UFUNC_BINOP_BOOL(equal)
  REGISTER_NUMPY_UFUNC_BINOP_BOOL(not_equal)

#define NEW_UFUNC(name, doc)                                                   \
  {                                                                            \
    PyObject *ufunc = PyUFunc_FromFuncAndData(0, 0, 0, 0, 1, 1, PyUFunc_None,  \
                                              (char *)#name, (char *)doc, 0);  \
    if (!ufunc) {                                                              \
      Py_DECREF(module);                                                       \
      return -1;                                                               \
    }                                                                          \
    PyModule_AddObject(module, #name, (PyObject *)ufunc);                      \
  }

  NEW_UFUNC(nominal, "Retrieves an ndarray of nominal values from an ndarray "
                     "of uncertain values.")
  NEW_UFUNC(uncertainty, "Retrieves an ndarray of uncertainties from an "
                         "ndarray of uncertain values.")

#define REGISTER_MODULE_UFUNC(name, ...)                                       \
  REGISTER_UFUNC(name, module, __VA_ARGS__)
#define REGISTER_MODULE_UFUNC_UNARY_FLOAT64(name)                              \
  REGISTER_MODULE_UFUNC(name, {npy_uncertain, NPY_FLOAT64})

  REGISTER_MODULE_UFUNC_UNARY_FLOAT64(nominal)
  REGISTER_MODULE_UFUNC_UNARY_FLOAT64(uncertainty)
}