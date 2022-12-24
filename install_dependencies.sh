python3 -m pip install --upgrade pip
python3 -m pip install Unidecode
python3 -m pip install PyMuPDF || python3 -m pip install -Iv PyMuPDF==1.16.7

cd supports-color-python
python3 -m pip install setuptools
python3 -m pip install -Iv urllib3==1.25.11
python3 -m pip install edict
python3 setup.py install
cd ..

# python3 -m pip install -U supports-color
# python3 -m pip freeze > requirements.txt
# python3 -m pip install -r requirements.txt
# del requirements.txt