import base64
import os
import re
import smtplib
import ssl
import sys
from email.message import EmailMessage
from email.mime.text import MIMEText
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


def send_emails(subject: str, message: str, email_list: list):
    print("try")
    SENDER_EMAIL = st.secrets["email"]
    PASSWORD = st.secrets["app_pass"]
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(SENDER_EMAIL, PASSWORD)
        subject = "My first email"
        msg = "how are you"
        smtp.sendmail(SENDER_EMAIL, "ataturhan21@gmail.com", msg)


def send_email(subject: str, message: str, email_list: list):
    msg = EmailMessage()
    msg.set_content(message)

    SENDER_EMAIL = st.secrets["email"]
    PASSWORD = st.secrets["app_pass"]
    # me == the sender's email address
    # you == the recipient's email address
    msg["Subject"] = "yes"
    msg["From"] = SENDER_EMAIL
    msg["To"] = "ataturhan21@gmail.com"

    # Login
    s = server = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER_EMAIL, PASSWORD)

    # Sending the message
    s.send_message(msg)
    s.quit()


def send_emai(subject: str, message: str, email_list: list):
    """
    Sends an email to multiple recipients.

    Parameters:
    - subject (str): The subject or title of the email.
    - message (str): The content or body of the email.
    - email_list (list): A list of email addresses to which the email will be sent.

    Returns:
    - None

    Example Usage:
    send_emails(subject='Greetings from the Community Website!',
                message='Hello everyone, we are thrilled to welcome you to our community!',
                email_list=['email1@example.com', 'email2@example.com'])

    Note:
    - This function uses SMTP (Simple Mail Transfer Protocol) to send emails. You'll need to have access to an SMTP server.
    - Ensure that the SMTP server configurations and credentials are properly set before using this function.
    - Be cautious about sending mass emails to avoid being marked as spam.
    """

    SENDER_EMAIL = st.secrets["email"]
    PASSWORD = st.secrets["app_pass"]

    # ---- SMTP Server Config ----
    port = 587
    SMTP_server = "smtp.gmail.com"

    # ---- Set up Server ----
    server = smtplib.SMTP(SMTP_server, port, SENDER_EMAIL, timeout=120)

    # ---- StartTLS ----
    context = ssl.create_default_context()
    starttls(server=server, context=context)

    # ---- Log in to the Sender Email ----
    login(server=server, sender_email=SENDER_EMAIL, sender_password=PASSWORD)

    # ---- Send mail to the receivers (Email List) ----
    mail = create_mail(
        sender_email=SENDER_EMAIL,
        message=message,
        subject=subject,
        email_list=email_list,
    )
    sendmail(
        server=server,
        sender_email=SENDER_EMAIL,
        email_list=email_list,
        mail=mail,
    )

    server.quit()


def create_mail(
    sender_email: str, message: str, subject: str, email_list: list
) -> MIMEText:
    mail = MIMEText(message, "html", "utf-8")
    mail["From"] = sender_email
    mail["Subject"] = subject
    mail["To"] = ",".join(email_list)
    return mail.as_string()


def starttls(server: smtplib.SMTP, context: ssl.SSLContext):
    return server.starttls(context=context)


def login(server: smtplib.SMTP, sender_email: str, sender_password: str):
    return server.login(sender_email, sender_password)


def sendmail(
    server: smtplib.SMTP, sender_email: str, email_list: list, mail: str
):
    return server.sendmail(sender_email, email_list, mail)


def get_context():
    return ssl.create_default_context()
