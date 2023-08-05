# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elpis',
 'elpis.datasets',
 'elpis.models',
 'elpis.trainer',
 'elpis.transcriber',
 'elpis.utils']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.6.1,<3.0.0',
 'librosa>=0.9.2,<0.10.0',
 'loguru>=0.6.0,<0.7.0',
 'pedalboard>=0.6.2,<0.7.0',
 'pympi-ling>=1.70.2,<2.0.0',
 'torch>=1.12.1,<2.0.0',
 'transformers>=4.23.1,<5.0.0']

setup_kwargs = {
    'name': 'elpis',
    'version': '0.1.1',
    'description': 'A library to perform automatic speech recognition with huggingface transformers.',
    'long_description': "# Elpis Core Library\n\nThe Core Elpis Library, providing a quick api to [:hugs: transformers](https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&sort=downloads)\nfor automatic-speech-recognition.\n\nYou can use the library to:\n\n- Perform standalone inference using a pretrained HFT model.\n- Fine tune a pretrained ASR model on your own dataset.\n- Generate text and Elan files from inference results for further analysis.\n\n## Documentation\n\nDocumentation for the library can be be found [here](https://coedl.github.io/elpis_lib/index.html).\n\n## Dependencies\n\nWhile we try to be as machine-independant as possible, there are some dependencies\nyou should be aware of when using this library:\n\n- Processing datasets (`elpis.datasets.processing`) requires `librosa`, which\n  depends on having `libsndfile` installed on your computer. If you're using\n  elpis within a docker container, you may have to manually install\n  `libsndfile`.\n- Transcription (`elpis.transcription.transcribe`) requires `ffmpeg` if your\n  audio you're attempting to transcribe needs to be resampled before it can\n  be used. The default sample rate we assume is 16khz.\n- The preprocessing flow (`elpis.datasets.preprocessing`) is free of external\n  dependencies.\n\n## Installation\n\nYou can install the elpis library with:\n`pip3 install elpis`\n",
    'author': 'Harry Keightley',
    'author_email': 'harrykeightley@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CoEDL/elpis_lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
