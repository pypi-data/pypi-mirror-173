from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    readme = fh.read()

setup(
    name='FuncsForSPO_l',
    version='1.0.1',
    url='https://github.com/gabriellopesdesouza2002/FuncsForSPO_l',
    license='MIT License',
    author='Gabriel Lopes de Souza',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='githubpaycon@gmail.com',
    keywords='Funções Para Melhorar Desenvolvimento de Robôs com Selenium - FOR LINUX',
    description=u'Funções Para Melhorar Desenvolvimento de Robôs com Selenium - FOR LINUX',
    packages=[
        'FuncsForSPO_l',
        'FuncsForSPO_l/fftp',
        'FuncsForSPO_l/fexceptions',
        'FuncsForSPO_l/fopenpyxl',
        'FuncsForSPO_l/fpysimplegui',
        'FuncsForSPO_l/fpython',
        'FuncsForSPO_l/focr',
        'FuncsForSPO_l/fregex',
        'FuncsForSPO_l/fselenium',
        'FuncsForSPO_l/fselenium',
        'FuncsForSPO_l/fwinotify',
        'FuncsForSPO_l/femails',
        'FuncsForSPO_l/fsqlite'
        ],
    
    install_requires=[
        'selenium', 
        'openpyxl', 
        'webdriver-manager', 
        'fake_useragent', 
        'requests',
        'pretty_html_table',
        'PySimpleGUI',
        'PyInstaller',
        'macholib',
        'wget',
        'winotify',
        'redmail',
        'packaging',
        ],
    )