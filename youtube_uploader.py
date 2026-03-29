import os, pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES         = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE     = "token.pickle"
CLIENT_SECRETS = "client_secrets.json"

def _auth():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE,"rb") as f: creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow  = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE,"wb") as f: pickle.dump(creds, f)
    return build("youtube","v3",credentials=creds)

def upload_video(video_path, script_data):
    print("[YouTube] Connecting...")
    yt = _auth()

    title = script_data["title"]
    if "#Shorts" not in title and "#shorts" not in title:
        title = (title[:88]+" #Shorts") if len(title)>88 else title+" #Shorts"

    body = {
        "snippet": {
            "title":           title,
            "description":     script_data["description"],
            "tags":            script_data["tags"],
            "categoryId":      "27",
            "defaultLanguage": "en",
        },
        "status": {
            "privacyStatus":           "public",
            "selfDeclaredMadeForKids": False,
        }
    }

    media = MediaFileUpload(
        video_path, mimetype="video/mp4",
        resumable=True, chunksize=5*1024*1024
    )

    print("[YouTube] Uploading...")
    req  = yt.videos().insert(part="snippet,status",body=body,media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status: print(f"[YouTube] {int(status.progress()*100)}%")

    vid_id = resp["id"]
    print(f"[YouTube] Live: https://youtube.com/shorts/{vid_id}")
    return vid_id
