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

import re
import shutil
import sys
from pathlib import Path

from beartype import beartype
from beartype.typing import List, Tuple, Dict

from Dictionnaire.chinese_struct import ChineseStruct
from Dictionnaire.chinese_token import ChineseToken, is_valid_format


# Grammar
# html_dict := line*\n
# line := (pinyin ideogram translation)
# pinyin := (a-zA-Zaccents)+
# ideogram := cjk_character
# translation := str

# full_ideogram_first := (ideogram pinyin translation)
# full_pinyin_first := (pinyin ideogram translation)  # original dict
# short_ideogram_first := (ideogram pinyin)
# short_pinyin_first := (pinyin ideogram)

@beartype
def split(line: str) -> Tuple[ChineseStruct, str]:
    line = line.strip()
    line = re.sub('\s+', ' ', line)

    if len(line) < 2:  # or line[0] != '(' or line[-1] != ')':
        raise Exception(f'invalid line: {line}')

    # line = line[1:-1]  # remove the parentheses
    tokens: List[str] = line.split(' ')
    if len(tokens) < 2:
        raise Exception(f'Invalid line, not enough tokens: {line}')
    elif len(tokens) == 2:  # only the pinyin and ideogram, no translation
        return ChineseStruct(tokens[0], tokens[1]), ''
    else:  # len(tokens) >= 3
        chinese_struct: ChineseStruct = ChineseStruct(tokens[0], tokens[1])
        translation: str = ' '.join(tokens[2:])
        return chinese_struct, translation


@beartype
def restructure(chinese_struct: ChineseStruct, translation: str, format: List[ChineseToken]) -> str:
    if not is_valid_format(format):
        raise Exception(f'Invalid format: {format}')

    new_line: str = ''
    for token in format:
        if token == ChineseToken.pinyin:
            new_line += f' {chinese_struct.pinyin}'
        elif token == ChineseToken.ideogram:
            new_line += f' {chinese_struct.ideogram}'
        elif token == ChineseToken.translation:
            new_line += f' {translation}'
        else:
            raise Exception(f'Unknown token: {token}')
    new_line = new_line.strip()
    new_line = f'({new_line})'

    return new_line


@beartype
def generate_html_dictionary(in_dict_path: Path, out_dict_path: Path, format: List[ChineseToken]):
    if in_dict_path == out_dict_path:
        raise Exception('in and out path should not be the same!')

    out_lines: List[str] = []
    with in_dict_path.open('r', encoding='utf-8') as in_dict_file:
        lines: List[str] = in_dict_file.readlines()
        for line in lines:
            if line.strip() == '':
                out_lines.append(line)
                continue
            parentheses: List[str] = line.split(')(')
            if not parentheses:
                raise Exception(f'invalid line: {parentheses}')
            parentheses[0] = parentheses[0].replace('(', '')
            parentheses[-1] = parentheses[-1].replace(')', '')
            out_parentheses: List[str] = []
            for parenthesis in parentheses:
                chinese_struct: ChineseStruct
                translation: str
                chinese_struct, translation = split(parenthesis)
                out_parentheses.append(restructure(chinese_struct, translation, format))
            # [:-1]: do not take the closing parenthesis (autocompletion)
            if out_parentheses[-1][-1] == ')':
                out_lines.append(''.join(out_parentheses)[:-1])
            else:
                out_lines.append(''.join(out_parentheses))
            # out_lines.append(''.join(out_parentheses))

    # Remove duplicates
    for i, line in enumerate(out_lines):
        if line.strip() != '':
            while line in out_lines[i + 1:]:
                index: int = out_lines[i + 1:].index(line) + i + 1
                out_lines.pop(index)

    out_lines = [f'{out_line}\n' for out_line in out_lines]
    out_lines = [re.sub('\n+', '\n', out_line) for out_line in out_lines]

    with out_dict_path.open('w', encoding='utf-8') as out_dict_file:
        out_dict_file.writelines(out_lines)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python generate_html_dictionary.py path_to_input_dictionary.md output_dir')
        raise Exception()

    src: Path = Path(sys.argv[1])
    out_dir: Path = Path(sys.argv[2])

    # Local backup, just in case
    shutil.copyfile(src, src.name)

    if not out_dir.is_dir():
        raise Exception(f'argument is not a dir: {out_dir}')

    formats: Dict[Path, List[ChineseToken]] = {
        # Just to have the same file without the closing parenthesis.
        out_dir.joinpath(Path(f'{src.stem}_full_pinyin_first{src.suffix}')): [ChineseToken.pinyin,
                                                                              ChineseToken.ideogram,
                                                                              ChineseToken.translation],
        out_dir.joinpath(Path(f'{src.stem}_short_pinyin_first{src.suffix}')): [ChineseToken.pinyin,
                                                                               ChineseToken.ideogram],
        out_dir.joinpath(Path(f'{src.stem}_full_han_first{src.suffix}')): [ChineseToken.ideogram,
                                                                           ChineseToken.pinyin,
                                                                           ChineseToken.translation],
        out_dir.joinpath(Path(f'{src.stem}_short_han_first{src.suffix}')): [ChineseToken.ideogram,
                                                                            ChineseToken.pinyin],
    }
    for path_out, format in formats.items():
        generate_html_dictionary(src, path_out, format)
