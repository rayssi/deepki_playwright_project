import pytest
from playwright.sync_api import Page
from pages.organsierDemo import OrgansierDemo

class TestDeepkiContact:

    def test_successful_Demo(self, page: Page):
        """Test de connexion réussie"""
        contact_page = OrgansierDemo(page)

        # Naviguer vers la page de contact
        contact_page.navigate_to_have_Demo()
        contact_page.request_demo()
        contact_page.fill_demo_fields()

        # Optionnel: faire une capture d'écran
        page.screenshot(path="screenshots/successful_login.png", full_page=True)

  