import os
import time
import html
import requests
import lxml
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from selenium import webdriver
from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format

NAVER_IMAGE = \
    'https://search.naver.com/search.naver?where=image&sm=tab_jum&'

# usr_agent = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#     'Accept-Encoding': 'none',
#     'Accept-Language': 'ko-KR',
#     'Connection': 'keep-alive',
# }

DEST_IMAGES = 'images'

def main():
    if not os.path.exists(DEST_IMAGES):
        os.mkdir(DEST_IMAGES)
    download_images()
    
def download_images():

    init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
    cprint(figlet_format('NAVER', font='rectangles'), 'green', attrs=['bold'])
    cprint(figlet_format('Image Scraper', font='larry3d'), 'green', attrs=['bold'])
    print("Developed by: Peter Hyunseok Jang (www.hsjang.com)\n")
    print("This software is licenced under GNU GPL.\n")
    print("Copyright: All rights reserved.\n")
    print("All images are copyright to their respective owners and \nare protected under international copyright laws.\n")
    # Ask user for search topic (사용자에게 검색 주제를 요청)
    print("**************************************************************************\n")
    data = input('What are you looking for? Please replace spaces with "+" instead.\n무엇을 찾고 있습니까? 공백 대신 "+"를 사용하십시오.\n\n')
    # Ask user for quantity (수량 요청)
    print("\n**************************************************************************\n")
    numberOfImages = int(input('How many images do you want?\n이미지 몇 장을 원하십니까?\n\n'))

    # Status
    print("\n*******************************\n")
    print('Searching...')
    print("*******************************\n")

    # Fetch URL + Manipulation (URL 가져 오기)
    url = NAVER_IMAGE + 'query=' + data
    print(url)
    urlRequest = requests.get(url)

    # Selenium
    # New Chrome session
    driver = webdriver.Chrome(executable_path = "C:\webdrivers\chromedriver.exe")
    driver.get(url) # open NAVER Images (url)
    driver.maximize_window() # maximize screen

    if (numberOfImages <= 50):
        naver_scroll_delay_mechanism = 2
    elif (numberOfImages <= 100):
        naver_scroll_delay_mechanism = 8
    else:
        naver_scroll_delay_mechanism = 60

    # Selenium: scroll to bottom of page (NAVER structure)
    t_end = time.time() + naver_scroll_delay_mechanism # seconds
    while time.time() < t_end:
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")

    # Web Crawl using Soup
    soup = BeautifulSoup(driver.page_source, "lxml")
    results = soup.findAll('a', {'class': 'thumb _thumb'}, limit = numberOfImages)
    
    # Obtain image data source links and put them into a list (이미지 데이터 소스 링크를 가져 와서 목록에 추가)
    imagelinks= [] # data source links (main database)
    for result in results:
        strParse = str(result)
        print(strParse)
        print(strParse.find("src="))
        print(strParse.find(" ", strParse.find("src=")))
        link = ""

        # URL manipulation
        for i in range(strParse.find("src=")+len("src=") + 1, strParse.find(" ", strParse.find("src=")) -1):
            link = link + strParse[i]
        imagelinks.append(link)
        print(imagelinks)

    # Display results (결과 표시)
    print(f'found {len(imagelinks)} images')

    # Status
    print('Download Starting... 다운로드 시작중...')

    # Download images from the "database" ("데이터베이스"에서 이미지 다운로드)
    for i, imagelink in enumerate(imagelinks):
        # Open and Save image (이미지 열기 및 저장)
        response = requests.get(imagelink)
        # File name and folder setup (파일 이름 및 폴더 설정)
        imagename = DEST_IMAGES + '/' + data + str(i+1) + '.jpg'
        
        for i in tqdm(range(1, 5), desc ="Downloading image" + ' ' + str(i + 1)): 
            with open(imagename, 'wb') as file:
                file.write(response.content)
            sleep(.1) 
        print("\n")            
    # Status
    print("Finished downloading" + ' ' + str(numberOfImages) + ' ' + "image(s) from NAVER.")
    
# Run only in Python (cmd/run)
if __name__ == '__main__':
    main()