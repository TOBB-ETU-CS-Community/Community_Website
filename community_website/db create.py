import os
import sqlite3

import pandas as pd
import streamlit as st
from modules.utils import load_excel
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Date, Time


def sqlcol(dfparam):
    dtypedict = {}
    for i, j in zip(dfparam.columns, dfparam.dtypes):
        if "object" in str(j):
            dtypedict.update({i: sqlalchemy.types.NVARCHAR(length=255)})

        if "datetime" in str(j):
            dtypedict.update({i: sqlalchemy.types.DateTime()})

        if "float" in str(j):
            dtypedict.update(
                {i: sqlalchemy.types.Float(precision=3, asdecimal=True)}
            )

        if "int" in str(j):
            dtypedict.update({i: sqlalchemy.types.INT()})

    return dtypedict


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        st.write(e)

    return conn


def create_database():
    st.markdown("# Create Database")

    st.write(
        """A database in SQLite is just a file on same server.
    By convention their names always end in .db"""
    )

    db_filename = st.text_input("DB Filename")
    create_db = st.button("Create Database")

    if create_db:
        if db_filename.endswith(".db"):
            conn = create_connection(db_filename)
            st.write(conn)  # success message?
            st.balloons()
            st.success("DB created successfully!")
        else:
            st.write("DB filename must end with .db, please retry.")


def upload_data():
    st.markdown("# Upload Data")
    # https://discuss.streamlit.io/t/uploading-csv-and-excel-files/10866/2
    sqlite_dbs = [file for file in os.listdir(".") if file.endswith(".db")]
    db_filename = st.selectbox("DB Filename", sqlite_dbs)

    create_connection(db_filename)
    file_path = os.path.join("static", "xlsx", "Etkinlik Takvimi.xlsx")
    date_columns = ["Tarih"]
    _, center_col, _ = st.columns(3)
    with center_col:
        with st.spinner("Data is loading"):
            calendar = load_excel(
                file_path=file_path, date_columns=date_columns
            )

    # calendar["Tarih"] = pd.to_datetime(calendar["Tarih"])
    # calendar["Başlangıç Saati"] = calendar["Başlangıç Saati"].apply(pd.Timestamp)
    # calendar["Bitiş Saati"] = pd.to_datetime(calendar["Bitiş Saati"])

    df_schema1 = {
        "İsim": NVARCHAR(80),
        "Tarih": Date(),
        "Başlangıç Saati": Time(),
        "Bitiş Saati": Time(),
        "Düzenleyen": NVARCHAR(80),
    }

    file_path = os.path.join("static", "xlsx", "Aylık Plan.xlsx")
    desired_date_format = "%d-%m-%Y"
    date_columns = ["Başlangıç", "Bitiş"]
    _, center_col, _ = st.columns(3)
    with center_col:
        with st.spinner("Veri yükleniyor"):
            plan = load_excel(
                file_path=file_path,
                date_columns=date_columns,
                new_format=desired_date_format,
            )

    df_schema2 = {
        "Görev": NVARCHAR(80),
        "Başlangıç": Date(),
        "Bitiş": Date(),
        "Kulüpler": NVARCHAR(80),
        "Detay": NVARCHAR(80),
    }

    file_path = os.path.join("static", "xlsx", "Topluluk Ekibi.xlsx")
    _, center_col, _ = st.columns(3)
    with center_col:
        with st.spinner("Veri yükleniyor"):
            team = load_excel(
                file_path=file_path,
            )

    df_schema3 = {
        "İsim": NVARCHAR(80),
        "Grup": NVARCHAR(80),
        "Rol": NVARCHAR(80),
        "Linkedin": NVARCHAR(80),
    }

    engine = create_engine("sqlite:///cs_com_db.db")

    if st.button("Upload dataframe as a table to db"):
        try:
            calendar.to_sql(
                name="event_calendar",
                con=engine,
                index=False,
                if_exists="replace",
                dtype=df_schema1,
            )
            st.write("Data uploaded successfully. These are the first 5 rows.")
            st.dataframe(calendar.head(5))

            plan.to_sql(
                name="plan",
                con=engine,
                index=False,
                if_exists="replace",
                dtype=df_schema2,
            )
            st.write("Data uploaded successfully. These are the first 5 rows.")
            st.dataframe(plan.head(5))

            team.to_sql(
                name="team",
                con=engine,
                index=False,
                if_exists="replace",
                dtype=df_schema3,
            )
            st.write("Data uploaded successfully. These are the first 5 rows.")
            st.dataframe(team.head(5))
        except Exception as e:
            st.write(e)


def run_query():
    st.markdown("# Run Query")
    sqlite_dbs = [file for file in os.listdir(".") if file.endswith(".db")]
    db_filename = st.selectbox("DB Filename", sqlite_dbs)

    query = st.text_area("SQL Query", height=100)
    conn = create_connection(db_filename)

    submitted = st.button("Run Query")

    if submitted:
        try:
            query = conn.execute(query)
            cols = [column[0] for column in query.description]
            results_df = pd.DataFrame.from_records(
                data=query.fetchall(), columns=cols
            )
            st.dataframe(results_df)
        except Exception as e:
            st.write(e)

    st.sidebar.markdown("# Run Query")


page_names_to_funcs = {
    "Create Database": create_database,
    "Upload Data": upload_data,
    "Run Query": run_query,
}

selected_page = st.sidebar.selectbox(
    "Select a page", page_names_to_funcs.keys()
)
page_names_to_funcs[selected_page]()
