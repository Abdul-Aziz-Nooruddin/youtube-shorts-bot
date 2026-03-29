# Run this ONCE on your local PC:  python setup_auth.py
# It connects your YouTube account and prints the GitHub secrets you need.

import pickle, base64, os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    print("\n" + "="*60)
    print("  YouTube Account Authorization")
    print("="*60)

    if not os.path.exists("client_secrets.json"):
        print("\n  client_secrets.json not found!")
        print("  Download it from Google Cloud Console.")
        print("  Rename it to client_secrets.json")
        print("  Put it in this folder.\n")
        return

    print("\n  Opening browser...")
    print("  Log in with your YouTube channel's Google account.")
    print("  Click Allow.\n")

    flow  = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
    creds = flow.run_local_server(port=0)

    with open("token.pickle","wb") as f: pickle.dump(creds,f)

    with open("token.pickle","rb") as f:
        b64_token = base64.b64encode(f.read()).decode("utf-8")

    with open("client_secrets.json","r") as f:
        client_secrets = f.read().strip()

    print("\n" + "="*60)
    print("  Authorization successful!")
    print("="*60)
    print("\n  Go to GitHub repo > Settings > Secrets and variables > Actions")
    print("  Add these 4 secrets:\n")

    print("  Secret 1:  GROQ_API_KEY")
    print("  Value:     your key from console.groq.com\n")

    print("  Secret 2:  PEXELS_API_KEY")
    print("  Value:     your key from pexels.com/api\n")

    print("  Secret 3:  YOUTUBE_TOKEN")
    print("  Value:")
    print("-"*60)
    print(b64_token)
    print("-"*60)

    print("\n  Secret 4:  YOUTUBE_CLIENT_SECRETS")
    print("  Value:")
    print("-"*60)
    print(client_secrets)
    print("-"*60)
    print()

if __name__ == "__main__":
    main()
