#!/usr/bin/env python3

from enum import IntEnum

class MineSweeperCellType(IntEnum): # type: ignore
    MINE = 0b0001
    OPEN = 0b0010
    CHECKED = 0b0100

    @classmethod
    @property
    def EMPTY(cls):
        return cls.MINE + 1


print(MineSweeperCellType.MINE)
print(MineSweeperCellType.EMPTY)
