#define PY_SSIZE_T_CLEAN
#include <Python.h> /* Python/C API */
#include "dclpy.h" /* �Ăяo������C����̊֐� */

static PyObject *
addWrapper(PyObject *self, PyObject *args) {

    int x, y;

    /* args����int�^�ɕϊ������f�[�^���Q�擾 */
    if (!PyArg_ParseTuple(args, "ii", &x, &y)) {
        /* �G���[���͗�O���� */
        return NULL;
    }

    /* �ړI��C����̊֐����Ăяo�� */
    int ret = add(x, y);

    /* ret��PybOject�\���̂ɕϊ����ăA�h���X�ԋp */
    return Py_BuildValue("i", ret);
}

static PyObject *
subWrapper(PyObject *self, PyObject *args) {

    int x, y;

    /* args����int�^�ɕϊ������f�[�^���Q�擾 */
    if (!PyArg_ParseTuple(args, "ii", &x, &y)) {
        /* �G���[���͗�O���� */
        return NULL;
    }

    /* �ړI��C����̊֐����Ăяo�� */
    int ret = sub(x, y);

    /* ret��PybOject�\���̂ɕϊ����ăA�h���X�ԋp */
    return Py_BuildValue("i", ret);
}

static PyMethodDef myCalcMethods[] = {
    {"MyAdd", addWrapper, METH_VARARGS, NULL},
    {"MySub", subWrapper, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL} /* �ԕ� */
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
