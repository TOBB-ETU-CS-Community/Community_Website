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
            "Report a bug": "https://tobbetu-bilgisayar-toplulugu.streamlit.app/Geri Bildirim Formu",
            "About": "Topluluğumuza ait web sayfasında bize dair pek çok bilgiye ulaşabilirsiniz. \
                Her türlü geri bildiriminize her zaman açığız.",
        },
    )

    add_bg_from_local("input/background.png")

    ekip = pd.read_excel(
        "input/Topluluk Ekibi.xlsx",
        sheet_name="Sheet1",
    )

    _, col2, _ = st.columns([2, 3, 1])
    col2.markdown(
        f"""
        <div style='text-align: left;  font-size: 20px;'>
        {ekip.iloc[0, 0] + ' - ' + ekip.iloc[0, 1]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    with col2:
        html(
            f"""
            <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
            <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL"
            data-vanity="oguzergin" data-version="v1"><a class="badge-base__link LI-simple-link"
            href="https://tr.linkedin.com/in/oguzergin/en?trk=profile-badge"></a></div>
            """,
            height=300,
            width=350,
        )

    _, col2, _ = st.columns([2, 3, 1])
    col2.markdown(
        f"""
        <div style='text-align: left;  font-size: 20px;'>
        {ekip.iloc[1, 0] + ' - ' + ekip.iloc[1, 1]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    with col2:
        html(
            f"""
            <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
            <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL"
            data-vanity="ata-turhan" data-version="v1"><a class="badge-base__link LI-simple-link"
            href="https://tr.linkedin.com/in/ata-turhan/en?trk=profile-badge"></a></div>
            """,
            height=300,
            width=350,
        )

    col2.markdown(
        """
        <br>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    col1.markdown(
        f"""
        <div style='text-align: center;  font-size: 20px;'>
        {ekip.iloc[2, 0] + ' - ' + ekip.iloc[2, 1]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    with col1:
        html(
            f"""
            <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
            <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL"
            data-vanity="mustafa-beyazıt-nural-37278325b" data-version="v1"><a class="badge-base__link LI-simple-link"
            href="https://tr.linkedin.com/in/mustafa-beyazıt-nural-37278325b/en?trk=profile-badge"></a></div>
            """,
            height=300,
            width=350,
        )

    col2.markdown(
        f"""
        <div style='text-align: center;  font-size: 20px;'>
        {ekip.iloc[3, 0] + ' - ' + ekip.iloc[3, 1]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    col3.markdown(
        f"""
        <div style='text-align: center;  font-size: 20px;'>
        {ekip.iloc[4, 0] + ' - ' + ekip.iloc[4, 1]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    with col3:
        html(
            f"""
            <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
            <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL"
            data-vanity="utku-murat-atasoy-55a458219" data-version="v1"><a class="badge-base__link LI-simple-link"
            href="https://tr.linkedin.com/in/utku-murat-atasoy-55a458219/en?trk=profile-badge"></a></div>
            """,
            height=300,
            width=350,
        )

    col4.markdown(
        f"""
        <div style='text-align: center;  font-size: 20px;'>
        {ekip.iloc[5, 0] + ' - ' + ekip.iloc[5, 1]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    with col4:
        html(
            f"""
            <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
            <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL"
            data-vanity="akif-emre-reis" data-version="v1"><a class="badge-base__link LI-simple-link"
            href="https://tr.linkedin.com/in/akif-emre-reis/en?trk=profile-badge"></a></div>
            """,
            height=300,
            width=350,
        )


if __name__ == "__main__":
    main()
