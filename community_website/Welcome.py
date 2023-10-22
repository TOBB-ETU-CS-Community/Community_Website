import gettext
import os

import streamlit as st
from modules.utils import add_bg_from_local, set_page_config
from st_pages import Page, show_pages


def main():
    set_page_config()

    show_pages(
        [
            Page("community_website/Welcome.py", "Welcome", "👋"),
            Page("community_website/pages/Team.py", "Team", "👥"),
            Page("community_website/pages/Calendar.py", "Event Calendar", "📅"),
            Page("community_website/pages/Plans.py", "Project Plans", "🚀"),
            Page("community_website/pages/Programs.py", "Youth Programs", "🌟"),
            Page("community_website/pages/Menu.py", "Biweekly Menu", "🍽️"),
            Page("community_website/pages/Feedback.py", "Feedback Form", "📝"),
        ]
    )

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

    lang_dict = {"English": "en", "Turkish": "tr"}
    with st.sidebar:
        lang = st.selectbox(
            "In which language would you like the website to be displayed?",
            (
                "English",
                "Turkish",
            ),
        )

    lang_translations = gettext.translation(
        "base", localedir="locales", languages=[lang_dict[lang]], fallback=True
    )
    lang_translations.install()
    _ = lang_translations.gettext

    st.markdown(
        """<h1 style='text-align: center; color: black; font-size: 60px;'>
        {headline_welcome}
        </h1> <br>""".format(
            headline_welcome=_("headline_welcome")
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        """<p style='text-align: center;  font-size: 20px;'>
        {text_welcome}
         </p> """.format(
            text_welcome=_("text_welcome")
        ),
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
