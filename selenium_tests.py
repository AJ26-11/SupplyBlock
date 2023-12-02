import unittest
from selenium import webdriver
import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CoffeeChainSeleniumTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_add_batch(self):
        driver = self.driver
        driver.get("http://localhost:8000/blockchain/add/")
        unique_batch_id = "TestBatch" + str(uuid.uuid4())[:8]

        # Fill out the add batch form
        batch_id_input = driver.find_element(By.ID, "batchId")
        farm_name_input = driver.find_element(By.ID, "farmName")
        origin_country_input = driver.find_element(By.ID, "originCountry")
        harvest_date_input = driver.find_element(By.ID, "harvestDate")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        batch_id_input.send_keys(unique_batch_id)
        farm_name_input.send_keys("Test Farm")
        origin_country_input.send_keys("Test Country")
        harvest_date_input.send_keys("2023-01-01")
        submit_button.click()

        # Check for success page
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[@class='title' and contains(text(),'Transaction Successful')]"))
        )

    def test_view_batch(self):
        driver = self.driver
        driver.get("http://localhost:8000/blockchain/view/")

        batch_id_input = driver.find_element(By.ID, "batchId")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        batch_id_input.send_keys("TestBatch01")
        submit_button.click()

        # Check for details display
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(),'Details for Batch ID:')]")))

    def test_update_batch(self):
        driver = self.driver
        driver.get("http://localhost:8000/blockchain/update/")

        batch_id_input = driver.find_element(By.ID, "batchId")
        processing_details_input = driver.find_element(By.ID, "processingDetails")
        roasting_date_input = driver.find_element(By.ID, "roastingDate")
        packaging_details_input = driver.find_element(By.ID, "packagingDetails")
        packaging_date_input = driver.find_element(By.ID, "packagingDate")
        is_shipped_checkbox = driver.find_element(By.ID, "isShipped")
        is_delivered_checkbox = driver.find_element(By.ID, "isDelivered")
        current_location_input = driver.find_element(By.ID, "currentLocation")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        batch_id_input.send_keys("TestBatch01")
        processing_details_input.send_keys("Updated Processing Details")
        roasting_date_input.send_keys("2023-02-01")
        packaging_details_input.send_keys("Updated Packaging Details")
        packaging_date_input.send_keys("2023-03-01")
        is_shipped_checkbox.click()
        is_delivered_checkbox.click()
        current_location_input.send_keys("Updated Location")
        submit_button.click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[@class='title' and contains(text(),'Transaction Successful')]"))
        )

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
