from setuptools import find_packages, setup
from typing import List



def get_requirements(file_path:str)->List[str]:
    '''
    Returns the requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        
        for req in range(len(requirements)):
            requirements[req] = requirements[req].strip()
        
        if "-e ." in requirements:
            requirements.remove("-e .")

    return requirements




setup(name = 'Ecommerce-chatbot',
      version = '0.0.1',
      author = 'Dhanush Raj',
      author_email = 'dhanushlogan1004@gmail.com',
      packages = find_packages(),
      install_requires = get_requirements('requirements.txt')  )