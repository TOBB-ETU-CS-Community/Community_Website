import os

import streamlit as st
from modules.utils import add_bg_from_local, load_excel, set_page_config
from streamlit.components.v1 import html


def get_name_role(name: str, role: str, align: str = "center"):
    return f"""<div style='text-align: {align};  font-size: 20px;'>
            {name}
            <br>
            {role}
            </div>"""


def get_linkedin_badge(name: str):
    return f"""<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
                <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL"
                data-vanity="{name}" data-version="v1"><a class="badge-base__link LI-simple-link"
                href="https://tr.linkedin.com/in/{name}/en?trk=profile-badge"></a></div>"""


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

    file_path = os.path.join("static", "xlsx", "Topluluk Ekibi.xlsx")
    _, center_col, _ = st.columns(3)
    with center_col:
        with st.spinner("Veri yükleniyor"):
            team = load_excel(
                file_path=file_path,
            )

    cols = st.columns([1, 1, 1], gap="large")

    for i in range(3):
        cols[i].markdown(
            f"""
           {get_name_role(team.iloc[i, 0], team.iloc[i, 2])}
            """,
            unsafe_allow_html=True,
        )
        _, center_col, _ = cols[i].columns([1, 8, 8], gap="small")
        with center_col:
            html(
                f"""
                {get_linkedin_badge(team.iloc[i, 3])}
                """,
                height=300,
                width=350,
            )

    clubs = [
        "Blockchain Kulübü",
        "Yapay Zeka Kulübü",
        "Oyun Geliştirme Kulübü",
        "Uygulama Geliştirme Kulübü",
        "Siber Güvenlik Kulübü",
    ]

    for c in range(len(clubs)):
        club_team = team.query(f"Grup=='{clubs[c]}'")

        with st.expander(clubs[c], expanded=False):
            cols = st.columns(3, gap="large")
            for i in range(len(club_team)):
                cols[i % 3].markdown(
                    f"""
                    {get_name_role(club_team.iloc[i, 0] , club_team.iloc[i, 2])}
                    """,
                    unsafe_allow_html=True,
                )
                _, center_col, _ = cols[i % 3].columns([1, 8, 8], gap="small")
                with center_col:
                    html(
                        f"""
                        {get_linkedin_badge(club_team.iloc[i, 3])}
                        """,
                        height=300,
                        width=350,
                    )


if __name__ == "__main__":
    main()
