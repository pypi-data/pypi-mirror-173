import atexit
import enum
import readline  # type: ignore  (Just importing readline activates it)
import statistics
import sys
import time
from abc import ABC, abstractmethod
from sys import stdout
from typing import (
    Any,
    Dict,
    Literal,
    Callable,
    Generic,
    Iterable,
    List,
    NoReturn,
    Optional,
    Tuple,
    TypeVar,
)
import typing

import blessings
import colorama


__all__ = [
    "Widget",
    "TextLine",
    "ProgressBar",
    "print",
    "print_chapter",
    "warning",
    "error",
    "fatal",
    "input",
    "Option",
    "select",
    "ask_short_option",
    "ask_yes_no",
]

# Keep track of global state
_active_widget: "Widget | None" = None
_chapter: str | None = None
_is_first_line = True


T = TypeVar("T")


_SENTINEL = object()


_py_input = input


class Widget(ABC):
    def __init__(self):
        self._parent: Optional[Widget] = None

    def mark_dirty(self) -> None:
        # If this widget has a parent, let that handle the call instead
        if self._parent is not None:
            self._parent.mark_dirty()
            return

        # The widget isn't active, there is nothing it can do
        if not self.is_active:
            return

        # Redraw
        term = blessings.Terminal()
        stdout.write(term.clear_bol())  # type: ignore
        stdout.write(term.move_x(0 if _chapter is None else 3))
        self.draw(term)

    @property
    def is_active(self) -> bool:
        return self is _active_widget

    def on_activate(self) -> None:
        pass

    def on_deactivate(self) -> None:
        pass

    @abstractmethod
    def draw(self, term: blessings.Terminal) -> None:
        pass


class TextLine(Widget):
    _text: str

    def __init__(self, text: str = ""):
        super().__init__()

        self.text = text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: Any) -> None:
        self._text = str(value)
        self.mark_dirty()

    def draw(self, term: blessings.Terminal) -> None:
        stdout.write(self.text)
        stdout.flush()


class Unit(enum.Enum):
    COUNT = enum.auto()
    PERCENT = enum.auto()
    BYTE = enum.auto()
    TIME = enum.auto()

    @classmethod
    def from_string(cls, value: Literal["count", "percent", "byte", "time"]) -> "Unit":
        if value == "count":
            return cls.COUNT
        elif value == "percent":
            return cls.PERCENT
        elif value == "byte":
            return cls.BYTE
        elif value == "time":
            return cls.TIME
        else:
            raise ValueError(f"Unknown unit type: {value}")

    def _units(self) -> Iterable[Tuple[str, float, bool]]:
        """
        Return names of all units for this type and the divisor to convert from
        the base unit to them. The results are ordered from smallest to largest.
        In addition, a boolean is also returned, which indicates whether this
        unit is favorable (i.e. not an outdated or otherwise undesirable unit).
        """

        if self is Unit.COUNT:
            yield "", 1, True

        elif self is Unit.PERCENT:
            yield "%", 100, True

        elif self is Unit.BYTE:
            yield "B", 1, True
            yield "KB", 1000, False
            yield "KiB", 1024, True
            yield "MB", 1000**2, False
            yield "MiB", 1024**2, True
            yield "GB", 1000**3, False
            yield "GiB", 1024**3, True
            yield "TB", 1000**4, False
            yield "TiB", 1024**4, True
            yield "PB", 1000**5, False
            yield "PiB", 1024**5, True

        elif self is Unit.TIME:
            yield "ms", 1 / 1000, True
            yield "s", 1, False
            yield "second", 1, True
            yield "m", 60, False
            yield "minute", 60, True
            yield "h", 60 * 60, False
            yield "hour", 60 * 60, True
            yield "d", 60 * 60 * 24, False
            yield "day", 60 * 60 * 24, True

        else:
            raise NotImplementedError(f"Unknown unit type: {self}")

    def pretty_approximate_value(self, value: int | float) -> str:
        # Count specific: there is nothing to do here
        if self == Unit.COUNT:
            return str(value)

        # Time: This is a special case, because multiple units are used in the
        # result
        if self == Unit.TIME:
            seconds = int(value)

            # Special case: 0
            if seconds == 0:
                return "0 seconds"

            # Determine the time, in multiple sub-units
            units = (
                ("second", 60),
                ("minute", 60),
                ("hour", 24),
                ("day", None),
            )

            parts = []

            amount = seconds
            for unit_info in units:
                unit_name, unit_factor = unit_info

                if unit_factor is None:
                    cur = amount
                else:
                    cur = amount % unit_factor
                    amount = amount // unit_factor

                if cur == 0:
                    continue

                parts.append((unit_name, cur))

            # Drop any pointless ones
            while len(parts) > 2:
                parts.pop(0)

            # Turn everything into a string
            chunks = []
            for unit_name, amount in reversed(parts):
                if amount == 1:
                    chunks.append(f"1 {unit_name}")

                else:
                    chunks.append(f"{amount} {unit_name}s")

            return " ".join(chunks)

        # All other units: Find the largest unit that is still smaller than the
        # value
        unit_name, unit_factor = "", 1

        for next_unit_name, next_unit_factor, desirable in self._units():
            if not desirable:
                continue

            if value < next_unit_factor:
                break

            unit_name, unit_factor = next_unit_name, next_unit_factor

        # Round as appropriate
        unit_value = value / unit_factor

        if unit_value == int(unit_value):
            unit_value = int(unit_value)
        elif unit_value < 10:
            unit_value = round(unit_value, 1)
        else:
            unit_value = round(unit_value)

        return f"{unit_value}{unit_name}"  # type: ignore


class ProgressBar(Widget):
    _progress: float
    _width: int

    def __init__(
        self,
        progress: int | float = 0.0,
        max: int | float = 1.0,
        width: int = 50,
        unit: Literal["count", "percent", "byte", "time"] = "percent",
    ):
        super().__init__()

        # Data used to predict an ETA. This is a list of (timestamp, progress)
        # tuples, with `progress` being in range [0, 1]
        self._progress_timestamps: List[Tuple[float, float]] = []

        self.max = max
        self.progress = progress
        self.width = width
        self.unit = unit

        # TODO styling:
        # - start, end
        # - start cap, end cap, one cap
        # - blocks

        # TODO: use the unit

    @property
    def progress(self) -> int | float:
        return self._progress

    @progress.setter
    def progress(self, value: int | float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("The progressbar's progress must be an integer or float")

        self._progress = value
        self.mark_dirty()

        # Keep track of the progress so an ETA can be calculated later on
        self._progress_timestamps.append((time.time(), min(value / self.max, 1.0)))

    @property
    def max(self) -> int | float:
        return self._max

    @max.setter
    def max(self, value: int | float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("The progressbar's maximum value must be a float")

        if value < 0:
            raise ValueError("The progressbar's maximum value cannot be negative")

        self._max = value
        self.mark_dirty()

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("The progressbar's width must be an integer")

        if value < 0:
            raise ValueError("The progressbar's width must be a positive integer")

        self._width = value
        self.mark_dirty()

    def draw(self, term: blessings.Terminal) -> None:
        # Display the progressbar
        fraction = min(self.progress / self.max, 1.0)

        # blocks = "░█"
        blocks = ".▏▎▍▌▋▊▉█"
        # blocks = "◻◼"
        # blocks = "▁▂▃▄▅▆▇█"
        # blocks = "░▒▓█"
        # blocks = ".-=#"

        n_blocks_remaining = self.width
        n_blocks_filled = int(fraction * n_blocks_remaining)
        stdout.write(n_blocks_filled * blocks[-1])
        n_blocks_remaining -= n_blocks_filled

        partial_frac = fraction * self.width - n_blocks_filled
        partial_index = round(partial_frac * (len(blocks) - 1))
        if n_blocks_remaining > 0 and partial_index != 0:
            stdout.write(blocks[partial_index])
            n_blocks_remaining -= 1

        stdout.write(colorama.Style.DIM)

        stdout.write(n_blocks_remaining * blocks[0])

        # Display written progress
        unit = Unit.from_string(self.unit)  # type: ignore
        stdout.write(colorama.Style.NORMAL)
        if unit == Unit.PERCENT:
            stdout.write(f"  {fraction*100:5.1f}%")
        elif unit == Unit.TIME:
            if fraction != 1:
                stdout.write(
                    f"  {unit.pretty_approximate_value(self.max - self.progress)}"
                )
        elif fraction == 0 or fraction == 1:
            stdout.write(f"  {unit.pretty_approximate_value(self.max)}")
        else:
            stdout.write(
                f"  {unit.pretty_approximate_value(self.progress)}{colorama.Style.DIM} ╱ {colorama.Style.NORMAL}{unit.pretty_approximate_value(self.max)}"
            )

        # Display an ETA
        speed_timestamps = []
        for ii in range(1, len(self._progress_timestamps)):
            prev_ts, prev_progress = self._progress_timestamps[ii - 1]
            cur_ts, cur_progress = self._progress_timestamps[ii]
            speed_timestamps.append(
                (cur_ts, (cur_progress - prev_progress) / (cur_ts - prev_ts))
            )

        # Get the speeds within a window, but also at least a minimum amount
        now = time.time()
        window_min = now - 30
        ii_min = len(speed_timestamps) - 6

        speeds = [
            speed
            for ii, (ts, speed) in enumerate(speed_timestamps)
            if (ts >= window_min or ii >= ii_min)
        ]

        if speed_timestamps and speed_timestamps[0][0] < now - 15 and fraction != 1:
            speed = statistics.median(speeds)
            eta = (1 - self.progress / max(self.max, 0.0001)) / max(speed, 0.0001)
            pretty_str = Unit.TIME.pretty_approximate_value(eta)

            stdout.write(colorama.Style.DIM)
            stdout.write(f" — about {pretty_str} remaining")

        stdout.write(colorama.Style.RESET_ALL)
        stdout.flush()


def get_active_widget() -> Optional[Widget]:
    return _active_widget


def print_chapter(name: str | None) -> None:
    global _chapter

    # Spacing to previous content
    stdout.write("\n")
    if not _is_first_line:
        stdout.write("\n")

    # Print the chapter name
    if name is not None:
        stdout.write(colorama.Style.BRIGHT)
        stdout.write(colorama.Fore.BLUE)
        stdout.write(" > ")
        stdout.write(name)
        stdout.write(colorama.Style.RESET_ALL)

    # Update global state
    _chapter = name


Tprint = TypeVar("Tprint", bound=Widget)


@typing.overload
def print(*values: Tprint, make_active: bool = True) -> Tprint:
    ...


@typing.overload
def print(*values: Any, make_active: bool = True) -> TextLine:
    ...


def print(*values: Any, make_active: bool = True) -> Widget:
    global _active_widget, _is_first_line

    # Convert the inputs to a single Widget
    if len(values) == 1 and isinstance(values[0], Widget):
        widget = values[0]
    else:
        widget = TextLine(" ".join(str(v) for v in values))

    # If requested, make it active
    if make_active:
        if _active_widget is not None:
            _active_widget.on_deactivate()

        widget.on_activate()
        _active_widget = widget

        stdout.write("\n")

    # Display the widget
    term = blessings.Terminal()

    stdout.write(term.clear_bol())  # type: ignore
    stdout.write(term.move_x(0 if _chapter is None else 3))

    widget.draw(term)

    # Re-display the active widget
    if not make_active and _active_widget is not None:
        stdout.write("\n")
        stdout.write(term.move_x(0 if _chapter is None else 3))
        _active_widget.draw(term)

    # Update global state
    _is_first_line = False

    return widget


def warning(*values: Any):
    """
    Displays a warning message, highlighted to draw attention to it.
    """
    print(
        colorama.Fore.YELLOW + "Warning:",
        *values,
        colorama.Style.RESET_ALL,
        make_active=False,
    )


def error(*values: Any):
    """
    Displays an error message, highlighted to draw attention to it.
    """
    return print(
        colorama.Fore.RED + "ERROR:",
        *values,
        colorama.Style.RESET_ALL,
        make_active=False,
    )


def fatal(*values: Any, status_code: int = 1) -> NoReturn:
    """
    Displays an error message, highlighted to draw attention to it, and then
    exits the program.
    """
    print(
        colorama.Fore.RED + colorama.Style.BRIGHT + "ERROR:",
        *values,
        colorama.Style.RESET_ALL,
        make_active=False,
    )
    sys.exit(status_code)


def input(
    prompt: str = "",
    default: T = _SENTINEL,
    *,
    parse: Callable[[str], T] = str,
) -> T:
    """
    Asks the user for a value and returns it. If `prompt` is given, it is
    displayed first. `parse` is applied to the user's input, and its result
    returned. If `parse` raises a `ValueError` the user is asked for another
    value. Lastly, if `default` is given, it is returned if the user enters an
    empty string.
    """

    # Ask for values, until a valid one comes along
    while True:
        # Get a value
        print(f"{prompt} ")
        value = _py_input().strip()

        # Use the default value?
        if not value and default is not _SENTINEL:
            return default  # type: ignore

        # Try to parse it, thus verifying it's valid
        try:
            value = parse(value)
        except ValueError:
            continue

        return value


class Option(Generic[T]):
    def __init__(
        self,
        name: str,
        value: Any,
        alt_names: Iterable[str] = tuple(),
        *,
        is_default: bool = False,
    ):
        if not isinstance(name, str):
            raise TypeError(f"Option names need to be strings, got {name!r}")

        alt_names = list(alt_names)
        for alt_name in alt_names:
            if not isinstance(alt_name, str):
                raise TypeError(
                    f"Option alt-names need to be strings, got {alt_name!r}"
                )

        if not isinstance(is_default, bool):
            raise TypeError(f"Option is_default needs to be a bool, got {is_default!r}")

        self.name = name
        self.value = value
        self.alt_names = alt_names
        self.is_default = is_default

    def _all_names(self) -> Iterable[str]:
        yield self.name
        yield from self.alt_names


def select(prompt: str = "", *options: Option[T]) -> T:
    """
    Asks the user to select one of the given options. If `prompt` is given, it
    is displayed first. The options are displayed as a numbered list, and the
    user is asked to select one of them. If the user enters an empty string, the
    default option is selected if provided.
    """

    opt_list = list(options)
    default_option: Optional[Option] = None

    for opt in opt_list:
        if not isinstance(opt, Option):
            raise TypeError(f"Options need to be Option instances, got {opt!r}")

        if opt.is_default:
            if default_option is not None:
                raise ValueError("Only one option can be the default")

            default_option = opt

    # Display the options
    print(prompt)
    for ii, option in enumerate(opt_list):
        print(f"{colorama.Style.DIM}{ii + 1}. {colorama.Style.NORMAL}{option.name}")

    # Ask for a selection
    while True:
        selection = input()

        # Select the default?
        if not selection and default_option is not None:
            return default_option.value

        # Was this a numeric selection?
        try:
            selection = int(selection)
        except ValueError:
            pass
        else:
            if 1 <= selection <= len(opt_list):
                return opt_list[selection - 1].value
            else:
                continue

        # Find all matching options
        matches = []
        selection_normalized = selection.lower()

        for option in opt_list:
            for name in option._all_names():
                name_normalized = name.lower()

                # Exact match, this is it
                if name_normalized == selection_normalized:
                    return option.value

                # Partial match, add it to the list
                if selection_normalized in name_normalized:
                    matches.append(option)
                    break

        # If there are no matches, try again
        if not matches:
            continue

        # If the match is unique, return it
        if len(matches) == 1:
            return matches[0].value

        # Otherwise, ask the user to discriminate between all matches
        return select("", *matches)


def ask_short_option(
    prompt: str,
    options: Dict[str, Any],
    *,
    default_str: Optional[str] = None,
    add_yes_no_options: bool = False,
) -> Any:
    """
    TODO
    """
    for opt in options.keys():
        assert opt == opt.lower(), opt

    # Prepared, commonly used options
    if add_yes_no_options:
        t = {
            "y": True,
            "yes": True,
            "1": True,
            "t": True,
            "true": True,
            "n": False,
            "no": False,
            "0": False,
            "f": False,
            "false": False,
        }
        t.update(options)
        options = t

    # Make sure the default is valid
    assert default_str is None or default_str == default_str.lower(), default_str
    assert default_str is None or default_str in options, (
        default_str,
        options.keys(),
    )

    # Prepare the option strings for the prompt. There's no point in showing all
    # options, as many map to the same values. Instead, show the first option
    # corresponding to each value, while prioritizing the default option.
    #
    # TODO: This currently requires the returned value to be hashable.
    primary_options = {}
    for opt, value in options.items():
        assert opt == opt.lower(), opt

        if default_str is not None and opt == default_str:
            opt = opt.upper()
            primary_options[value] = opt
        else:
            primary_options.setdefault(value, opt)

    options_string = "/".join(primary_options.values())
    full_prompt = f"{prompt} [{options_string}] "

    # Keep asking until there is a valid response
    while True:
        # Ask for input
        response = input(full_prompt).strip().lower()

        if not response and default_str is not None:
            response = default_str

        try:
            return options[response]
        except KeyError:
            pass

        # Ask again if it's invalid
        sys.stdout.write(f"\nPlease respond with one of {options_string}")


def ask_yes_no(prompt: str, default_value: Optional[bool] = None) -> bool:
    """
    Displays the prompt to the user, and returns True if the user responds with
    yes, and False if the user responds with no. If no input is entered and a
    default value is provided it is returned instead.

    The function makes a best effort to interpret the user's input, and will
    accept a variety of possible values.
    """
    if default_value is None:
        default_str = None
    elif default_value:
        default_str = "y"
    else:
        default_str = "n"

    return ask_short_option(
        prompt,
        {},
        default_str=default_str,
        add_yes_no_options=True,
    )


def _on_exit():
    stdout.write("\n")


atexit.register(_on_exit)
