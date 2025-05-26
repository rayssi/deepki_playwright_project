from playwright.sync_api import Page
from pages.organsierDemo import OrgansierDemo
import pytest


class TestDeepkiContact:

    def test_successful_Demo(self, page: Page):
        """Test d'une demande d'une demo """
        contact_page = OrgansierDemo(page)
        contact_page.navigate_to_have_Demo()
        contact_page.request_demo()
        contact_page.fill_demo_fields()

  