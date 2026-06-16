# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
import cython

class Command:
    """
    The base class for all command messages.

    Parameters
    ----------
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    correlation_id : UUID4, optional
        The correlation ID. If provided, this command is correlated to another command or request.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """
    id: Any
    ts_init: int
    correlation_id: Any

    def __init__(self, command_id: Any, ts_init: int, correlation_id: Any=None):
        ...

    def __getstate__(self):
        ...

    def __setstate__(self, state):
        ...

    def __eq__(self, other: Command) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

class Document:
    """
    The base class for all document messages.

    Parameters
    ----------
    document_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """
    id: Any
    ts_init: int

    def __init__(self, document_id: Any, ts_init: int):
        ...

    def __getstate__(self):
        ...

    def __setstate__(self, state):
        ...

    def __eq__(self, other: Document) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

@cython.auto_pickle(False)
class Event:
    """
    The abstract base class for all event messages.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """

    @property
    def id(self) -> Any:
        """
        The event message identifier.

        Returns
        -------
        UUID4

        """

    @property
    def ts_event(self) -> int:
        """
        UNIX timestamp (nanoseconds) when the event occurred.

        Returns
        -------
        int

        """

    @property
    def ts_init(self) -> int:
        """
        UNIX timestamp (nanoseconds) when the object was initialized.

        Returns
        -------
        int

        """

class Request:
    """
    The base class for all request messages.

    Parameters
    ----------
    callback : Callable[[Any], None]
        The delegate to call with the response.
    request_id : UUID4
        The request ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    correlation_id : UUID4, optional
        The correlation ID. If provided, this request is correlated to another request.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """
    id: Any
    ts_init: int
    callback: object
    correlation_id: Any

    def __init__(self, callback: Callable[[Any], None] | None, request_id: Any, ts_init: int, correlation_id: Any=None):
        ...

    def __getstate__(self):
        ...

    def __setstate__(self, state):
        ...

    def __eq__(self, other: Request) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

class Response:
    """
    The base class for all response messages.

    Parameters
    ----------
    correlation_id : UUID4
        The correlation ID.
    response_id : UUID4
        The response ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """
    id: Any
    ts_init: int
    correlation_id: Any

    def __init__(self, correlation_id: Any, response_id: Any, ts_init: int):
        ...

    def __getstate__(self):
        ...

    def __setstate__(self, state):
        ...

    def __eq__(self, other: Response) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...