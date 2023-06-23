import pandas as pd
import streamlit as st
from modules.utils import add_bg_from_local, set_page_config
from streamlit.components.v1 import html


def get_name_role(name: str, role: str, align: str = "left"):
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

    add_bg_from_local(
        background_file="input/Community Logo.png",
        sidebar_background_file="input/Lila Gradient.png",
    )

    team = pd.read_excel(
        "input/Topluluk Ekibi.xlsx",
        sheet_name="Sheet1",
    )

    cols = st.columns([1, 1, 1], gap="small")

    for i in range(3):
        cols[i].markdown(
            f"""
           {get_name_role(team.iloc[i, 0], team.iloc[i, 2])}
            """,
            unsafe_allow_html=True,
        )

        with cols[i]:
            html(
                f"""
                {get_linkedin_badge(team.iloc[i, 3])}
                """,
                height=300,
                width=350,
            )

    st.markdown(
        f"""
           <hr>
           <br>
            """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4, gap="medium")
    clubs = [
        "Blockchain Kulübü",
        "Yapay Zeka Kulübü",
        "Oyun Geliştirme Kulübü",
        "Uygulama Geliştirme Kulübü",
    ]

    for c in range(4):
        club_team = team.query(f"Grup=='{clubs[c]}'")

        for i in range(len(club_team)):
            cols[c].markdown(
                f"""
                {get_name_role(club_team.iloc[i, 0] , club_team.iloc[i, 1], "center")}
                """,
                unsafe_allow_html=True,
            )

            with cols[c]:
                html(
                    f"""
                    {get_linkedin_badge(club_team.iloc[i, 3])}
                    """,
                    height=300,
                    width=350,
                )

    _, col2, _ = st.columns(3)

    siber_ekibi = team.query("Grup=='Siber Güvenlik Kulübü'")
    for i in range(len(siber_ekibi)):
        col2.markdown(
            f"""
            {get_name_role(siber_ekibi.iloc[i, 0] , siber_ekibi.iloc[i, 1], "center")}
            """,
            unsafe_allow_html=True,
        )

        with col2:
            html(
                f"""
                {get_linkedin_badge(siber_ekibi.iloc[i, 3])}
                """,
                height=300,
                width=350,
            )


if __name__ == "__main__":
    main()
