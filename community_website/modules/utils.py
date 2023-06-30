import base64
from datetime import datetime

import pandas as pd
import streamlit as st


def add_bg_from_local(background_img_path, sidebar_background_img_path):
    with open(background_img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    with open(sidebar_background_img_path, "rb") as image_file:
        sidebar_encoded_string = base64.b64encode(image_file.read())

    page = f"""<style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: 1500px 700px;
        }}

        section[data-testid="stSidebar"] {{
            background-image: url(data:image/png;base64,{sidebar_encoded_string.decode()});
            background-size: 400px 800px;
        }}
    </style>"""

    st.markdown(page, unsafe_allow_html=True)


def set_page_config():
    st.set_page_config(
        page_title="Bilgisayar Topluluğu",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/TOBB-ETU-CS-Community",
            "Report a bug": "https://tobbetu-bilgisayar-toplulugu.streamlit.app/Geri_Bildirim_Formu",
            "About": "Topluluğumuza ait web sayfasında bize dair pek çok bilgiye ulaşabilirsiniz. \
                Her türlü geri bildiriminize her zaman açığız.",
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
    date_columns: list = None,
    original_format: str = "%d.%m.%Y",
    new_format: str = "%Y-%m-%d",
):
    excel = pd.read_excel(
        io=file_path,
        sheet_name="Sheet1",
    )
    if date_columns is not None:
        for date_column in date_columns:
            for i in range(len(excel)):
                date_string = excel[date_column][i]
                date_object = datetime.strptime(date_string, original_format)
                new_date_string = date_object.strftime(new_format)
                excel[date_column][i] = datetime.strptime(
                    new_date_string, new_format
                )
            excel.sort_values(by=date_column, inplace=True)
            excel.reset_index(drop=True, inplace=True)
    return excel
