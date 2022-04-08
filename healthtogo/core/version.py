from typing import Optional
from functools import lru_cache
import json
import os
import dateutil.parser


HERE = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(HERE, '..', 'static')


@lru_cache(maxsize=1)
def get_build_info() -> Optional[dict]:
    civars_json_path = f'{STATIC_DIR}/civars.json'
    if os.path.exists(civars_json_path):
        with open(civars_json_path) as raw_build_info:
            res = json.load(raw_build_info)

            if 'CI_BUILD_EPOCH' not in res and 'BUILD_DATE' in res:
                res['CI_BUILD_EPOCH'] = int(dateutil.parser.parse(res['BUILD_DATE']).strftime('%s'))

            return res
    return {}


def app_version(default_version="unknown") -> str:
    """Setup Sentry.io reporting of exceptions"""
    build_info: dict = get_build_info()

    if build_info:
        return (build_info.get('CI_COMMIT_TAG') or
                build_info.get('CI_COMMIT_SHA', default_version))
    else:
        return default_version
