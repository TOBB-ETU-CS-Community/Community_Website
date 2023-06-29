import os

import streamlit as st
from modules.utils import add_bg_from_local, set_page_config
from PIL import Image


def main():
    set_page_config()

    background_img_file = os.path.join("input", "Community Logo.png")
    sidebar_background_img_file = os.path.join("input", "Lila Gradient.png")
    add_bg_from_local(
        background_img_file=background_img_file,
        sidebar_background_img_file=sidebar_background_img_file,
    )

    st.markdown(
        "<h1 style='text-align: center; color: black; font-size: 60px;'> 🍲 Haftalık Menü </h1>",
        unsafe_allow_html=True,
    )

    main_message = '<p style="font-family:Arial; font-size: 30px;" align="center"> \
    ETU Mutfağın 2 haftalık menüsünü sürekli güncelliyoruz. Afiyet olsun 😋</p>'
    st.markdown(main_message, unsafe_allow_html=True)

    image_path = os.path.join("input", "Haftalık Menü.png")
    image = Image.open(image_path)
    st.image(image)


if __name__ == "__main__":
    main()
