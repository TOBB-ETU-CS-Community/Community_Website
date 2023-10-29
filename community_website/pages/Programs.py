import gettext
import os
from datetime import date

import pandas as pd
import streamlit as st
from modules.utils import add_bg_from_local, set_page_config
from PIL import Image
from st_pages import Page, show_pages


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


@st.cache_data
def get_open_programs(programs: pd.DataFrame, today: date):
    open_programs = pd.DataFrame(columns=programs.columns)
    for i in range(len(programs)):
        if (programs["Bitiş"][i]).date() >= today:
            open_programs.loc[len(open_programs)] = programs.iloc[i]
    return open_programs


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
        """<h1 style='text-align: center; color: black; font-size: 40px;'>{headline_programs}</h1>
        <br>
        """.format(
            headline_programs=_("headline_programs")
        ),
        unsafe_allow_html=True,
    )

    db_file = "sqlite:///cs_com_db.db"
    programs = pd.read_sql_table("program", db_file)

    choice = st.sidebar.radio(
        _("Which programs would you like to see?"),
        (
            _("All programs"),
            _("Open programs"),
        ),
    )
    if choice == _("Open programs"):
        programs_to_show = get_open_programs(programs, today=date.today())
    else:
        programs_to_show = programs

    for i in range(len(programs_to_show)):
        _, center_col, _ = st.columns([1, 5, 1])
        center_col.markdown(
            f"""
                <div style='text-align: center;  font-size: 40px;'>
                <a href={programs_to_show['Link'][i]}>
                {programs_to_show["İsim"][i]}
                <br>
                </a>
                </div>
                """,
            unsafe_allow_html=True,
        )
        deadline_date_format = "%d-%m-%Y"
        deadline = programs_to_show["Bitiş"][i].strftime(deadline_date_format)
        center_col.markdown(
            f"""
                <div style='text-align: center;  font-size: 30px;'>
                Deadline: {deadline}
                <br>
                <br>
                </div>
                """,
            unsafe_allow_html=True,
        )
        image_path = os.path.join(
            "static", "programs", f"{programs_to_show['İsim'][i]}.jpg"
        )
        image = Image.open(image_path)
        center_col.image(image)
        center_col.markdown(
            "<hr>",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
