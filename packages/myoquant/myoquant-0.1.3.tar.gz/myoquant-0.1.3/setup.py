# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myoquant']

package_data = \
{'': ['*']}

install_requires = \
['cellpose>=2.1.0,<3.0.0',
 'csbdeep>=0.7.2,<0.8.0',
 'imageio>=2.21.1,<3.0.0',
 'pandas>=1.4.3,<2.0.0',
 'rich',
 'scikit-image>=0.19.3,<0.20.0',
 'stardist>=0.8.3,<0.9.0',
 'tensorflow>=2.9.1,<3.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['myoquant = myoquant.__main__:app']}

setup_kwargs = {
    'name': 'myoquant',
    'version': '0.1.3',
    'description': 'Command line interface (CLI) for MyoQuant, my histology image quantification tool.',
    'long_description': "# MyoQuant\n\nMyoQuant command line tool to quantifying pathological feature in histology images.  \nIt is built using CellPose, Stardist and custom models and image analysis techniques to automatically analyze myopathy histology images. An online demo with a web interface is availiable at [https://lbgi.fr/MyoQuant/](https://lbgi.fr/MyoQuant/).\n\n### **Warning:** This tool is still in alpha stage and might not work perfectly... yet.\n\n## How to install\n\n### Installing from PyPi\n\nUsing pip, you can simply install MyoQuant in a python environnement with a simple: `pip install myoquant`\n\n### Installing from source\n\n1. Clone this repository using `git clone https://github.com/lambda-science/MyoQuant.git`\n2. Create a virtual environnement by using `python -m venv .venv`\n3. Activate the venv by using `source .venv/bin/activate`\n4. Install MyoQuant by using `pip install -e .`\n\nYou are ready to go !\n\n## How to Use\n\nTo use the command-line tool, first activate your venv `source .venv/bin/activate`  \nThen you can perform SDH or HE analysis. You can use the command `myoquant --help` to list available commands.\n\n- **For SDH Image Analysis** the command is:  \n  `myoquant sdh_analysis IMAGE_PATH`  \n  Don't forget to run `myoquant sdh_analysis --help` for information about options.\n- **For HE Image Analysis** the command is:  \n  `myoquant he_analysis IMAGE_PATH`  \n   Don't forget to run `myoquant he_analysis --help` for information about options.\n\n_If you're running into an issue such as `myoquant: command not found` please check if you activated your virtual environment with the package installed. And also you can try to run it with the full command: `python -m myoquant sdh_analysis --help`_\n\n## Examples\n\nFor HE Staining analysis, you can download this sample image: [HERE](https://www.lbgi.fr/~meyer/SDH_models/sample_he.jpg)  \nFor SDH Staining analysis, you can download this sample image: [HERE](https://www.lbgi.fr/~meyer/SDH_models/sample_sdh.jpg)\n\n1. Example of successful SDH analysis with: `myoquant sdh_analysis sample_sdh.jpg`\n\n![image](https://user-images.githubusercontent.com/20109584/198278737-24d69f61-058e-4a41-a463-68900a0dcbb6.png)\n\n2. Example of successful HE analysis with: `myoquant he_analysis sample_he.jpg`\n\n![image](https://user-images.githubusercontent.com/20109584/198280366-1cb424f5-50af-45f9-99d1-34e191fb2e20.png)\n\n## Who and how\n\n- Creator and Maintainer: [Corentin Meyer, 3rd year PhD Student in the CSTB Team, ICube — CNRS — Unistra](https://lambda-science.github.io/)\n- The source code for this application is available [HERE](https://github.com/lambda-science/MyoQuant)\n\n## Advanced informations\n\nFor the SDH Analysis our custom model will be downloaded and placed inside the myoquant package directory. You can also download it manually here: [https://lbgi.fr/~meyer/SDH_models/model.h5](https://lbgi.fr/~meyer/SDH_models/model.h5) and then you can place it in the directory of your choice and provide the path to the model file using:  \n`myoquant sdh_analysis IMAGE_PATH --model_path /path/to/model.h5`\n",
    'author': 'Corentin Meyer',
    'author_email': 'corentin.meyer@etu.unistra.fr',
    'maintainer': 'Corentin Meyer',
    'maintainer_email': 'corentin.meyer@etu.unistra.fr',
    'url': 'https://lbgi.fr/MyoQuant/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
