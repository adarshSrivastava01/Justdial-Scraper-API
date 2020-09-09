from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import flask
import os
from flask import request
from flask_cors import CORS
from flask import jsonify as json

app = flask.Flask(__name__)
app_setting = os.getenv("APP_SETTINGS")
app.config.from_object(app_setting)
CORS(app)
app.config["DEBUG"] = True

chrome_driver_path = 'C:\\Users\\lenovo\\Downloads\\chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
userAgent = 'Safari/537.36'
chrome_options.add_argument('user-agent=Safari/537.36')
driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver_path)

def remove(string):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', string)

class Scraper:
    def __init__(self):
        pass

    def returnData(self, city, location):
        objectArray = []

        driver.get(f'https://www.justdial.com/{city}/{location}')

        for i in range(20):
            time.sleep(2)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        time.sleep(10)

        try:
            driver.find_element_by_class_name('jcl').click()
            time.sleep(10)
        except:
            pass

        elem = driver.find_element_by_xpath("//*")
        source_code = elem.get_attribute("innerHTML")

        soup = BeautifulSoup(source_code, "lxml")

        for divs in soup.find_all('div', class_='col-sm-5 col-xs-8 store-details sp-detail paddingR0'):
            try:
                name = divs.h2.span.a.span.text
                rating = divs.p.a.find('span', class_='green-box').text
                votes = remove(divs.p.a.find('span', class_='rt_count lng_vote').text)
                address = divs.find('p', class_='address-info tme_adrssec').span.a.find(
                    'span', class_='mrehover dn').find('span', class_='cont_fl_addr').text
                eachObject = {
                    "name": name,
                    "rating": rating,
                    "votes": votes,
                    "address": address,
                }
                objectArray.append(eachObject)
            except:
                continue
        
        return {
            "data": objectArray,
        }

@app.route("/", methods = ["GET"])
def home():
    return json({"data": "This is the Home Page designed by Adarsh Srivastava. Follow Github www.github.com/adarshSrivastava01 for more."})

@app.route("/takeData", methods=["GET"])
def info():
    obj = Scraper()
    output = {}
    try:
        city = request.args.get("city")
        location = request.args.get("location")
        output = json(obj.returnData(city, location))
    except:
        output = {"data": "Some Error Occured."}
    return output

@app.route("/bye", methods=["GET"])
def bye():
    return json({"bye": 404})

if __name__ == "__main__":
    app.run()