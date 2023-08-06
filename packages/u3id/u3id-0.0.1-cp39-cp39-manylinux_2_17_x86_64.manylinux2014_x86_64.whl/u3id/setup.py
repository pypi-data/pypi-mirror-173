from setuptools import Extension, setup
from Cython.Build import cythonize

# setup(
#     ext_modules = cythonize("u3id.pyx")
# )

extensions = [Extension(
    'u3id',
    sources = ['u3id.pyx', 'u3id_generate.c'],
    libraries=['ssl', 'crypto']
)]

setup(
    ext_modules = cythonize(extensions)
)