from datetime import date, timedelta

import pandas as pd
import streamlit as st
from calendar_view.calendar import Calendar
from calendar_view.config import style
from calendar_view.core import data
from calendar_view.core.config import CalendarConfig
from calendar_view.core.event import Event, EventStyles
from modules.configurations import add_bg_from_local


def load_calendar_excel():
    calendar = pd.read_excel(
        "input/Etkinlik Takvimi.xlsx",
        sheet_name="Sheet1",
    )
    return calendar


def show_calendar(calendar, start_date, end_date):
    start_date = start_date - timedelta(days=start_date.weekday())

    end_date = end_date - timedelta(days=end_date.weekday())
    end_date = end_date + timedelta(days=6)

    calendar["Tarih"] = pd.to_datetime(calendar["Tarih"]).dt.date

    style.hour_height = 80
    current_date = start_date
    while current_date < end_date:
        end_of_week = current_date + timedelta(days=6)

        selected_calendar = calendar[
            (current_date <= calendar["Tarih"])
            & (calendar["Tarih"] <= end_of_week)
        ]
        if len(selected_calendar) > 0:
            config = CalendarConfig(
                lang="en",
                title="TOBB ETU Bilgisayar Topluluğı Geçmiş Etkinlik Takvimi",
                dates=f"{current_date} - {end_of_week}",
                hours="12 - 22",
                show_date=True,
                show_year=True,
                legend=False,
                title_vertical_align="center",
            )
            data.validate_config(config)

            events = []

            for i in range(len(selected_calendar)):
                row = selected_calendar.iloc[i]
                color = EventStyles.GRAY
                if row["Düzenleyen"] == "Blockchain Kulübü":
                    color = EventStyles.BLUE
                elif row["Düzenleyen"] == "Yapay Zeka Kulübü":
                    color = EventStyles.GREEN
                elif row["Düzenleyen"] == "Oyun Geliştirme Kulübü":
                    color = EventStyles.RED

                event = Event(
                    day_of_week=row["Tarih"].weekday(),
                    start=row["Başlangıç Saati"],
                    end=row["Bitiş Saati"],
                    title=row["İsim"] + f"\n({row['Düzenleyen']})",
                    style=color,
                )
                events.append(event)

            calendar_view = Calendar.build(config)
            calendar_view.add_events(events)
            calendar_view.save("takvim.png")
            st.image("takvim.png")

        current_date = current_date + timedelta(days=7)


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
    start_date = col1.date_input(
        "Tarih aralığının başlangıcını seçin:",
        min_value=date(2022, 3, 31),
        max_value=date.today() + pd.DateOffset(months=2),
    )
    end_date = col2.date_input(
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
        calendar = load_calendar_excel()
        show_calendar(calendar, start_date, end_date)


if __name__ == "__main__":
    main()
