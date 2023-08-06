@ECHO OFF
cd package
py -m build
py -m twine upload dist/*
PAUSE