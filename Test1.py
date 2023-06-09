import os
import playsound
import speech_recognition as sr
import time
import sys
import calendar
import ctypes
import wikipedia
import wolframalpha
import datetime
from tkinter import *
from tkinter import ttk
import json
from googletrans import Translator 
import re
import webbrowser  as wb
import smtplib
import requests
import urllib
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch
language = 'vi'
wikipedia.set_lang('vi')


def speak(text):
    print("Bot: {}".format(text))
    tts = gTTS(text=text, lang=language, slow = False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", False)
    os.remove("sound.mp3")

def get_voice():
     r = sr.Recognizer()
     with sr.Microphone() as source:
        speak("Bạn nói!")
        time.sleep(1)
        print("Tôi: ", end = '')
        audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text
        except:
            print("...")
            return 0
    
def stop():
    speak("Đã thoát chương trình. Hẹn gặp lại bạn nhé!")
    time.sleep(3)

def get_text():
    for i in range(5):
        text = get_voice()
        if text:
            return text.lower()
        elif i < 2:
            speak("Bot không nghe rõ, hãy nói lại?")
            time.sleep(3)
    stop()
    return 0

def open_website(text):
    regex = re.search ('mở (.+)', text)
    if regex: 
        domain = regex.group(1)
        url = 'https://www.' + domain
        wb.open(url)
        speak("Trang web bạn đã được mở lên")
        time.sleep(3)
        return True
    else:
         return False
    
def google_search(text):
    speak("Bạn muốn tìm kiếm thứ gì?")
    time.sleep(2)
    giong = get_text()
    time.sleep(2)
    url = f"https://google.com/search?q={giong}"
    wb.get().open(url)
    speak(f"Đã tìm thấy {giong} trên google")
    time.sleep(5)

def print_calendar():
    speak("Nhập năm và tháng?")
    time.sleep(2)
    speak("Nhập năm: ")
    nam = int(input())
    time.sleep(2)
    speak("Nhập tháng: ")
    time.sleep(2)
    thang = int(input())
    time.sleep(2)
    print(calendar.month(nam, thang))
    speak("Đã in lịch ra: ")
    time.sleep(3)

def get_time(text):
    now = datetime.datetime.now()
    time.sleep(2)
    if "giờ" in text:
        speak("Bây giờ là %d giờ %d phút" % (now.hour, now.minute))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d " % (now.day, now.month, now.year))
        time.sleep(2)
    else:
        speak("Bot không hiểu")

def play_youtube():
    speak("Xin mời bạn chọn bài hát")
    time.sleep(3)
    my_song = get_text()
    while True:
        result = YoutubeSearch(my_song, max_results = 10).to_dict()
        if result:
            break;
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    wb.open(url)
    speak("Bài hát của bạn đã được mở, hãy thưởng thức nó!")
    time.sleep(5)

def weather():
    speak("Bạn muốn xem thời tiết ở đâu!")
    time.sleep(3)
    url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temp = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        sun_time  = data["sys"]
        sun_rise = datetime.datetime.fromtimestamp(sun_time["sunrise"])
        sun_set = datetime.datetime.fromtimestamp(sun_time["sunset"])
        wther = data["weather"]
        weather_des = wther[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day, month = now.month, year= now.year, hourrise = sun_rise.hour, minrise = sun_rise.minute,
                                                                           hourset = sun_set.hour, minset = sun_set.minute, 
                                                                           temp = current_temp, pressure = current_pressure, humidity = current_humidity)
        speak(content)
        time.sleep(25)
    else:
        speak("Không tìm thấy thành phố!")


def dichTiengAnh():
        speak("Bạn hãy đọc từ khóa cần dịch")
        time.sleep(3)
        tiengAnh = get_text()
        url = "https://translate.google.com/?hl=vi&sl=vi&tl=en&text=" + tiengAnh
        wb.open(url)
        speak("Đã dịch từ khóa trên google")
        time.sleep(6)

# Mở ứng dụng trong máy tính
def open_application(text):
    if "google" in text:
        speak("Mở Google Chrome")
        os.startfile('C:\Program Files\Google\Chrome\Application\chrome.exe')
        time.sleep(1)
    elif "visual studio code" in text:
        speak("Mở Visual VS Code")
        os.startfile('D:\Microsoft VS Code\Code.exe')
        time.sleep(1)
    else: 
        speak("Phần mềm chưa cài đặt?")

def tell_me():
    try:
        speak("Bạn muốn nghe về gì!")
        time.sleep(2)
        text = get_text()
        contents = wikipedia.summary(text).split('.')
        speak(contents[0])
        time.sleep(20)
        for content in contents[1:]:
            speak("Bạn muốn nghe tiếp hay không ?")
            time.sleep(3)
            ans = get_text()
            if "không" in ans:
                speak("Cảm ơn bạn đã lắng nghe!")
                time.sleep(3)
                break
            elif "có" in ans:
                speak(content)
                time.sleep(20)
    except:
        speak("Bot không định nghĩa được ngôn ngữ của bạn!")
        time.sleep(4)

def help():
    speak("""Tôi có thể làm những việc sau:
    1. Tìm kiếm thông tin trên Wikipedia
    2. Hiển thị giờ, ngày
    3. Mở website, application
    4. Tìm kiếm trên Google
    5. Mở nhạc Youtube
    6. Dự báo thời tiết
    7. Mở lịch Việt Nam trên Youtube
    8. Nhập năm và nhập tháng xem có bao nhiêu ngày
    9. Đọc thời tiết hôm nay
    10. Dịch tiếng Anh trên Trang Website Google
    11. Đọc thời gian hiện thại (sáng, chiều, tối)
     """)
    time.sleep(20)

def docBuoi():
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng. Chúc bạn ngày mới tốt làm")
    elif day_time < 18:
        speak("Bây giờ là buổi chiều")
    else: 
        speak("Bây giờ là buổi tối")
    time.sleep(3)

def maytinh():
    speak("Bạn muốn tính bao nhiêu?")
    time.sleep(2)
    try:
        speak("Nhập biểu thức của bạn vào đây!")
        x = input("==> ")
        speak("Kết quả là: ")
        time.sleep(1)
        speak(str(eval(x)))
        time.sleep(3)
    except:
        speak("Kết quả này không tính được!")

def dichTieng():
    translator = Translator()
    speak("Mời bạn nói từ cần dịch")
    time.sleep(3)
    text = get_text()
    translated = translator.translate(text, dest = "en")
    # speak(translated)
    time.sleep(1)
    speak(translated.text)
    time.sleep(3)

def my():
    client = wolframalpha.Client('T3453J-TXHKYVJHU7')
    speak('Đọc số:') 
    time.sleep(1)
    query = str(get_text())
    time.sleep(2)
    res = client.query(query)
    out = next(res.results).text
    speak(out) 
    time.sleep(2)


def xemLichVietNam():
    url = "https://www.informatik.uni-leipzig.de/~duc/amlich/"
    wb.open(url)
    speak("Đã chuyển trang xem lịch Việt Nam")
    time.sleep(6)
    
def call_sen():
    speak("Bạn muốn giúp gì?!")
    time.sleep(1)
    while True:
        text = get_text()
        if not text:
            break
        elif "thôi" in text or "dừng" in text or "thoát" in text or "tắt" in text or "off" in text:
            stop()
            break
        elif "mở" in text:
            if "mở google và tìm kiếm" in text or "mở google tìm kiếm" in text or  "mở thông tin trên google" in text:
                google_search(text)
            elif "." in text:
                open_website(text)
            elif "mở ứng dụng google" in text:
                open_application(text)       
        elif "ngày" in text  or "giờ" in text:
            get_time(text)
            time.sleep(2)
        elif "youtube" in text:
            play_youtube()
            time.sleep(2)
        elif "thời tiết" in text:
            weather()
        elif "tìm định nghĩa" in text or "wikipedia" in text:
            tell_me()
        elif "có thể làm gì" in text or "chức năng của bạn" in text or "chức năng" in text:
            help()
        elif "stranslate" in text:
            dichTiengAnh() 
        elif "dịch tiếng" in text or "google dịch" in text:
            dichTieng()   
        elif "xem lịch trên google" in text or "xem lịch" in text:
            xemLichVietNam()  
        elif "nhập lịch" in text or "in lịch" in text:
            print_calendar()     
        elif "tính toán" in text or "phép toán" in text:
            maytinh()
        elif "buổi nào" in text or "xem buổi" in text:
            docBuoi() 
        elif "đọc máy tính" in text or "máy tính" in text:
            my() 

# call_sen()
# 

root = Tk()
root.geometry('1100x520')
root.resizable(0, 0)
# root.iconbitmap('logo hehehe')
root['bg'] = 'skyblue'
root.title('Trợ lý ảo ma')
Label(root, text="Trợ lý ảo! ", font="Arial 20 bold").pack()

Label(root, text="Khả năng của tôi nè!", font="Arial 13", bg = "white smoke").place(x=165, y=90)
Label(root, text="Tìm kiếm thông tin trên Wikipedia", font="Arial 13", bg = "white smoke").place(x=165, y=150)
Label(root, text="Hiển thị giờ ngày", font="Arial 13", bg = "white smoke").place(x=165, y=180)
Label(root, text="Mở website, application", font="Arial 13", bg = "white smoke").place(x=165, y=210)
Label(root, text="Tìm kiếm thông tin trên Google", font="Arial 13", bg = "white smoke").place(x=165, y=240)
Label(root, text="Mở nhạc Youtube", font="Arial 13", bg = "white smoke").place(x=165, y=270)
Label(root, text="Dự báo thời tiết", font="Arial 13", bg = "white smoke").place(x=165, y=300)
Label(root, text="Mở lịch Việt Nam trên Youtube", font="Arial 13", bg = "white smoke").place(x=165, y=330)
Label(root, text="Đọc thời tiết hôm nay", font="Arial 13", bg = "white smoke").place(x=165, y=360)
Label(root, text="Đọc thời gian hiện tại (sáng, chiều, tối)", font="Arial 13", bg = "white smoke").place(x=165, y=390)
Label(root, text="tính toán", font="Arial 13", bg = "white smoke").place(x=165, y=420)

main = Button(root, text = 'Đánh thức quỷ đỏ', font="Arial 13 bold", pady = 5, command = call_sen, bg = 'red', activebackground = 'green')
main.place(x = 475, y = 180 )

Label(root, text="Kết quả ở đâyyyy!", font="Arial 13 bold", bg = "white smoke").place(x=780, y=90)
Output_text = Text(root, font = "Arial 10 bold", height = 11, wrap = WORD, padx = 5, pady = 5, width = 50)
Output_text.place(x = 700, y = 130)

root.mainloop()
# 
    
# SVM
# tim duong sao cho dien gan nhat duong thang do la xa nhat
# Khong tim thay duong thang trong mat phang nay thi se tim trong mat phang nhieu chieu

# Tree decision Chia de tri
# Bieu dien tren oxy xet chan giua

# KNN
# Tim tam sau do tu tam ve den ban kinh tiep theo do diem vs tam thang nao gan nhat lay nhe may ba

# SOM G m thi den (ve cac diem thanh cac cac mang luoi)
# ve cac diem thanh mang luoi sau do do khoang cach dien vs cac diem trong mang luoi

# PCA 
# Bai toan khong giai duoc tren nhieu chieu thi se giai o duoc it chieu hon
# ve duong thang chieu cac diem vuong goc xuong duong thang roi phan chia

#python -m PyInstaller --onefile TroLyAo.py