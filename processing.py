from datetime import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

import config


def process(self, INPUTFILEPATHListed, gui_queue=None):
    INPUTFILEPATHListed: str = INPUTFILEPATHListed
    print("Starting upload for:", INPUTFILEPATHListed)
    # Start upload
    CLIENT_SECRET_FILE = 'Client_Secret.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    titleFinal: str = config.titleStart + " - (" + str(config.today.year) + "-" + str(config.today.month) + "-" + str(config.today.day) + ")"
    print("Final Title:", titleFinal)
    # Scheduled time to release on youtube
    upload_date_time = datetime(int(config.today.year), int(config.today.month), int(config.today.day), config.publishHour, 0, 0).isoformat() + '.000Z'
    print("Scheduled time:", config.today.year, config.today.month, config.today.day, config.publishHour)
    print("Scheduled time raw:", upload_date_time)
    # Category IDs https://gist.github.com/dgp/1b24bf2961521bd75d6c
    request_body = {
        'snippet': {
            'categoryI': '19',
            'title': titleFinal,
            'description': config.description,
            'tags': config.tags
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': True
    }

    mediaFile = MediaFileUpload(config.videoUploadDirectory + """\\""" + INPUTFILEPATHListed)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    # Old thumbnail C:\SyncFiles\Automated\Thumbnails\NLSS_Overlay_Highlights.png
    service.thumbnails().set(
        videoId=response_upload.get('id'),
        media_body=MediaFileUpload('C:\Thumbnails\Highlights.png')
    ).execute()
    # End Upload
    print("Posted to yt:", INPUTFILEPATHListed)
    return
