# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2026 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

"""Type stubs for nautilus_trader.model.identifiers (Cython extension)."""

from typing import Any


class Identifier:
    """Abstract base class for all identifiers."""

    def __getstate__(self) -> str: ...
    def __setstate__(self, state: str) -> None: ...
    def __lt__(self, other: Identifier) -> bool: ...
    def __le__(self, other: Identifier) -> bool: ...
    def __gt__(self, other: Identifier) -> bool: ...
    def __ge__(self, other: Identifier) -> bool: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

    @property
    def value(self) -> str:
        """Return the identifier (ID) value."""
        ...


class Symbol(Identifier):
    """Represents a valid ticker symbol ID for a tradable instrument."""

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: Symbol) -> bool: ...
    def __hash__(self) -> int: ...

    def is_composite(self) -> bool:
        """Return True if the symbol string contains a period ('.')."""
        ...

    def root(self) -> str:
        """Return the symbol root (substring before first '.')."""
        ...

    def topic(self) -> str:
        """Return the symbol topic (root with '*' appended if composite)."""
        ...


class Venue(Identifier):
    """Represents a valid trading venue ID."""

    def __init__(self, name: str) -> None: ...
    def __eq__(self, other: Venue) -> bool: ...
    def __hash__(self) -> int: ...

    @staticmethod
    def from_code(code: str) -> Venue | None:
        """Return the venue with the given code from the built-in internal map."""
        ...

    def is_synthetic(self) -> bool:
        """Return True if the venue is 'SYNTH'."""
        ...


class InstrumentId(Identifier):
    """Represents a valid instrument ID (Symbol + Venue)."""

    def __init__(self, symbol: Symbol, venue: Venue) -> None: ...
    def __eq__(self, other: InstrumentId) -> bool: ...
    def __hash__(self) -> int: ...

    @property
    def symbol(self) -> Symbol:
        """Return the instrument ticker symbol."""
        ...

    @property
    def venue(self) -> Venue:
        """Return the instrument trading venue."""
        ...

    @staticmethod
    def from_str(value: str) -> InstrumentId:
        """Parse an instrument ID from string (e.g. 'BTCUSDT.BINANCE')."""
        ...

    def is_synthetic(self) -> bool:
        """Return True if the venue is 'SYNTH'."""
        ...

    @staticmethod
    def from_pyo3(pyo3_instrument_id: Any) -> InstrumentId: ...
    def to_pyo3(self) -> Any: ...


class TraderId(Identifier):
    """Represents a valid trader ID (e.g. 'TESTER-001')."""

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: TraderId) -> bool: ...
    def __hash__(self) -> int: ...

    def get_tag(self) -> str:
        """Return the order ID tag value (part after the hyphen)."""
        ...


class StrategyId(Identifier):
    """Represents a valid strategy ID (e.g. 'EMACross-001')."""

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: StrategyId) -> bool: ...
    def __hash__(self) -> int: ...

    def get_tag(self) -> str:
        """Return the order ID tag value (part after the hyphen)."""
        ...

    def is_external(self) -> bool:
        """Return True if this is the global 'external' strategy ID."""
        ...


class AccountId(Identifier):
    """Represents a valid account ID (e.g. 'IB-D02851908')."""

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: AccountId) -> bool: ...
    def __hash__(self) -> int: ...

    def get_issuer(self) -> str:
        """Return the account issuer (part before the hyphen)."""
        ...

    def get_id(self) -> str:
        """Return the account ID without issuer (part after the hyphen)."""
        ...


class ClientOrderId(Identifier):
    """Represents a valid client order ID (assigned by the Nautilus system)."""

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: ClientOrderId) -> bool: ...
    def __hash__(self) -> int: ...


class VenueOrderId(Identifier):
    """Represents a valid venue order ID (assigned by a trading venue)."""

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: VenueOrderId) -> bool: ...
    def __hash__(self) -> int: ...


class PositionId(Identifier):
    """Represents a valid position ID."""

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: PositionId) -> bool: ...
    def __hash__(self) -> int: ...

    @property
    def is_virtual(self) -> bool:
        """Return True if the position ID is virtual (starts with 'P-')."""
        ...


class ComponentId(Identifier):
    """Represents a valid component ID."""

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: ComponentId) -> bool: ...
    def __hash__(self) -> int: ...


class ClientId(Identifier):
    """Represents a system client ID."""

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: ClientId) -> bool: ...
    def __hash__(self) -> int: ...


class ExecAlgorithmId(Identifier):
    """Represents a valid execution algorithm ID."""

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: ExecAlgorithmId) -> bool: ...
    def __hash__(self) -> int: ...


class OrderListId(Identifier):
    """Represents a valid order list ID."""

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: OrderListId) -> bool: ...
    def __hash__(self) -> int: ...


class TradeId(Identifier):
    """Represents a valid trade match ID (max 36 chars)."""

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: TradeId) -> bool: ...
    def __hash__(self) -> int: ...


# ---------------------------------------------------------------------------
# Generic spread ID functions
# ---------------------------------------------------------------------------

GENERIC_SPREAD_ID_SEPARATOR: str

def new_generic_spread_id(
    instrument_ratios: list[tuple[InstrumentId, int]],
) -> InstrumentId:
    """Create a spread InstrumentId from a list of (instrument_id, ratio) tuples."""
    ...


def generic_spread_id_to_list(
    instrument_id: InstrumentId,
) -> list[tuple[InstrumentId, int]]:
    """Parse a spread InstrumentId back into a list of (instrument_id, ratio) tuples."""
    ...


def is_generic_spread_id(instrument_id: InstrumentId) -> bool:
    """Return True if the instrument ID is a spread instrument."""
    ...


def generic_spread_id_n_legs(instrument_id: InstrumentId) -> int:
    """Return the total number of legs in a spread instrument ID."""
    ...
