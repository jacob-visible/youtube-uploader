import os
import time
import queue
import threading

import config
import layout
import utility


window = layout.sg.Window("Youtube Uploader", layout.layout)

# Event listners for each button press
inputFilepathsListed: list[str] = []
inputFilenamesListed: list[str] = []
currentCompletedTasks: int = -1
taskDialogs: list[str] = []
currentProgress: int = -1
entireRuntimeStart = time.time()
currentRunTimeWatch = time.time()
stepProgressSeconds: float = config.stepProgressSecondsDefault
gui_queue = queue.Queue()  # queue used to communicate between the gui and the threads
while True:
    event, values = window.read(timeout=100)
    if event == layout.sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == "-FILE-":
        try:
            addingFilePath: str = values["-FILE-"]
            if addingFilePath not in inputFilepathsListed:
                if os.path.exists(addingFilePath):
                    inputFilepathsListed.append(addingFilePath)
                    inputFilenamesListed.append(addingFilePath.rsplit('/', 1)[1])
                    print("Notification - File added:", addingFilePath)
                else:
                    print("Alert - Can not verify file exists:", addingFilePath)
            else:
                print("Notification - File already added:", addingFilePath)
        except Exception as e:
            print("Alert - File not found.", e)
    elif event == "-FOLDER-":
        try:
            addingFolderPath: str = values["-FOLDER-"]
            if os.path.exists(addingFolderPath):
                for file in os.listdir(addingFolderPath):
                    for extension in config.extenionsList:
                        if file.endswith(extension) and (addingFolderPath + """/""" + file) not in inputFilepathsListed and os.path.exists(addingFolderPath + """/""" + file):
                            inputFilepathsListed.append(addingFolderPath + """/""" + file)
                            inputFilenamesListed.append(file)
                            print("Notification - File added:", addingFolderPath + """/""" + file)
        except Exception as e:
            print("Alert - Folder not found.", e)
    elif event == "-CLEAR-":
        inputFilepathsListed.clear()
        inputFilenamesListed.clear()
    elif event == "-EXECUTE-":
        if len(inputFilepathsListed) > 0:
            currentCompletedTasks: int = 0
            taskDialogs: list[str] = []
            queueVariables: list[list] = []
            window["-PROGRESS BAR-"].update(current_count=0)
            window["-EXECUTE-"].update(disabled=True)
            window["-CLEAR-"].update(disabled=True)
            window["-FILE-"].update(disabled=True)
            window["-FOLDER-"].update(disabled=True)
            window.Element("-DIALOG-").update("(" + str(1) + "/" + str(len(inputFilepathsListed)) + ")" + " Processing... " + inputFilepathsListed[0].rsplit("/", 1)[1])
            fileCount: int = 0
            # Progress bar
            entireRuntimeStart = time.time()
            currentRunTimeWatch = time.time()
            print("Step Progress Seconds:", stepProgressSeconds)
            for INPUTFILEPATH in inputFilepathsListed:
                fileCount += 1
                print("Notification - Added Task:", fileCount, INPUTFILEPATH)
                window.refresh()
                # append text to the filename start
                OUTPUTFILEPATH: str = INPUTFILEPATH.rsplit("/", 1) [0] + """/""" + config.completedAppendStart + INPUTFILEPATH.rsplit("/", 1)[1]
                # append text to the filename end
                OUTPUTFILEPATH = OUTPUTFILEPATH.rsplit(".", 1)[0] + config.completedAppendEnd + "." + OUTPUTFILEPATH.rsplit(".", 1)[1]
                if not OUTPUTFILEPATH.rsplit(".", 1)[1] in config.extenionsOutputList:
                    print("Notification - Extension not found in output list:", INPUTFILEPATH.rsplit(".", 1)[1], config.extenionsOutputList)
                    OUTPUTFILEPATH = OUTPUTFILEPATH.rsplit(".", 1)[0] + ".mp4"
                i: int = 0
                while os.path.exists(OUTPUTFILEPATH):
                    i += 1
                    if not os.path.exists(OUTPUTFILEPATH.rsplit(".", 1)[0] + "(" + str(i) + ")" + "." + INPUTFILEPATH.rsplit(".", 1)[1]):
                        OUTPUTFILEPATH: str = OUTPUTFILEPATH.rsplit(".", 1)[0] + "(" + str(i) + ")" + "." + INPUTFILEPATH.rsplit(".", 1)[1]
                        break
                taskDialogs.append("(" + str(fileCount) + "/" + str(len(inputFilepathsListed)) + ")" + " Processing... " + INPUTFILEPATH.rsplit("/", 1)[1])
                queueVariables.append([INPUTFILEPATH, OUTPUTFILEPATH, 0])
            window["-PROGRESS BAR-"].update(current_count=0)
            window.Element("-DIALOG-").update(taskDialogs[0])
            processTimeIntialEstimate: int = int((stepProgressSeconds/60*100))
            window.Element("-DIALOGTIME-").update(str("~" + str(processTimeIntialEstimate) + " mins remain"))
            threading.Thread(target=utility.queue_runner, args=(queueVariables, gui_queue), daemon=True).start() # Multithreading

    elif event == "Properties":
        if currentCompletedTasks == -1:
            print("Properties")
    elif event == "About":
        print("About")  # This can be a link to our website's about page
    elif event == "Update":
        print("Update")  # This can be a link to our website's latest download page. With the installer it should upgrade an existing version.

    window["-FILE LIST-"].update(inputFilenamesListed)
    try: # Multithreading
        message = gui_queue.get_nowait()
    except queue.Empty:
        message = None
    if message:
        print("Got message from queue:", message)
    if message == "100":
        currentCompletedTasks += 1
        window["-PROGRESS BAR-"].update(current_count=0)
        if currentCompletedTasks >= len(inputFilepathsListed):
            currentCompletedTasks = -1
            currentProgress = -1
            window["-PROGRESS BAR-"].update(current_count=100)
            window["-EXECUTE-"].update(disabled=False)
            window["-CLEAR-"].update(disabled=False)
            window["-FILE-"].update(disabled=False)
            window["-FOLDER-"].update(disabled=False)
            window.Element("-DIALOG-").update("Tasks Completed")
            window.Element("-DIALOGTIME-").update("")
            utility.jobs_done(window, entireRuntimeStart)
    if message == "0" and currentCompletedTasks > -1:
        window.Element("-DIALOG-").update(taskDialogs[currentCompletedTasks])

    if (time.time() - stepProgressSeconds) >= currentRunTimeWatch and currentCompletedTasks > -1:
        currentRunTimeWatch = time.time()
        if (currentProgress+1) not in config.progressStages:
            currentProgress += 1
            window["-PROGRESS BAR-"].update(current_count=currentProgress)
            if currentProgress > 0:
                # Show the estimated remaining time
                remainingTime: float = ((currentRunTimeWatch - entireRuntimeStart) / float(currentProgress))*(100-currentProgress)/60
                if remainingTime > 1:
                    window.Element("-DIALOGTIME-").update("~" + str(int(remainingTime)) + " mins remain")
                elif round(remainingTime) == 1:
                    window.Element("-DIALOGTIME-").update("~1 min remain")
                else:
                    window.Element("-DIALOGTIME-").update("~" + str(int(remainingTime*60)) + " sec remain")

    if message == str(config.progressStages[0]):
        currentProgress = config.progressStages[0]
        window["-PROGRESS BAR-"].update(current_count=currentProgress)

window.close()
