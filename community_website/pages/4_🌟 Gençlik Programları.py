import os
from datetime import date

import pandas as pd
import streamlit as st
from modules.utils import add_bg_from_local, set_page_config
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

    st.markdown(
        """<h1 style='text-align: center; color: black; font-size: 40px;'> You can find
        youth programs for university students below. </h1>
        <br>
        """,
        unsafe_allow_html=True,
    )

    db_file = "sqlite:///cs_com_db.db"
    programs = pd.read_sql_table("program", db_file)

    choice = st.sidebar.radio(
        "Which programs would you like to see?",
        (
            "All programs",
            "Open programs",
        ),
    )
    if choice == "Open programs":
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
                Deadline: {deadline}
                <br>
                <br>
                </div>
                """,
            unsafe_allow_html=True,
        )
        image_path = os.path.join(
            "static", "programs", f"{programs_to_show['İsim'][i]}.jpg"
        )
        image = Image.open(image_path)
        center_col.image(image)
        center_col.markdown(
            f"""
                <hr>
                """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
