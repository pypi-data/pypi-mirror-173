from setuptools import setup, find_packages

setup(
    name="pyipcore",
    version="0.1.1",
    author="eaglebaby",
    author_email="2229066748@qq.com",
    description="pyipcore = python (pseudo) (verilog) IP core (rebuilder). Properly adjust your own. v file as an open source IP core, so that it can be easily reconfigured to new projects. Console cmd: iprebuild",

    #url="http://iswbm.com/", 

    packages=find_packages(),

    classifiers = [
        'Development Status :: 2 - Pre-Alpha',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
    ],

    install_requires=['pyperclip', "files3"],

    python_requires='>=3',

    entry_points = {
        'console_scripts': [
            'iprebuild = pyipcore.ipg:IPRebuild',
        ]
    },
    package_data={
        'ipcore':['example.v']
    },
)