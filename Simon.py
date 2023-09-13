import requests
from playwright.sync_api import sync_playwright, TimeoutError

def login(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://simon.sfx.vic.edu.au/Login/Default.aspx")

        username_elem = page.locator('//*[@id="inputUsername"]')
        password_elem = page.locator('//*[@id="inputPassword"]')

        username_elem.fill(username)
        password_elem.fill(password)

        login_button = page.locator('//*[@id="buttonLogin"]')
        login_button.click()
        xpath_to_wait_for = '//*[@id="app"]/div[1]/main/div/div[2]/div/div/div[1]/div/div[1]'
        try:
            page.wait_for_selector(f'xpath={xpath_to_wait_for}', timeout=1000)
            detected = 200
        except TimeoutError:
            detected = 404

        cookies = page.context.cookies()
        for cookie in cookies:
            if cookie['name'] == 'adAuthCookie':
                cookie = cookie['value']

        browser.close()

        return detected, cookie

def checkCookie(cookie):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/UserInformation"
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"adAuthCookie={cookie}"
    }



    response = requests.post(url, headers=headers)

    if response.status_code == 401:
        return False
    else:
        return True

def getTimetable(cookie, time):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/GetTimetable"
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"adAuthCookie={cookie}"
    }

    data = {
        "selectedDate": time,
        "selectedGroup": None
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()

def getDailyMessages(cookie, time):
    url = "https://simon.sfx.vic.edu.au/WebServices/SchoolMessagesAPI.asmx/GetWorkDeskDailyMessages"
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"adAuthCookie={cookie}"
    }

    data = {
        "messageDate": time,
        "messageType": "DAILY"
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()

def getUserInfo(cookie):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/UserInformation"
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"adAuthCookie={cookie}"
    }



    response = requests.post(url, headers=headers)

    return response.json()

def getToday(cookie):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/GetCalendarEvents"
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"adAuthCookie={cookie}"
    }


    response = requests.post(url, headers=headers)
    return response.json()

def getClasses(cookie):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/GetClassResources"
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"adAuthCookie={cookie}"
    }
    data = {
        "FileSeq": 44,
        "UserID": None
    }


    response = requests.post(url, headers=headers, json=data)
    return response.json()

