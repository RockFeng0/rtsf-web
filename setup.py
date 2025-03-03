#! python3
# -*- encoding: utf-8 -*-


import os
import io
import sys
from shutil import rmtree
from setuptools import setup, find_packages, Command
from webuidriver import __about__

here = os.path.abspath(os.path.dirname(__file__))

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()


class UploadCommand(Command):
    """ Build and publish this package.
        Support setup.py upload. Copied from requests_html.
    """

    user_options = []

    @staticmethod
    def status(s):
        """Prints things in green color."""
        print("\033[0;32m{0}\033[0m".format(s))

    def initialize_options(self):
        """ override
        """
        pass

    def finalize_options(self):
        """ override
        """
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Publishing git tags…')
        os.system('git tag v{0}'.format(__about__.__version__))
        os.system('git push --tags')

        sys.exit()


install_requires = [
    # 如果使用selenium 4，需要python>=3.7
    # Selenium Manager 在selenium V4.6引入的，每次开启driver都会去请求国外网址
    #   因为国内网络原因，selenium manager需要访问的站点，会报错error sending request for url
    #   selenium > 4.6，建议配置环境变量 SE_CHROMEDRIVER,指定driver路径
    "selenium (>=3.141.0, !=4.17)",  # 建议版本 python 3.6 + selenium 3.141.0;
    "requests",
    "rtsf",
]

# dependency_links=[
# "git+https://github.com/RockFeng0/rtsf.git#egg=rtsf-0"
# ]

setup(
        name=__about__.__title__,
        version=__about__.__version__,
        description=__about__.__short_desc__,
        long_description=long_description,
        long_description_content_type='text/markdown',
        author=__about__.__autor__,
        author_email=__about__.__author_email__,
        url=__about__.HOME_PAGE,
        license=__about__.__license__,
        python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
        packages=find_packages(exclude=()),
        keywords='test web ui',
        install_requires=install_requires,
        # dependency_links=dependency_links,
        extras_require={},
        entry_points={
            'console_scripts': [
                'wldriver=webuidriver.cli:local_main_run',  # local driver
                'wrdriver=webuidriver.cli:remote_main_run',  # remote driver
                'wrhub=webuidriver.cli:hub_main_run',  # selenium grid hub
                'wrnode=webuidriver.cli:node_main_run',  # selenium grid node
            ]
        },
        # $ setup.py upload support.
        cmdclass={
            'upload': UploadCommand
        }
    )
