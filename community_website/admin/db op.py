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
        """<h1 style='text-align: center; color: black; font-size: 60px;'> Admin Panel
        </h1>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
