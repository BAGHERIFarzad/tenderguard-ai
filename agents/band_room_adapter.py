import os
from typing import Optional

import requests
from dotenv import load_dotenv

from agent_models import AgentMessage, ReviewContext


load_dotenv(override=True)


class BandRoomAdapter:
    """
    Band adapter for TenderGuard AI.

    It stores every message locally for the app response,
    and when AGENT_ROOM_MODE=band, it also sends messages to Band.
    """

    def __init__(self, room_name: str):
        self.room_name = room_name
        self.base_url = os.getenv("BAND_BASE_URL", "https://app.band.ai").rstrip("/")
        self.chat_id = os.getenv("BAND_CHAT_ID", "").strip()
        self.orchestrator_api_key = os.getenv("BAND_ORCHESTRATOR_API_KEY", "").strip()
        self.verify_ssl = os.getenv("BAND_VERIFY_SSL", "true").lower().strip() != "false"
        
        print(f"[BandRoomAdapter] base_url={self.base_url}")
        print(f"[BandRoomAdapter] chat_id={self.chat_id}")
        print(f"[BandRoomAdapter] verify_ssl={self.verify_ssl}")

    def post_message(
        self,
        context: ReviewContext,
        from_agent: str,
        to_agent: str,
        message: str,
        message_type: str,
    ) -> None:
        local_message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message=message,
            message_type=message_type,
        )

        # Always keep local timeline for our API/frontend
        context.messages.append(local_message)

        if not self.chat_id or not self.orchestrator_api_key:
            context.messages.append(
                AgentMessage(
                    from_agent="Band Adapter",
                    to_agent="@Developer",
                    message=(
                        "Band mode is enabled, but BAND_CHAT_ID or "
                        "BAND_ORCHESTRATOR_API_KEY is missing. Message kept locally."
                    ),
                    message_type="Band Adapter Notice",
                )
            )
            return

        try:
            self._send_to_band(local_message)
        except Exception as exc:
            context.messages.append(
                AgentMessage(
                    from_agent="Band Adapter",
                    to_agent="@Developer",
                    message=f"Failed to send message to Band: {exc}",
                    message_type="Band Adapter Error",
                )
            )

    def _send_to_band(self, local_message: AgentMessage) -> Optional[dict]:
        url = f"{self.base_url}/api/v1/agent/chats/{self.chat_id}/messages"

        owner_id = os.getenv("BAND_OWNER_USER_ID", "").strip()
        owner_name = os.getenv("BAND_OWNER_NAME", "Farzad Bagheri").strip()
        owner_handle = os.getenv("BAND_OWNER_HANDLE", "farzadbagheri33").strip()

        band_text = (
            f"@{owner_handle}\n\n"
            f"**{local_message.from_agent} → {local_message.to_agent}**\n"
            f"[{local_message.message_type}]\n"
            f"{local_message.message}"
        )

        payload = {
            "message": {
                "content": band_text,
                "mentions": [
                    {
                        "id": owner_id,
                        "name": owner_name,
                        "handle": owner_handle,
                    }
                ],
            }
        }

        headers = {
            "X-API-Key": self.orchestrator_api_key,
            "Content-Type": "application/json",
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=20,
            verify=self.verify_ssl,
        )

        if not response.ok:
            raise RuntimeError(
                f"{response.status_code} {response.reason} - {response.text}"
            )

        return response.json() if response.content else {}