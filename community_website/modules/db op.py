import os
import sqlite3

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Date, Time
from utils import add_bg_from_local, load_excel, set_page_config


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


def update_database():
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

    try:
        calendar.to_sql(
            name="calendar",
            con=engine,
            index=False,
            if_exists="replace",
            dtype=df_schema1,
        )

        plan.to_sql(
            name="plan",
            con=engine,
            index=False,
            if_exists="replace",
            dtype=df_schema2,
        )

        team.to_sql(
            name="team",
            con=engine,
            index=False,
            if_exists="replace",
            dtype=df_schema3,
        )
        st.success("Database updated successfuly")
        main()
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

    st.markdown(
        """<h1 style='text-align: center; color: black; font-size: 40px;'> Database
        Operations </h1>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("Current databases")
        show_tables_query = """
        SELECT
            name
        FROM
            sqlite_schema
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
        if st.button("Update databases"):
            update_database()

    _, center_col, _ = st.columns([1, 3, 1])
    query = center_col.text_area("SQL Query", height=100)

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
