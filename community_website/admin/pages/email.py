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
        """<h1 style='text-align: center; color: black; font-size: 40px;'> Send Emails </h1>
    """,
        unsafe_allow_html=True,
    )
    _, center_col, _ = st.columns([1, 3, 1])

    subject = center_col.text_input("Email subject")
    message = center_col.text_area("Email body", height=150)
    email_list = ["ataturhan21@gmail.com", "kuantum21fizik@gmail.com"]

    if center_col.button("Send"):
        try:
            send_emails(
                subject=subject, message=message, email_list=email_list
            )
            center_col.success("Operation executed successfully")
        except Exception as e:
            center_col.error(e)
            return


if __name__ == "__main__":
    main()
