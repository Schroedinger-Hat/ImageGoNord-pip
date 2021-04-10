FROM python:3.9-slim

WORKDIR /
COPY upload-release.sh .

RUN chmod +x upload-release.sh
ENTRYPOINT [ "upload-release.sh" ]