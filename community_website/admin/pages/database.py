import os
import sqlite3
import sys

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
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
        """<h1 style='text-align: center; color: black; font-size: 40px;'> Database
    Operations </h1>
    """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("Current databases")
        if st.button("Update databases"):
            update_database()
        show_tables_query = """
        SELECT
            name
        FROM
            sqlite_master
        WHERE
            type ='table' AND
            name NOT LIKE 'sqlite_%';
        """
        db_file = "cs_com_db.db"
        conn = sqlite3.connect(db_file)
        cur = conn.execute(show_tables_query)
        if cur:
            cols = [column[0] for column in cur.description]
            results_df = pd.DataFrame.from_records(
                data=cur.fetchall(), columns=cols
            )
            st.dataframe(results_df)

    _, center_col, _ = st.columns([1, 3, 1])
    query = center_col.text_area("SQL Query", height=150)

    if center_col.button("Run Query"):
        try:
            db_file = "cs_com_db.db"
            conn = sqlite3.connect(db_file)
            cur = conn.execute(query)
            if "drop" not in query.lower():
                cols = [column[0] for column in cur.description]
                results_df = pd.DataFrame.from_records(
                    data=cur.fetchall(), columns=cols
                )
                center_col.dataframe(results_df)
            center_col.success("Operation executed successfuly")
        except Exception as e:
            center_col.error(e)
            return


if __name__ == "__main__":
    main()
