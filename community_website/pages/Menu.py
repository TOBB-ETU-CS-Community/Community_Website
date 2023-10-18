import os

import streamlit as st
from modules.utils import add_bg_from_local, set_page_config
from PIL import Image


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
        "<h1 style='text-align: center; color: black; font-size: 60px;'> 🍽️ Weekly Menu </h1>",
        unsafe_allow_html=True,
    )

    main_message = '<p style="font-family:Arial; font-size: 30px;" align="center"> \
    We are constantly updating the 2-week menu of ETU Kitchen. Bon Appétit 😋</p>'
    st.markdown(main_message, unsafe_allow_html=True)

    image_path = os.path.join("static", "Haftalık Menü.png")
    image = Image.open(image_path)
    st.image(image)


if __name__ == "__main__":
    main()
