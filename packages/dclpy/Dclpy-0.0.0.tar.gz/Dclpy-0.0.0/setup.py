from distutils.core import setup, Extension

packagename = "dclpy"

setup(
    name='Dclpy',
    ext_modules = [
        Extension(
            'Dclpy',
            ['dclpy/dclpy.c', 'dclpy/dclpy_wrapper.c'],
            libraries=['gdbm'],
        )
    ]
)
