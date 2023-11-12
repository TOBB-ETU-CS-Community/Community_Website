chcp 65001

@echo

python i18n\py3.9\pygettext.py -d base -o locales\base.pot community_website\Welcome.py community_website\pages\Feedback.py community_website\pages\Calendar.py community_website\pages\Menu.py community_website\pages\Plans.py community_website\pages\Programs.py community_website\pages\Team.py

copy locales\base.pot locales\en\LC_MESSAGES\base.po
copy locales\base.pot locales\tr\LC_MESSAGES\base.po

pause


msgmerge [option] locales\en\LC_MESSAGES\base.po locales\base.pot
