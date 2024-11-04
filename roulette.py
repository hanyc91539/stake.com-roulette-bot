from datetime import datetime
from time import sleep
from threading import Thread
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service as ChromeService
import keyboard
import requests
import json

BUTTON_01_12 = '1 to 12'
BUTTON_13_24 = '13 to 24'
BUTTON_25_36 = '25 to 36'
BUTTON_01_18 = '1 to 18'
BUTTON_19_36 = '19 to 36'
BUTTON_ROW01 = 'row1'
BUTTON_ROW02 = 'row2'
BUTTON_ROW03 = 'row3'
BUTTON_EVEN = 'Even'
BUTTON_ODD = 'Odd'
BUTTON_RED = 'Red'
BUTTON_BLACK = 'Black'
BUTTON_BET = 'Bet'
BUTTON_HALF = '1/2'
BUTTON_DOUBLE = '2x'
BUTTON_UNDO = 'Undo'
BUTTON_CLEAR = 'Clear'

initChipValue = 0.01

betOptions = []
with open("strategy.json", "r") as file:
    betOptions = json.load(file)

url = "https://stake.com/casino/games/roulette"

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9025") #9025
options.add_argument("user-agent=Chrome/121.0.6167.185")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

pressedESC = False

Is_End = False


ID = {
    BUTTON_01_12 : "range0112",
    BUTTON_13_24 : "range1324",
    BUTTON_25_36 : "range2536",
    BUTTON_01_18 : "range0118",
    BUTTON_19_36 : "range1936",
    BUTTON_EVEN : "parityEven",
    BUTTON_ODD : "parityOdd",
    BUTTON_RED : "colorRed",
    BUTTON_BLACK : "colorBlack",
    BUTTON_ROW01 : "row1",
    BUTTON_ROW02 : "row2",
    BUTTON_ROW03 : "row3",
    BUTTON_BET : "variant-success",
    BUTTON_HALF : "input-button-wrap@0",
    BUTTON_DOUBLE : "input-button-wrap@1",
    BUTTON_UNDO : "button-undo",
    BUTTON_CLEAR : "button-clear"
}


def clickButton(buttonName):
    if not pressedESC:
        button = None
        if isinstance(buttonName, int):
            buttonId = "number%s" %buttonName
        else:
            buttonId = ID[buttonName]
        if "input-button-wrap" in buttonId:
            button = findElement(driver, By.CLASS_NAME, "input-button-wrap").find_elements(By.TAG_NAME, 'button')[int(buttonId.split("@")[1])]
        elif buttonId == "button-undo" or buttonId == "button-clear":
            button = findElement(driver, By.CSS_SELECTOR, f'button[data-testid="{buttonId}"]')
        else:
            button = findElement(driver, By.CLASS_NAME, buttonId)
        if button != None:
            try:
                button.click()
            except:
                driver.execute_script("arguments[0].click();", button)
            print(f'{datetime.now().strftime("%H:%M:%S")}, button clicked <{buttonName}>')
            sleep(0.5)


def Is_Win(zones):
    result = {
        BUTTON_01_12 : False,
        BUTTON_13_24 : False,
        BUTTON_25_36 : False,
        BUTTON_01_18 : False,
        BUTTON_19_36 : False,
        BUTTON_EVEN : False,
        BUTTON_ODD : False,
        BUTTON_RED : False,
        BUTTON_BLACK : False,
        BUTTON_ROW01 : False,
        BUTTON_ROW02 : False,
        BUTTON_ROW03 : False,
    }
    rollUp = 0
    while not pressedESC:
        try:
            rollUp = int(driver.find_element(By.CLASS_NAME, 'roll-up').text)
            if rollUp >= 1 and rollUp <= 12:
                result[BUTTON_01_12] = True

            if rollUp >= 13 and rollUp <= 24:
                result[BUTTON_13_24] = True

            if rollUp >= 25 and rollUp <= 36:
                result[BUTTON_25_36] = True

            if rollUp >= 1 and rollUp <= 18:
                result[BUTTON_01_18] = True

            if rollUp >= 19 and rollUp <= 36:
                result[BUTTON_19_36] = True

            if rollUp % 2 == 0:
                result[BUTTON_EVEN] = True
            else:
                result[BUTTON_ODD] = True

            if rollUp % 3 == 0:
                result[BUTTON_ROW01] = True
            elif rollUp % 3 == 2:
                result[BUTTON_ROW02] = True
            else:
                result[BUTTON_ROW03] = True

            if rollUp in [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]:
                result[BUTTON_BLACK] = True

            result[BUTTON_RED] = not result[BUTTON_BLACK]

            for zone in zones:
                if zone in result and result[zone]:
                    return "Win", rollUp
                else:
                    if rollUp == zone:
                        return "Win", rollUp
            return "Loss", rollUp
        except:
            pass
        sleep(0.1)
    return "ESC", rollUp


def setChipsToZone(zone, chips):
    if not pressedESC:
        chipButtons = findElement(driver, By.CLASS_NAME, 'scroll-wrap').find_elements(By.TAG_NAME, 'button')
        for index, unit in enumerate([100000000, 10000000, 1000000, 100000, 10000, 1000, 100, 10, 1]):
            count = int(chips / unit)
            chips %= unit
            if count > 0:
                if pressedESC:
                    break
                try:
                    chipButtons[8 - index].click()
                except:
                    driver.execute_script("arguments[0].click();", chipButtons[8 - index])
                for _ in range(count):
                    clickButton(zone)


def findElement(driver, by, value):
    element = None
    while not pressedESC:
        try:
            element = driver.find_element(by, value)
            break
        except:
            pass
        sleep(0.1)
    return element


def findElements(driver, by, value):
    elements = []
    while not pressedESC:
        try:
            elements = driver.find_elements(by, value)
            if elements:
                break
        except:
            pass
        sleep(0.1)
    return elements


def getBetAmount():
    betAmountUSD = float(findElement(driver, By.CLASS_NAME, 'currency-conversion').text.replace("$", ""))
    return betAmountUSD


def pressKey():
    global pressedESC
    while not Is_End:
        if keyboard.is_pressed('esc'):
            pressedESC = True
            # print(f'{datetime.now().strftime("%H:%M:%S")} pressed ESC key\n')
        sleep(0.1)


def Martingale():
    global Is_End
    global pressedESC

    chipValue = 0
    countStrategies = len(betOptions)
    indexStrategy = 0
    selectedStrategy = betOptions[indexStrategy]
    while not Is_End:
        for index, option in enumerate(selectedStrategy):
            if index == 0:
                chipValue = option["Chip Value"]
            else:
                chipValue *= option["Chip Value"]

            lossCount = option["Loss Count"]
            result = None
            if pressedESC:
                break
            for i in range(lossCount):
                clickButton(BUTTON_CLEAR)

                print(f'{datetime.now().strftime("%H:%M:%S")}, Chip Value: {chipValue}')
                zones = option["Zones"]
                for zone in zones:
                    setChipsToZone(zone, chipValue * 100000000)

                clickButton(BUTTON_BET)

                result, rollUp = Is_Win(zones)
                if result == "Win":
                    print(f'{datetime.now().strftime("%H:%M:%S")}, ~ ~ Roll Up: {rollUp}, Win ~ ~\n')
                    break
                elif result == "Loss":
                    print(f'{datetime.now().strftime("%H:%M:%S")}, - - Roll Up: {rollUp}, Loss {index + 1}:{i + 1} - -\n')
                else:
                    pass
                while True:
                    try:
                        lastBet = int(driver.find_element(By.CLASS_NAME, 'last-bet').text)
                        if rollUp == lastBet:
                            break
                    except:
                        pass
                    sleep(0.1)
                sleep(1.0)
                if pressedESC:
                    break
            if result == "Win":
                if index == len(selectedStrategy) - 1:
                    indexStrategy = (indexStrategy + 1) % countStrategies
                    selectedStrategy = betOptions[indexStrategy]
                    print(f'{datetime.now().strftime("%H:%M:%S")}, Moved to Strategy {indexStrategy+1}\n')
                break
        if pressedESC:
            response = input("It has now stopped running. Press the [y] key to run again, or press the [n] key to exit.")
            if response == "y":
                input("To run it again, you need to reset all states. Press the [Enter] key after initializing.")
                pressedESC = False
            else:
                break
    print(f'{datetime.now().strftime("%H:%M:%S")}, Ended')
    Is_End = True


def userVerify(url, payload):    
    global pressedKey
    global Is_End
    
    while True:
        sleep(3600)
        response = requests.request("POST", url, data=payload)
        data = response.json()["data"]
        print("")
        print(data + "\n")
        if data != "Successfully verified":
            pressedKey = True
            Is_End = True
            break


if __name__ == "__main__":
    while True:
        username = input("username: ")
        print("")
        password = input("password: ")
        print("")
        
        url = "http://87.251.88.14:80/login"

        payload = {
            'username': username,
            'password': password,
            'client_id': '123',
            'productName' : "roulette"
            }

        response = requests.request("POST", url, data=payload)
        data = response.json()["data"]
        
        print(data)
        print("")
        
        if data == "Successfully verified":
            break
        
    Thread(target=pressKey).start()
    Thread(target=userVerify, args=(url, payload, )).start()
    Martingale()
