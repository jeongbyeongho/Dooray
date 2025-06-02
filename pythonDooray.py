import requests
import json
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

# requests.get("https://api.gov-dooray.com")
requests.get("https://api.dooray.com")

sleep(10)
user = "id"
password = "pw"

driver = webdriver.Chrome()
driver.get("http://test.help.or.kr/login.aspx")

elem = driver.find_element("id","txtUserID")
elem.send_keys(user)
elem = driver.find_element("id","txtPassword")
elem.send_keys(password)
elem.send_keys(Keys.RETURN)
sleep(2)
title="test help : "
path = "D:\\test_helps\\"
filename = "history.txt"
filepath = path+filename

while True:
    print("Update")
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Failed to create folder")

    try:
        if not os.path.isfile(filepath):
            f=open(filepath,"w")
            f.close()

       # with open(filepath,"w") as f:
       #     f.write()
            
    except OSError:
        print("Failed to create file.")
    
    page_source = driver.page_source 
    soup = BeautifulSoup(page_source, "html.parser")
    contents = soup.select("#rptBoard_ctl00_hlkBoardView > b")
    if contents != []:
        testhref = driver.find_element("id","rptBoard_ctl00_hlkBoardView")
        href = testhref.get_attribute('href')
        
        contents_name = str(contents)
        contents_front = contents_name[4:]
        submit_title = contents_front[:-5]

        state = soup.select('#contentBody > div.section > div > table > tbody > tr:nth-child(1) > td:nth-child(7)')
        state_str = str(state)
        state_front = state_str[-10:]
        state_complete = state_front[:-6]
        
        with open(filepath,'r') as before_file:        
            size = os.path.getsize(filepath)
            if size == 0:
                print('The text file is empty. Replace with the first item.')
                with open(filepath,'w') as f:
                    f.write(str(submit_title))
                    
            before_contents = before_file.readline()
            print("before : ", before_contents)        
            print("Updated Comparison Values : ", submit_title)
            print("Update Time", )
            
        if submit_title == before_contents:
            time_duration = 240
            time.sleep(time_duration)
            print("Update!")
        elif submit_title != before_contents and state_complete =='complete':
            print("It's a new post that's been processed.", submit_title)
            with open(filepath,'w') as f:
                f.write(str(submit_title))                
            continue
        elif submit_title != before_contents and state_complete !='complete':
            print("New post", submit_title)
            with open(filepath,'w') as f:
                f.write(str(submit_title))                
            
            # 1:1 message
            # datas = {"text" :str(submit_title)+'\n'+str(href), "organizationMemberId": "value"} 
            # chatting room
            datas = {"text" :str(submit_title)+'\n'+str(href)}
            json_data = json.dumps(datas,default=str,ensure_ascii=False)


            print(type(submit_title))
            headers = {}
            headers.setdefault('Content-Type','application/json')
            headers.setdefault('Authorization','dooray-api api key')        
            
            chattingRoomID =  'room id' # room ID
            # direct-send
			# url = 'https://api.dooray.com/messenger/v1/channels/direct-send'
            
            # chattingRoom
			url = 'https://api.dooray.com/messenger/v1/channels/'+chattingRoomID+'/logs'        
                        
            try:            
                requestData = requests.post(url,json=datas,headers=headers)
            except Exception as e:
                print(e);
                
    else:
        print('No request')
        sleep(120)

