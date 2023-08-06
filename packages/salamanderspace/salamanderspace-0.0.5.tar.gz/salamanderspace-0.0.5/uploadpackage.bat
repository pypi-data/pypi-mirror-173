@ECHO OFF
py -m build
py -m twine upload dist/*
PAUSE