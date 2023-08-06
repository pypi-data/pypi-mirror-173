#define PY_SSIZE_T_CLEAN
#include <Python.h> /* Python/C API */
#include "dclpy.h" /* 呼び出したいC言語の関数 */

static PyObject *
addWrapper(PyObject *self, PyObject *args) {

    int x, y;

    /* argsからint型に変換したデータを２つ取得 */
    if (!PyArg_ParseTuple(args, "ii", &x, &y)) {
        /* エラー時は例外発生 */
        return NULL;
    }

    /* 目的のC言語の関数を呼び出し */
    int ret = add(x, y);

    /* retをPybOject構造体に変換してアドレス返却 */
    return Py_BuildValue("i", ret);
}

static PyObject *
subWrapper(PyObject *self, PyObject *args) {

    int x, y;

    /* argsからint型に変換したデータを２つ取得 */
    if (!PyArg_ParseTuple(args, "ii", &x, &y)) {
        /* エラー時は例外発生 */
        return NULL;
    }

    /* 目的のC言語の関数を呼び出し */
    int ret = sub(x, y);

    /* retをPybOject構造体に変換してアドレス返却 */
    return Py_BuildValue("i", ret);
}

static PyMethodDef myCalcMethods[] = {
    {"MyAdd", addWrapper, METH_VARARGS, NULL},
    {"MySub", subWrapper, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL} /* 番兵 */
};

static PyModuleDef myCalcModule = {
    PyModuleDef_HEAD_INIT,
    "MyCalc",
    NULL,
    -1,
    myCalcMethods
};

PyMODINIT_FUNC
PyInit_MyCalc(void) {
    return PyModule_Create(&myCalcModule);
}
