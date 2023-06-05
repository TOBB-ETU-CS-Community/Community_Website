from datetime import date

import pandas as pd
import streamlit as st
from calendar_view.calendar import Calendar
from calendar_view.core import data
from calendar_view.core.config import CalendarConfig
from calendar_view.core.event import Event, EventStyles
from modules.configurations import add_bg_from_local


def show_calendar():
    config = CalendarConfig(
        lang="en",
        title="TOBB ETU Bilgisayar Topluluğı Geçmiş Etkinlik Takvimi",
        dates="Mo - Su",
        hours="12 - 22",
        show_date=False,
        legend=False,
    )
    data.validate_config(config)

    events = [
        Event(
            day_of_week=1,
            start="18:00",
            end="19:15",
            title="HOT Core Yoga, 75 mins, with David",
            style=EventStyles.RED,
        ),
        Event(
            day_of_week=2,
            start="19:00",
            end="20:15",
            title="Hatha Yoga, 75 mins, with Jo",
            style=EventStyles.GREEN,
        ),
        Event(
            day_of_week=3,
            start="19:00",
            end="21:00",
            title="Pilates, 60 mins, with Erika",
            style=EventStyles.BLUE,
        ),
        Event(
            day_of_week=4,
            start="18:30",
            end="20:00",
            title="Kundalini Yoga, 90 mins, with Dan",
            style=EventStyles.RED,
        ),
        Event(
            day_of_week=6,
            start="14:00",
            end="15:15",
            title="Hatha Yoga, 75 mins, with Vick",
            style=EventStyles.GREEN,
        ),
    ]

    calendar = Calendar.build(config)
    calendar.add_events(events)
    calendar.save("takvim.png")
    st.image("takvim.png")


def main():
    st.set_page_config(
        page_title="💻Bilgisayar Topluluğu",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/TOBB-ETU-CS-Community",
            "Report a bug": "https://tobbetu-bilgisayar-toplulugu.streamlit.app/Geri Bildirim Formu",
            "About": "Topluluğumuza ait web sayfasında bize dair pek çok bilgiye ulaşabilirsiniz. \
            Her türlü geri bildiriminize her zaman açığız.",
        },
    )
    add_bg_from_local("input/background.png")

    st.markdown(
        "<h1 style='text-align: center; color: black; font-size: 40px;'> Etkinlik takvimimize aşağıdaki \
             araç yardımıyla tarih aralığını seçerek ulaşabilirsiniz </h1> \
        <br> <br>",
        unsafe_allow_html=True,
    )
    _, col1, col2, _ = st.columns([1, 2, 2, 1])
    col1.date_input(
        "Tarih aralığının başlangıcını seçin:",
        min_value=date(2022, 3, 31),
        max_value=date.today() + pd.DateOffset(months=2),
    )
    col2.date_input(
        "Tarih aralığının sonunu seçin:",
        min_value=date(2022, 3, 31),
        max_value=date.today() + pd.DateOffset(months=2),
    )

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    _, center_col, _ = st.columns([3, 3, 1])

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    if center_col.button("Takvimi Getir"):
        show_calendar()


if __name__ == "__main__":
    main()
