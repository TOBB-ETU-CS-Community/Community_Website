chcp 65001

@echo
poetry shell

python C:\Users\NEO\AppData\Local\Programs\Python\Python39\Tools\i18n\pygettext.py -d base -o locales\base.pot community_website\👋Hoşgeldiniz.py

copy locales\base.pot locales\en\LC_MESSAGES\base.po
copy locales\base.pot locales\tr\LC_MESSAGES\base.po

Exit
