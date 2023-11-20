import os
import smtplib
import sys
import unittest

import pandas as pd

path = os.getcwd()
parent_directory = os.path.abspath(os.path.join(path, os.pardir))
sys.path.append(parent_directory)

from community_website.modules.utils import (
    create_mail,
    get_context,
    login,
    sendmail,
    starttls,
    translate_excel,
)


class TestTranslateExcel(unittest.TestCase):
    def test_nonexistent_excel_file(self):
        excel_file_path = "tests/nonexistent_file.xlsx"
        to_language = "en"
        result = translate_excel(excel_file_path, to_language)
        self.assertIsNone(
            result, "Expected None for a non-existent Excel file"
        )

    def test_empty_excel_file(self):
        excel_file_path = "tests/test_excels/empty_file.xlsx"
        to_language = "en"
        result = translate_excel(excel_file_path, to_language)
        self.assertIsNone(result, "Expected None for an empty Excel file")

    def test_translation_without_export(self):
        expected_df = pd.DataFrame(["Turkish"], columns=["table"])
        excel_file_path = "tests/test_excels/sample.xlsx"
        to_language = "en"
        result = translate_excel(excel_file_path, to_language)
        print(result)
        self.assertIsInstance(result, pd.DataFrame, "Expected a DataFrame")
        self.assertFalse(result.empty, "Expected non-empty DataFrame")
        self.assertEqual(
            result.columns, expected_df.columns, "Columns translated correctly"
        )
        self.assertEqual(
            result.values, expected_df.values, "Rows translated correctly"
        )

    def test_translation_with_export(self):
        excel_file_path = "tests/test_excels/sample.xlsx"
        to_language = "en"
        result = translate_excel(excel_file_path, to_language, export=True)
        self.assertIsNone(result, "Expected None when exporting")
        self.assertTrue(
            os.path.isfile("tests/test_excels/sample_translated.xlsx"),
            "File created successfully",
        )


"""
class TestSendingEmails(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        SENDER_EMAIL = ""  # Topluluk gmaili gelecek
        PASSWORD = ""  # Topluluk gmail şifresi gelecek. Ayrıntıları aşağıda.

        # ---- Set up Server ----
        PORT = 587
        SMTP_SERVER = "smtp.gmail.com"
        self.server = smtplib.SMTP(SMTP_SERVER, PORT)

        # ---- StartTLS ----
        context = get_context()
        self.stls = starttls(server=self.server, context=context)

        # ---- Log in to the Sender Email ----
        self.log = login(
            server=self.server, sender_email=SENDER_EMAIL, sender_password=PASSWORD
        )

        # ---- Send mail to the receivers (Email List)----
        email_list = ["zedopdir@gmail.com", "ezrealopdir@gmail.com"]
        mail = create_mail(
            sender_email=SENDER_EMAIL,
            subject="Deneme Subject",
            message="Deneme message qweqweqwedew lorem ipsum",
            email_list=email_list,
        )
        self.sendm = sendmail(
            server=self.server,
            sender_email=SENDER_EMAIL,
            email_list=email_list,
            mail=mail,
        )

        self.server.close()

    def test_starttls(self):
        self.assertTupleEqual(
            self.stls, (220, b"2.0.0 Ready to start TLS")
        )  # starttls: Returns this tuple when Starting TLS is successful.

    def test_login(self):
        self.assertTupleEqual(
            self.log, (235, b"2.7.0 Accepted")
        )  # login: Returns this tuple when Logging in to the sender_email is successful.

    def test_sendmail(self):
        self.assertDictEqual(
            self.sendm, {}
        )  # sendmail: Returns dict of unsuccessful mails. If empty dict, all of them are successful.
"""

if __name__ == "__main__":
    unittest.main()
