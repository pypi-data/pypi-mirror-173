from setuptools import setup, find_packages
from setuptools.command.install import install
import os
path = os.getcwd()
os.system("sh "+path+"/data/gen.sh")

class Install_with_sym(install):
    def run(self):
        install.run(self)
setup(
    name='hello_publish',
    version='0.1.2',
    cmdclass={'install': Install_with_sym},
    packages=find_packages(include=['hello_publish', 'hello_publish.*']),
    scripts=['data/gen.sh'],
    include_package_data=True,
    package_data={'hello_publish': ['countries.csv']}
)

# setup(name='Tzara---A-Personal-Assistant',
#       version='1.0.6',
#       description='A Virtual Personal Assistant',
#       url='https://github.com/Suman7495/Tzara---A-Personal-Assistant',
#       author='MyName',
#       author_email='myemail@gmail.com',
#       license='MIT',
#       packages=['tzara'],
#       classifiers=['Development Status :: 4 - Beta',
#       'Programming Language :: Python :: 2.7',            
#       ],
#       scripts=['bin/desktopsetup.sh', 'bin/startup.sh'],
#       cmdclass={'install': MyInstall},
# )