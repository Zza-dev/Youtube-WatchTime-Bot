from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import time
import sys
import concurrent.futures
import scrapetube
import random
import pyautogui

path = '_list.txt'

class Logger:
 
    def __init__(self, filename):
        self.console = sys.stdout
        self.file = open(filename, 'w', encoding='utf-8')
 
    def write(self, message):
        self.console.write(message)
        self.file.write(message)
 
    def flush(self):
        self.console.flush()
        self.file.flush()

sys.stdout = Logger(path)

channel_id_input = "ENTER CHANNEL ID"
channel_id = channel_id_input.strip("https://www.youtube.com/channel/")

videos = scrapetube.get_channel(channel_id)
urls = []
for video in videos:
    container = video['title']
    title_dict = container["runs"]
    title_dict2 = title_dict[0]
    title = title_dict2["text"]
    # print("https://www.youtube.com/watch?v="+str(video['videoId'])+"--"+str(title))
    urls.insert(1, "https://www.youtube.com/watch?v="+str(video['videoId']))

total_urls = len(urls)
proxies=[]
try:
    with open('proxy-list.txt', 'r') as f:
        proxies=f.readlines()
        print("Lista adaugata")
except:
    print('[EROARE]\t"proxy-list.txt" nu a fost gasit !!')
    exit()
print('[***]\tTotal Proxi-uri :',len(proxies))

def getViews(proxy):
    options = ChromeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option('detach', True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--proxy-server=%s' %proxy)
    options.add_argument('--window-size=640,480')
    print("Videoclipuri pe canal: "+str(len(urls)))
    try:
        while True:
            random_number = random.randint(1, total_urls - 1)
            url, duration = str(urls[random_number]), 120
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            print("Pagina a fost deschisa cu succes")
            time.sleep(9)
            player_container = driver.find_element_by_id('player')
            print("Playerul a aparut")
            player_container_size = player_container.size
            player_container_location = player_container.location
            player_x = player_container_location['x'] + player_container_size['width'] // 2
            player_y = player_container_location['y'] + player_container_size['height'] // 2
            
            actions = ActionChains(driver)
            actions.move_to_element(player_container).click().perform()
            actions.send_keys(Keys.SPACE).perform()
            # driver.execute_script("document.getElementById('player').playVideo();")
            print("Video Pornit")
            time.sleep(duration)
        
    except Exception as e:
        print("EROARE: "+ e)
        traceback.print_exc()  # Print the full exception traceback
        driver.quit()

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(getViews, proxies)


