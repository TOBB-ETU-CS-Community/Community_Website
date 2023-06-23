import plotly.express as px
import streamlit as st
from modules.utils import add_bg_from_local, load_excel, set_page_config


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
    set_page_config()

    add_bg_from_local(
        background_file="input/Community Logo.png",
        sidebar_background_file="input/Lila Gradient.png",
    )

    st.markdown(
        "<h1 style='text-align: center; color: black; font-size: 40px;'> Aylık planlarımızı aşağıdaki \
            gantt chart üzerinden inceleyebilirsiniz </h1> \
        ",
        unsafe_allow_html=True,
    )

    plan = load_excel(
        file="input/Aylık Plan.xlsx",
        date_column="Başlangıç",
        new_format="%Y-%m-%d",
    )

    chart = draw_gantt_chart(plan)

    st.plotly_chart(chart, use_container_width=True, theme="streamlit")


if __name__ == "__main__":
    main()
