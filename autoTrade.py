import pygetwindow as gw
import pytesseract
import PIL
import cv2
import pyautogui
import numpy as np
from time import sleep

#Use this filepath for tesseract
# Define the text to search for
target_text = "Gems"
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'




#########################################
#Check if Leaf blower is open to get the application window
def lbrOpenCheck():
    # Define the window search keyword
    window_search_keyword = "Leaf Blower"
    # Get a list of all currently open windows
    all_windows = gw.getAllTitles()
    # Search for windows that contain the window search keyword in their titles
    matching_windows = [window for window in all_windows if window_search_keyword in window]
    if len(matching_windows) == 0:
        print(f"No window titles contain the keyword '{window_search_keyword}'.")
        return
    else:
        print(f"{matching_windows} found!")
    # Assuming you want to interact with the first matching window found
    app_window_title = matching_windows[0]
    app_window = gw.getWindowsWithTitle(app_window_title)

    if len(app_window) == 0:
        print(f"Window with title '{app_window_title}' not found.")
        quit()
    else:
        print(f"{app_window_title} found!")
        app_window = app_window[0]
        app_window.activate()  # Focus on the application window
        return(app_window)
        print(f"TOP LEFT: {app_window.topleft}, WIDTH: {app_window.width}, HEIGHT: {app_window.height}")

#########################################

##########################################
#Read the output text of pytesseract.image_to_data and convert it to a Dict and return
def parse_tabular_text_to_dict(text):
    lines = text.strip().split("\n")  # Split the text into lines
    keys = lines[0].split()  # Extract the header as keys
    data = [line.split() for line in lines[1:]]  # Extract the remaining lines as data

    # Convert each row into a dictionary using the keys
    result = [dict(zip(keys, row)) for row in data]

    return result
########################################

#########################################
#Open the small screen window with Drawn Text
def runScreen():
        screen = np.array(PIL.ImageGrab.grab(bbox=(PIL.ImagePath.Path(PIL.Image.open('LBR-Testing-Trade-5.png')).getbbox())))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)


        cv2.imshow('window', cv2.resize(screen, (960, 540)))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            quit()
#########################################
#########################################
def clickCentre(data):
    print("Clicking ", data[1][0][0], data[1][0][1])
    pyautogui.moveTo(data[1][0][0]+30, data[1][0][1]+5)
    pyautogui.mouseDown()
    pyautogui.click()
    sleep(0.15) 
    pyautogui.mouseUp()
#########################################


#########################################
#Return the value from the key
def getValue(data, keyName):
    for key, value in data.items():
       if key == keyName: 
            return int(value)
#########################################
#Run Image scan, look for 
def findGem(imageText):
    matching_gems = []
    #Iterate through each row of Data and get lines with text='function input'
    for line in imageText:
        for key, value in line.items():
            if key == "text":
                if "gems" in value.lower():
                    matching_gems.append(line)
    return matching_gems
    #print("THIS", matching_gems)

    #Look through items 
    # for gem in matching_gems:
    #     gemTop = getValue(gem, "top")
    #     for start in matching_start:
    #         startTop = getValue(start, "top")
    #         print(startTop, gemTop)
    #         if gemTop - startTop <= 50:
    #             print("Found matching Start and Gem!")
    #             print(f"{start} and {gem}")
        

#############################
def findButton(imageText,searchText):
    matching=[]
    for line in imageText:
        for key, value in line.items():
            if key == "text":
                if searchText.lower() in value.lower():
                    matching.append(line)
    return matching            

#########################################
#########################################
#Get bbox coords
def getCoords(data):
    x1, y1, x2, y2 = 0,0,0,0
    for key, value in data.items():
        if key == "left":
            x1 = int(value)
        elif key == "top":
            y1 = int(value)
        elif key == "width" and x1 != 0:
            x2 = int(value) + int(x1)
        elif key == "height" and y1 != 0:
            y2 = int(value) + int(y1)
    return([[(x1, y1),(x2,y2)], [(x1+2100, y1+50),(x2+2100,y2+50)]])
#########################################


#########################################
#Draw boundingbox on xy coords
def drawBounding(data):
    xy = getCoords(data)

    image=PIL.Image.open('new.png')
    #Create a drawing object
    draw = PIL.ImageDraw.Draw(image)

    draw.rectangle(xy[0], outline="Blue", fill= None, width = 5)
    draw.rectangle(xy[1], outline="Blue", fill= None, width = 5)

    #Save or display the modified image
    image.save("new.png")
    

# def drawDot(x,y):
#     image=PIL.Image.open('new.png')
#     #Create a drawing object
#     draw = PIL.ImageDraw.Draw(image)
#     #Add text to the image
#     draw.text(xy=(x,y), text="X", fill="Red", size=30)

#     #Save or display the modified image
#     image.save("new.png")
#########################################


###############################
#Press the hotkey R used for trades in leaf blower
def refreshTrde():
    pyautogui.press('r')

#########################
#Screenshot and scan

def snapScan():
    x1 = lbr_app.left
    y1 = lbr_app.top
    x2 = lbr_app.width
    y2 = lbr_app.height


    screenshot = pyautogui.screenshot(region=(x1,y1,x2,y2))
    # Save the screenshot to a file
    screenshot.save('./screenshot.png')

    imgBW = PIL.Image.open('screenshot.png')#.convert('L')
    imgBW.save('newBW.png')
    imgText = parse_tabular_text_to_dict(pytesseract.image_to_data(PIL.Image.open('newBW.png')))
    return imgText
############################
############################
#MANUAL COORDS for BOOST ALL
def clickBoost():
    pyautogui.moveTo(1249+lbr_app.left,942+lbr_app.top)
    pyautogui.mouseDown()
    pyautogui.click()
    sleep(0.15) 
    pyautogui.mouseUp()

# MANUAL COORDS for COLLECT ALL
def clickCollect():
    pyautogui.moveTo(1600+lbr_app.left,942+lbr_app.top)
    pyautogui.mouseDown()
    pyautogui.click()
    sleep(0.15) 
    pyautogui.mouseUp()


def doTheThing():
    clickBoost()
    clickCollect()
    scanData = snapScan()
    matches = findGem(scanData)
    print(matches)
    if len(matches) < 1:
        refreshTrde()
        sleep(0.1)
        doTheThing()
    else:  
        for gem in matches:
            # for match in lastMatch:
            #     if gem == match:
            #         matches[gem].remove()
            coords = getCoords(gem)
            clickCentre(coords)
            sleep(0.1)
        refreshTrde()
        doTheThing()
    #last_matches = matches
    


# Capture the screen of the specified application window
lbr_app = lbrOpenCheck()
sleep(0.5)

for inter in range(1,50000):
    doTheThing()





