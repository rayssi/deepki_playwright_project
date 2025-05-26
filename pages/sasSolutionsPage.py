from playwright.sync_api import Page
from pages.base_page import BasePage
import allure


class SolutionsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.navigate_to()
        self.solutions_section_selector = "//a[normalize-space()='Découvrir nos solutions SaaS']"
        self.investisseur_section_selector = '.txt-sol-wrap:has-text("Investisseurs")'
        self.cookies_button_selector="//button[@id='tarteaucitronAllDenied2']"

        
        
    def navigate_to_sas_solutions(self):
       with allure.step("Navigue vers la page d'accuei"):
        cookies_button = self.page.wait_for_selector(self.cookies_button_selector, timeout=5000)
        cookies_button.click()
      
        
    def click_discover_saas_solutions(self):
     with allure.step("Cliquer sur le bouton pour découvrir les solutions Saa"):
        sas_solutions_button = self.page.wait_for_selector(self.solutions_section_selector, timeout=5000)
        sas_solutions_button.click()
       
      
        
    def navigate_to_request_demo(self):
     with allure.step("Cliquer sur lien pour découvrir les solutions SaaS"):
        investisseurs_section = self.page.locator(self.investisseur_section_selector)
        investisseurs_section.locator('a:has-text("En savoir plus")').click()
        allure.attach(
          self.page.screenshot(full_page=True),
          name="screenshot la solution SAS  ",
          attachment_type=allure.attachment_type.PNG
        )