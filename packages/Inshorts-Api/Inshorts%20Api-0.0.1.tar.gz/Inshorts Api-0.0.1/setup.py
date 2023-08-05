from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'InShorts Api'
LONG_DESCRIPTION = 'Shorts Api in a python package that help you to information from Inshorts webpage'

setup(
    name='Inshorts Api',
    version=VERSION,
    license='MIT',
    author="M.NAVEEN",
    author_email='practicalengineers05@gmail.com',
    packages=find_packages(),
    url='https://github.com/engineerscodes/Inshorts-Api',
    keywords=['python', 'Inshorts', 'InshortsApi', 'Inshorts-Api'],
    install_requires=[
        'requests',
        'bs4',
        'lxml',
        'html5lib'
    ],

)
