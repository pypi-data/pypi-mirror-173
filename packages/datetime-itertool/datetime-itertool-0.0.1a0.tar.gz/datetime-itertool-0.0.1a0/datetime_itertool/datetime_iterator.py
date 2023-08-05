import datetime
from typing import Protocol


class DateTimeIteratorInterface(Protocol):
    """Interface for datetime iterators."""

    def __iter__(self) -> 'DateTimeIteratorInterface':
        """Iterator entrypoint.

        :return: DateTimeIterator
        """
        raise NotImplementedError

    def __next__(self) -> datetime.datetime:
        """Iteration next value.

        :return: datetime.datetime
        :raises StopIteration: if iteration is ended
        """
        raise NotImplementedError


_default_step = datetime.timedelta(days=1)


class DateTimeIterator(DateTimeIteratorInterface):
    """Iterating by time."""

    _shift = datetime.timedelta(days=0)

    def __init__(
        self,
        start_datetime: datetime.datetime,
        finish_datetime: datetime.datetime,
        step: datetime.timedelta = _default_step,
    ):
        """Class constructor.

        :param start_datetime: datetime.datetime
        :param finish_datetime: datetime.datetime
        :param step: datetime.timedelta
        """
        self._start_datetime = start_datetime
        self._finish_datetime = finish_datetime
        self._step = step

    def __iter__(self):
        """Iterator entrypoint.

        :return: DateTimeIterator
        """
        return self

    def __next__(self):
        """Iteration next value.

        :return: datetime.datetime
        :raises StopIteration: if iteration is ended
        """
        if self._finish_datetime <= self._start_datetime:
            raise StopIteration
        iteration_value = self._start_datetime + self._shift
        if iteration_value >= self._finish_datetime:
            raise StopIteration
        self._shift += self._step  # noqa: WPS601 rewrite class attribute
        return iteration_value
