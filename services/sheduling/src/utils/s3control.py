import json
import logging
import os
from pathlib import Path
from typing import List

import boto3
from botocore.exceptions import ClientError

from utils import TMP_FLD

logger = logging.getLogger(__name__)

########
# AWS S3
########

_bucket_instance = None


class S3ClientError(Exception):
    pass


class S3NotFoundError(Exception):
    pass


def _get_bucket_object():
    global _bucket_instance
    if _bucket_instance is not None:
        return _bucket_instance
    cfg_path = Path(__file__).parent.as_posix() + '/config.json'
    with open(cfg_path) as f:
        cfg = json.load(f)['s3']

    bucket_name = cfg['bucket_name']
    s3_region = cfg['s3_region']
    s3_profile = cfg['s3_profile']

    session = boto3.session.Session(profile_name=s3_profile, region_name=s3_region)
    s3 = session.resource('s3')

    _bucket_instance = s3.Bucket(bucket_name)
    return _bucket_instance


def get_model_buckets(prefix='automlracer') -> List[str]:
    bucket = _get_bucket_object()
    model_names = {obj.key.split('/')[0] for obj in bucket.objects.filter(Prefix=prefix)}
    model_names = sorted(model_names)
    logger.info(f"S3: {model_names}")
    return model_names


def load_file(model_name: str, fname: str, out_fld=TMP_FLD) -> str:
    assert model_name
    assert fname
    assert out_fld
    bucket = _get_bucket_object()
    source_fpath = f'{model_name}/{fname}'

    out_fld = os.path.join(out_fld, model_name)
    os.makedirs(out_fld, exist_ok=True)
    out_fpath = os.path.join(out_fld, os.path.basename(fname))
    try:
        bucket.download_file(source_fpath, out_fpath)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            raise S3NotFoundError(e)
        else:
            raise S3ClientError(e)
    return out_fpath
