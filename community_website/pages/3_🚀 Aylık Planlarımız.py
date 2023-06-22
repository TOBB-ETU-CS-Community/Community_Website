from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st
from modules.configurations import add_bg_from_local


@st.cache_data
def load_plan_excel():
    plan = pd.read_excel(
        "input/Aylık Plan.xlsx",
        sheet_name="Sheet1",
    )
    original_format = "%d.%m.%Y"
    new_format = "%Y-%m-%d"
    for i in range(len(plan)):
        date_string = plan["Başlangıç"][i]
        date_object = datetime.strptime(date_string, original_format)
        new_date_string = date_object.strftime(new_format)
        plan["Başlangıç"][i] = new_date_string
    return plan


def draw_gantt_chart(plan):
    fig = px.timeline(
        plan,
        x_start="Başlangıç",
        x_end="Bitiş",
        y="Görev",
        color="Sorumlular",
        hover_name="Detay",
    )
    fig.update_layout(plot_bgcolor="white")

    fig.update_layout(
        hoverlabel_bgcolor="#DAEEED",  # Change the hover tooltip background color to a universal light blue color. If not specified, the background color will vary by team or completion pct, depending on what view the user chooses
        bargap=0.2,
        height=700,
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(
            tickfont_size=20,
            tickangle=270,
            rangeslider_visible=True,
            side="top",  # Place the tick labels on the top of the chart
            showgrid=True,
            zeroline=True,
            showline=True,
            showticklabels=True,
            tickformat="%x\n",  # Display the tick labels in certain format. To learn more about different formats, visit: https://github.com/d3/d3-format/blob/main/README.md#locale_format
        ),
    )

    fig.update_yaxes(
        tickangle=0, tickfont=dict(family="Arial", color="black", size=15)
    )
    fig.update_xaxes(tickfont=dict(family="Arial", color="blue", size=15))
    return fig


def main():
    st.set_page_config(
        page_title="💻Bilgisayar Topluluğu",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/TOBB-ETU-CS-Community",
            "Report a bug": "https://tobbetu-bilgisayar-toplulugu.streamlit.app/Geri_Bildirim_Formu",
            "About": "Topluluğumuza ait web sayfasında bize dair pek çok bilgiye ulaşabilirsiniz. \
            Her türlü geri bildiriminize her zaman açığız.",
        },
    )
    add_bg_from_local("input/Community Logo.png", "input/Lila Gradient.png")

    st.markdown(
        "<h1 style='text-align: center; color: black; font-size: 40px;'> Aylık planlarımızı aşağıdaki \
            gantt chart üzerinden inceleyebilirsiniz </h1> \
        ",
        unsafe_allow_html=True,
    )

    plan = load_plan_excel()

    chart = draw_gantt_chart(plan)

    st.plotly_chart(chart, use_container_width=True, theme="streamlit")


if __name__ == "__main__":
    main()
