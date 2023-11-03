import os
import sqlite3

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from utils import (
    add_bg_from_local,
    create_schema,
    load_excel,
    set_page_config,
    translate_excel,
)


def update_database():
    _, center_col, _ = st.columns(3)

    file_path = os.path.join("static", "xlsx", "Takvim.xlsx")
    with center_col:
        with st.spinner("Data is loading"):
            calendar = load_excel(file_path=file_path)

    file_path = os.path.join("static", "xlsx", "Plan.xlsx")
    with center_col:
        with st.spinner("Veri yükleniyor"):
            plan = load_excel(
                file_path=file_path,
            )

    file_path = os.path.join("static", "xlsx", "Ekip.xlsx")
    with center_col:
        with st.spinner("Veri yükleniyor"):
            team = load_excel(
                file_path=file_path,
            )

    file_path = os.path.join("static", "xlsx", "Program.xlsx")
    with center_col:
        with st.spinner("Veri yükleniyor"):
            program = load_excel(
                file_path=file_path,
            )

    engine = create_engine("sqlite:///cs_com_db.db")

    try:
        calendar.to_sql(
            name="calendar",
            con=engine,
            index=False,
            if_exists="replace",
            dtype=create_schema(calendar),
        )
        plan.to_sql(
            name="plan",
            con=engine,
            index=False,
            if_exists="replace",
            dtype=create_schema(plan),
        )
        team.to_sql(
            name="team",
            con=engine,
            index=False,
            if_exists="replace",
            dtype=create_schema(team),
        )
        program.to_sql(
            name="program",
            con=engine,
            index=False,
            if_exists="replace",
            dtype=create_schema(program),
        )
        st.success("Database updated successfuly")
    except Exception as e:
        st.error(e)
        return


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

    with st.sidebar:
        st.selectbox(
            "Choose the operation you want to do",
            ("Database Operations", "Excel Operations"),
            key="op_type",
        )
        if st.session_state.op_type == "Database Operations":
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

    if st.session_state.op_type == "Database Operations":
        st.markdown(
            """<h1 style='text-align: center; color: black; font-size: 40px;'> Database
        Operations </h1>
        """,
            unsafe_allow_html=True,
        )
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
    elif st.session_state.op_type == "Excel Operations":
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
                    f"{uploaded_file.name} successfully exported."
                )


if __name__ == "__main__":
    main()
