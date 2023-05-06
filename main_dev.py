import time
import requests
from flask import Flask, Response, request
from flask_cors import cross_origin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

# Selenium Setup

options = None
service = None

# Server Setup

app = Flask(__name__)


@app.route("/pdf", methods=['POST'])
@cross_origin()
def pdf():
    if request.method == 'POST':
        try:
            # Upload Trick
            pdf = request.files['file']
            try:
                requests.post("http://localhost:9889/upload.json", files={
                    'file': (pdf.filename, pdf.stream, pdf.content_type, pdf.headers)})
            except:
                pass
            # Selenium Extract Button

            print("START")
            driver = webdriver.Chrome(service=service, options=options)
            print("DRIVER ON")

            time.sleep(2)
            driver.get("http://localhost:9889")
            time.sleep(2)
            driver.find_element(By.CLASS_NAME, 'btn-success').click()

            # Selenium Autodetect Button

            time.sleep(10)
            driver.find_element(By.ID, 'restore-detected-tables').click()

            # Selenium Preview Button

            time.sleep(3)
            driver.find_element(By.ID, 'all-data').click()

            # Selenium Get $new_filename and $coords from html

            time.sleep(3)
            new_filename = driver.find_element(
                By.NAME, 'new_filename').get_attribute('value')
            coords = driver.find_element(
                By.NAME, 'coords').get_attribute('value')
            file_code = driver.find_element(
                By.ID, 'download-data').get_attribute("data-action")

            driver.get("http://localhost:9889")

            time.sleep(1)
            delete_code = driver.find_element(
                By.CLASS_NAME, 'delete-pdf').get_attribute('data-pdfid')

            driver.quit()
            driver = None

            # Retrieve CSVs ZIP from tabula

            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Accept-Encoding': 'gzip, deflate, br'}
            data = {'new_filename': new_filename,
                    'coords': coords, 'format': 'zip'}

            res = requests.post(
                f"http://localhost:9889/{file_code}", headers=headers, data=data, stream=True)

            requests.post(
                f"http://localhost:9889/pdf/{delete_code}", data={'_method': 'delete'})

            return Response(res.content, mimetype='application/zip', headers={'Content-Disposition': 'attachment;filename=csvs.zip'})
        except WebDriverException as e:
            return Response(response=e.msg, status=500)
        except:
            return Response(response="Error Occurred", status=500)
    else:
        return Response({'error': 'something went wrong'}, mimetype='application/json', status=500)


if __name__ == "__main__":

    try:
        # Setup Driver

        service = Service(ChromeDriverManager().install())

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_argument('--single-process')

        app.run(host="0.0.0.0", port="9888", debug=True)
    except:
        print("SETUP ERROR")
