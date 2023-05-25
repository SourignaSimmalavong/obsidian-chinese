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
from beartype.typing import List

opening_parenthesis: str = r'[\(（]'
closing_parenthesis: str = r'[\)）]'
ideogram: str = r'.'
tone1: str = 'āēīōūĀĒĪŌŪ'
tone2: str = 'áéíóúÁÉÍÓÚ'
tone3: str = 'ǎěǐǒǔǍĚǏǑǓ'
tone4: str = 'àèìòùÀÈÌÒÙ'
tone_neutral: str = ''


@beartype
def get_pinyin_word(tone: str) -> str:
    return fr'[a-zA-ZüÜ{tone}]+'


rules_to_html: List[str] = []
rules_to_edit: List[str] = []
for index, tone in enumerate([tone_neutral, tone1, tone2, tone3, tone4]):
    pinyin_word: str = get_pinyin_word(tone)
    # pinyin_words: str = rf'{pinyin_word}[\s+{pinyin_word}]*'
    cjk_range: str = '\u4e00-\u9fff'
    translation_character: str = fr'{cjk_range}a-zA-Z0-9\-\_\/\|\[\]\'\\āēīōūĀĒĪŌŪáéíóúÁÉÍÓÚǎěǐǒǔǍĚǏǑǓàèìòùÀÈÌÒÙäëïöüÄËÏÖÜâêîôûÂÊÎÔÛçÇ'
    translation_proposition: str = fr'[{translation_character}]+[\s{translation_character}]*'
    # translation_propositions: str = fr'/{translation_proposition}(?<=/){translation_proposition}*/'

    tone_index: int = index  # + 1

    ######################################
    # writing to html

    # Using single quotes instead of double quotes so that we can also use it in frontmatter metadata for dataview.

    # (ideogram pinyin translation)
    chinese_edit_input1: str = f'{opening_parenthesis}({ideogram})\s+({pinyin_word})\s+({translation_proposition}){closing_parenthesis}'
    chinese_html_output1: str = fr"<span class='container tone{tone_index}'><span class='sup'>$3</span><span class='ideogram'>$1</span><span class='sub'>$2</span></span>"
    # (pinyin ideogram translation)
    chinese_edit_input2: str = f'{opening_parenthesis}({pinyin_word})\s+({ideogram})\s+({translation_proposition}){closing_parenthesis}'
    chinese_html_output2: str = fr"<span class='container tone{tone_index}'><span class='sup'>$3</span><span class='ideogram'>$2</span><span class='sub'>$1</span></span>"
    # (ideogram pinyin)
    chinese_edit_input3: str = f'{opening_parenthesis}({ideogram})\s+({pinyin_word}){closing_parenthesis}'
    chinese_html_output3: str = fr"<span class='container tone{tone_index}'><span class='ideogram'>$1</span><span class='sub'>$2</span></span>"
    # (pinyin ideogram)
    chinese_edit_input4: str = f'{opening_parenthesis}({pinyin_word})\s+({ideogram}){closing_parenthesis}'
    chinese_html_output4: str = fr"<span class='container tone{tone_index}'><span class='ideogram'>$2</span><span class='sub'>$1</span></span>"

    ######################################
    # html to writing
    tone_range: str = '[0-4]'

    # (pinyin ideogram translation)
    chinese_html_input2: str = fr"<span class='container tone{tone_range}'><span class='sup'>({translation_proposition})</span><span class='ideogram'>({ideogram})</span><span class='sub'>({pinyin_word})</span></span>"
    chinese_edit_output2: str = f'($3 $2 $1)'
    # (pinyin ideogram)
    chinese_html_input4: str = fr"<span class='container tone{tone_range}'><span class='ideogram'>({ideogram})</span><span class='sub'>({pinyin_word})</span></span>"
    chinese_edit_output4: str = f'($2 $1)'

    rules_to_html += [f""""{chinese_edit_input1}"->"{chinese_html_output1}\"""",
                      f""""{chinese_edit_input2}"->"{chinese_html_output2}\"""",
                      f""""{chinese_edit_input3}"->"{chinese_html_output3}\"""",
                      f""""{chinese_edit_input4}"->"{chinese_html_output4}\""""]
    rules_to_edit += [f""""{chinese_html_input2}"->"{chinese_edit_output2}\"""",
                      f""""{chinese_html_input4}"->"{chinese_edit_output4}\""""]

if __name__ == '__main__':
    for rule in rules_to_html:
        print(rule)

    print('--------------------------------------------')

    for rule in rules_to_edit:
        print(rule)
