# setup.py
from setuptools import setup, find_packages

setup(
   name="new_library_package",
   author="An amazing developer",
   description="Private Python library who provides incredible features.",
   packages=find_packages(),
   include_package_data=True,
   classifiers=[
      
       "Intended Audience :: Developers",
       
       "Programming Language :: Python",
       "Programming Language :: Python :: 3",
       
   ],
  
)
