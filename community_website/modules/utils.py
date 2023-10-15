import base64

import pandas as pd
import streamlit as st
from sqlalchemy.types import INT, NVARCHAR, DateTime, Float


@st.cache_data
def add_bg_from_local(background_img_path, sidebar_background_img_path):
    with open(background_img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    with open(sidebar_background_img_path, "rb") as image_file:
        sidebar_encoded_string = base64.b64encode(image_file.read())

    return f"""<style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: 1500px 700px;
        }}

        section[data-testid="stSidebar"] {{
            background-image: url(data:image/png;base64,{sidebar_encoded_string.decode()});
            background-size: 400px 800px;
        }}
    </style>"""


def set_page_config():
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


def local_css(file_name):
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
def load_excel(
    file_path: str,
):
    excel = pd.read_excel(
        io=file_path,
        sheet_name="Sheet1",
    )
    excel = excel.convert_dtypes()
    return excel


def create_schema(df):
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
