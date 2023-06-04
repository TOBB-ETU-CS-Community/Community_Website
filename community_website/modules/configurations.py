import base64

import streamlit as st


def add_bg_from_local(background_file, sidebar_background_file=None):
    with open(background_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    page = f"""<style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
        }}
        """
    if sidebar_background_file is not None:
        with open(sidebar_background_file, "rb") as image_file:
            sidebar_encoded_string = base64.b64encode(image_file.read())
            page += f"""
        section[data-testid="stSidebar"] div[class="css-6qob1r e1fqkh3o3"] {{
            background-image: url(data:image/png;base64,{sidebar_encoded_string.decode()});
            background-size: 400px 800px;
        }}
    """
    page += """</style>"""
    st.markdown(page, unsafe_allow_html=True)


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
