from .get import get
from .get_many import get_many
from .utility import rate_limit_time_left, is_rate_limit_exception, api_calls_made, api_calls_remaining
from .metadata import metadata
from .metric_complexity import metric_complexity
from .available_metrics import available_metrics, available_metrics_for_slug, available_metric_for_slug_since
from .batch import Batch
from .async_batch import AsyncBatch
from .api_config import ApiConfig
import pkg_resources
import requests
import json
from warnings import warn

PROJECT = 'sanpy'


def get_latest():
    url = 'https://pypi.python.org/pypi/%s/json' % (PROJECT)
    try:
        response = requests.get(url).text
        return json.loads(response)['info']['version']
    except requests.exceptions.RequestException as e:
        return pkg_resources.get_distribution(PROJECT).version
