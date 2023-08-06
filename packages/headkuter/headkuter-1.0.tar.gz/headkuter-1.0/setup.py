from setuptools import setup, find_packages
import app

setup(
    name='headkuter',
    version=1.0,
    packages = ['Module','Module.veracrypt','Module.keepass','Module.formosa','Module.gui','Module.formosa.themes'],
    py_modules=['app','autoVera'],
    package_data={'Module.formosa.themes':['finances.json','copy_left.json','harry_potter.json','medieval_fantasy.json','sci-fi.json','the_big_bang_theory.json','tourism.json']},
    entry_points={
        'console_scripts': [
            'headkuter =app:headkurter'  #ponting to executeable function
        ]
    },
    install__requires=[
        'click==8.1.3',
        'colorama==0.4.4',
    ],
    include_package_data= True,
        #zip_safe = False
    )