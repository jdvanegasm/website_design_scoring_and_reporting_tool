"""
cloud integrations: uploads files to Google Drive and logs summary to Google Sheets
supports either a service-account JSON *or* an OAuth client_secret.json (desktop)
the path is read from config.yaml ➜ google.service_account_json
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import List, Dict

import gspread
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account, credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from config_loader import cfg
G = cfg().get("google", {})


# helpers


_SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/spreadsheets",
]


def _get_creds():
    """
    loads creds once and reuses:
        • if the json is a service-account key → use it directly
        • else treat it as OAuth client_secret and cache token next to it
    """
    path = Path(G["service_account_json"])
    data = json.loads(path.read_text())

    # service-account flow
    if data.get("type") == "service_account":
        return service_account.Credentials.from_service_account_file(path, scopes=_SCOPES)

    # OAuth installed-app flow
    token_path = path.with_suffix(".token.json")
    creds: credentials.Credentials | None = None

    if token_path.exists():
        creds = credentials.Credentials.from_authorized_user_file(token_path, _SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(path), _SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())

    return creds


_CREDS = _get_creds()
_DRIVE = build("drive", "v3", credentials=_CREDS)
_SHEETS = gspread.authorize(_CREDS).open_by_key(G["sheet_id"]).sheet1


def _upload_file(local_path: Path, mime: str) -> str:
    """
    uploads a file and returns shareable link
    """
    file_metadata = {"name": local_path.name, "parents": [G["drive_folder_id"]]}
    media = MediaFileUpload(local_path, mimetype=mime, resumable=True)
    f = (
        _DRIVE.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    _DRIVE.permissions().create(
        fileId=f["id"], body={"type": "anyone", "role": "reader"}
    ).execute()
    return f"https://drive.google.com/file/d/{f['id']}/view"


# public gateway


def push_to_drive_and_sheet(
    url: str,
    score: float,
    breakdown: Dict[str, float],
    screenshot_path: Path,
    report_paths: List[Path],
):
    """
    1. uploads screenshot + reports to Drive (folder from config)
    2. appends a row to the first sheet
    """
    links: Dict[str, str] = {}
    links["screenshot"] = _upload_file(screenshot_path, "image/png")
    for p in report_paths:
        mime = "application/pdf" if p.suffix == ".pdf" else "text/plain"
        links[p.suffix.lstrip(".")] = _upload_file(p, mime)

    row = [
        dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        url,
        score,
        str(breakdown),
        links.get("pdf", ""),
        links["screenshot"],
    ]
    _SHEETS.append_row(row, value_input_option="USER_ENTERED")