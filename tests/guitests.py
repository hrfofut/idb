import unittest

from flask_testing import LiveServerTestCase
from selenium import webdriver

from idb import create_app

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


class FirefoxTestCase(LiveServerTestCase):

    def create_app(self):
        app = create_app("__test__")
        print(app.instance_path)
        print(app.root_path)
        print(app.template_folder)
        return app

    def setUp(self):

        options = Options()
        options.log.level = 'trace'
        self.driver = Firefox(options=options)
        self.driver.get(self.get_server_url())

    def tearDown(self):
        self.driver.close()

    # Test that all navbar links are functional
    def test_navbar_links(self):
        driver = self.driver
        driver.implicitly_wait(5)
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
        self.assertIn("About Us", driver.title)

    # Test that food grid card title links lead to the correct instance that displays the name properly
    def test_food_grid_links(self):
        driver = self.driver
        driver.implicitly_wait(5)
        driver.find_element_by_link_text('Foods').click()

        food_item = driver.find_element_by_class_name('card-title')
        food_name = food_item.text
        food_item.click()
        self.assertEqual(food_name, driver.find_element_by_tag_name('h1').text)

    # Test that workout grid card title links lead to the correct instance that displays the name properly
    def test_workout_grid_links(self):
        driver = self.driver
        driver.implicitly_wait(5)
        driver.find_element_by_link_text('Workouts').click()

        workout_item = driver.find_element_by_class_name('card-title')
        workout_name = workout_item.text
        workout_item.click()
        self.assertEqual(workout_name, driver.find_element_by_tag_name('h1').text)

    # Test that gym grid card title links lead to the correct instance that displays the name properly
    def test_gym_grid_links(self):
        driver = self.driver
        driver.implicitly_wait(5)
        driver.find_element_by_link_text('Gyms').click()

        gym_item = driver.find_element_by_class_name('card-title')
        gym_name = gym_item.text
        gym_item.click()
        self.assertEqual(gym_name, driver.find_element_by_tag_name('h1').text)

    # Test that store grid card title links lead to the correct instance that displays the name properly
    def test_store_grid_links(self):
        driver = self.driver
        driver.implicitly_wait(5)
        driver.find_element_by_link_text('Stores').click()

        store_item = driver.find_element_by_class_name('card-title')
        store_name = store_item.text
        store_item.click()
        self.assertEqual(store_name, driver.find_element_by_tag_name('h1').text)

    # Test that going back and forth in the navigation history doesn't break the website
    def test_navigation_history(self):
        driver = self.driver
        driver.implicitly_wait(5)
        driver.find_element_by_link_text('About').click()
        driver.find_element_by_link_text('Foods').click()
        driver.find_element_by_class_name('card-title').click()
        driver.find_element_by_link_text('Stores').click()
        driver.back()
        driver.forward()
        driver.back()
        driver.back()
        driver.back()
        self.assertEqual("About Calorie Killer Club", driver.find_element_by_tag_name('h2').text)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
