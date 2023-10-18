import os
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st
from modules.utils import add_bg_from_local, set_page_config


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
        """<h1 style='text-align: center; color: black; font-size: 40px;'> You can review
        our project plans via the gantt chart below. </h1>
        """,
        unsafe_allow_html=True,
    )

    db_file = "cs_com_db.db"
    conn = sqlite3.connect(db_file)
    query = "SELECT * FROM plan;"
    cur = conn.execute(query)
    cols = [column[0] for column in cur.description]
    plan = pd.DataFrame.from_records(data=cur.fetchall(), columns=cols)

    chart = draw_gantt_chart(plan)
    st.plotly_chart(chart, use_container_width=True, theme="streamlit")


if __name__ == "__main__":
    main()
