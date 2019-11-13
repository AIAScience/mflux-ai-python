import warnings

from mflux_ai.core import init as core_init
from mflux_ai.core import get_minio_client as core_get_minio_client
from mflux_ai.core import ensure_bucket_exists as core_ensure_bucket_exists
from mflux_ai.core import put_dataset as core_put_dataset
from mflux_ai.core import get_dataset as core_get_dataset


SERVER_HOST = "https://www.mflux.ai"
_minio_client = None


def init(project_token):
    """
    Note: This function has been moved from mflux_ai.mflux_ai to mflux_ai
    """
    warnings.warn(
        "The init function has been moved. If you are doing \n"
        "from mflux_ai import mflux_ai\n"
        'mflux_ai.init("your_project_token_goes_here")\n'
        "then you should instead do this:\n"
        "import mflux_ai\n"
        'mflux_ai.init("your_project_token_goes_here")',
        DeprecationWarning,
    )
    core_init(project_token)


def get_minio_client():
    """
    Note: This function has been moved from mflux_ai.mflux_ai to mflux_ai
    """
    warnings.warn(
        "The get_minio_client function has been moved. If you are doing \n"
        "from mflux_ai import mflux_ai\n"
        "mflux_ai.get_minio_client(...)\n"
        "then you should instead do this:\n"
        "import mflux_ai\n"
        "mflux_ai.get_minio_client(...)",
        DeprecationWarning,
    )
    return core_get_minio_client()


def ensure_bucket_exists(bucket_name):
    """
    Note: This function has been moved from mflux_ai.mflux_ai to mflux_ai
    """
    warnings.warn(
        "The ensure_bucket_exists function has been moved. If you are doing \n"
        "from mflux_ai import mflux_ai\n"
        "mflux_ai.ensure_bucket_exists(...)\n"
        "then you should instead do this:\n"
        "import mflux_ai\n"
        "mflux_ai.ensure_bucket_exists(...)",
        DeprecationWarning,
    )
    return core_ensure_bucket_exists(bucket_name)


def put_dataset(value, object_name, bucket_name="datasets"):
    """
    Note: This function has been moved from mflux_ai.mflux_ai to mflux_ai
    """
    warnings.warn(
        "The put_dataset function has been moved. If you are doing \n"
        "from mflux_ai import mflux_ai\n"
        "mflux_ai.ensure_bucket_exists(...)\n"
        "then you should instead do this:\n"
        "import mflux_ai\n"
        "mflux_ai.ensure_bucket_exists(...)",
        DeprecationWarning,
    )
    core_put_dataset(value, object_name, bucket_name)


def get_dataset(object_name, bucket_name="datasets"):
    """
    Note: This function has been moved from mflux_ai.mflux_ai to mflux_ai
    """
    warnings.warn(
        "The get_dataset function has been moved. If you are doing \n"
        "from mflux_ai import mflux_ai\n"
        "mflux_ai.ensure_bucket_exists(...)\n"
        "then you should instead do this:\n"
        "import mflux_ai\n"
        "mflux_ai.ensure_bucket_exists(...)",
        DeprecationWarning,
    )
    core_get_dataset(object_name, bucket_name)
