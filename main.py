from playwright.sync_api import sync_playwright
from pages.organsierDemo import OrgansierDemo
import os
import allure
from dotenv import load_dotenv


def main():
    load_dotenv()

    with sync_playwright() as p:
        # Lancer le navigateur
        headless = os.getenv("HEADLESS", "False").lower() == "true"

        # Créer un contexte et une page
        browser = p.firefox.launch(headless=headless)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        try:
            # Créer l'instance de la page de contact
            organsierDemo = OrgansierDemo(page)
            print("Navigation vers la page de login...")
            
            # Navigation
            organsierDemo.navigate_to_have_Demo()
            
            # Screenshot de succès avec Allure
            screenshot_bytes = page.screenshot(full_page=True)
            
            # Sauvegarder localement (optionnel)
            os.makedirs("screenshots", exist_ok=True)
            with open("screenshots/success.png", "wb") as f:
                f.write(screenshot_bytes)
            
            # Attacher à Allure
            allure.attach(
                screenshot_bytes,
                name="Screenshot_Success",
                attachment_type=allure.attachment_type.PNG
            )
            
            print("✅ Test terminé avec succès")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            
            # Screenshot d'erreur
            screenshot_bytes = page.screenshot(full_page=True)
            
            # Sauvegarder localement
            os.makedirs("screenshots", exist_ok=True)
            with open("screenshots/error.png", "wb") as f:
                f.write(screenshot_bytes)
            
            # Attacher à Allure
            allure.attach(
                screenshot_bytes,
                name="Screenshot_Error",
                attachment_type=allure.attachment_type.PNG
            )
            
            # Re-lever l'exception pour que le test échoue
            raise e

        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    main()