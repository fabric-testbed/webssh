import sys
import logging
import logging.handlers
import os.path as path
import os
from webssh._version import __version__, __version_info__


__author__ = 'Shengdun Hua <webmaster0115@gmail.com> bastion support by Ilya Baldin <ibaldin@renci.org>'

if sys.platform == 'win32' and sys.version_info.major == 3 and \
        sys.version_info.minor >= 8:
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


sshlogger = None
if path.exists('log/'):
    # instantiate a logger into a file
    sshlogger = logging.getLogger('ssh_logger')
    fh = logging.handlers.RotatingFileHandler(f'log/webssh-{os.environ["HOSTNAME"]}.log',
                                              maxBytes=10*1024*1024, backupCount=5)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    fh.setFormatter(formatter)
    sshlogger.addHandler(fh)
    sshlogger.info(f'WebSSH Logging system initialized on host {os.environ["HOSTNAME"]}')
    fh.flush()
