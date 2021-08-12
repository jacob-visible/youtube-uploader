from datetime import datetime

# User settings
extenionsList: list[str] = [".mp4",".avi",".mov",".wmv",".mkv",".webm",".flv",".vob",".ogg",".avi",".drc",".gif",".gifv",".mng",".mts",".m2ts",".ts",".mov",".qt",".wmv",".yuv",".rm",".rmvb",".viv",".asf",".amv",".m4p",".m4v",".mpg",".mp2",".mpeg",".mpe",".mpv",".m2v",".m4v",".svi",".3gp",".3g2",".mxf",".roq",".nsv",".flv",".f4v",".f4p",".f4a",".f4b"]

# Testing settings
verboseLogs: bool = False

# Default variables specific to this program. Do not touch unless you know what you're doing.
today = datetime.today()
titleStart = "Upload Title"
videoUploadDirectory: str = r'C:\Uploads'
publishHour: int = 23
description: str = "Subscribe to see more."
tags: str = 'Gaming Highlights'
stepProgressSecondsDefault: float = 2.2
progressStages: list[int] = [96]
