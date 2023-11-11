import gettext
import os
import sqlite3

import pandas as pd
import streamlit as st
from modules.utils import add_bg_from_local, set_page_config
from st_pages import Page, show_pages
from streamlit.components.v1 import html

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


def get_name_role(name: str, role: str, align: str = "center"):
    return f"""<div style='text-align: {align};  font-size: 20px;'>
            {name}
            <br>
            {role}
            </div>"""


def get_linkedin_badge(name: str):
    return f"""<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
                <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL"
                data-vanity="{name}" data-version="v1"><a class="badge-base__link LI-simple-link"
                href="https://tr.linkedin.com/in/{name}/en?trk=profile-badge"></a></div>"""


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

    db_file = "cs_com_db.db"
    conn = sqlite3.connect(db_file)
    table_name = "Team" + "_tr" if st.session_state["lang_set"] == "tr" else ""
    query = f"SELECT * FROM {table_name};"
    cur = conn.execute(query)
    cols = [column[0] for column in cur.description]
    team = pd.DataFrame.from_records(data=cur.fetchall(), columns=cols)

    cols = st.columns([1, 1, 1], gap="large")

    for i in range(3):
        cols[i].markdown(
            f"""
           {get_name_role(team.iloc[i, 0], team.iloc[i, 2])}
            """,
            unsafe_allow_html=True,
        )
        _, center_col, _ = cols[i].columns([1, 8, 8], gap="small")
        with center_col:
            html(
                f"""
                {get_linkedin_badge(team.iloc[i, 3])}
                """,
                height=300,
                width=350,
            )

    clubs = [
        _("Blockchain Kulübü"),
        _("Yapay Zeka Kulübü"),
        _("Oyun Geliştirme Kulübü"),
        _("Uygulama Geliştirme Kulübü"),
        _("Siber Güvenlik Kulübü"),
    ]

    for c in range(len(clubs)):
        club_team = team.query(f"{_('Grup')}=='{clubs[c]}'")

        with st.expander(clubs[c], expanded=False):
            cols = st.columns(3, gap="large")
            for i in range(len(club_team)):
                cols[i % 3].markdown(
                    f"""
                    {get_name_role(club_team.iloc[i, 0] , club_team.iloc[i, 2])}
                    """,
                    unsafe_allow_html=True,
                )
                _, center_col, _ = cols[i % 3].columns([1, 8, 8], gap="small")
                with center_col:
                    html(
                        f"""
                        {get_linkedin_badge(club_team.iloc[i, 3])}
                        """,
                        height=300,
                        width=350,
                    )


if __name__ == "__main__":
    main()
