import glob
import os
import shutil

import requests

from blam_sdk.agent_core.agent_conf import AgentConf
from blam_sdk.services import AssetService


class BaseActionHandler:
    ### Abstract methods
    @staticmethod
    def get_action_config():
        raise NotImplementedError()

    def inner_perform_action(self, message_body, asset_path=None):
        raise NotImplementedError()

    def prepare_action(self, message_body, asset_path=None):
        pass

    ### Core methods
    def __init__(
        self,
        agent_conf: AgentConf,
        clean_before=True,
        clean_after=True,
        download_asset=False,
    ):
        self.agent_conf = agent_conf
        self.asset_service = AssetService()
        self._clean_before = clean_before
        self._clean_after = clean_after
        self._download_asset = download_asset

    def perform_action(self, message_body={}):
        if self._clean_before:
            self.clean_working_dir()

        if self._download_asset:
            asset_path = self.download_action_asset(message_body)
        else:
            asset_path = None

        self.prepare_action(message_body, asset_path)
        self.inner_perform_action(message_body, asset_path)

        if self._clean_after:
            self.clean_working_dir()

    def download_action_asset(self, message_body):
        download_url = self.asset_service.get_download_url(
            message_body["asset_id"]
        )
        file_ext = download_url.split("?")[0].split(".")[-1]
        req = requests.get(download_url, stream=True)
        dl_path = f"{self.agent_conf.working_dir}/{message_body['asset_id']}.{file_ext}"
        with open(dl_path, "wb") as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return dl_path

    def clean_working_dir(self):
        files = glob.glob(f"{self.agent_conf.working_dir}/*")
        for f in files:
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.remove(f)
