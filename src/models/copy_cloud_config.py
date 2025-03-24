from typing import ClassVar, Final, Mapping, Optional, Sequence

from typing_extensions import Self
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.services.generic import *
from viam.utils import SensorReading, ValueTypes, struct_to_dict
from viam.app.viam_client import ViamClient
from viam.rpc.dial import DialOptions

import os
import asyncio
import psutil
import os
import signal
import subprocess
import time

class CopyCloudConfig(Generic, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(
        ModelFamily("mcvella", "service"), "copy-cloud-config"
    )

    part_id: str = ""
    api_key_id: str = ""
    api_key: str = ""
    config_location: str = "/etc/viam.json"

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Generic service.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both implicit and explicit)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        attributes = struct_to_dict(config.attributes)
        
        part_id = attributes.get("part_id", "")
        if part_id == "":
            raise Exception(f"part_id must be defined, referencing an existing part_id.")

        api_key_id = attributes.get("api_key_id", "")
        if part_id == "":
            raise Exception(f"api_key_id must be defined, an api key ID that has access to the part_id from which you wish to copy config.")  
        
        api_key = attributes.get("api_key", "")
        if api_key == "":
            raise Exception(f"api_key must be defined, an api key that has access to the part_id from which you wish to copy config.")  
        
        return []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        attributes = struct_to_dict(config.attributes)
        
        self.part_id = attributes.get("part_id", "")
        self.api_key_id = attributes.get("api_key_id", "")
        self.api_key = attributes.get("api_key", "")

        self.config_location = attributes.get("config_location", "/etc/viam.json")


        asyncio.ensure_future(self.copy_config())
    
        return super().reconfigure(config, dependencies)

    async def viam_connect(self) -> ViamClient:
        dial_options = DialOptions.with_api_key( 
            api_key=self.api_key,
            api_key_id=self.api_key_id
        )

        return await ViamClient.create_from_dial_options(dial_options)
    
    def find_process(self, name):
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if proc.info['name'] == name:
                return proc.info['pid']
        return None

    def restart_process(self, process):
        pid = self.find_process(process)

        if pid:
            self.logger.info(f"Found {process} with PID {pid}. Restarting...")
            os.kill(pid, signal.SIGHUP)  # Gracefully restart

    async def copy_config(self):
        app_client = await self.viam_connect()
        part = await app_client.app_client.get_robot_part(self.part_id)
        cfg = '{"cloud":{"app_address":"https://app.viam.com:443", "id":"' + self.part_id + '", "secret":"' +  part.secret + '"}}'
        with open(self.config_location, "w") as file:
            file.write(cfg)

        self.restart_process("viam-server")

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        self.logger.error("`do_command` is not implemented")
        raise NotImplementedError()
