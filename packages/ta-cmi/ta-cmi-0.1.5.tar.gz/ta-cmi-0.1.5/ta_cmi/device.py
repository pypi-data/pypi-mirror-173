from typing import Dict, Any, List

from aiohttp import ClientSession

from .baseApi import BaseAPI
from .channel import Channel

from .const import DEVICES, ReadOnlyClass, ChannelMode


class Device(BaseAPI, metaclass=ReadOnlyClass):
    """Class to interact with a device"""

    def __init__(self, node_id: str, host: str, username: str, password: str, session: ClientSession = None):
        """Initialize."""
        super().__init__(username, password, session)
        self.id: str = node_id
        self.host: str = host

        self.apiVersion: int = 0
        self.deviceType: str = "00"

        self.inputs: Dict[int, Channel] = {}
        self.outputs: Dict[int, Channel] = {}

    def _extractDeviceInfo(self, json: Dict[str, Any]):
        """Extract device info from request response."""
        self.apiVersion: int = json["Header"]["Version"]
        self.deviceType: str = json["Header"]["Device"]

    @staticmethod
    def _extractChannels(mode: ChannelMode, raw_channels: List[Dict[str, Any]]) -> Dict[int, Channel]:
        """Extract channel info from data array from request."""
        list_of_channels: Dict[int, Channel] = {}
        for channel_raw in raw_channels:
            ch: Channel = Channel(mode, channel_raw)
            list_of_channels[ch.index] = ch

        return list_of_channels

    async def update(self):
        """Update data."""
        url: str = f"{self.host}/INCLUDE/api.cgi?jsonparam=I,O&jsonnode={self.id}"
        res: Dict[str, Any] = await self._make_request(url)

        self._extractDeviceInfo(res)
        if "Inputs" in res["Data"]:
            self.inputs: Dict[int, Channel] = self._extractChannels(ChannelMode.INPUT, res["Data"]["Inputs"])
        if "Outputs" in res["Data"]:
            self.outputs: Dict[int, Channel] = self._extractChannels(ChannelMode.OUTPUT, res["Data"]["Outputs"])

    def getDeviceType(self) -> str:
        return DEVICES.get(self.deviceType, "Unknown")

    def __repr__(self) -> str:
        return f"Node {self.id}: Type: {self.getDeviceType()}, Inputs: {len(self.inputs)}, Outputs: {len(self.outputs)}"
