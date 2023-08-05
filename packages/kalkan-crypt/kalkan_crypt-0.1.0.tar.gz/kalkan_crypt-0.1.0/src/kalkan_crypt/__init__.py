import os

from .adapter import KalkanAdapter


if os.environ.get('CI_COMMIT_TAG'):
    __version__ = os.environ['CI_COMMIT_TAG']
else:
    __version__ = os.environ.get('CI_JOB_ID', '0.1.0')
