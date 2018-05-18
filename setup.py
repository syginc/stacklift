from setuptools import setup

setup(
    name='stacklift',
    version='0.0.1',
    description='CloudFormation stack management tool',
    url='https://github.com/syginc/stacklift',
    author='syg',
    author_email='info@syginc.jp',
    license='MIT',
    keywords='aws cloudformation',
    packages=[
        "stacklift"
    ],
    install_requires= [
        "pyyaml",
        "boto3"
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Build Tools'
    ],
)
