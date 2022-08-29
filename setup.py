from setuptools import setup, find_packages

VERSION = "0.1"
DESCRIPTION = "Une simple librairie pour gérer des self bot sur discord"

readme = ''
with open('README.md') as f:
    readme = f.read()
    
setup(
    name='pydiscordself',
    version=VERSION,
    license='MIT',
    author="Borane#9999",
    packages=[
        "pydiscordself"
    ],
    url='https://github.com/8borane8/pydiscordself',
    keywords='discord self bot',
    python_requires='>=3.6',
    description=DESCRIPTION,
    install_requires=[
          'websocket-client',
          'requests'
    ]
)