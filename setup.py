from setuptools import setup

setup(
    name='magskeeball',
    version='0.0.0.0.1',
    author="Eric Buzan",
    author_email="eric.buzan@gmail.com",
    url='https://github.com/ericbuzan/magskeeball',
    description='Skee Ball!',
    packages=['magskeeball'],
    install_requires=['Pillow','pygame'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'magskeeball = magskeeball.main:main'
        ]
    }
)