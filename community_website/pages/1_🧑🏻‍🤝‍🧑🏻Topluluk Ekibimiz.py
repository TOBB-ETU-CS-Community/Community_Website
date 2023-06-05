import pandas as pd
import streamlit as st
from modules.configurations import add_bg_from_local


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

    _, col2, _ = st.columns([1, 3, 1])
    col2.markdown(
        f"""
        <div style='text-align: center;  font-size: 20px;'>
        <a href='https://www.linkedin.com/in/oguzergin'>{ekip.iloc[0, 0] + ' - ' + ekip.iloc[0, 1]}<a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col2.markdown(
        """
        <br> <br>
        """,
        unsafe_allow_html=True,
    )

    _, col2, _ = st.columns([1, 3, 1])
    col2.markdown(
        f"""
        <div style='text-align: center;  font-size: 20px;'>
        <a href='https://www.linkedin.com/in/ata-turhan-555b5b160/'>{ekip.iloc[1, 0] + ' - ' + ekip.iloc[1, 1]}<a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col2.markdown(
        """
        <br> <br> <br>
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

    col4.markdown(
        f"""
        <div style='text-align: center;  font-size: 20px;'>
        {ekip.iloc[5, 0] + ' - ' + ekip.iloc[5, 1]}
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
