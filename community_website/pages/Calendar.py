import json
import os

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

    db_file = "sqlite:///cs_com_db.db"
    calendar = pd.read_sql_table("calendar", db_file)

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
        start = calendar["Başlangıç"][i]
        end = calendar["Bitiş"][i]
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
            "headline": calendar["İsim"][i],
            "text": f"<p> {calendar['Düzenleyen'][i]} </p>",
        }

        items.append(item)

    json_object["events"] = items
    json_string = json.dumps(json_object)
    timeline(json_string, height=450)


if __name__ == "__main__":
    main()
