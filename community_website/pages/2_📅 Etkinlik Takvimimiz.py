import os

import streamlit as st
from modules.utils import add_bg_from_local, load_excel, set_page_config
from streamlit_timeline import st_timeline


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
    desired_date_format = "%Y-%m-%d"
    date_columns = ["Tarih"]
    _, center_col, _ = st.columns(3)
    with center_col:
        with st.spinner("Veri yükleniyor"):
            calendar = load_excel(
                file_path=file_path, date_columns=date_columns
            )

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
