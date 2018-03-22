import unittest

from flask_testing import LiveServerTestCase
from selenium import webdriver

from idb import create_app


class FirefoxTestCase(LiveServerTestCase):

    def create_app(self):
        app = create_app("__test__")
        # app.config['APPLICATION_ROOT'] = '/idb'
        print(app.instance_path)
        print(app.root_path)
        print(app.template_folder)
        return app

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_navbar_food_link(self):
        driver = self.driver
        driver.implicitly_wait(3)
        driver.get(self.get_server_url())
        self.assertIn("Let's Get Fit", driver.title)

        foods_link = driver.find_element_by_link_text('Foods')
        foods_link.click()

        workouts_link = driver.find_element_by_link_text('Workouts')
        workouts_link.click()

        gyms_link = driver.find_element_by_link_text('Gyms')
        gyms_link.click()

        stores_link = driver.find_element_by_link_text('Stores')
        stores_link.click()

        about_link = driver.find_element_by_link_text('About')
        about_link.click()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
