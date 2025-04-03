import nodriver as uc
from time import sleep

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'  # Reemplaza con la ruta a tu archivo credentials.json
TOKEN_PICKLE = 'token.pickle'

def get_credentials():
    creds = None
    # Comprobar si ya existe un token de acceso guardado.
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    # Si no hay credenciales válidas, inicia el flujo de OAuth.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para usos futuros.
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def save_html_to_doc(html):
        with open("pagina.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        creds = get_credentials()
        drive_service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {
            'name': 'Documento de Google (convertido desde HTML)',
            'mimeType': 'application/vnd.google-apps.document'
        }

        media = MediaFileUpload("pagina.html", mimetype='text/html', resumable=True)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Documento creado con ID: {file.get('id')}")


URL = 'https://www.turingpost.com/p/coa-and-co-rag?_bhlid=87457dd233fa0a5f7ca6ec61c6c3c41219da3b63&utm_campaign=topic-27-what-are-chain-of-agents-and-chain-of-rag&utm_medium=newsletter&utm_source=www.turingpost.com'

async def main():

    driver = await uc.start(
        user_data_dir="userFolder/"
    )
    tab = await driver.get(URL)
    
    sleep(10)
    
    html = await tab.get_content()
    save_html_to_doc(html)
    
    sleep(8.5)

if __name__ == '__main__':

    # since asyncio.run never worked (for me)
    uc.loop().run_until_complete(main())