import gettext
import os

import streamlit as st
from modules.utils import add_bg_from_local
from st_pages import Page, show_pages

if "lang_set" not in st.session_state:
    st.session_state["lang_set"] = "en"

lang_box = {
    "selectbox_text": {
        "en": "In which language would you like the website to be displayed?",
        "tr": "Sayfayı hangi dilde görüntülemek istersiniz?",
    },
    "lang1": {
        "en": "English",
        "tr": "İngilizce",
    },
    "lang2": {
        "en": "Turkish",
        "tr": "Türkçe",
    },
}


def set_lang(lang):
    lang_translations = gettext.translation(
        "base",
        localedir="locales",
        languages=[lang],
        fallback=True,
    )
    lang_translations.install()
    return lang_translations.gettext


lang_dict = {
    "English": "en",
    "Turkish": "tr",
    "İngilizce": "en",
    "Türkçe": "tr",
}


def change_lang():
    st.session_state.lang_set = lang_dict[st.session_state.lang_selected]


st.sidebar.selectbox(
    lang_box["selectbox_text"][st.session_state["lang_set"]],
    (
        lang_box["lang1"][st.session_state["lang_set"]],
        lang_box["lang2"][st.session_state["lang_set"]],
    ),
    key="lang_selected",
    on_change=change_lang,
)


_ = set_lang(st.session_state.lang_set)


def main():
    # set_page_config()

    show_pages(
        [
            Page("community_website/Welcome.py", _("Welcome"), "👋"),
            Page("community_website/pages/Team.py", _("Team"), "👥"),
            Page(
                "community_website/pages/Calendar.py", _("Event Calendar"), "📅"
            ),
            Page("community_website/pages/Plans.py", _("Project Plans"), "🚀"),
            Page(
                "community_website/pages/Programs.py", _("Youth Programs"), "🌟"
            ),
            Page("community_website/pages/Menu.py", _("Biweekly Menu"), "🍽️"),
            Page(
                "community_website/pages/Feedback.py", _("Feedback Form"), "📝"
            ),
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
