import asyncio
from viam.module.module import Module
try:
    from models.copy_cloud_config import CopyCloudConfig
except ModuleNotFoundError:
    # when running as local module with run.sh
    from .models.copy_cloud_config import CopyCloudConfig


if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
