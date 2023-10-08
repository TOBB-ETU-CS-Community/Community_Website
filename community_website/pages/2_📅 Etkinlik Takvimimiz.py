import json
import os
import sqlite3

import pandas as pd
import streamlit as st
from modules.utils import add_bg_from_local, set_page_config
from streamlit_timeline import timeline


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
        our event calendar on the timeline below. </h1>
        """,
        unsafe_allow_html=True,
    )

    os.path.join("static", "xlsx", "Etkinlik Takvimi.xlsx")
    """
    date_columns = ["Tarih"]
    _, center_col, _ = st.columns(3)
    with center_col:
        with st.spinner("Data is loading"):
            calendar = load_excel(
                file_path=file_path, date_columns=date_columns
            )
    """

    db_file = "cs_com_db.db"
    conn = sqlite3.connect(db_file)
    query = "SELECT * FROM activity;"
    query = conn.execute(query)
    cols = [column[0] for column in query.description]
    calendar = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    st.write(calendar.dtypes)
    st.write(calendar)
    calendar["Tarih"] = pd.to_datetime(calendar["Tarih"])
    calendar["Başlangıç Saati"] = pd.to_datetime(
        calendar["Başlangıç Saati"].str[:5], format="%H:%M"
    )
    st.write(calendar.dtypes)

    json_object = {
        "title": {
            "text": {
                "headline": "Event Calendar",
                "text": """<p>You can access every event we have held or attended since
                our establishment in April 2022 through this timeline.</p>""",
            },
        },
        "events": [],
    }
    items = []

    for i in range(len(calendar)):
        item = {}
        date = calendar["Tarih"][i]
        hour = calendar["Başlangıç Saati"][i]
        item["start_date"] = {
            "year": f"{date.year}",
            "month": f"{date.month}",
            "day": f"{date.day}",
            "hour": f"{hour.hour}",
            "minute": f"{hour.minute}",
        }
        item["text"] = {
            "headline": calendar["İsim"][i],
            "text": f"<p> {calendar['Düzenleyen'][i]} </p>",
        }

        items.append(item)

    json_object["events"] = items
    json_string = json.dumps(json_object)
    timeline(json_string, height=450)


if __name__ == "__main__":
    main()
