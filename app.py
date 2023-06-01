from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException

from urllib.parse import quote

import time

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def visit_links(url, parent_id=None, depth=0, max_depth=5):
    data = {
        'id': parent_id,
        'children': []
    }

    if depth >= max_depth:
        return data

    chrome_options = webdriver.ChromeOptions()
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")  # set window size
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")


    driver = webdriver.Chrome(executable_path=r'/path/to/chromedriver', options=chrome_options) 
    driver.maximize_window()
    driver.get(url)

    for attempt in range(5):
        try:
            time.sleep(2)
            continuity_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'link_app-data-continuity')))
            continuity_button.click()
            time.sleep(2)
            break
        except TimeoutException:
            if attempt < 4:
                driver.refresh()
            else:
                raise

    links = driver.find_elements(By.XPATH, "//h4[text()='Child data']/following::a[@id='link_continuity-child-childAppTxt']")

    for i in range(len(links)):
        links = driver.find_elements(By.XPATH, "//h4[text()='Child data']/following::a[@id='link_continuity-child-childAppTxt']")
        link = links[i]
        parent = link.find_element(By.XPATH, '..') 
        try:
            next_6_td_elements = parent.find_elements(By.XPATH, './following-sibling::td')
            child_data = {
                'id': link.text,
                'details': [td.text for td in next_6_td_elements],
                'children': []
            }

            child_application_number = quote(link.text, safe='')
            child_url = 'https://patentcenter.uspto.gov/applications/' + child_application_number

            
            child_data['children'] = visit_links(child_url, parent_id=child_data['id'], depth=depth + 1, max_depth=max_depth)['children']
            data['children'].append(child_data)
        except Exception as e:
            print(f"Unable to visit child page for {link.text}. Error: {str(e)}")

    driver.quit()

    return data


@app.route('/get_data/<application_number>')
def get_data(application_number):
    max_depth = request.args.get('max_depth', 5, type=int)
    url = f'https://patentcenter.uspto.gov/applications/{application_number}'
    data = visit_links(url, parent_id=application_number, max_depth=max_depth)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
