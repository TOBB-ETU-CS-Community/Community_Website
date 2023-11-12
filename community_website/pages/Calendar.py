import gettext
import json
import os

import pandas as pd
import streamlit as st
from modules.utils import add_bg_from_local, set_page_config
from st_pages import Page, show_pages
from streamlit_timeline import timeline

if "lang_set" not in st.session_state:
    st.session_state["lang_set"] = "en"

if "lang_dict" not in st.session_state:
    st.session_state.lang_dict = {
        "English": "en",
        "Turkish": "tr",
        "İngilizce": "en",
        "Türkçe": "tr",
    }

if "inv_lang_dict" not in st.session_state:
    st.session_state.inv_lang_dict = {
        "en": "English",
        "tr": "Türkçe",
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


if "translator" not in st.session_state:
    st.session_state["translator"] = set_lang(st.session_state["lang_set"])


def change_lang():
    st.session_state.lang_set = st.session_state.lang_dict[
        st.session_state.lang_selected
    ]
    st.session_state["translator"] = set_lang(st.session_state["lang_set"])


def main():
    set_page_config()

    st.session_state.lang_selected = st.session_state.inv_lang_dict[
        st.session_state.lang_set
    ]
    _ = st.session_state["translator"]
    st.sidebar.selectbox(
        _("In which language would you like the website to be displayed?"),
        (
            _("English"),
            _("Turkish"),
        ),
        key="lang_selected",
        on_change=change_lang,
    )
    _ = st.session_state["translator"]

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
        """<h1 style='text-align: center; color: black; font-size: 40px;'>{headline_calendar}</h1>
        """.format(
            headline_calendar=_("headline_calendar")
        ),
        unsafe_allow_html=True,
    )

    db_file = "sqlite:///cs_com_db.db"
    table_name = "Events"
    table_name += "_tr" if st.session_state["lang_set"] == "tr" else ""
    calendar = pd.read_sql_table(table_name, db_file)

    json_object = {
        "title": {
            "text": {
                "headline": _("Event Calendar"),
                "text": """<p>{text_calendar}</p>""".format(
                    text_calendar=_("text_calendar")
                ),
            },
        },
        "events": [],
    }
    items = []
    group = _("Group")

    for i in range(len(calendar)):
        item = {}
        start = calendar[_("Beginning")][i]
        end = calendar[_("End")][i]
        item["start_date"] = {
            "year": f"{start.year}",
            "month": f"{start.month}",
            "day": f"{start.day}",
            "hour": f"{start.hour}",
            "minute": f"{start.minute}",
        }
        item["end_date"] = {
            "year": f"{end.year}",
            "month": f"{end.month}",
            "day": f"{end.day}",
            "hour": f"{end.hour}",
            "minute": f"{end.minute}",
        }
        item["text"] = {
            "headline": calendar[_("Name")][i],
            "text": f"<p> {calendar[group][i]} </p>",
        }

        items.append(item)

    json_object["events"] = items
    json_string = json.dumps(json_object)
    timeline(json_string, height=450)


if __name__ == "__main__":
    main()
