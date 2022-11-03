#!/usr/bin/env bash

# just say CMD ["run_server"] in Dockerfile and everything happens correctly
if [[ "$1" = 'run_server' ]]; then
    # setup virtual environment
    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

    # EDIT HERE TO SWITCH FROM STANDALONE TO BEHIND NGINX CONFIGURATION
    # run the standalonw server
    #python3 run.py --port=8888 --sslport=8889 --certfile=/etc/ssl/beta-5_fabric-testbed_net.pem --keyfile=/etc/ssl/beta-5_fabric-testbed_net.key 
    # run under nginx
    python3 run.py --port=8888 
else
    exec "$@"
fi
