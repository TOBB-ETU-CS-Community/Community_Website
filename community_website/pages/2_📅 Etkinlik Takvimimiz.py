import os

import streamlit as st
from modules.utils import add_bg_from_local, load_excel, set_page_config
from streamlit_timeline import st_timeline


def main():
    set_page_config()

    background_img_file = os.path.join("input", "Community Logo.png")
    sidebar_background_img_file = os.path.join("input", "Lila Gradient.png")
    add_bg_from_local(
        background_img_file=background_img_file,
        sidebar_background_img_file=sidebar_background_img_file,
    )

    st.markdown(
        "<h1 style='text-align: center; color: black; font-size: 40px;'> Etkinlik takvimimizi aşağıdaki \
            zaman çizelgesi üzerinden inceleyebilirsiniz </h1> \
        ",
        unsafe_allow_html=True,
    )

    file_path = os.path.join("input", "Etkinlik Takvimi.xlsx")
    desired_date_format = "%Y-%m-%d"
    date_columns = ["Tarih"]
    calendar = load_excel(file_path=file_path, date_columns=date_columns)

    items = []

    for i in range(len(calendar)):
        item = {
            "id": i,
            "content": calendar["İsim"][i],
            # "start": new_date_string
            "start": calendar["Tarih"][i].strftime(desired_date_format)
            + " "
            + str(calendar["Başlangıç Saati"][i])
            + ":00",
            "title": calendar["Düzenleyen"][i],
        }
        items.append(item)

    timeline = st_timeline(items, groups=[], options={}, height="600px")


if __name__ == "__main__":
    main()
