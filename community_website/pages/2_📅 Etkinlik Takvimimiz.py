import json
import os

import streamlit as st
from modules.utils import add_bg_from_local, load_excel, set_page_config
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
        "<h1 style='text-align: center; color: black; font-size: 40px;'> Etkinlik takvimimizi aşağıdaki \
            zaman çizelgesi üzerinden inceleyebilirsiniz </h1> \
        ",
        unsafe_allow_html=True,
    )

    file_path = os.path.join("static", "xlsx", "Etkinlik Takvimi.xlsx")

    date_columns = ["Tarih"]
    _, center_col, _ = st.columns(3)
    with center_col:
        with st.spinner("Veri yükleniyor"):
            calendar = load_excel(
                file_path=file_path, date_columns=date_columns
            )

    json_object = {
        "title": {
            "text": {
                "headline": "TOBB ETU Bilgisayar Topluluğu Etkinlik Takvimi",
                "text": "<p>2022 Nisan ayındaki kuruluşumuzdan bu yana gerçekleştirdiğimiz ya da katıldığımız \
                 her etkinliğe bu zaman çizelgesi üzerinden ulaşabilirsiniz.</p>",
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
