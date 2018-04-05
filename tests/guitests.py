import unittest

from flask_testing import LiveServerTestCase
from selenium import webdriver

from idb import create_app

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FirefoxTestCase(LiveServerTestCase):

    def create_app(self):
        app = create_app("__test__")
        print(app.instance_path)
        print(app.root_path)
        print(app.template_folder)
        return app

    def setUp(self):

        options = Options()
        options.add_argument('--port=5000')
        options.log.level = 'debug'
        self.driver = Firefox(options=options)
        self.driver.implicitly_wait(10)
        self.driver.get(self.get_server_url())

    def tearDown(self):
        self.driver.close()

    # Test that all navbar links are functional
    def test_navbar_links(self):
        driver = self.driver
        self.assertIn("Let's Get Fit", driver.title)

        foods_link = driver.find_element_by_link_text('Foods')
        foods_link.click()
        self.assertIn("CKC - Foods", driver.title)

        workouts_link = driver.find_element_by_link_text('Workouts')
        workouts_link.click()
        self.assertIn("CKC - Workouts", driver.title)

        gyms_link = driver.find_element_by_link_text('Gyms')
        gyms_link.click()
        self.assertIn("CKC - Gyms", driver.title)

        stores_link = driver.find_element_by_link_text('Stores')
        stores_link.click()
        self.assertIn("CKC - Stores", driver.title)

        about_link = driver.find_element_by_link_text('About')
        about_link.click()

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.title_is(('About Us')))
        self.assertIn("About Us", driver.title)

    # Test that food grid card title links lead to the correct instance that displays the name properly
    def test_food_grid_links(self):
        driver = self.driver
        driver.find_element_by_link_text('Foods').click()

        self.assertIn("CKC - Foods", driver.title)  # Adding to make it wait

        food_item = driver.find_element_by_class_name('card-title')
        food_name = food_item.text
        food_item.click()

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.title_is((food_name)))
        self.assertEqual(food_name, driver.find_element_by_tag_name('h1').text)

    # Test that workout grid card title links lead to the correct instance that displays the name properly
    def test_workout_grid_links(self):
        driver = self.driver
        driver.find_element_by_link_text('Workouts').click()

        self.assertIn("CKC - Workouts", driver.title)
        workout_item = driver.find_element_by_class_name('card-title')
        workout_name = workout_item.text
        workout_item.click()

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.title_is((workout_name)))
        self.assertEqual(workout_name, driver.find_element_by_tag_name('h1').text)

    # Test that gym grid card title links lead to the correct instance that displays the name properly
    def test_gym_grid_links(self):
        driver = self.driver
        driver.find_element_by_link_text('Gyms').click()

        self.assertIn("CKC - Gyms", driver.title)
        gym_item = driver.find_element_by_class_name('card-title')
        gym_name = gym_item.text
        gym_item.click()

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.title_is((gym_name)))
        self.assertEqual(gym_name, driver.find_element_by_tag_name('h1').text)

    # Test that store grid card title links lead to the correct instance that displays the name properly
    def test_store_grid_links(self):
        driver = self.driver
        driver.find_element_by_link_text('Stores').click()

        self.assertIn("CKC - Stores", driver.title)
        store_item = driver.find_element_by_class_name('card-title')
        store_name = store_item.text
        store_item.click()

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.title_is((store_name)))
        self.assertEqual(store_name, driver.find_element_by_tag_name('h1').text)

    # Test that going back and forth in the navigation history doesn't break the website
    def test_navigation_history(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        driver.find_element_by_link_text('About').click()
        element = wait.until(EC.title_is(('About Us')))

        driver.find_element_by_link_text('Foods').click()
        element = wait.until(EC.title_is(('CKC - Foods')))

        driver.find_element_by_link_text('Stores').click()
        driver.back()
        driver.forward()
        driver.back()
        driver.back()

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.title_is(('About Us')))
        self.assertEqual("About Calorie Killer Club", driver.find_element_by_tag_name('h2').text)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
