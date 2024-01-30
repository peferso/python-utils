import logging
import boto3
import numpy as np
import os


s3 = boto3.resource('s3')


def create_logger(
    name='default',
    level='INFO'
):
    grey = "\x1b[38;20m"
    # yellow = "\x1b[33;20m"
    # red = "\x1b[31;20m"
    # bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        fh = logging.StreamHandler()
        fh_formatter = logging.Formatter(
            grey +
            "[%(levelname)s]" +
            "[%(asctime)s]" +
            "[%(name)s:%(funcName)s]" +
            " %(message)s" +
            reset
        )
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)
    _level = getattr(logging, level)
    logger.setLevel(_level)
    logger.propagate = False
    return logger


def mkdirs(
    folder_path: str,
    logger: logging.Logger
):
    i = 1
    finished = False
    while not finished:
        folder = '/'.join(folder_path.split('/')[0:i])
        if folder.rsplit('/', 1)[-1] in [''] or '.' in folder.rsplit('/', 1)[-1]:
            msg = (
                f'Invalid directory: "{folder}". Please'
                ' pass a relative path not'
                ' starting with "." or "/", '
                ' neither intermediate "." nor multiple "//".'
            )
            logger.error(msg)
            raise Exception(msg)
        elif not os.path.exists(folder):
            os.mkdir(folder)
            logger.warning(f'Created directory: {folder}')
        else:
            logger.debug(f'Directory "{folder}" exists.')
        i += 1
        if folder == folder_path:
            finished = True
    else:
        logger.debug('Finished directories creation')


def download_file(
    bucket: s3.Bucket,
    file_s3_path: list,
    local_dir: str,
    logger: logging.Logger,
    error_logger: logging.Logger = None,
    preserve_file_name: bool = False,
    str_sep: str = ':',
    skip_download: bool = False
):
    """
    Downloads 1 file from s3 and saves it under
    tmp_dir.
    If preserve_file_name=True then will use
    only the json name, but note that this will
    override existing jsons with same name.
    If preserve_file_name=False then the full
    path to s3 replacing '/' by ':' will be used as
    name.
    """
    logger.debug(f'Downloading file {file_s3_path}...')
    if not os.path.exists(local_dir):
        mkdirs(local_dir, logger)
    if not preserve_file_name:
        json_name = file_s3_path.replace('/', str_sep)
    else:
        json_name = file_s3_path.rsplit('/', 1)[-1]
    local_file_path = f'{local_dir}/{json_name}'
    try:
        if not skip_download:
            bucket.download_file(
                file_s3_path,
                local_file_path
            )   
    except Exception as msg:
        if error_logger is not None:
            error_logger.error(f';{file_s3_path};{msg}')
        else:
            logger.error(f'Error downloading {file_s3_path}: {msg}')
    logger.debug('Done')
    return local_file_path


def list_folders_in_s3_path(
    path: str,
    bucket: s3.Bucket,
    bucket_name: str
) -> list:
    response = bucket\
        .meta\
        .client\
        .list_objects_v2(
            Bucket=bucket_name,
            Prefix=path,
            Delimiter='/'
        )
    # Extract folder names
    folders = [
        common_prefix.get('Prefix')
        for common_prefix in response.get('CommonPrefixes', [])
    ]
    return folders


def get_batch_slice(
    total_records: int,
    total_batches: int,
    batch: int,
    logger: logging.Logger
) -> tuple:
    batch_size = int(np.ceil(total_records/total_batches))
    i0 = (batch - 1)*batch_size
    i1 = min((batch)*batch_size, total_records)
    logger.info(f'Batch {batch} of {total_batches}.')
    logger.info(f'\tBatch size {batch_size}.')
    logger.info(f'\ti0 {i0}.')
    logger.info(f'\ti1 {i1}.')
    return (i0, i1)


def find_encoding(file):
    encodings = ['utf-8', 'latin-1', 'ascii', 'us-ascii', 'utf-16', 'utf-32']
    for encoding in encodings:
        try:
            with open(file, 'r', encoding=encoding) as f:
                _ = f.read()
        except Exception as msg:
            pass
        else:
            return encoding
    return 'utf-8'


def create_error_logger(
    logfile,
    logsdir,
    logger
):
    error_logger = logging.getLogger("error_logger")
    error_logger.setLevel(logging.DEBUG)
    if not os.path.exists(logsdir):
        mkdirs(logsdir, logger)
    if os.path.exists(logfile):
        os.remove(logfile)
    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(logging.DEBUG)
    # Create a formatter and attach it to the handler
    formatter = logging.Formatter("")
    file_handler.setFormatter(formatter)
    error_logger.addHandler(file_handler)
    return error_logger


def listfiles(dir):
    return [f'{dir}/{i}' for i in os.listdir(dir)]


def setup_bucket(
    bucket_name: str,
    profile_name: str
):
    boto3.setup_default_session(profile_name=profile_name)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    return bucket
