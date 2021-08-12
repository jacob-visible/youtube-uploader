import PySimpleGUI as sg


sg.theme("LightTeal") # Maybe DarkAmber
# Elements in layout
menu_def = [['&File', ['&Properties', '&Exit']], ['&Help', ['&About', '&Update']]]

# Main layout
column1 = [
    [
        sg.Menu(menu_definition=menu_def, tearoff=False, pad=(200, 1))
    ],
    [
        sg.FileBrowse(enable_events=True, key="-FILE-", button_text="Add File", file_types=(("", ".mp4"), ("", ".avi"), ("", ".mov"), ("", ".wmv"), ("", ".mkv"), ("", ".webm"), ("", ".flv"), ("", ".vob"), ("", ".ogg"), ("", ".avi"), ("", ".drc"), ("", ".gif"), ("", ".gifv"), ("", ".mng"), ("", ".mts"), ("", ".m2ts"), ("", ".ts"), ("", ".mov"), ("", ".qt"), ("", ".wmv"), ("", ".yuv"), ("", ".rm"), ("", ".rmvb"), ("", ".viv"), ("", ".asf"), ("", ".amv"), ("", ".m4p"), ("", ".m4v"), ("", ".mpg"), ("", ".mp2"), ("", ".mpeg"), ("", ".mpe"), ("", ".mpv"), ("", ".m2v"), ("", ".m4v"), ("", ".svi"), ("", ".3gp"), ("", ".3g2"), ("", ".mxf"), ("", ".roq"), ("", ".nsv"), ("", ".flv"), ("", ".f4v"), ("", ".f4p"), ("", ".f4a"), ("", ".f4b"),)),  # file_type not supported on MAC
    ],
    [
        sg.FolderBrowse(enable_events=True, key="-FOLDER-", button_text="Add Folder"),
    ],
    [
        sg.Button(button_text="Clear", enable_events=True, key="-CLEAR-"),
    ],
    [
        sg.Button(button_text="Upload", enable_events=True, key="-EXECUTE-"),
    ],
]
column2 = [
    [
        sg.Listbox(values=[], select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, enable_events=True, size=(80, 12), key="-FILE LIST-") # , highlight_background_color="Black", highlight_text_color="White"
    ],
]
bottomBar = [
    [
        sg.ProgressBar(max_value=100, size=(53, 20), key="-PROGRESS BAR-")
    ],
    [
        sg.Text(key="-DIALOG-", text="", size=(69, 1)), sg.Text(key="-DIALOGTIME-", text="", size=(13, 1))
    ],
]
layout = [
    [
    sg.Column(column1),
    sg.Column(column2),
    ],
    [
        sg.HSeparator(),
    ],
    [
        bottomBar
    ]
]
