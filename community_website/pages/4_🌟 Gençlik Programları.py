import os
from datetime import date

import pandas as pd
import streamlit as st
from modules.utils import add_bg_from_local, load_excel, set_page_config
from PIL import Image


@st.cache_data
def get_open_programs(programs: pd.DataFrame, today: date):
    open_programs = pd.DataFrame(columns=programs.columns)
    for i in range(len(programs)):
        if (programs["Bitiş"][i]).date() >= today:
            open_programs.loc[len(open_programs)] = programs.iloc[i]
    return open_programs


def main():
    set_page_config()

    background_img_file = os.path.join("input", "Community Logo.png")
    sidebar_background_img_file = os.path.join("input", "Lila Gradient.png")
    add_bg_from_local(
        background_img_file=background_img_file,
        sidebar_background_img_file=sidebar_background_img_file,
    )

    st.markdown(
        """<h1 style='text-align: center; color: black; font-size: 40px;'> Üniversite öğrencilerine
         yönelik gençlik programlarını aşağıda bulabilirsiniz. </h1>
        <br>
        """,
        unsafe_allow_html=True,
    )

    desired_date_format = "%d-%m-%Y"
    date_columns = ["Bitiş"]
    programs = load_excel(
        file="input/Programlar.xlsx",
        date_columns=date_columns,
        new_format=desired_date_format,
    )

    choice = st.sidebar.radio(
        "Hangi programları görmek istersiniz?",
        (
            "Tüm Programlar",
            "Açık Programlar",
        ),
    )
    if choice == "Açık Programlar":
        programs_to_show = get_open_programs(programs, today=date.today())
    else:
        programs_to_show = programs

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
        deadline_date_format = "%d-%m-%Y"
        deadline = programs_to_show["Bitiş"][i].strftime(deadline_date_format)
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
