# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable

class OrderManager:
    """
    Provides a generic order execution manager.

    Parameters
    ----------
    clock : Clock
        The clock for the order manager.
    msgbus : MessageBus
        The message bus for the order manager.
    cache : Cache
        The cache for the order manager.
    component_name : str
        The component name for the order manager.
    active_local : str
        If the manager is for active local orders.
    submit_order_handler : Callable[[SubmitOrder], None], optional
        The handler to call when submitting orders.
    cancel_order_handler : Callable[[Order], None], optional
        The handler to call when canceling orders.
    modify_order_handler : Callable[[Order, Quantity], None], optional
        The handler to call when modifying orders (limited to modifying quantity).
    debug : bool, default False
        If debug mode is active (will provide extra debug logging).

    Raises
    ------
    TypeError
        If `submit_order_handler` is not ``None`` and not of type `Callable`.
    TypeError
        If `cancel_order_handler` is not ``None`` and not of type `Callable`.
    TypeError
        If `modify_order_handler` is not ``None`` and not of type `Callable`.
    """
    active_local: bool
    debug: bool
    log_events: bool
    log_commands: bool

    def __init__(self, clock: Any, msgbus: Any, cache: Any, component_name: str, active_local: bool, submit_order_handler: Any | None=None, cancel_order_handler: Any | None=None, modify_order_handler: Any | None=None, debug: bool=False, log_events: bool=True, log_commands: bool=True):
        ...

    def get_submit_order_commands(self) -> dict:
        """
        Return the managers cached submit order commands.

        Returns
        -------
        dict[ClientOrderId, SubmitOrder]

        """

    def cache_submit_order_command(self, command: Any) -> None:
        """
        Cache the given submit order `command` with the manager.

        Parameters
        ----------
        command : SubmitOrder
            The submit order command to cache.

        """

    def pop_submit_order_command(self, client_order_id: Any) -> Any:
        """
        Pop the submit order command for the given `client_order_id` out of the managers
        cache (if found).

        Parameters
        ----------
        client_order_id : ClientOrderId
            The client order ID for the command to pop.

        Returns
        -------
        SubmitOrder or ``None``

        """

    def reset(self) -> None:
        """
        Reset the manager, clearing all stateful values.
        """

    def cancel_order(self, order: Any) -> None:
        """
        Cancel the given `order` with the manager.

        Parameters
        ----------
        order : Order
            The order to cancel.

        """

    def modify_order_quantity(self, order: Any, new_quantity: Any) -> None:
        """
        Modify the given `order` with the manager.

        Parameters
        ----------
        order : Order
            The order to modify.

        """

    def create_new_submit_order(self, order: Any, position_id: Any=None, client_id: Any=None) -> None:
        """
        Create a new submit order command for the given `order`.

        Parameters
        ----------
        order : Order
            The order for the command.
        position_id : PositionId, optional
            The position ID for the command.
        client_id : ClientId, optional
            The client ID for the command.

        """

    def should_manage_order(self, order: Any) -> bool:
        """
        Check if the given order should be managed.

        Parameters
        ----------
        order : Order
            The order to check.

        Returns
        -------
        bool
            True if the order should be managed, else False.

        """

    def handle_event(self, event: Any) -> None:
        """
        Handle the given `event`.

        If a handler for the given event is not implemented then this will simply be a no-op.

        Parameters
        ----------
        event : Event
            The event to handle

        """

    def handle_order_rejected(self, rejected: Any) -> None:
        ...

    def handle_order_canceled(self, canceled: Any) -> None:
        ...

    def handle_order_expired(self, expired: Any) -> None:
        ...

    def handle_order_updated(self, updated: Any) -> None:
        ...

    def handle_order_filled(self, filled: Any) -> None:
        ...

    def handle_contingencies(self, order: Any) -> None:
        ...

    def handle_contingencies_update(self, order: Any) -> None:
        ...

    def handle_position_event(self, event: Any) -> None:
        ...

    def send_emulator_command(self, command: Any) -> None:
        ...

    def send_algo_command(self, command: Any, exec_algorithm_id: Any) -> None:
        ...

    def send_risk_command(self, command: Any) -> None:
        ...

    def send_exec_command(self, command: Any) -> None:
        ...

    def send_risk_event(self, event: Any) -> None:
        ...

    def send_exec_event(self, event: Any) -> None:
        ...