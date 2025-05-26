from playwright.sync_api import Page
import os

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = os.getenv("DEEPKI_URL", "https://www.deepki.com/fr/")

    def navigate_to(self, path: str = ""):
        full_url = f"{self.base_url}{path}"
        self.page.goto(full_url,timeout=8000)
        self.page.wait_for_load_state("networkidle",timeout=8000)

    def wait_for_element(self, selector: str, timeout: int = 8000):
        return self.page.wait_for_selector(selector, timeout=timeout)

    def click_element(self, selector: str):
        element = self.wait_for_element(selector)
        element.click()

    def fill_input(self, selector: str, value: str):
        element = self.wait_for_element(selector)
        element.clear()
        element.fill(value)
