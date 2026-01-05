import asyncio
from typing import Dict, List, Callable, Any, Awaitable
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    topic: str
    sender_id: str
    data: Dict[str, Any]
    sender_priority: int = 1 # Default priority
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Event], Awaitable[None]]]] = defaultdict(list)
        self._history: List[Event] = []

    def subscribe(self, topic: str, handler: Callable[[Event], Awaitable[None]]):
        """Register a handler for a specific topic."""
        self._subscribers[topic].append(handler)
        print(f"[EventBus] Subscribed to '{topic}'")

    async def publish(self, event: Event):
        """Broadcast an event to all subscribers."""
        self._history.append(event)
        
        # Notify specific topic subscribers + wildcard subscribers
        # Use a new list to avoid mutating the original subscriber lists
        handlers = list(self._subscribers[event.topic]) + list(self._subscribers["*"])
        
        print(f"[EventBus] Publishing '{event.topic}' from {event.sender_id} to {len(handlers)} handlers")
        
        if not handlers:
            return

        # Execute handlers concurrently
        await asyncio.gather(*[h(event) for h in handlers], return_exceptions=False) # Set to False to see errors in logs

    def get_history(self) -> List[Event]:
        return self._history
