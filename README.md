obsidian-chinese
================
Chinese tools and scripts for obsidian, for Chinese learning as a foreign language.

Partly inspired from the excellent [Chinese words separator](https://chrome.google.com/webstore/detail/chinese-words-separator/gacfacdpfimbkgcnlegknnmcccjgcbnp) chrome extension.

# Chinese tones, pinyin and translation HTML rendering
Raw input:<br />
![image](https://user-images.githubusercontent.com/47475038/229428006-d3359be6-d786-4830-b063-92461a6a7296.png)

HTML result after applying regex ruleset:<br />
![image](https://user-images.githubusercontent.com/47475038/229427966-cd561f07-5cbb-4dac-8c8f-497ecb21c4ef.png)

The conversion to html allows convenient way to display the ideogram, the pinyin, the translation and also a color depending on the tone.

Of course, another regex ruleset is available to switch back to raw input.<br />
The raw input may be more convenient for editing and the html output may be more convenient for final reading result.

The html rendering is available both in edit and reading views.

# Pinyin rules

Convenient ways to add different diacritics, chinese tones included:
```
a-- => ā
a'  => á
a^^ => ǎ
a`  => à

a`' => ǎ
a`" => ǎ

a^  => â
a.. => ä
```
(these are just human readable rules, not the actual rules to feed to [typing transformer](https://github.com/aptend/typing-transformer-obsidian)!)<br />
These rules are available for all vowels, upper and lower case.

# How to install

## Dependencies
Tested on obsidian 1.1.16 (desktop).

Please install the following community dependencies:
* [typing transformer 0.4.0](https://github.com/aptend/typing-transformer-obsidian)
* [regex pipeline 1.4.0](https://github.com/No3371/obsidian-regex-pipeline)
* [optional] a python environment (e.g. conda) with beartype and numpy

## Chinese tones, pinyin and translation HTML rendering
Copy `.obsidian/snippets/chinese_tones.css` into the same relative path in your obsidian vault.
Activate the CSS in `Settings -> Appearance -> CSS snippets -> chinese_tones`

Copy `regex-rulesets/Chinese tones.regex` and `regex-rulesets/Erase chinese tone.regex` into `.obsidian/regex_rulesets` (default) or into `./regex_rulesets` in your obsidian vault, depending on your [regex pipeline](https://github.com/No3371/obsidian-regex-pipeline) settings.

I strongly advise to bind hotkeys to `Regex Pipeline: Chinese tone.regex` and `Regex Pipeline: Erase chinese tone.regex`.

## Pinyin rules

Copy the content of pinyin_rules.txt into [typing transformer](https://github.com/aptend/typing-transformer-obsidian) rules (`Settings -> Community plugins -> Typing Transformer options -> Rules`).

If you need to edit the rules, you can also achieve the same by copying the output of `python typing_transformer_rules_generator.py` (you will need a python environment with beartype and numpy installed).<br />

# Misc
Not tested on mobile.<br />
Tested on Windows only.<br />

I work with [dvorak programmer](https://www.kaufmann.no/roland/dvorak/) keyboard layout. More common keyboards like QWERTY or AZERTY keyboard layouts might have a different diacritics typing experience.
