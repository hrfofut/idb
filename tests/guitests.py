from selenium import webdriver


def test_sel():
    browser = webdriver.Firefox()
    browser.get('http://127.0.0.1:5000/')

if __name__ == "__main__":  # pragma: no cover
    test_sel()
