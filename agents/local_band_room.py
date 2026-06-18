from agent_models import AgentMessage, ReviewContext


class LocalBandRoom:
    """
    Local simulation of a Band collaboration room.

    Later, this file will be replaced or extended with real Band SDK/API calls.
    For now, it proves the core workflow:
    - agent-to-agent messages
    - directed mentions
    - shared context
    - audit-style timeline
    """

    def __init__(self, room_name: str):
        self.room_name = room_name

    def post_message(
        self,
        context: ReviewContext,
        from_agent: str,
        to_agent: str,
        message: str,
        message_type: str,
    ) -> None:
        context.messages.append(
            AgentMessage(
                from_agent=from_agent,
                to_agent=to_agent,
                message=message,
                message_type=message_type,
            )
        )