import os
import sqlite3
import sys

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from modules.utils import (
    add_bg_from_local,
    create_schema,
    load_excel,
    send_emails,
    set_page_config,
    translate_excel,
)
from st_pages import Page, show_pages

show_pages(
    [
        Page(
            "community_website/admin/db op.py",
            "Admin Panel",
        ),
        Page(
            "community_website/admin/pages/database.py",
            "Database Operations",
        ),
        Page(
            "community_website/admin/pages/excel.py",
            "Excel Operations",
        ),
        Page(
            "community_website/admin/pages/email.py",
            "Email Operations",
        ),
    ]
)


def load_excel_files():
    en_files_path = os.path.join("static", "xlsx", "en")
    en_files = [f for f in os.listdir(en_files_path)]
    tr_files_path = os.path.join("static", "xlsx", "tr")
    tr_files = [f for f in os.listdir(tr_files_path)]

    en_file_path = os.path.join("static", "xlsx", "en")
    tr_file_path = os.path.join("static", "xlsx", "tr")
    files = []

    _, center_col, _ = st.columns([1, 5, 1])
    with center_col:
        with st.spinner("Data is loading"):
            for en_file in en_files:
                file_path = os.path.join(en_file_path, en_file)
                excel = load_excel(file_path=file_path)
                files.append(excel)
            for tr_file in tr_files:
                file_path = os.path.join(tr_file_path, tr_file)
                excel = load_excel(file_path=file_path)
                files.append(excel)
    return files


def upload_excel_files_to_sql(files: list):
    engine = create_engine("sqlite:///cs_com_db.db")
    try:
        for file in files:
            file.to_sql(
                name=file.name,
                con=engine,
                index=False,
                if_exists="replace",
                dtype=create_schema(file),
            )
        st.success("Database updated successfuly")
    except Exception as e:
        st.error(e)
        return


def update_database():
    files = load_excel_files()
    upload_excel_files_to_sql(files)


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
        """<h1 style='text-align: center; color: black; font-size: 40px;'> Excel
    Operations </h1>
    """,
        unsafe_allow_html=True,
    )
    _, center_col, _ = st.columns([1, 5, 1])
    uploaded_file = center_col.file_uploader(
        label="Upload the excel you want to translate",
        type=["xlx", "xlsx"],
    )
    if uploaded_file is not None:
        # df = load_excel(uploaded_file)
        _, center_col, _ = st.columns([1, 3, 1])
        col1, col2 = center_col.columns(2)
        if col1.button("Translate and Show"):
            center_col.subheader("Translated DataFrame")
            with center_col:
                with st.spinner("Translating the excel file"):
                    df = translate_excel(
                        uploaded_file,
                        to_language="en",
                        from_language="tr",
                    )
            center_col.dataframe(df)
        if col2.button("Translate and Export"):
            with center_col:
                with st.spinner("Translating the excel file"):
                    df = translate_excel(
                        uploaded_file,
                        to_language="en",
                        from_language="tr",
                        export=True,
                    )
            center_col.success(
                f"{uploaded_file.name} successfully translated and exported."
            )


if __name__ == "__main__":
    main()
