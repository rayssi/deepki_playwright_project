import allure
from playwright.sync_api import Page
from pages.base_page import BasePage

class OrgansierDemo(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.contact_button_selector = "//div[@class='no-wrap get-demo-header']//a[normalize-space()='Organiser une démo']"
        self.cookies_button_selector="//button[@id='tarteaucitronAllDenied2']"
        self.nom_input_selector = "//input[@id='lastname-673c4d7c-8d51-43a6-8956-117c5d029886']"
        self.prenom_input_selector =  "//input[@id='firstname-673c4d7c-8d51-43a6-8956-117c5d029886']"
        self.email_input_selector ="//input[@id='email-673c4d7c-8d51-43a6-8956-117c5d029886']"
        self.phone_input_selector="//input[@id='phone-673c4d7c-8d51-43a6-8956-117c5d029886']"  
        self.entreprise_input_selector="//input[@id='company-673c4d7c-8d51-43a6-8956-117c5d029886']"    
        self.fonction_list_selector="hierarchy-673c4d7c-8d51-43a6-8956-117c5d029886"
        
    

    def navigate_to_have_Demo(self):
     with allure.step('Given I access the Demo'):
        self.navigate_to()
        cookies_button = self.page.wait_for_selector(self.cookies_button_selector, timeout=5000)
        cookies_button.click()
      
  
    def request_demo(self):
      with allure.step('Given I request a demo'):
        try:
            contact_button = self.page.wait_for_selector(self.contact_button_selector, timeout=5000)
            contact_button.click()
            with self.page.expect_navigation():
                 self.page.wait_for_load_state("networkidle", timeout=1000)
        except:       
            pass

        assert self.page.is_visible("//h1[normalize-space()='Contact']")


      
    def fill_demo_fields(self):
        with allure.step('Given I fill demo fields'):
          self.page.fill(self.nom_input_selector, "John")
          self.page.fill(self.prenom_input_selector,"claude")
          self.page.fill(self.email_input_selector,"testAuto@Deepki.com")
          self.page.fill(self.phone_input_selector,"+33125462650")
          self.page.fill(self.entreprise_input_selector,"Qualite entreprise")
          self.page.get_by_label('Fonction*').select_option('VP')
          self.page.get_by_label("Département*").select_option('Technical / IT')
          self.page.get_by_label("Nombre d'actifs immobiliers*").select_option('Between 100 and 200')
          self.page.get_by_label("Pourquoi souhaitez-vous être contacté ?*").select_option('Get a demonstration')
          self.page.get_by_label("Centres d'intérêt*").select_option('ESG')
        allure.attach(
          self.page.screenshot(full_page=True),
          name="screenshot  la demande ",
          attachment_type=allure.attachment_type.PNG
          
        )
        
        
         