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

from beartype import beartype
from beartype.typing import Final, List, Dict
import numpy as np

from numpy._typing import NDArray

# ǖ: TODO or not TODO?

untoned_characters_indices: Final[Dict[str, int]] = {'a': 0, 'e': 1, 'i': 2, 'o': 3, 'u': 4}
# a-- = ā
# a'  = á
# a`' = ǎ
# a`  = à
# a^^ = ǎ
# a`" = ǎ  # for convenience in dvorak programmer, no need to release the shift while doing both accents
tones: Final[NDArray] = np.array([['--', '', ''],
                                  [r"\'", '', ''],
                                  [r"`\'", r"\'\"", r"^^"],
                                  ['`', '', '']])
tones_indices: Final[Dict[int, int]] = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2}
other_accents: Final[NDArray] = np.array(['^', '..'])
other_accents_indices: Final[Dict[int, int]] = {1: 0, 2: 1}
lowercase_index: Final[int] = 0
uppercase_index: Final[int] = 1

unaccented_characters: Final[NDArray] = np.array(['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U'])
# [char][capital][accent]
toned_characters: Final[NDArray] = np.array([[['ā', 'á', 'ǎ', 'à'], ['Ā', 'Á', 'Ǎ', 'À']],
                                             [['ē', 'é', 'ě', 'è'], ['Ē', 'É', 'Ě', 'È']],
                                             [['ī', 'í', 'ǐ', 'ì'], ['Ī', 'Í', 'Ǐ', 'Ì']],
                                             [['ō', 'ó', 'ǒ', 'ò'], ['Ō', 'Ó', 'Ǒ', 'Ò']],
                                             [['ū', 'ú', 'ǔ', 'ù'], ['Ū', 'Ú', 'Ǔ', 'Ù']]])
# [char][capital][accent]
characters_other_accents: Final[NDArray] = np.array([[['â', 'ä'], ['Â', 'Ä']],
                                                     [['ê', 'ë'], ['Ê', 'Ë']],
                                                     [['î', 'ï'], ['Î', 'Ï']],
                                                     [['ô', 'ö'], ['Ô', 'Ö']],
                                                     [['û', 'ü'], ['Û', 'Ü']]])

unaccented_other_characters: Final[NDArray] = np.array(['c', 'C'])
other_characters_accents: Final[NDArray] = np.array([',,'])
# [char][accent][capital]
accented_other_characters: Final[NDArray] = np.array([[['ç'], ['Ç']]])

all_accented_characters: Final[NDArray] = np.dstack((toned_characters, characters_other_accents))


@beartype
def unaccented_character(c: str) -> str:
    assert len(c) == 1
    coords: NDArray = np.argwhere(all_accented_characters == c)
    if not coords:
        coords = np.argwhere(accented_other_characters == c)
        if not coords:
            return ''
        else:
            return unaccented_other_characters[coords[0]]
    return unaccented_characters[coords[0]]


@beartype
def make_add_accent_rule(inputs: NDArray) -> str:
    input: str
    accent: str
    output: str
    input, accent, output = inputs
    return f"'{input}{accent}|' -> '{output}|'"


@beartype
def make_remove_accent_rule(inputs: NDArray) -> str:
    input: str
    output: str
    input, output = inputs
    return f"'{input}|' -x '{output}|'"


@beartype
def make_correct_ellipsis_rule(inputs: NDArray) -> str:
    input: str
    output: str
    input, output = inputs
    return f"'{input}.|' -> '{output}...|'"


@beartype
def make_3rd_tone_from_double_quotes_rule(inputs: NDArray) -> str:
    input: str
    output: str
    input, output = inputs
    return f"'{input}\"|' -> '{output}|'"


@beartype
def make_3rd_tone_from_double_circumflex_rule(inputs: NDArray) -> str:
    input: str
    output: str
    input, output = inputs
    return f"'{input}^|' -> '{output}|'"


@beartype
def make_3rd_tone_from_quote_rule(inputs: NDArray) -> str:
    input: str
    output: str
    input, output = inputs
    return fr"'{input}\'|' -> '{output}|'"


@beartype
def make_3rd_tone_rules() -> List[str]:
    tone2: str = '`'
    tone2_index: int = np.where(tones == tone2)[0][0]
    # [char][capital][accent]
    input: NDArray = toned_characters[:, :, tone2_index]
    input = input.reshape([input.size, 1])
    tone3: str = r"`\'"
    tone3_index: int = np.where(tones == tone3)[0][0]
    output: NDArray = toned_characters[:, :, tone3_index]
    output = output.reshape([output.size, 1])
    input_output: NDArray = np.hstack((input, output))

    rules: List[str] = []
    # 'à'' to 'ǎ'
    rules += np.apply_along_axis(make_3rd_tone_from_quote_rule, 1, input_output).flat
    # 'à"' to 'ǎ'
    rules += np.apply_along_axis(make_3rd_tone_from_double_quotes_rule, 1, input_output).flat

    # 'â"' to 'ǎ'
    circumflex_index: int = np.where(other_accents == '^')[0][0]
    input = characters_other_accents[:, :, circumflex_index]
    input = input.reshape([input.size, 1])
    input_output: NDArray = np.hstack((input, output))
    rules += np.apply_along_axis(make_3rd_tone_from_double_circumflex_rule, 1, input_output).flat

    return rules


@beartype
def make_correct_ellipsis_rules() -> List[str]:
    # 'ä.' to 'a...'
    other_accent: str = '..'
    other_accent_index: int = np.where(other_accents == other_accent)[0][0]
    # [char][capital][accent]
    input: NDArray = characters_other_accents[:, :, other_accent_index]
    input = input.reshape([input.size, 1])
    input_output: NDArray = np.hstack(
        (input,
         unaccented_characters.reshape(([unaccented_characters.size, 1]))))
    current_rules: NDArray = np.apply_along_axis(make_correct_ellipsis_rule, 1, input_output)
    return List[str](current_rules.flat)


@beartype
def make_toneX_to_letter_rules() -> List[str]:
    rules: List[str] = []

    input: NDArray = toned_characters.reshape([toned_characters.size, 1])
    output: NDArray = unaccented_characters.reshape(([unaccented_characters.size, 1]))
    output = np.repeat(output, tones.shape[0])
    output = output.reshape(([output.size, 1]))
    input_output: NDArray = np.hstack((input, output))
    current_rules: NDArray = np.apply_along_axis(make_remove_accent_rule, 1, input_output)
    rules += current_rules.flat

    input: NDArray = accented_other_characters.reshape([accented_other_characters.size, 1])
    output: NDArray = unaccented_other_characters.reshape(([unaccented_other_characters.size, 1]))
    output = np.repeat(output, accented_other_characters.size / 2)  # div 2 because lower case and upper case
    output = output.reshape(([output.size, 1]))
    input_output: NDArray = np.hstack((input, output))
    current_rules: NDArray = np.apply_along_axis(make_remove_accent_rule, 1, input_output)
    rules += current_rules.flat

    # Characters like "ç" -> "c"
    # for other_characters_accent_index, other_characters_accent in enumerate(other_characters_accents):
    input: NDArray = accented_other_characters.reshape(([accented_other_characters.size, 1]))
    output: NDArray = unaccented_other_characters.reshape(([unaccented_other_characters.size, 1]))
    input_output: NDArray = np.hstack((input, output))
    current_rules: NDArray = np.apply_along_axis(make_remove_accent_rule, 1, input_output)
    rules += current_rules.flat

    return rules


@beartype
def make_letter_to_toneX_rules() -> List[str]:
    rules: List[str] = []
    for tone_index, tone in enumerate(tones):
        for tone_modifier in tone:
            if tone_modifier == '':
                continue
            # [char][capital][accent]
            output: NDArray = toned_characters[:, :, tone_index]
            output = output.reshape([output.size, 1])
            input_output: NDArray = np.hstack(
                (unaccented_characters.reshape(([unaccented_characters.size, 1])),
                 [[tone_modifier]] * unaccented_characters.size,
                 output))
            current_rules: NDArray = np.apply_along_axis(make_add_accent_rule, 1, input_output)
            rules += current_rules.flat

    # 'â' and 'ä' accents
    for other_accent_index, other_accent in enumerate(other_accents):
        # [char][capital][accent]
        output: NDArray = characters_other_accents[:, :, other_accent_index]
        output = output.reshape([output.size, 1])
        input_output: NDArray = np.hstack(
            (unaccented_characters.reshape(([unaccented_characters.size, 1])),
             [[other_accent]] * unaccented_characters.size,
             output))
        current_rules: NDArray = np.apply_along_axis(make_add_accent_rule, 1, input_output)
        rules += current_rules.flat

    # Characters like "c" -> "ç"
    for other_characters_accent_index, other_characters_accent in enumerate(other_characters_accents):
        output: NDArray = accented_other_characters[:, :, other_characters_accent_index]
        output = output.reshape([output.size, 1])
        input_output: NDArray = np.hstack(
            (unaccented_other_characters.reshape(([unaccented_other_characters.size, 1])),
             [[other_characters_accent]] * unaccented_other_characters.size, output))
        current_rules: NDArray = np.apply_along_axis(make_add_accent_rule, 1, input_output)
        rules += current_rules.flat

    return rules


@beartype
def make_other_rules() -> List[str]:
    return [
        r"'qu\'|' -> 'qu\'|'  # for French",
        r"')\n|)' -> ')|'  # for smoother auto-completion with obsidian-chinese",
        r"'\n|)' -> ')|'  # for smoother auto-completion with obsidian-chinese"
    ]


@beartype
def make_arrows_rules() -> List[str]:
    return [
        # Arrows
        r"'⇐>|' -> '⇔|'",
        r"'←>|' -> '↔|'",
        r"'=>|' -> '⇒|'",
        r"'<=|' -> '⇐|'",
        r"'->|' -> '→|'",
        r"'<-|' -> '←|'",
        r"'-^|' -> '↗|'  # '⤴|'",
        r"'-v|' -> '↘|'  # '⤵|'",
        r"'\|\|^|' -> '⇑|'",
        r"'\|\|v|' -> '⇓|'",
        r"'\|v|' -> '↓|'",
        r"'\|^|' -> '↑|'",
        r"'^\\|' -> '↖|'",
        r"'\\v|' -> '↘|'",
        r"'/^|' -> '↗|'",
        r"'v/|' -> '↙|'",
    ]


@beartype
def make_math_rules() -> List[str]:
    rules: Dict[str, str] = {
        'exists': '∃',
        'nexists': '∄',
        'sum': '∑',
        'prod': '∏',
        'bigcap': '⋂',
        'bigcup': '⋃',
        'in': '∈',
        'notin': '∉',
        'ni': '∋',
        'forall': '∀'
    }

    slash_rules: List[str] = []
    for a, b in rules.items():
        if a[0] != 'n':
            slash_rules.append(fr"'\{a}|' -> '{b}|'")

    dollar_rules: List[str] = []
    for a, b in rules.items():
        dollar_rules.append(fr"'${a}|' -> '{b}|'")

    return slash_rules + dollar_rules + [r"'=/=|' -> '≠|'"]


@beartype
def make_special_characters_rules() -> List[str]:
    return [
        r"'o->|' -> '♂|'",
        r"'o+|' -> '♀|'",
        r"'>o+|' -> '☿|'",
    ]


@beartype
def make_trigrams_rules() -> List[str]:
    return [
        r"'\|\|\||' -> '☰|'",
        r"':::|' -> '☷|'",
        r"'\|:\||' -> '☲|'",
        r"'::\||' -> '☳|'",
        r"'\|\|:|' -> '☴|'",
        r"':\|:|' -> '☵|'",
        r"'\|::|' -> '☶|'",
        r"':\|\||' -> '☱|'",
    ]


@beartype
def make_rules() -> str:
    rules: str = ''
    rules += '\n# Other rules\n'
    rules += '\n'.join(make_other_rules())
    rules += '\n# Normal letter to accented letter\n'
    rules += '\n'.join(make_letter_to_toneX_rules())
    rules += '\n# Accented letter to normal letter\n'
    rules += '\n'.join(make_toneX_to_letter_rules())
    rules += '\n# Ellipsis correction on unwanted diaeresis ("trema")\n'
    rules += '\n'.join(make_correct_ellipsis_rules())
    rules += '\n# 3rd tone from 2nd tone or from circumflex\n'
    rules += '\n'.join(make_3rd_tone_rules())
    rules += '\n#Special characters\n'
    rules += '\n'.join(make_special_characters_rules())
    rules += '\n# Arrow rules\n'
    rules += '\n'.join(make_arrows_rules())
    rules += '\n# Math symbols\n'
    rules += '\n'.join(make_math_rules())
    rules += '\n# Trigrams\n'
    rules += '\n'.join(make_trigrams_rules())

    return rules


if __name__ == '__main__':
    print(make_rules())
