# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['h5darkframes']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=2.4.1,<3.0.0',
 'h5py>=3.7.0,<4.0.0',
 'numpy>=1.23.4,<2.0.0',
 'opencv-python>=4.6.0.66,<5.0.0.0',
 'pytest>=7.1.3,<8.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['darkframes-display = '
                     'h5darkframes.main:darkframes_display',
                     'darkframes-info = h5darkframes.main:darkframes_info',
                     'darkframes-zwoasi-config = '
                     'h5darkframes.main:asi_zwo_darkframes_config',
                     'darkframes-zwoasi-library = '
                     'h5darkframes.main:asi_zwo_darkframes_library']}

setup_kwargs = {
    'name': 'h5darkframes',
    'version': '0.1.0',
    'description': 'python API for creating and using hdf5 darkframes libraries ',
    'long_description': '![unit tests](https://github.com/MPI-IS/h5darkframes/actions/workflows/tests.yaml/badge.svg)\n![mypy](https://github.com/MPI-IS/h5darkframes/actions/workflows/python_mypy.yml/badge.svg)\n\n# H5DARKFRAMES (beta)\n\nH5Darkframes is a python library for generating and using darkframes library.\nFor now, it supports only asi zwo cameras (see [https://github.com/MPI-IS/camera_zwo_asi](https://github.com/MPI-IS/camera_zwo_asi)).\n\n> This is beta, and need some more testing\n\n\n## Installation\n\nfrom source:\n\n```bash\ngit clone https://github.com/MPI-IS/h5darkframes.git\ncd h5darkframes\npip install .\n```\n\nfrom pypi:\n```bash\npip install h5darkframes\n```\n\n## Usage\n\nAssuming that [camera-zwo-asi](https://github.com/MPI-IS/camera_zwo_asi) is installed and a camera is plugged:\n\n### creating a darkframe library\n\nFirst, a configuration file must be created. In a terminal:\n\n```bash\ndarkframes-zwoasi-config\n```\n\nThis will create in the current directory a file ```darkframes.toml``` with a content similar to:\n\n```\n[darkframes]\naverage_over = 5\n\n[camera.controllables]\nAutoExpMaxExpMS = 30000\nAutoExpMaxGain = 285\nAutoExpTargetBrightness = 100\nBandWidth = "auto"\nCoolerOn = 0\nExposure = 300\nFlip = 0\nGain = 400\nHighSpeedMode = 0\nMonoBin = 0\nOffset = 8\nTargetTemp = 26\nWB_B = 95\nWB_R = 52\n\n[camera.roi]\nstart_x = 0\nstart_y = 0\nwidth = 4144\nheight = 2822\nbins = 1\ntype = "raw8"\n\n[darkframes.controllables.TargetTemp]\nmin = -15\nmax = 15\nstep = 3\nthreshold = 1\ntimeout = 600\n\n[darkframes.controllables.Exposure]\nmin = 1000000\nmax = 30000000\nstep = 5000000\nthreshold = 1\ntimeout = 0.1\n\n[darkframes.controllables.Gain]\nmin = 200\nmax = 400\nstep = 100\nthreshold = 1\ntimeout = 0.1\n```\n\nYou may edit this file to setup:\n\n- your desired camera configuration\n\n- the controllables over which darkframes will be created, and over which range\n\n- the number of pictures that will be averaged per darkframes\n\n\nFor example:\n\n```\n[darkframes.controllables.TargetTemp]\nmin = -15\nmax = 15\nstep = 3\nthreshold = 1\ntimeout = 600\n```\n\nimplies that darkframes will be taken for values of temperature -15, -12, -9, ... up to +15.\n\n### creating the darkframes library\n\nCall in a terminal:\n\n```bash\n# change "mylibraryname" to a name of your choice\ndarkframes-zwoasi-library --name mylibraryname\n```\n\nYou may get stats regarding the library:\n\n```bash\ndarkframes-info\n```\n\n### using the library\n\n```python\n\nimport h5darkframes as dark\nimport camera_zwo_asi as zwo\nfrom pathlib import Path\n\n# path to the library\npath = Path("/path/to/darkframes.hdf5")\n\n# handle over the library\nlibrary = dark.ImageLibrary(path)\n\n# handle over the camera\ncamera = zwo.Camera(0)\n\n# taking a picture. Image is an instance of zwo.Image\nimage = camera.capture()\n\n# getting the current camera configuration\ncontrols = camera.get_controls()\n\n# "Temperature", "Exposure" and "Gain" must be the\n# controllables that have been iterated over\n# during the creation of the library\ndarkframe_target = {\n       "Temperature": controls["Temperature"].value,\n       "Exposure": controls["Exposure"].value,\n       "Gain": controls["Gain"].value\n}\n\n# getting the darkframe that is the closest to the target\n# darkframe: a numpy array\n# darkframe_config: the config of the camera when the darkframe was taken\ndarkframe, darkframe_config= library.get(darkframe_target)\n\n# optional sanity checks\nassert image.get_data().shape == darkframe.shape\nassert image.get_data().dtype = darkframe.dtype\n\n# substracting the darkframe\nsubstracted_image = image.get_data()-darkframe\n\n\n```',
    'author': 'Vincent Berenz',
    'author_email': 'vberenz@tuebingen.mpg.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MPI-IS/h5darkframes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
