from dataclasses import dataclass

@dataclass(frozen=True)
class YouTubeChannel():
    id: str
    name: str
    subscriber_count: int