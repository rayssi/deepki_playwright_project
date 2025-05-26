import pytest
from playwright.sync_api import Page
from pages.sasSolutionsPage import SolutionsPage
import os

class TestSASSolutions:

    def test_discover_sas_solutions(self, page: Page):

        """Test de découvrir la solution SAS"""
        sas_solutions_page = SolutionsPage(page)  
        sas_solutions_page.navigate_to_sas_solutions()     
        sas_solutions_page.click_discover_saas_solutions()
        sas_solutions_page.navigate_to_request_demo()