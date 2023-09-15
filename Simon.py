import requests, time, re
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

def getUserProfileInfo(cookieRaw, uuid):

    profileInformation = {
        "name": "",
        "studentID": "",
        "yearLevel": "",
        "house": "",
        "attendence": {
            "percent": "",
            "pna": "",
            "late": "",
            "sick": "",
            "leave": ""
        },
        "courage": {
            "total": "",
            "community": "",
            "faith": "",
            "learning": "",
            "positive": ""
        },
    }
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        cookie = {
            'name': 'adAuthCookie',
            'value': cookieRaw,
            'domain': 'simon.sfx.vic.edu.au',  # Ensure this is set to the correct domain
            'path': '/'
        }

        page.context.add_cookies([cookie])
            
    # Main Page
        page.goto(f'https://simon.sfx.vic.edu.au/WebModules/Profiles/Student/GeneralInformation/StudentDashboard.aspx?UserGUID={uuid}')

        element = page.wait_for_selector("#attendanceBox")

        try:
            attendenceBox = page.wait_for_selector(f'#attendanceBox', timeout=6000)
        except Exception as e:
            return False

    # Getting default information
        studentNameId = page.wait_for_selector(f'xpath=//*[@id="mainPanelCard"]/div/div/div[1]/h2').text_content()
        profileInformation['studentID'] = re.sub(r'\D', '', studentNameId)
        profileInformation['name'] = re.sub(r' +', ' ', re.sub(r'[^a-zA-Z ]', '', studentNameId)).strip()

        yearLevel = page.wait_for_selector(f'xpath=//*[@id="FormPlaceHolder_FormContent_DefaultDomainInfo_InfoContent_YearLevelHeader"]').text_content()
        profileInformation['yearLevel'] = yearLevel

        house = page.wait_for_selector(f'xpath=//*[@id="FormPlaceHolder_FormContent_DefaultDomainInfo_InfoContent_HouseHeader"]').text_content()
        profileInformation['house'] = house


    # Getting attendence information
        attendencePercent = page.wait_for_selector(f'#attendanceBox > div:nth-child(2) > div:nth-child(1) > div.progress > div > span').text_content()
        profileInformation['attendence']['percent'] = attendencePercent

        pna = page.wait_for_selector(f'xpath=//*[@id="pnlAttendance"]/div/div[2]/a[1]/span').text_content()
        profileInformation['attendence']['pna'] = pna

        late = page.wait_for_selector(f'xpath=//*[@id="pnlAttendance"]/div/div[2]/a[2]/span').text_content()
        profileInformation['attendence']['late'] = late

        sick = page.wait_for_selector(f'xpath=//*[@id="pnlAttendance"]/div/div[2]/a[3]/span').text_content()
        profileInformation['attendence']['sick'] = sick

        leave = page.wait_for_selector(f'xpath=//*[@id="pnlAttendance"]/div/div[2]/a[4]/span').text_content()
        profileInformation['attendence']['leave'] = leave

    # Commendations
        url = "https://simon.sfx.vic.edu.au/WebServices/BehaviouralTracking.asmx/GetWorkDeskCommendationsPaged"
        headers = {
                "Content-Type": "application/json",
                "Cookie": f"adAuthCookie={cookieRaw}"
        }


        data = {
            "endDate": "2026-12-19T13:00:00.000Z",
            "filter": None,
            "page": 1,
            "pageSize": 100,
            "showMyRecordsOnly": False,
            "skip": 0,
            "startDate": "2017-01-27T13:00:00.000Z",
            "take": 10,
            "userGUID": uuid,
            "sort": [{'field': "CommendationDate", 'dir': "desc"}]
        }

        response = requests.post(url, headers=headers, json=data)

        courageTotal = 0
        courageCommunity = 0
        courageFaith = 0
        courageLearning = 0
        couragePositive = 0
        for commendation in response.json()['d']['Data']:
            courageTotal += 1

            if commendation['CategoryDescription'] == "Leadership in Community and Culture":
                courageCommunity += 1
            elif commendation['CategoryDescription'] == "Leadership in Faith and Service":
                courageFaith += 1
            elif commendation['CategoryDescription'] == "Leadership in Learning":
                courageLearning += 1
            elif commendation['CategoryDescription'] == "Leadership in Learning Partnerships":
                couragePositive += 1
            else:
                courageCommunity += 1

        profileInformation['courage']['total'] = courageTotal
        profileInformation['courage']['community'] = courageCommunity
        profileInformation['courage']['faith'] = courageFaith
        profileInformation['courage']['learning'] = courageLearning
        profileInformation['courage']['positive'] = couragePositive
        
        browser.close()

    return profileInformation
    
        
