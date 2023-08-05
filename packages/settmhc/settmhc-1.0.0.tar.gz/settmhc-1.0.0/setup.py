from setuptools import setup,find_packages

with open('./README.md', 'r') as f:
    readme = f.read()
with open('./requirements.txt') as f:
    requires_packages  = f.read().splitlines()

setup(
    name='settmhc',
    version='1.0.0',
    description='A peptide-MHC binding predictor based on sequence-structure information',
    author='Chen Wenfan',
    author_email='wenfanchan@zju.edu.cn',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'settmhc = settmhc.settmhc_main:main',
            'pshm = settmhc.pshm:main',
            'pmhc-model = settmhc.structure_modeling:structure_generator', ],
    },
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires = requires_packages
)
