import gettext
import os
import sys

import streamlit as st
from modules.utils import add_bg_from_local, set_page_config

if sys.platform.startswith("win"):
    import locale

    if os.getenv("LANG") is None:
        lang, enc = locale.getdefaultlocale()
        os.environ["LANG"] = lang


def trial():
    for lang in ["es", "en"]:
        # set current language
        lang_translations = gettext.translation(
            "base", localedir="locales", languages=[lang]
        )
        lang_translations.install()
        # define _ shortcut for translations
        _ = lang_translations.gettext

        # mark a string translatable
        print(_("Hello World"))


def main():
    set_page_config()

    background_img_path = os.path.join(
        "static", "background", "Community Logo.png"
    )
    sidebar_background_img_path = os.path.join(
        "static", "background", "Lila Gradient.png"
    )
    page_markdown = add_bg_from_local(
        background_img_path=background_img_path,
        sidebar_background_img_path=sidebar_background_img_path,
    )
    st.markdown(page_markdown, unsafe_allow_html=True)
    trial()

    st.markdown(
        """<h1 style='text-align: center; color: black; font-size: 60px;'> Welcome to the TOBB ETU Computer Science Community
     Website 👋 </h1> \
        <br>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<p style='text-align: center;  font-size: 20px;'>
        TOBB ETU Computer Science Community was founded in April 2022 as a student community. The primary goal of this community
        is to create opportunities for students to develop themselves socially and technically. To achieve this goal, we
        organize online and face-to-face events, participate in national and international competitions, and develop
        open-source projects. We are ready to collaborate with people from all over Turkey and from all levels of
        education for our community.
        <br> <br>
        You can reach our different platform accounts at <a href='https://linktr.ee/tobbbilgisayartoplulugu'>Linktr.ee</a>
        </p> """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
