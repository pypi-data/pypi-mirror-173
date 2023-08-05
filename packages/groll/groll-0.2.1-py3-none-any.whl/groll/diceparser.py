"""
Dice parsing using standard dice notation
"""

import math
import random
import re
from typing import List

from attrs import define


@define
class Dice:
    num: int
    sides: int

    def roll(self) -> List[int]:
        rolled = []
        for _ in range(self.num):
            rolled.append(random.randint(1, self.sides))
        return rolled

    def average(self, roundup=False):
        averaged = []
        for _ in range(self.num):
            if roundup:
                averaged.append(math.ceil((self.sides + 1) / 2))
            else:
                averaged.append(math.floor((self.sides + 1) / 2))
        return averaged

    def min(self):
        minimised = []
        for _ in range(self.num):
            minimised.append(1)
        return minimised

    def max(self):
        maxed = []
        for _ in range(self.num):
            maxed.append(self.sides)
        return maxed


@define
class DiceParser:
    roundup: bool = False
    debug: bool = False
    _ddict = {}

    def _count_sides(self, num_str: str):
        if not num_str:
            return 1
        return int(num_str)

    def _parse(self, input_):
        for die in re.finditer(r"(\d*)d(\d+)", input_):
            num, sides = map(self._count_sides, die.group().split("d"))
            self._ddict.update({die.group(): Dice(num, sides)})

    def roll(self, input_):
        self._parse(input_)
        out = input_
        for key, val in self._ddict.items():
            out = out.replace(key, str(sum((val.roll()))))
        return self.safe_eval(out)

    def average(self, input_):
        self._parse(input_)
        out = input_
        for key, val in self._ddict.items():
            out = out.replace(key, str(sum((val.average(roundup=self.roundup)))))
        return self.safe_eval(out)

    def min(self, input_):
        self._parse(input_)
        out = input_
        for key, val in self._ddict.items():
            out = out.replace(key, str(sum((val.min()))))
        return self.safe_eval(out)

    def max(self, input_):
        self._parse(input_)
        out = input_
        for key, val in self._ddict.items():
            out = out.replace(key, str(sum((val.max()))))
        return self.safe_eval(out)

    def safe_eval(self, dstr: str):
        out = dstr
        if self.debug:
            print(out)
        while True:
            match = re.search(r"(\d+)\s*([-+\/*])\s*(\d+)", out)
            if match:
                match_dict = match.groups()
                if match_dict[1] == "+":
                    out = out.replace(
                        match.group(), str(int(match_dict[0]) + int(match_dict[2]))
                    )
                elif match_dict[1] == "-":
                    out = out.replace(
                        match.group(), str(int(match_dict[0]) - int(match_dict[2]))
                    )
                elif match_dict[1] == "*":
                    out = out.replace(
                        match.group(), str(int(match_dict[0]) * int(match_dict[2]))
                    )
                else:
                    if self.roundup:
                        out = out.replace(
                            match.group(),
                            str(math.ceil(int(match_dict[0]) / int(match_dict[2]))),
                        )
                    else:
                        out = out.replace(
                            match.group(),
                            str(int(int(match_dict[0]) / int(match_dict[2]))),
                        )

                if self.debug:
                    print(out)
            else:
                break
        return out
