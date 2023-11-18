import base64
import os
import re
import sys
from typing import Any, Dict, Union

import pandas as pd
import streamlit as st
import translators as ts
from sqlalchemy.types import INT, NVARCHAR, DateTime, Float

if sys.platform.startswith("win"):
    import locale

    if os.getenv("LANG") is None:
        lang, enc = locale.getdefaultlocale()
        os.environ["LANG"] = lang


@st.cache_data
def add_bg_from_local(
    background_img_path: str, sidebar_background_img_path: str
) -> str:
    with open(background_img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    with open(sidebar_background_img_path, "rb") as image_file:
        sidebar_encoded_string = base64.b64encode(image_file.read())

    return f"""<style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
        }}

        section[data-testid="stSidebar"] {{
            background-image: url(data:image/png;base64,{sidebar_encoded_string.decode()});
            background-size: cover;
        }}
    </style>"""


def set_page_config() -> None:
    st.set_page_config(
        page_title="CS Community",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/TOBB-ETU-CS-Community",
            "Report a bug": "https://tobbetu-bilgisayar-toplulugu.streamlit.app/Geri_Bildirim_Formu",
            "About": """On our community's website, you can find a wealth of information about us.
             We are always open to any feedback you may have.""",
        },
    )


def local_css(file_name: str) -> None:
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    style = """<style>
        .row-widget.stButton {text-align: center;}
        div[data-testid="column"]:nth-of-type(1)
            {
                text-align: center;
            }
            div[data-testid="column"]:nth-of-type(2)
            {
                text-align: center;
            }
            div[data-testid="column"]:nth-of-type(3)
            {
                text-align: center;
            }
    </style>"""
    st.markdown(style, unsafe_allow_html=True)


@st.cache_data
def load_excel(file_path: str) -> pd.DataFrame:
    excel = pd.read_excel(
        io=file_path,
        sheet_name="Sheet1",
    )
    excel = excel.convert_dtypes()
    excel.name = re.split(r"[/\\]", file_path)[-1].split(".")[0]
    return excel


def create_schema(df: pd.DataFrame) -> Dict[str, Any]:
    schema = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j) or "string" in str(j):
            schema.update({i: NVARCHAR(length=255)})
        if "datetime" in str(j):
            schema.update({i: DateTime()})
        if "float" in str(j):
            schema.update({i: Float(precision=3, asdecimal=True)})
        if "int" in str(j):
            schema.update({i: INT()})
    return schema


def translate_excel(
    excel_file_path: str,
    to_language: str,
    from_language: str = "auto",
    export: bool = False,
    target_sheet_name: str = "Sheet1",
) -> Union[pd.DataFrame, None]:
    try:
        df = pd.read_excel(excel_file_path)
    except FileNotFoundError:
        print("The Excel file was not found")
        return
    if df.empty:
        print("The Excel file is empty")
        return None

    df = df.applymap(
        lambda cell: ts.translate_text(
            query_text=cell,
            to_language=to_language,
            from_language=from_language,
        )
        if pd.notna(cell) and isinstance(cell, str)
        else cell
    )
    df.columns = [
        ts.translate_text(
            query_text=col,
            to_language=to_language,
            from_language=from_language,
        )
        if isinstance(col, str)
        else col
        for col in df.columns
    ]

    if not export:
        return df
    else:
        try:
            name = excel_file_path.name
        except Exception as e:
            name = excel_file_path
        index = name.find(".xlsx")
        file_name = name[:index]
        output_file_path = file_name + "_translated.xlsx"
        df.to_excel(
            output_file_path, sheet_name=target_sheet_name, index=False
        )
        return None
