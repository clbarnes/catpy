#!/usr/bin/env python3
import datetime as dt
import runpy
from pathlib import Path
import warnings
from argparse import ArgumentParser


def get_current() -> str:
    proj_root = Path(__file__).resolve().parent
    version_path = proj_root / "catpy" / "version.py"

    return runpy.run_path(version_path)["__version__"]


def get_next(current) -> str:
    new_str = dt.date.today().strftime("%Y.%m.%d")

    if not current.startswith(new_str):
        return new_str

    trailing = current.split(".")[3:]
    if trailing:
        suffix = int(trailing[0]) + 1
        if suffix > 9:
            warnings.warn(
                f"Sub-day release ('{suffix}') has >1 digit, which will break version ordering."
            )
    else:
        suffix = 1

    return f"{new_str}.{suffix}"


def main():
    parser = ArgumentParser()
    parser.add_argument("-v", action="store_true", help="prefix with 'v'")
    parser.add_argument(
        "-c", "--current",
        action="store_true",
        help="return the current, rather than the next, version"
    )
    parsed = parser.parse_args()
    v = "v" if parsed.v else ""
    current = get_current()
    if parsed.current:
        print(v + current)
    else:
        print(v + get_next(current))


if __name__ == "__main__":
    main()
