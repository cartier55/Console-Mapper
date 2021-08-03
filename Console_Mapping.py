import selenium
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.keys import Keys
import requests
import re
import argparse
from types import SimpleNamespace

# url = "https://calo-new.cisco.com/#/tools/start_here"
login = {
    "username":"Carjames",
    "password":"cJ24549bdedibdedi24549?"
}


TEST_DEVICE = "02B3ABE"
PATH = "C:\Program Files (x86)\chromedriver.exe"
OT6 = "https://calo-new.cisco.com/#/tools/start_here"
GOOGLE = "https://www.google.com/"

soup = ''
with open("Calo_Login.html") as html:
    soup = BeautifulSoup(html, "html.parser")
inputs = soup.select('input.form-control')


parser = argparse.ArgumentParser(description='''
Console Mapper.py

Automates cisco OT6 device mapping process
''')
parser.add_argument('file', type=str, help="Formated file of itms#, location, and port#")
parser.add_argument('-C', default=False, action='store_true', help="Flag to check COMM ports against file")
args = parser.parse_args()
# driver = webdriver.Chrome(PATH)


filename = args.file
with open(filename, 'r+') as f:
    file = f.read()
location_regex = re.compile(r'(LAB:)(.*)', re.I)
itms_regex = re.compile(r'[a-z0-9]{7}', re.I)
port_regex = re.compile(r'\[[0-9]+\]')

pod = {'devices':dict(),'comm_ports':dict()}
pod = SimpleNamespace(**pod)

devices = re.findall(itms_regex, file)
ports = re.findall(port_regex, file)
lab = re.search(location_regex, file)

pod.devices = dict(zip(devices, ports))
pod.lab = lab.group(2)
print(pod.devices)
# login()
for d, i in pod.devices.items():
    print(pod.lab)
    print(d, i)
    search({'lab':})

def main():
    """
    1)Read in ConsoleMap.txt files with ITMS#, Location Info, Port#
    2)Start console mapping process for ever device in ConsoleMap.txt by sending varibale obj to login()
    """
        # search()
    
    ...


def login():
    """
    Login to calo OT6 page
    
    driver = webdriver.Firefox(PATH)
    driver = webdriver.Edge(PATH)
    """
    driver.get(OT6)
    print(driver.title)
    sleep(5)
    userb = driver.find_element_by_name("username")
    passb = driver.find_element_by_name("password")
    userb.send_keys(login['username'])
    passb.send_keys(login['password'])
    driver.find_element_by_css_selector('div.clearfix > button.width-35').click()
    return

def search():
    """
    Select Quick Find serach bar enter first device itms# and search
    """
    sleep(5)
    quick_search = driver.find_element_by_id('nav-search-input')
    quick_search.send_keys(TEST_DEVICE)
    quick_search.send_keys(Keys.RETURN)
    curComm()

def curComm():
    """
    Find the current telnet console address
    """
    sleep(5)
    telnet_comm = driver.find_element_by_css_selector('a[href*="telnet"]')
    print(telnet_comm.text)


def accessMeth():
    """
    Go to access methods page to change console port
    """
    url = re.split('/(?=[a-zA-z0-9#])',driver.current_url ) #Split the url so the slashs are removed
    url[-2] = 'access_methods'
    driver.get('/'.join(url))

def formEntry():
    """
    Find form entry 1 for console access port inside of form_area table body
    """
    sleep(5)
    form_entry_1 = ''
    form_entries = driver.find_elements_by_css_selector('tbody[id$="form_area"] > tr[id*="form_entry"]') #Find the tr entries for the form_area table 
    for i in form_entries:
        if i.get_attribute('id') == "1_form_entry":
            form_entry_1 = i

    # Find td with console addresse inside form entry 1
    form_data = form_entry_1.find_elements_by_css_selector('td > input.form-control')

    #Find Current Console addresse
    try:
        cur_console = form_data[-1].get_attribute('value')
        print(cur_console) #Prints the current console addresse
    except:
        print('[-]No Console Port')

#Change the console address
# form_data[1].clear() #Clears the console address form td
# form_data[1].send_keys('hello console world') #Enters data for the console addresse

#Save Console Addresse Changes
# submit_console = driver.find_element_by_css_selector('center > button.btn-white')
# print(submit_console.get_attribute("outerHTML"))
# submit_console.click()

