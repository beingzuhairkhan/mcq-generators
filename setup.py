from setuptools import find_packages , setup 

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='zuhair khan',
    author_email='zuhairkhan5134@gmail.com',
    install_requires=['openai' , 'langchain' , 'streamlit' , 'python-dotenv' , 'pyPDF2'],
    packages=find_packages()
)