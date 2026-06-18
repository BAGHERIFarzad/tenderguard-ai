import os

from dotenv import load_dotenv

from band_room_adapter import BandRoomAdapter
from local_band_room import LocalBandRoom


load_dotenv()


def create_room(room_name: str):
    mode = os.getenv("AGENT_ROOM_MODE", "local").lower().strip()

    if mode == "band":
        return BandRoomAdapter(room_name)

    return LocalBandRoom(room_name)