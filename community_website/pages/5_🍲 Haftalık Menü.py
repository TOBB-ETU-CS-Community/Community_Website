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
    add_bg_from_local(
        background_img_path=background_img_path,
        sidebar_background_img_path=sidebar_background_img_path,
    )

    st.markdown(
        "<h1 style='text-align: center; color: black; font-size: 60px;'> 🍲 Haftalık Menü </h1>",
        unsafe_allow_html=True,
    )

    main_message = '<p style="font-family:Arial; font-size: 30px;" align="center"> \
    ETU Mutfağın 2 haftalık menüsünü sürekli güncelliyoruz. Afiyet olsun 😋</p>'
    st.markdown(main_message, unsafe_allow_html=True)

    image_path = os.path.join("static", "Haftalık Menü.png")
    image = Image.open(image_path)
    st.image(image)


if __name__ == "__main__":
    main()
