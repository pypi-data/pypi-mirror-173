from setuptools import setup

from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='L_SpaceCurves',
    version='0.0.8',
    license='MIT License',
    author='Thiago Santos',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='tthiagosantos38@gmail.com',
    keywords='Peano, Hilbert',
    description=u'Space filling curves in python',
    packages=['L_SpaceCurves'],
    install_requires=['matplotlib',"numpy","requests"])
