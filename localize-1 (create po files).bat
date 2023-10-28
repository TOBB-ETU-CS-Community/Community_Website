chcp 65001

@echo

python i18n\py3.9\pygettext.py -d base -o locales\base.pot community_website\Welcome.py community_website\pages\Feedback.py

copy locales\base.pot locales\en\LC_MESSAGES\base.po
copy locales\base.pot locales\tr\LC_MESSAGES\base.po

pause
