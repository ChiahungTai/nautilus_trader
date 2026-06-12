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

from typing import Any


class Condition:
    """Design-by-contract static condition checks. Raises on failure."""

    @staticmethod
    def is_true(predicate: bool, fail_msg: str, ex_type: type | None = ...) -> None:
        """Raise if predicate is False."""
        ...

    @staticmethod
    def is_false(predicate: bool, fail_msg: str, ex_type: type | None = ...) -> None:
        """Raise if predicate is True."""
        ...

    @staticmethod
    def none(argument: Any, param: str, ex_type: type | None = ...) -> None:
        """Raise if argument is not None."""
        ...

    @staticmethod
    def not_none(argument: Any, param: str, ex_type: type | None = ...) -> None:
        """Raise if argument is None."""
        ...

    @staticmethod
    def type(argument: Any, expected: type | tuple[type, ...], param: str, ex_type: type | None = ...) -> None:
        """Raise if argument is not an instance of expected type."""
        ...

    @staticmethod
    def type_or_none(argument: Any, expected: type | tuple[type, ...], param: str, ex_type: type | None = ...) -> None:
        """Raise if argument is not None and not an instance of expected type."""
        ...

    @staticmethod
    def callable(argument: Any, param: str, ex_type: type | None = ...) -> None:
        """Raise if argument is not callable."""
        ...

    @staticmethod
    def callable_or_none(argument: Any, param: str, ex_type: type | None = ...) -> None:
        """Raise if argument is not None and not callable."""
        ...

    @staticmethod
    def equal(argument1: Any, argument2: Any, param1: str, param2: str, ex_type: type | None = ...) -> None:
        """Raise if arguments are not equal."""
        ...

    @staticmethod
    def not_equal(argument1: Any, argument2: Any, param1: str, param2: str, ex_type: type | None = ...) -> None:
        """Raise if arguments are equal."""
        ...

    @staticmethod
    def list_type(argument: list, expected_type: type, param: str, ex_type: type | None = ...) -> None:
        """Raise if list contains elements not of expected type."""
        ...

    @staticmethod
    def dict_types(argument: dict, key_type: type, value_type: type, param: str, ex_type: type | None = ...) -> None:
        """Raise if dict keys/values do not match expected types."""
        ...

    @staticmethod
    def is_in(element: Any, collection: Any, param1: str, param2: str, ex_type: type | None = ...) -> None:
        """Raise if element is not in collection."""
        ...

    @staticmethod
    def not_in(element: Any, collection: Any, param1: str, param2: str, ex_type: type | None = ...) -> None:
        """Raise if element is in collection."""
        ...

    @staticmethod
    def not_empty(collection: Any, param: str, ex_type: type | None = ...) -> None:
        """Raise if collection is empty."""
        ...

    @staticmethod
    def empty(collection: Any, param: str, ex_type: type | None = ...) -> None:
        """Raise if collection is not empty."""
        ...

    @staticmethod
    def positive(value: float, param: str, ex_type: type | None = ...) -> None:
        """Raise if value is not positive (> 0)."""
        ...

    @staticmethod
    def positive_int(value: int, param: str, ex_type: type | None = ...) -> None:
        """Raise if integer value is not positive (> 0)."""
        ...

    @staticmethod
    def not_negative(value: float, param: str, ex_type: type | None = ...) -> None:
        """Raise if value is negative (< 0)."""
        ...

    @staticmethod
    def not_negative_int(value: int, param: str, ex_type: type | None = ...) -> None:
        """Raise if integer value is negative (< 0)."""
        ...

    @staticmethod
    def in_range(value: float, start: float, end: float, param: str, ex_type: type | None = ...) -> None:
        """Raise if value is outside [start, end] (inclusive, with epsilon)."""
        ...

    @staticmethod
    def in_range_int(value: int, start: int, end: int, param: str, ex_type: type | None = ...) -> None:
        """Raise if integer value is outside [start, end] (inclusive)."""
        ...

    @staticmethod
    def valid_string(argument: str, param: str, ex_type: type | None = ...) -> None:
        """Raise if string is None, empty, or whitespace."""
        ...


class PyCondition:
    """Pure-Python mirror of Condition. Same API, delegates to Condition internally."""

    @staticmethod
    def is_true(predicate: bool, fail_msg: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def is_false(predicate: bool, fail_msg: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def none(argument: Any, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def not_none(argument: Any, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def type(argument: Any, expected: type | tuple[type, ...], param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def type_or_none(argument: Any, expected: type | tuple[type, ...], param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def callable(argument: Any, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def callable_or_none(argument: Any, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def equal(argument1: Any, argument2: Any, param1: str, param2: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def not_equal(argument1: Any, argument2: Any, param1: str, param2: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def list_type(argument: list, expected_type: type, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def dict_types(argument: dict, key_type: type, value_type: type, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def is_in(element: Any, collection: Any, param1: str, param2: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def not_in(element: Any, collection: Any, param1: str, param2: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def not_empty(collection: Any, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def empty(collection: Any, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def positive(value: float, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def positive_int(value: int, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def not_negative(value: float, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def not_negative_int(value: int, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def in_range(value: float, start: float, end: float, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def in_range_int(value: int, start: int, end: int, param: str, ex_type: type | None = ...) -> None: ...

    @staticmethod
    def valid_string(argument: str, param: str, ex_type: type | None = ...) -> None: ...
