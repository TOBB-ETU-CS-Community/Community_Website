import os

import streamlit as st
from modules.utils import add_bg_from_local, local_css, set_page_config


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

    css_file = os.path.join("style", "style.css")
    local_css(css_file)

    st.markdown(
        "<h1 style='text-align: center; color: black; font-size: 60px;'> 📝 Feedback Form </h1> <br>",
        unsafe_allow_html=True,
    )

    feedback_message = """<p style="font-family:Arial; font-size: 30px;" align="center">
    You can tell us your opinions about the community by filling in the text field below. Thanks!</p>
    <br>"""
    st.markdown(feedback_message, unsafe_allow_html=True)
    contact_form = """
    <form action="https://formsubmit.co/kuantum21fizik@gmail.com" method="POST" align="center">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_subject" value="CS Community Feedback!">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your feedback"></textarea>
        <button type="submit">Submit</button>
        <input type="hidden" name="_next" value="https://tobbetu-bilgisayar-toplulugu.streamlit.app">
    </form>
    """
    _, center_col, _ = st.columns([1, 3, 1])
    center_col.markdown(contact_form, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
