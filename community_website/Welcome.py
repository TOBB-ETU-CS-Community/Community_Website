import json
import os

import streamlit as st
from modules.utils import add_bg_from_local, set_page_config
from st_pages import Page, show_pages


def main():
    set_page_config()

    show_pages(
        [
            Page("community_website/Welcome.py", "Welcome", "👋"),
            Page("community_website/pages/Team.py", "Team", "👥"),
            Page("community_website/pages/Calendar.py", "Event Calendar", "📅"),
            Page("community_website/pages/Plans.py", "Project Plans", "🚀"),
            Page("community_website/pages/Programs.py", "Youth Programs", "🌟"),
            Page("community_website/pages/Menu.py", "Biweekly Menu", "🍽️"),
            Page("community_website/pages/Feedback.py", "Feedback Form", "📝"),
        ]
    )

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

    msgs = {
        "headline_welcome": {
            "en": "Welcome to the TOBB ETU Computer Science Community Website 👋",
            "tr": "TOBB ETU Bilgisayar Topluluğu Web Sayfasına Hoşgeldiniz 👋",
        },
    }

    with open("translations.json", "w") as json_file:
        json.dump(msgs, json_file)

    with open("translations.json", "r") as json_file:
        msgs = json.load(json_file)

    lang_dict = {"English": "en", "Turkish": "tr"}
    with st.sidebar:
        lang = st.selectbox(
            "In which language would you like the website to be displayed?",
            (
                "English",
                "Turkish",
            ),
        )

    st.markdown(
        f"""<h1 style='text-align: center; color: black; font-size: 60px;'>
        {msgs["headline_welcome"][lang_dict[lang]]}
        </h1> <br>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""<p style='text-align: center;  font-size: 20px;'>
        TOBB ETU Computer Science Community was founded in April 2022 as a student community. The primary goal of this community
        is to create opportunities for students to develop themselves socially and technically. To achieve this goal, we
        organize online and face-to-face events, participate in national and international competitions, and develop
        open-source projects. We are ready to collaborate with people from all over Turkey and from all levels of
        education for our community.
        <br> <br>
        You can reach our different platform accounts at <a href='https://linktr.ee/tobbbilgisayartoplulugu'>Linktr.ee</a>
         </p> """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
