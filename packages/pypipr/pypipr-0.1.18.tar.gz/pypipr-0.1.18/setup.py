# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypipr']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.5,<0.5.0', 'pytz>=2022.4,<2023.0']

extras_require = \
{':platform_system == "Linux"': ['getch>=1.0,<2.0']}

setup_kwargs = {
    'name': 'pypipr',
    'version': '0.1.18',
    'description': 'The Python Package Index Project',
    'long_description': '# About\nThe Python Package Index Project (pypipr)\n\n\n# Setup\nInstall with pip\n```\npython -m pip install pypipr\n```\n\nTest with\n```python\nfrom pypipr.pypipr import Pypipr\nPypipr.test_print()\n```\n\n\n# Pypipr Class\n`test_print()` memastikan module sudah terinstal dan dapat dijalankan\n```python\nfrom pypipr.pypipr import Pypipr\nPypipr.test_print()\n```\n\n\n# pypipr\n`sets_ordered()` Hanya mengambil nilai unik dari suatu list\n\n```python\nfrom pypipr.pypipr import sets_ordered\n\narray = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]\nprint([i for i in sets_ordered(array)])\n```\n\n\n`list_unique()` sama seperti `sets_ordered()`\n\n```python\nfrom pypipr.pypipr import list_unique\n\narray = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]\nprint([i for i in list_unique(array)])\n```\n\n\n`chunck_array()` membagi array menjadi potongan dengan besaran yg diinginkan\n\n```python\nfrom pypipr.pypipr import chunck_array\n\narray = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]\nprint([i for i in chunck_array(array, 5)])\n```\n\n\n# iconsole\n`print_colorize()` print ke console dengan warna\n\n```python\nfrom pypipr.iconsole import print_colorize\nprint_colorize("Print some text")\n```\n\n\n`@Log()` / `Log decorator` akan melakukan print ke console. Mempermudah pembuatan log karena tidak perlu mengubah fungsi yg sudah ada. Berguna untuk memberikan informasi proses program yg sedang berjalan.\n\n```python\nfrom pypipr.iconsole import log\n\n@log("Calling some function")\ndef some_function():\n    ...\n    return\n```\n\n\n`print_log` akan melakukan print ke console. Berguna untuk memberikan informasi proses program yg sedang berjalan.\n\n```python\nfrom pypipr.iconsole import print_log\nprint_log("Standalone Log")\n```\n\n\n`input_char()` meminta masukan satu huruf tanpa menekan enter. Char tidak ditampilkan.\n\n```python\nfrom pypipr.iconsole import input_char\ninput_char("Input Char without print : ")\n```\n\n\n`input_char()` meminta masukan satu huruf tanpa menekan enter. Char ditampilkan.\n\n```python\nfrom pypipr.iconsole import input_char_echo\ninput_char_echo("Input Char n : ")\n```\n\n\n# idatetime\n`datetime_now()` memudahkan dalam membuat tanggal dan waktu untuk suatu timezone\n\n```python\nfrom pypipr.idatetime import datetime_now\ndatetime_now("Asia/Jakarta")\ndatetime_now("GMT")\ndatetime_now("Etc/GMT+7")\n```\n\n\n# iconstant\n`WINDOWS` True apabila berjalan di platform Windows\n\n```python\nfrom pypipr.iconstant import WINDOWS\nprint(WINDOWS)\n```\n\n\n`LINUX` True apabila berjalan di platform Linux\n\n```python\nfrom pypipr.iconstant import LINUX\nprint(LINUX)\n```\n\n\n# ifile\n`file_put_contents()` membuat file kemudian menuliskan contents ke file. Apabila file memiliki contents, maka contents akan di overwrite.\n\n```python\nfrom pypipr.ifile import file_put_contents\nfile_put_contents("ifile_test.txt", "Contoh menulis content")\n```\n\n\n`file_get_contents()` membaca contents file ke memory.\n\n```python\nfrom pypipr.ifile import file_get_contents\nprint(file_get_contents("ifile_test.txt"))\n```\n\n\n`create_folder()` membuat folder secara recursive.\n\n```python\nfrom pypipr.ifile import create_folder\ncreate_folder("contoh_membuat_folder")\ncreate_folder("contoh/membuat/folder/recursive")\ncreate_folder("./contoh_membuat_folder/secara/recursive")\n```\n\n\n# iregex\n`regex_multiple_replace()` Melakukan multiple replacement untuk setiap list regex. \n\n```python\nfrom pypipr.iregex import regex_multiple_replace\n\nregex_replacement_list = [\n    {"regex": r"\\{\\{\\s*ini\\s*\\}\\}", "replacement": "itu"},\n    {"regex": r"\\{\\{\\s*sini\\s*\\}\\}", "replacement": "situ"},\n]\ndata = "{{ ini }} adalah ini. {{sini}} berarti kesini."\ndata = regex_multiple_replace(data, regex_replacement_list)\nprint(data)\n```\n',
    'author': 'ufiapjj',
    'author_email': 'ufiapjj@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
