[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# tpfinalpython

[![GitHub issues](https://img.shields.io/github/issues/lossh/tpfinalpython.svg?style=plastic)](https://github.com/lossh/tpfinalpython/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/lossh/tpfinalpython.svg?style=plastic)](https://github.com/lossh/tpfinalpython/graphs/contributors)
[![GitHub last commit](https://img.shields.io/github/last-commit/lossh/tpfinalpython.svg?style=plastic)](https://github.com/lossh/tpfinalpython/commits/master)
[![HitCount](http://hits.dwyl.io/lossh/tpfinalpython.svg?style=plastic)](http://hits.dwyl.io/lossh/tpfinalpython)

## Dependencias
[Python 3.6](https://www.python.org/downloads/release/python-368/) (con 3.7 no anda la librería [pattern](https://github.com/clips/pattern/issues/243#issuecomment-430067331)):

`python3 --version`

`sudo apt-get update`

`sudo apt-get install python3.6`

Si no se encuentra:
```
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6
```
[PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/#installing-pysimplegui):

`python3 -m pip install pysimplegui`

[playsound](https://pypi.org/project/playsound/):

`python3 -m pip install playsound`

Y para este último se necesita gst:

`sudo apt-get install python-gst-1.0`

[Pattern](https://github.com/clips/pattern#installation):

`python3 -m pip install pattern3`.

<details>
  <summary>Errores</summary>
  
  Errores al intentar instalar pattern:
`python3 -m pip install pattern`
```
OSError: mysql_config not found
```
`sudo pip3 install pattern`
```
OSError: mysql_config not found
```
`sudo pip3 install pattern3`
```
THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE. If you have updated the package versions, please update the hashes. Otherwise, examine the package contents carefully; someone may have tampered with them.
    pattern3 from https://www.piwheels.org/simple/pattern3/pattern3-3.0.0-py2.py3-none-any.whl#sha256=149eee8bbf7a4960d5445fedfffbc35182506181d784221186ca040bc2d1b98c:
        Expected sha256 149eee8bbf7a4960d5445fedfffbc35182506181d784221186ca040bc2d1b98c
             Got        ec5d73acec5bccd8849a375942b4226b8ed9c29ebacca566a389a50662ce92aa
```
`sudo pip install pattern`
```
CherryPy requires Python '>=3.5' but the running Python is 2.7.13
```
`sudo pip3 install pattern`
```
TypeError: unsupported operand type(s) for -=: 'Retry' and 'int'
```
`pip3 install pattern`
```
TypeError: unsupported operand type(s) for -=: 'Retry' and 'int'
```
`pip3 install pattern`
```
TypeError: unsupported operand type(s) for -=: 'Retry' and 'int'
```
</details>

# Clonar de github:
```console
git clone https://github.com/lossh/tpfinalpython
cd tpfinalpython
```
# Correr _run.py_ 
`python3 run.py`
