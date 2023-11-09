import gettext
import os
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st
from modules.utils import add_bg_from_local, set_page_config
from st_pages import Page, show_pages

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


@st.cache_data
def draw_gantt_chart(plan):
    fig = px.timeline(
        plan,
        x_start="Başlangıç",
        x_end="Bitiş",
        y="Görev",
        color="Kulüpler",
        hover_name="Detay",
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="rgba(256, 256, 256, 0.3)",
    )

    fig.update_layout(
        hoverlabel_bgcolor="#DAEEED",
        bargap=0.2,
        # barmode="group",
        height=len(plan) * 100,
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(
            tickfont_size=20,
            tickangle=0,
            rangeslider_visible=True,
            side="top",
            showgrid=True,
            zeroline=True,
            showline=True,
            showticklabels=True,
            tickformat="%d %b\n",
        ),
    )
    fig.update_yaxes(
        tickangle=0, tickfont=dict(family="Arial", color="black", size=15)
    )
    fig.update_xaxes(
        tickfont=dict(family="Arial", color="black", size=15),
    )
    return fig


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
        """<h1 style='text-align: center; color: black; font-size: 40px;'>{headline_plans}</h1>
        """.format(
            headline_plans=_("headline_plans")
        ),
        unsafe_allow_html=True,
    )

    db_file = "cs_com_db.db"
    conn = sqlite3.connect(db_file)
    table_name = (
        "Plans" + "_tr" if st.session_state["lang_set"] == "tr" else ""
    )
    query = f"SELECT * FROM {table_name};"
    cur = conn.execute(query)
    cols = [column[0] for column in cur.description]
    plan = pd.DataFrame.from_records(data=cur.fetchall(), columns=cols)

    chart = draw_gantt_chart(plan)
    st.plotly_chart(chart, use_container_width=True, theme="streamlit")


if __name__ == "__main__":
    main()
