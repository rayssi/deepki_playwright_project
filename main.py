from playwright.sync_api import sync_playwright
from pages.organsierDemo import OrgansierDemo
import os
from dotenv import load_dotenv

def main():
    load_dotenv()

    with sync_playwright() as p:
        # Lancer le navigateur
        headless = os.getenv("HEADLESS", "False").lower() == "true"

        # Créer un contexte et une page
        browser = p.firefox.launch(headless=headless, viewport={"width": 1920, "height": 1080})
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # Créer l'instance de la page de contact
            organsierDemo = OrgansierDemo(page)

            print("Navigation vers la page de login...")
            # Fixed: Added parentheses to call the method
            organsierDemo.navigate_to_have_Demo()

        except Exception as e:
            print(f"❌ Erreur: {e}")
            # Create screenshots directory if it doesn't exist
            os.makedirs("screenshots", exist_ok=True)
            page.screenshot(path="screenshots/error.png", full_page=True)

        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    main()