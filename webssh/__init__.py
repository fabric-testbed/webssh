import sys
import logging
import os.path as path
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
    fh = logging.FileHandler('log/webssh.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    fh.setFormatter(formatter)
    sshlogger.addHandler(fh)
    sshlogger.info('WebSSH Logging system initialized')