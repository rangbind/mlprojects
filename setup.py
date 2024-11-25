from setuptools import find_packages,setup
from typing import List
HYPEN_E_DOT='-e .'

def get_requirement(file_path: str)->List[str]:
    '''
    This function will return requirements
    '''
    requirements = []
    with open(file_path) as file_object:
        requirements = file_object.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

setup(
    name='mlprojects',
    version='0.1',
    author='rang',
    author_email='rbid403@gmail.com',
    packages=find_packages(),
    install_requires=get_requirement('requirements.txt')
)