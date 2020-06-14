#!/usr/bin/env python

from selenium import webdriver
from datetime import datetime
import time
import re
from os.path import join, exists
import pandas as pd
import numpy as np


if __name__ == '__main__':

    # Configuration
    url = 'https://txdshs.maps.arcgis.com/apps/opsdashboard/index.html#/ed483ecd702b4298ab01e8b9cafc8b83'
    wait_time = 10


    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("--remote-debugging-port=9222")


    # Crawl and parse data form page
    with webdriver.Chrome(options=options) as driver:

        print('Opening URL %s' % url)
        driver.get(url)

        print('Waiting %i seconds for page to load' % wait_time)
        time.sleep(wait_time)

        print('Scraping TxHHS')

        total_tests_path = '/html/body/div/div/div/div/div/div/margin-container/full-container/div[2]/margin-container/full-container/div/div/div/div[2]'
        cases_reported_path = '/html/body/div/div/div/div/div/div/margin-container/full-container/div[5]/margin-container/full-container/div/div/div/div[1]'
        fatalities_path = '/html/body/div/div/div/div/div/div/margin-container/full-container/div[7]/margin-container/full-container/div/div/div/div[1]'
        updated_path = '/html/body/div/div/div/div/div/div/margin-container/full-container/div[45]/margin-container/full-container/div/div/div/div[2]'

        data = {
            'ts': datetime.now(),
            'total_tests': float(re.sub(r'[^0-9]', '', driver.find_element_by_xpath(total_tests_path).text)),
            'currently_in_hospitals': -1,
            'public_labs': -1,
            'private_labs': -1,
            'cases_reported': float(re.sub(r'[^0-9]', '', driver.find_element_by_xpath(cases_reported_path).text)),
            'fatalities': float(re.sub(r'[^0-9]', '', driver.find_element_by_xpath(fatalities_path).text)),
            'updated': datetime.strptime(driver.find_element_by_xpath(updated_path).text, '%m/%d/%Y %H:%M%p'),
        }

        print(data)

    # Determine output path
    data_base = 'data'
    file_name = data['updated'].strftime('%Y-%m-%d') + '.csv'
    output_path = join(data_base, file_name)

    if exists(output_path):
        raise ValueError('File %s already exists' % output_path)

    # Save file
    print('Writing to %s' % output_path)
    df = pd.DataFrame([data])
    df.to_csv(output_path, index=True)

    print('ending')
