## WebSSH

[![Build Status](https://travis-ci.org/huashengdun/webssh.svg?branch=master)](https://travis-ci.org/huashengdun/webssh)
[![codecov](https://codecov.io/gh/huashengdun/webssh/branch/master/graph/badge.svg)](https://codecov.io/gh/huashengdun/webssh)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/webssh.svg)
![PyPI](https://img.shields.io/pypi/v/webssh.svg)


### Introduction

A simple web application to be used as an ssh client to connect to your ssh servers. It is written in Python, base on tornado, paramiko and xterm.js.

### Features

* SSH password authentication supported, including empty password.
* SSH public-key authentication supported, including DSA RSA ECDSA Ed25519 keys.
* Encrypted keys supported.
* Two-Factor Authentication (time-based one-time password) supported.
* Fullscreen terminal supported.
* Terminal window resizable.
* Auto detect the ssh server's default encoding.
* Modern browsers including Chrome, Firefox, Safari, Edge, Opera supported.

This version differs from the [original](https://github.com/huashengdun/webssh) in that
* It supports bastion hosts
* It takes separate login and private keys options for bastion and target hosts
* It resets the form after submission for security reasons (not to retain private keys)
* The paramiko code is modified to support logging in over a bastion host if bastion
host info is provided
* Form can be filled in remotely via two cookies provided by caller 
(`credentials` and `bastion_credentials`) and if cookies are set the form auto submits; this allows
external invocation (care must be taken to limit CSRF appropriately); cookies are
removed once used.
* Note that this only works with cookies being set in the same domain. Cookie setter should set a very limited expiry (a few seconds) and unset them if possible.

### Preview

![Login](preview/login.png)
![Terminal](preview/terminal.png)


### How it works
```
+---------+     http     +--------+    ssh    +-----------+
| browser | <==========> | webssh | <=======> | ssh server|
+---------+   websocket  +--------+    ssh    +-----------+
```

### Requirements

* Python 2.7/3.4+


### Quickstart

1. Install this app, run command `pip install webssh`
2. Start a webserver, run command `wssh`
3. Open your browser, navigate to `127.0.0.1:8888`
4. Input your data, submit the form.


### Server options

```bash
# start a http server with specified listen address and listen port
wssh --address='2.2.2.2' --port=8000

# start a https server, certfile and keyfile must be passed
wssh --certfile='/path/to/cert.crt' --keyfile='/path/to/cert.key'

# missing host key policy
wssh --policy=reject

# logging level
wssh --logging=debug

# log to file
wssh --log-file-prefix=main.log

# more options
wssh --help
```

### Browser console

```javascript
// connect to your ssh server
wssh.connect(hostname, port, username, password, privatekey, passphrase, totp);

// pass an object to wssh.connect
var opts = {
  hostname: 'hostname',
  port: 'port',
  username: 'username',
  password: 'password',
  privatekey: 'the private key text',
  passphrase: 'passphrase',
  totp: 'totp'
};
wssh.connect(opts);

// without an argument, wssh will use the form data to connect
wssh.connect();

// set a new encoding for client to use
wssh.set_encoding(encoding);

// reset encoding to use the default one
wssh.reset_encoding();

// send a command to the server
wssh.send('ls -l');
```

### Custom Font

To use custom font, put your font file in the directory `webssh/static/css/fonts/` and restart the server.

### URL Arguments

Support passing arguments by url (query or fragment) like following examples:

Passing form data (password must be encoded in base64, privatekey not supported)
```bash
http://localhost:8888/?hostname=xx&username=yy&password=str_base64_encoded
```

Passing a terminal background color
```bash
http://localhost:8888/#bgcolor=green
```

Passing a terminal font color
```bash
http://localhost:8888/#fontcolor=red
```

Passing a user defined title
```bash
http://localhost:8888/?title=my-ssh-server
```

Passing an encoding
```bash
http://localhost:8888/#encoding=gbk
```

Passing a font size
```bash
http://localhost:8888/#fontsize=24
```

Passing a command executed right after login
```bash
http://localhost:8888/?command=pwd
```

Passing a terminal type
```bash
http://localhost:8888/?term=xterm-256color
```

### Use Docker

Start up the app
```
docker-compose up
```

Tear down the app
```
docker-compose down
```

### Tests

Requirements
```
pip install pytest pytest-cov codecov flake8 mock
```

Use unittest to run all tests
```
python -m unittest discover tests
```

Use pytest to run all tests
```
python -m pytest tests
```

### Deployment

Running as a standalone app (in a venv, for example) with self-signed certs:
```bash
wssh --port=8888 --sslport=8889 --certfile='ssl/cert.pem' --keyfile='ssl/key.pem' --xheaders=False --policy=reject
```

Running without certs:
```bash
wssh --port=8888 --xheaders=False --policy=reject
```

Running in a Docker with self-signed certs (relies on cert and key files in ssl/; edit docker-entrypoint.sh):
```bash
$ docker compose -f docker-compose-self-signed.yml build
$ docker compose -f docker-compose-self-signed.yml up
```
Service will run on ports 8888(http) and 8889(https).

Running in a Docker with production certs (be sure to edit docker-compose-standalone.yml volumes section and docker-entrypoint.sh):
```bash
$ docker compose -f docker-compose-standalone.yml build
$ docker compose -f docker-compose-standalone.yml up
```
Service will run on ports 8888(http) and 8889(https).

Running behind an Nginx server with or without scaling (be sure to edit docker-compose-nginx.yml volumes section and docker-entrypoint.sh):
```bash
$ docker compose -f docker-compose-standalone.yml build
$ docker compose -f docker-compose-standalone.yml up
```
or if you want to scale up:
```bash
$ docker compose -f docker-compose-standalone.yml build
$ docker compose -f docker-compose-standalone.yml up --scale webssh=3
```
Service will run on ports 80(http) and 443(https).

Nginx configuration automatically redirects from port 80 to port 443 and uses `ip_hash` session stickiness which should support most reasonable cases.

More information on Nginx and docker-compose configuration can be found [here](https://pspdfkit.com/blog/2018/how-to-use-docker-compose-to-run-multiple-instances-of-a-service-in-development/)

### Tips

* For whatever deployment choice you choose, don't forget to enable SSL.
* By default plain http requests from a public network will be either redirected or blocked and being redirected takes precedence over being blocked.
* Try to use reject policy as the missing host key policy along with your verified known_hosts, this will prevent man-in-the-middle attacks. The idea is that it checks the system host keys file("~/.ssh/known_hosts") and the application host keys file("./known_hosts") in order, if the ssh server's hostname is not found or the key is not matched, the connection will be aborted.
