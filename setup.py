from setuptools import setup, find_packages
setup(
    name='mineager',
    packages=find_packages(),
    version='0.0.1',
    include_package_data=True,
    install_requires=[
        'Click',
        'PyYAML',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        mineager=mineager.mineager:cli
    ''',
)
