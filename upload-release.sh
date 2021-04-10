#!/bin/sh -l

if $TWINE_USERNAME == "" || $TWINE_PASSWORD == ""
then
    echo "No twine info in the environment variables"
    return -1
fi

python setup.py sdist bdist_wheel
echo "Build finished"

# TODO: check if dist & build directory are existing and also with the correct files

echo "Twine init"
twine upload dist/*
echo "Twine ended"