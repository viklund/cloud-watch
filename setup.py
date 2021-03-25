from setuptools import setup, find_packages

setup(
        name             = 'cloud-watch',
        version          = '0.0.2',

        author           = 'Johan Viklund',
        author_email     = 'johan.viklund@gmail.com',
        description      = 'Cloud-watch - a system to check machines in ze clouds',
        license          = 'AGPL3',

        install_requires = [ 'apache-libcloud==2.4.0', 'PyYAML==5.4', 'tabulate==0.8.3', 'pytz' ],
        python_requires  = '>3.6.0',
        packages         = [ 'cloud_watch' ],

        entry_points     = {
            'console_scripts': [
                    'cw = cloud_watch.main:main'
                ],
            },
)
