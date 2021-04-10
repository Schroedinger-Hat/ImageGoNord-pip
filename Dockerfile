FROM python:3.9-slim

WORKDIR /
COPY upload-release.sh .

RUN pip install twine && pip install setuptools

RUN chmod +x upload-release.sh
ENTRYPOINT [ "upload-release.sh" ]