from __future__ import annotations

import argparse
from typing import Literal, overload

from .battle import BattleManager
from .parse import parse_ko


@overload
def game(
    name1: str,
    name2: str,
    seed: str = "",
    return_as_list: Literal[True] = True,
) -> list[str]:
    ...


@overload
def game(
    name1: str,
    name2: str,
    seed: str = "",
    return_as_list: Literal[False] = False,
) -> str:
    ...


@overload
def game(
    name1: str,
    name2: str,
    seed: str = "",
    return_as_list: bool = False,
) -> str | list[str]:
    ...


def game(
    name1: str,
    name2: str,
    seed: str = "",
    return_as_list: bool = False,
) -> str | list[str]:
    battle_manager = BattleManager(name1, name2, seed)
    result = battle_manager.battle()
    result_parse = parse_ko(result)

    if return_as_list:
        return result_parse

    return "\n".join(result_parse)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("name1", type=str)
    parser.add_argument("name2", type=str)
    parser.add_argument("-s", "--seed", type=str)
    args = parser.parse_args()

    result = game(args.name1, args.name2, args.seed, return_as_list=False)
    print(result)


if __name__ == "__main__":
    cli()
