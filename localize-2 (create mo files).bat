chcp 65001

@echo

python i18n\py3.9\msgfmt.py -o locales\en\LC_MESSAGES\base.mo locales\en\LC_MESSAGES\base

python i18n\py3.9\msgfmt.py -o locales\tr\LC_MESSAGES\base.mo locales\tr\LC_MESSAGES\base

pause
