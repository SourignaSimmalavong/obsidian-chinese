# MIT License
#
# Copyright (c) 2023 ESUNA - Sourigna SIMMALAVONG
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from enum import Enum, auto

from beartype import beartype
from beartype.typing import List


class ChineseToken(Enum):
    pinyin = auto(),
    ideogram = auto(),
    translation = auto(),


@beartype
def is_valid_format(format: List[ChineseToken]) -> bool:
    return format == [ChineseToken.pinyin, ChineseToken.ideogram, ChineseToken.translation] or \
           format == [ChineseToken.pinyin, ChineseToken.ideogram] or \
           format == [ChineseToken.ideogram, ChineseToken.pinyin, ChineseToken.translation] or \
           format == [ChineseToken.ideogram, ChineseToken.pinyin]
