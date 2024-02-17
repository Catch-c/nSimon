import requests, time, re
from playwright.sync_api import sync_playwright, TimeoutError
from bs4 import BeautifulSoup


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
        xpath_to_wait_for = (
            '//*[@id="app"]/div[1]/main/div/div[2]/div/div/div[1]/div/div[1]'
        )
        try:
            page.wait_for_selector(f"xpath={xpath_to_wait_for}", timeout=5000)
            detected = 200
        except TimeoutError:
            detected = 404

        cookies = page.context.cookies()
        for cookie in cookies:
            if cookie["name"] == "adAuthCookie":
                cookie = cookie["value"]

        browser.close()

        return detected, cookie


def checkCookie(cookie):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/UserInformation"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    response = requests.post(url, headers=headers)

    if response.status_code == 401:
        return False 
    else:
        return True


def getTimetable(cookie, time, campus):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/GetTimetable"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    data = {"selectedDate": time, "selectedGroup": campus}


    response = requests.post(url, headers=headers, json=data)

    return response.json()


def getDailyMessages(cookie, time):
    url = "https://simon.sfx.vic.edu.au/WebServices/SchoolMessagesAPI.asmx/GetWorkDeskDailyMessages"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    data = {"messageDate": time, "messageType": "DAILY"}

    response = requests.post(url, headers=headers, json=data)

    return response.json()


def getUserInformation(cookie):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/UserInformation"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    response = requests.post(url, headers=headers)

    return response.json()


def getUserProfileImage(cookie):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/UserInformation"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    response = requests.post(url, headers=headers)

    return response.json()


def getCalendarEvents(cookie):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/GetCalendarEvents"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    response = requests.post(url, headers=headers)
    return response.json()


def getClassResources(cookie):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/GetClassResources"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}
    data = {"FileSeq": 45, "UserID": None}

    response = requests.post(url, headers=headers, json=data)
    return response.json()


def getDashboardData(cookie, uuid):
    unix_seconds = time.time()

    unix_milliseconds = int(unix_seconds * 1000)

    url = f"https://simon.sfx.vic.edu.au/WebModules/Profiles/Student/GeneralInformation/StudentDashboard.aspx/GetDashboardData?{unix_milliseconds}"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}
    data = {"guidString": uuid, "semester": None}

    response = requests.post(url, headers=headers, json=data)
    return response.json()


def getStudentProfile(cookie):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/GetStudentProfiles"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    response = requests.post(url, headers=headers)
    return response.json()


def getSimonStudentImageURL(cookie):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/GetUserInfo"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    response = requests.post(url, headers=headers)
    data = response.json()

    if "d" in data and "UserPhotoUrl" in data["d"]:
        user_photo_url = data["d"]["UserPhotoUrl"]
        full_image_url = f"https://simon.sfx.vic.edu.au{user_photo_url}"
        return full_image_url

    return None


def getStudentProfileDetails(cookie):
    studentIDSimon = getStudentProfile(cookie)["d"][0]["StudentID"]

    url = "https://simon.sfx.vic.edu.au/WebModules/Profiles/Student/StudentProfiles.asmx/StudentProfileDetails"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    data = {"studentId": studentIDSimon}

    response = requests.post(url, headers=headers, json=data)

    return response.json()


def getStudentProfileBehaviouralHistory(cookie):
    unix_seconds = time.time()

    unix_milliseconds = int(unix_seconds * 1000)

    url = f"https://simon.sfx.vic.edu.au/WebServices/BehaviouralTracking.asmx/GetStudentProfileBehaviouralHistory?{unix_milliseconds}"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    profileData = getStudentProfileDetails(cookie)

    commID = profileData["d"]["UID"]
    data = {
        "communityUID": profileData["d"]["UID"],
        "selectedAcademicYearID": 0,
        "yearLevelCode": profileData["d"]["YearLevelCode"],
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


def getCalendar(cookie, date):
    url = "https://simon.sfx.vic.edu.au/Default.asmx/GetWorkdeskCalendar"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    data = {
        "startOfWeek": date,
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()


def getCommendations(cookie, GUID):
    url = f"https://simon.sfx.vic.edu.au/WebServices/BehaviouralTracking.asmx/GetWorkDeskCommendationsPaged"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    data = {
        "sort": [{"field": "CommendationDate", "dir": "desc"}],
        "filter": None,
        "userGUID": GUID,
        "startDate": "2015-02-01T13:00:00.000Z",
        "endDate": "2024-12-19T13:00:00.000Z",
        "showMyRecordsOnly": False,
        "take": 70,
        "skip": 0,
        "page": 1,
        "pageSize": 70,
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


def getTaskSubmission(cookie, classID, taskID):
    unix_seconds = time.time()

    unix_milliseconds = int(unix_seconds * 1000)

    url = f"https://simon.sfx.vic.edu.au/WebModules/LearningAreas/LearningAreas.asmx/GetStudentTaskSubmissionInfo?{unix_milliseconds}"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    data = {"classId": classID, "taskId": taskID, "inactiveClassFlag": False}

    response = requests.post(url, headers=headers, json=data)
    responsejson = response.json()

    return responsejson


def getTaskRubric(cookie, classID, taskID):
    subID = getTaskSubmission(cookie, classID, taskID)["d"]["TaskResult"][
        "SubmissionID"
    ]

    url = f"https://simon.sfx.vic.edu.au/WebModules/LearningAreas/LearningAreas.asmx/GetSubmissionMarkingRubric"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}
    data = {
        "classId": classID,
        "taskId": taskID,
        "inactiveClassFlag": False,
        "submissionID": subID,
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()


def getAssessmentReports(cookie, guid):
    url = f"https://simon.sfx.vic.edu.au/WebModules/Profiles/Student/StudentAssessment/StudentProfileStudentReportsArchive.aspx?UserGUID={guid}"
    headers = {"Content-Type": "application/json", "Cookie": f"adAuthCookie={cookie}"}

    response = requests.get(url, headers=headers)

    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    reportDivs = soup.find_all("div", class_="list-group-item clearfix")

    reports = []

    for div in reportDivs:
        aElement = div.find("a")
        spanElement = div.find("span")

        report = {
            "name": spanElement.text.strip() if spanElement else None,
            "download": aElement.get("href") if aElement else None,
        }

        reports.append(report)

    return reports



