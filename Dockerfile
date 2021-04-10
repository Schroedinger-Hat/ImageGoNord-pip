FROM python:3.9-slim

WORKDIR /app
COPY upload-release.sh .

RUN pip install twine && pip install setuptools

RUN chmod +x upload-release.sh
ENTRYPOINT [ "/app/upload-release.sh" ]