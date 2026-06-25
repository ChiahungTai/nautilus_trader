# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
from nautilus_trader.execution.matching_core import MatchingCore
from nautilus_trader.execution.messages import SubmitOrder, TradingCommand

class OrderEmulator(Any):
    """
    Provides order emulation for specified trigger types.

    Parameters
    ----------
    portfolio : PortfolioFacade
        The read-only portfolio for the order emulator.
    msgbus : MessageBus
        The message bus for the order emulator.
    cache : Cache
        The cache for the order emulator.
    clock : Clock
        The clock for the order emulator.
    config : OrderEmulatorConfig, optional
        The configuration for the order emulator.

    """
    debug: bool
    command_count: int
    event_count: int

    def __init__(self, portfolio: Any, msgbus: Any, cache: Any, clock: Any, config: Any | None | None=None) -> None:
        ...

    @property
    def subscribed_quotes(self) -> list[Any]:
        """
        Return the subscribed quote feeds for the emulator.

        Returns
        -------
        list[InstrumentId]

        """

    @property
    def subscribed_trades(self) -> list[Any]:
        """
        Return the subscribed trade feeds for the emulator.

        Returns
        -------
        list[InstrumentId]

        """

    def get_submit_order_commands(self) -> dict[Any, SubmitOrder]:
        """
        Return the emulators cached submit order commands.

        Returns
        -------
        dict[ClientOrderId, SubmitOrder]

        """

    def get_matching_core(self, instrument_id: Any) -> MatchingCore | None:
        """
        Return the emulators matching core for the given instrument ID.

        Returns
        -------
        MatchingCore or ``None``

        """

    def on_start(self) -> None:
        ...

    def on_event(self, event: Any) -> None:
        """
        Handle the given `event`.

        Parameters
        ----------
        event : Event
            The received event to handle.

        """

    def on_stop(self) -> None:
        ...

    def on_reset(self) -> None:
        ...

    def on_dispose(self) -> None:
        ...

    def execute(self, command: TradingCommand) -> None:
        """
        Execute the given command.

        Parameters
        ----------
        command : TradingCommand
            The command to execute.

        """

    def create_matching_core(self, instrument_id: Any, price_increment: Any) -> MatchingCore:
        """
        Create an internal matching core for the given `instrument`.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the matching core.
        price_increment : Price
            The minimum price increment (tick size) for the matching core.

        Returns
        -------
        MatchingCore

        Raises
        ------
        KeyError
            If a matching core for the given `instrument_id` already exists.

        """

    def on_order_book_deltas(self, deltas) -> None:
        ...

    def on_quote_tick(self, tick: Any) -> None:
        ...

    def on_trade_tick(self, tick: Any) -> None:
        ...