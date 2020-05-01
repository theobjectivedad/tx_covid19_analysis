#!/usr/bin/env python

from selenium import webdriver
from datetime import datetime
import time
import re
from os.path import join, exists
import pandas as pd


if __name__ == '__main__':

    # Configuration
    url = 'https://txdshs.maps.arcgis.com/apps/opsdashboard/index.html#/ed483ecd702b4298ab01e8b9cafc8b83'
    wait_time = 10

    # Crawl and parse data form page
    with webdriver.Chrome() as driver:

        print('Opening URL %s' % url)
        driver.get(url)

        print('Waiting %i seconds for page to load' % wait_time)
        time.sleep(wait_time)

        print('Scraping TxHHS')

        data = {
            'ts': datetime.now(),
            'total_tests': float(re.sub(r'[^0-9]', '', driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/margin-container/full-container/div[2]/margin-container/full-container/div/div/div/div[1]').text)),
            'currently_in_hospitals': float(re.sub(r'[^0-9]', '', driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/margin-container/full-container/div[5]/margin-container/full-container/div/div/div/div[2]').text)),
            'public_labs': float(re.sub(r'[^0-9]', '', driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/margin-container/full-container/div[3]/margin-container/full-container/div/div/div/div[1]').text)),
            'private_labs': float(re.sub(r'[^0-9]', '', driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/margin-container/full-container/div[4]/margin-container/full-container/div/div/div/div[1]').text)),
            'cases_reported': float(re.sub(r'[^0-9]', '', driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/margin-container/full-container/div[6]/margin-container/full-container/div/div/div/div[1]').text)),
            'fatalities': float(re.sub(r'[^0-9]', '', driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/margin-container/full-container/div[7]/margin-container/full-container/div/div/div/div[1]').text)),
            'updated': datetime.strptime(driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/margin-container/full-container/div[53]/margin-container/full-container/div/div/div/div[2]').text, '%m/%d/%Y %H:%M%p'),
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
