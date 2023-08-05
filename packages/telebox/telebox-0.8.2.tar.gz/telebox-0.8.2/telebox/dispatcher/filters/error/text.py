from telebox.dispatcher.filters.error_filter import AbstractErrorFilter
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType


class ErrorTextFilter(AbstractErrorFilter):

    def __init__(self, *texts: str, full_match: bool = True, ignore_case: bool = False):
        if not texts:
            raise ValueError("No texts!")

        self._texts = {i.lower() for i in texts} if ignore_case else set(texts)
        self._full_match = full_match
        self._ignore_case = ignore_case

    def get_value(self, error: Exception, event: Event, event_type: EventType) -> str:
        return str(error)

    def check_value(self, value: str) -> bool:
        if self._ignore_case:
            value = value.lower()

        if self._full_match:
            return value in self._texts
        else:
            return any(i in value for i in self._texts)
