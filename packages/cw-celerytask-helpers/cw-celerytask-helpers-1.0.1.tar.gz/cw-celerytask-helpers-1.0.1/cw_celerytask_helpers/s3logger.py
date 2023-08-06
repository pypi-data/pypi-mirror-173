"""Helpers for managing logging to S3 in cubicweb-celerytask workers

Add this module 'cw_celerytask_helpers.s3logger' to CELERY_IMPORTS
"""
from __future__ import absolute_import

import os
import logging
from signal import Signals

import celery
from celery import signals

from .s3utils import get_bucket_name, get_key_name, get_s3_client
from .s3utils import get_task_logs, flush_task_logs  # noqa


@signals.task_prerun.connect
def setup_logging(conf=None, **kwargs):
    bucket = get_bucket_name()
    if not bucket:
        raise RuntimeError(
            "You asked for S3-based log storage of the task logs "
            "but CUBICWEB_CELERYTASK_S3_BUCKET is not configured. "
            "Please either set CUBICWEB_CELERYTASK_S3_BUCKET in your "
            "celery configuration, or set the AWS_S3_BUCKET_NAME "
            "environment variable.")
    task_id = kwargs.get('task_id')
    if task_id in ('???', None):
        return
    key = get_key_name(task_id)
    handler = S3Handler(level=logging.DEBUG, bucket=bucket, key=key,
                        task_id=task_id)
    handler.setFormatter(logging.Formatter(
        fmt="%(levelname)s %(asctime)s %(module)s %(process)d %(message)s\n"))
    logger = logging.getLogger('celery.task')
    logger.addHandler(handler)


@signals.task_postrun.connect
def uninstall_logging(conf=None, **kwargs):
    task_id = kwargs.get('task_id')
    if task_id in ('???', None):
        return
    logger = logging.getLogger('celery.task')
    for handler in logger.handlers:
        if isinstance(handler, S3Handler):
            logger.removeHandler(handler)
            handler.send()


@signals.task_revoked.connect
def send_revoked_log(conf=None, **kwargs):
    """executed on main celery process, hence logging handler is destroyed"""
    if 'signum' in kwargs and not isinstance(kwargs['signum'], Signals):
        # workaround for revoked task signal executed twice
        return
    request = kwargs.get('request')
    if not request:
        return
    task_id = request.get('id')
    if task_id in ('???', None):
        return
    bucket = get_bucket_name()
    if not bucket:
        return
    key = get_key_name(task_id)
    fname = get_log_file_name(task_id)
    if not os.path.exists(fname):
        return
    try:
        client = get_s3_client()
        with open(fname, 'rb') as fobj:
            client.upload_fileobj(fobj, bucket, key)
    finally:
        os.unlink(fname)


class S3Handler(logging.Handler):
    def __init__(self, *args, **kwargs):
        self.key = kwargs.pop('key')
        self.bucket = kwargs.pop('bucket')
        self.task_id = kwargs.pop('task_id')
        self.closed = False
        self.fobj = open(get_log_file_name(self.task_id), 'w+b')
        self.s3_cnx = get_s3_client()
        super(S3Handler, self).__init__(*args, **kwargs)

    def emit(self, record):
        if self.closed or record.task_id in ('???', None):
            return
        formatted = self.format(record)
        self.fobj.write(formatted.encode('utf-8'))

    def send(self):
        self.closed = True
        try:
            self.fobj.seek(0)
            self.s3_cnx.upload_fileobj(self.fobj, self.bucket, self.key)
            self.fobj.close()
        finally:
            os.unlink(self.fobj.name)


def get_log_file_name(task_id):
    tmpdir = celery.current_app.conf.get(
        'CUBICWEB_CELERYTASK_S3_TMPDIR', '/tmp')
    return '%s/%s' % (tmpdir, task_id)
