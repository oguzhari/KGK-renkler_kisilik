from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path
import os
import streamlit as st
import requests as rs
import mimetypes

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds


def mime_init(from_addr, recipients_addr, subject, body):
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = ",".join(recipients_addr)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    return msg


def send_analysis(recipients_addr, files_path=None, server="smtp.gmail.com"):
    FROM = "Sakarya Üniversitesi Kariyer Geliştirme Koordinatörlüğü <kariyer@sakarya.edu.tr>"
    TO = (
        recipients_addr
        if isinstance(recipients_addr, list)
        else recipients_addr.split(" ")
    )
    SUBJECT = "Renkler ve Kişilik Envanteri Sonuçları"
    BODY = "Tamamlamış olduğunuz envantere ait sonuçlar ekte yer almaktadır."
    msg = mime_init(FROM, TO, SUBJECT, BODY)

    for file_path in files_path or []:
        path_obj = Path(file_path)
        file_name = path_obj.name
        if path_obj.suffix == "":
            file_name += ".docx"

        with open(file_path, "rb") as fp:
            part = MIMEBase(
                "application",
                "vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            part.set_payload(fp.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename=file_name)
            msg.attach(part)

    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    message = {"raw": raw}
    service.users().messages().send(userId="me", body=message).execute()


def send_analysis_to_danisman(
    recipients_addr, files_path=None, server="smtp.gmail.com"
):
    FROM = "Sakarya Üniversitesi Kariyer Geliştirme Koordinatörlüğü <kariyer@sakarya.edu.tr>"
    TO = (
        recipients_addr
        if isinstance(recipients_addr, list)
        else recipients_addr.split(" ")
    )
    SUBJECT = "Renkler ve Kişilik Envanteri Sonuçları"
    BODY = "Öğrencinize ait envanter ektedir."
    msg = mime_init(FROM, TO, SUBJECT, BODY)

    for file_path in files_path or []:
        path_obj = Path(file_path)
        file_name = path_obj.name
        if path_obj.suffix == "":
            file_name += ".docx"

        with open(file_path, "rb") as fp:
            part = MIMEBase(
                "application",
                "vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            part.set_payload(fp.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename=file_name)
            msg.attach(part)

    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    message = {"raw": raw}
    service.users().messages().send(userId="me", body=message).execute()
