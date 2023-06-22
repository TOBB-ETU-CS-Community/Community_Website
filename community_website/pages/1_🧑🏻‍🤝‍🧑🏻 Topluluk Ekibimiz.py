import pandas as pd
import streamlit as st
from modules.configurations import add_bg_from_local
from streamlit.components.v1 import html


def main():
    st.set_page_config(
        page_title="💻Bilgisayar Topluluğu",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/TOBB-ETU-CS-Community",
            "Report a bug": "https://tobbetu-bilgisayar-toplulugu.streamlit.app/Geri_Bildirim_Formu",
            "About": "Topluluğumuza ait web sayfasında bize dair pek çok bilgiye ulaşabilirsiniz. \
                Her türlü geri bildiriminize her zaman açığız.",
        },
    )

    add_bg_from_local("input/Community Logo.png", "input/Lila Gradient.png")

    ekip = pd.read_excel(
        "input/Topluluk Ekibi.xlsx",
        sheet_name="Sheet1",
    )

    cols = st.columns([1, 1, 1], gap="small")

    for i in range(3):
        cols[i].markdown(
            f"""
            <div style='text-align: left;  font-size: 20px;'>
            {ekip.iloc[i, 0] + ' <br> ' + ekip.iloc[i, 2]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        with cols[i]:
            html(
                f"""
                <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
                <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL"
                data-vanity="{ekip.iloc[i, 3]}" data-version="v1"><a class="badge-base__link LI-simple-link"
                href="https://tr.linkedin.com/in/{ekip.iloc[i, 3]}/en?trk=profile-badge"></a></div>
                """,
                height=300,
                width=350,
            )

    st.markdown(
        """
        <hr>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4, gap="small")
    clubs = [
        "Blockchain Kulübü",
        "Yapay Zeka Kulübü",
        "Oyun Geliştirme Kulübü",
        "Uygulama Geliştirme Kulübü",
    ]

    for c in range(4):
        club_team = ekip.query(f"Grup=='{clubs[c]}'")

        for i in range(len(club_team)):
            cols[c].markdown(
                f"""
                <div style='text-align: center;  font-size: 20px;'>
                {club_team.iloc[i, 0] + ' <br> ' + club_team.iloc[i, 1]}
                </div>
                """,
                unsafe_allow_html=True,
            )

            with cols[c]:
                html(
                    f"""
                    <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
                    <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL"
                    data-vanity="{club_team.iloc[i, 3]}" data-version="v1"><a class="badge-base__link LI-simple-link"
                    href="https://tr.linkedin.com/in/{club_team.iloc[i, 3]}/en?trk=profile-badge"></a></div>
                    """,
                    height=300,
                    width=350,
                )

    _, col2, _ = st.columns(3)

    siber_ekibi = ekip.query("Grup=='Siber Güvenlik Kulübü'")
    for i in range(len(siber_ekibi)):
        col2.markdown(
            f"""
            <div style='text-align: left;  font-size: 20px;'>
            {siber_ekibi.iloc[i, 0] + ' <br> ' + siber_ekibi.iloc[i, 1]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        with col2:
            html(
                f"""
                <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
                <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL"
                data-vanity="{siber_ekibi.iloc[i, 3]}" data-version="v1"><a class="badge-base__link LI-simple-link"
                href="https://tr.linkedin.com/in/{siber_ekibi.iloc[i, 3]}/en?trk=profile-badge"></a></div>
                """,
                height=300,
                width=350,
            )


if __name__ == "__main__":
    main()
