#!/usr/bin/bash

if TWINE_USERNAME == "" || TWINE_PASSWORD == ""
then
    echo "No twine username"
    exit()
fi

exec python .\setup.py sdist bdist_wheel

# TODO: check if dist & build directory are existing and also with the correct files

exec twine -u TWINE_USERNAME -p TWINE_PASSWORD upload dist/*