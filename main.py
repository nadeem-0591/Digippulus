from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

driver = webdriver.Chrome()
base_url = 'https://altus.search-prop.com/properties?page='
driver.implicitly_wait(10)

data_list = []

num_pages = 27

for page_number in range(1, num_pages + 1):
    url = f'{base_url}{page_number}'
    driver.get(url)

    product_elements = driver.find_elements(By.CLASS_NAME, 'col-xs-12.col-sm-6.col-md-4.flexItem.grid')

    for i in range(len(product_elements)):
        product_elements = driver.find_elements(By.CLASS_NAME, 'col-xs-12.col-sm-6.col-md-4.flexItem.grid')
        product = product_elements[i]

        try:
            product.click()
            time.sleep(2)  

            try:
                property_name = driver.find_element(By.XPATH, "//h2[@class='white']").text
            except NoSuchElementException:
                property_name = "Not available"

            try:
                property_type = driver.find_element(By.XPATH, "//td[text()='Property Type']/following-sibling::td").text
            except NoSuchElementException:
                property_type = "Not available"

            try:
                tenure = driver.find_element(By.XPATH, '//td[text()="Tenure"]/following-sibling::td').text
            except NoSuchElementException:
                tenure = "Not available"

            try:
                size = driver.find_element(By.XPATH, '//td[text()="Size"]/following-sibling::td').text
            except NoSuchElementException:
                size = "Not available"

            try:
                business_rates = driver.find_element(By.XPATH, '//td[text()="Business Rates"]/following-sibling::td').text
            except NoSuchElementException:
                business_rates = "Not available"

            try:
                relatable_value = driver.find_element(By.XPATH, '//td[text()="Rateable Value"]/following-sibling::td').text
            except NoSuchElementException:
                relatable_value = "Not available"

            try:
                service_charge = driver.find_element(By.XPATH, '//td[text()="Service Charge"]/following-sibling::td').text
            except NoSuchElementException:
                service_charge = "Not available"

            try:
                energy_performance_rating = driver.find_element(By.XPATH, '//td[text()="Energy Performance Rating"]/following-sibling::td').text
            except NoSuchElementException:
                energy_performance_rating = "Not available"

            try:
                key_features = driver.find_element(By.XPATH, '/html/body/section[2]/div/div[2]/div[1]/ul').text
            except NoSuchElementException:
                key_features = "Not available"

            try:
                additional_info = driver.find_element(By.XPATH, '//h4[text()="Key Features"]/following-sibling::p[1]').text
            except NoSuchElementException:
                additional_info = "Not available"

            try:
                location = driver.find_element(By.XPATH, '//h4[text()="Location"]/following-sibling::p[1]').text
            except NoSuchElementException:
                location = "Not available"

            try:
                area_available = driver.find_element(By.XPATH, '//div[@class="accommodation-table"]').text
            except NoSuchElementException:
                area_available = "Not available"

            try:
                terms = driver.find_element(By.XPATH, '//h4[text()="Terms"]/following-sibling::p[1]').text
            except NoSuchElementException:
                terms = "Not available"
            try:
                image_url = driver.find_element(By.XPATH, '/html/body/section[2]/div/div[2]/div[1]/div[1]/div/div/div/div/div/img').get_attribute("src")
            except NoSuchElementException:
                image_url = "Not available"

            # Extract agent details
            try:
                agent_name_elements = driver.find_elements(By.XPATH, '//div[@class="prop-team-member-deets"]//h4')
                agent_names = [agent_name.text for agent_name in agent_name_elements]
            except NoSuchElementException:
                agent_names = ["Not available"]

            try:
                agent_phone_numbers = driver.find_elements(By.XPATH, '//div[@class="prop-team-member-deets"]//p[contains(text(),"Tel:")]')
                agent_phone_numbers = [phone.text for phone in agent_phone_numbers]
            except NoSuchElementException:
                agent_phone_numbers = ["Not available"]


            data_list.append({
                "Property Name": property_name,
                "Property Type": property_type,
                "Tenure": tenure,
                "Size": size,
                "Business Rates": business_rates,
                "Relatable Value": relatable_value,
                "Service Charge": service_charge,
                "Energy Performance Rating": energy_performance_rating,
                "Key Features": key_features,
                "Additional Info": additional_info,
                "Location": location,
                "Area Available": area_available,
                "Terms": terms,
                "Image URL": image_url,
                "Agent Names": agent_names,
                "Agent Phone Numbers": agent_phone_numbers
            })

            driver.back()
        except Exception as e:

            print(f"Error processing product {i + 1} on page {page_number}: {str(e)}")


df = pd.DataFrame(data_list)

df.to_csv('property_data.csv', index=False)

print(df)

driver.quit()
