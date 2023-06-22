from datetime import datetime

import pandas as pd
import streamlit as st
from modules.configurations import add_bg_from_local
from PIL import Image


@st.cache_data
def load_program_excel():
    programlar = pd.read_excel(
        "input/Programlar.xlsx",
        sheet_name="Sheet1",
    )
    original_format = "%d.%m.%Y"
    new_format = "%d-%m-%Y"
    for i in range(len(programlar)):
        date_string = programlar["Bitiş"][i]
        date_object = datetime.strptime(date_string, original_format)
        new_date_string = date_object.strftime(new_format)
        programlar["Bitiş"][i] = pd.to_datetime(
            new_date_string,
            format=new_format,
        )
    return programlar


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
    add_bg_from_local("input/Community Logo.png", "input/Lila Gradient.png")

    st.markdown(
        """<h1 style='text-align: center; color: black; font-size: 40px;'> Başvuruları açık olan,
        üniversite öğrencilerine yönelik gençlik programlarını aşağıda bulabilirsiniz. </h1>
        <br>
        """,
        unsafe_allow_html=True,
    )

    programs = load_program_excel()
    programs.sort_values(by="Bitiş", inplace=True)
    programs.reset_index(drop=True, inplace=True)

    choice = st.sidebar.radio(
        "Hangi programları görmek istersiniz?",
        ("Açık Programlar", "Tüm Programlar"),
    )
    if choice == "Açık Programlar":
        programs_to_show = programs.loc[programs["Bitiş"] >= datetime.now()]
        programs_to_show.reset_index(drop=True, inplace=True)
    else:
        programs_to_show = programs

    # st.write(programs)
    # st.write(programs_to_show)

    for i in range(len(programs_to_show)):
        _, center_col, _ = st.columns([1, 5, 1])
        center_col.markdown(
            f"""
                <div style='text-align: center;  font-size: 40px;'>
                <a href={programs_to_show['Link'][i]}>
                {programs_to_show["İsim"][i]}
                <br>
                </a>
                </div>
                """,
            unsafe_allow_html=True,
        )
        format_to_show = "%d-%m-%Y"
        deadline = programs_to_show["Bitiş"][i].strftime(format_to_show)
        center_col.markdown(
            f"""
                <div style='text-align: center;  font-size: 30px;'>
                Son Başvuru Tarihi: {deadline}
                <br>
                <br>
                </div>
                """,
            unsafe_allow_html=True,
        )
        image = Image.open(
            f"input/program_images/{programs_to_show['İsim'][i]}.jpg"
        )
        center_col.image(image)
        center_col.markdown(
            f"""
                <hr>
                """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
