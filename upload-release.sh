#!/bin/sh -l

# if $TWINE_USERNAME == "" || $TWINE_PASSWORD == ""
# then
#     echo "No twine username"
#     return -1
# fi

exec python setup.py sdist bdist_wheel
echo "Build finished"

# TODO: check if dist & build directory are existing and also with the correct files

echo "Twine init"
exec twine upload dist/*
echo "Twine ended"