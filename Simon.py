import requests
import os, time

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

