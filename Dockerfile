FROM python:3.17-alpine

LABEL maintainer='ibaldin@renci.org'
LABEL version='1.6.0b'

COPY . /code
WORKDIR /code

RUN \
  python3 -m pip install virtualenv && \
  apk add --no-cache libc-dev libffi-dev gcc bash && \
  pip install -r requirements.txt --no-cache-dir && \
  apk del gcc libc-dev libffi-dev && \
  addgroup webssh && \
  adduser -Ss /bin/false -g webssh webssh && \
  chown -R webssh:webssh /code

EXPOSE 8888/tcp
EXPOSE 8889/tcp
USER webssh

ENTRYPOINT ["/code/docker-entrypoint.sh"]
CMD ["run_server"]
