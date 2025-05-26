import pytest
from playwright.sync_api import Playwright, Browser, BrowserContext, Page
import os
from dotenv import load_dotenv
import allure
from datetime import datetime




load_dotenv()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "timeout": 30000,  # 30 secondes
        "ignore_https_errors": True,

    }

@pytest.fixture(scope="function")
def context(browser: Browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext):
    page = context.new_page()
    yield page
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook pour générer les rapports de test et capturer les captures d'écran en cas d'échec
    """
    outcome = yield
    report = outcome.get_result()
    
    # Ajouter des informations supplémentaires au rapport Allure
    if hasattr(item, 'funcargs'):
        # Capturer les informations du test
        test_name = item.name
        test_file = item.fspath.basename if hasattr(item, 'fspath') else 'Unknown'
        
        # Ajouter des métadonnées au rapport Allure
        if report.when == "call":
            allure.dynamic.title(f"Test: {test_name}")
            allure.dynamic.description(f"Fichier de test: {test_file}")
            
            # En cas d'échec du test
            if report.failed:
                # Capturer la capture d'écran
                capture_screenshot_on_failure(item)
                
                # Ajouter les logs d'erreur
                if hasattr(report, 'longrepr') and report.longrepr:
                    allure.attach(
                        str(report.longrepr),
                        name="Détails de l'erreur",
                        attachment_type=allure.attachment_type.TEXT
                    )
                
                # Ajouter l'horodatage de l'échec
                failure_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                allure.attach(
                    f"Échec du test le: {failure_time}",
                    name="Horodatage de l'échec",
                    attachment_type=allure.attachment_type.TEXT
                )
            
            # En cas de succès du test
            elif report.passed:
                success_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                allure.attach(
                    f"Test réussi le: {success_time}",
                    name="Horodatage du succès",
                    attachment_type=allure.attachment_type.TEXT
                )


def capture_screenshot_on_failure(item):
    """
    Fonction pour capturer des captures d'écran en cas d'échec
    """
    try:
        # Essayer d'obtenir la page depuis les fixtures
        page = None
        if hasattr(item, 'funcargs'):
            page = item.funcargs.get('page')
        
        if page:
            # Capturer la capture d'écran de la page complète
            screenshot_bytes = page.screenshot(full_page=True)
            
            # Attacher la capture d'écran au rapport Allure
            allure.attach(
                screenshot_bytes,
                name=f"Capture d'écran - Échec du test",
                attachment_type=allure.attachment_type.PNG
            )
            
            # Capturer également les informations de la page
            try:
                page_url = page.url
                page_title = page.title()
                
                page_info = f"""
URL de la page: {page_url}
Titre de la page: {page_title}
Résolution de l'écran: {page.viewport_size}
"""
                allure.attach(
                    page_info,
                    name="Informations de la page",
                    attachment_type=allure.attachment_type.TEXT
                )
            except Exception as e:
                print(f"Impossible de capturer les informations de la page: {e}")
                
        else:
            print("Aucune page disponible pour la capture d'écran")
            
    except Exception as e:
        print(f"Erreur lors de la capture d'écran: {e}")
        # Attacher l'erreur au rapport
        allure.attach(
            f"Erreur de capture d'écran: {str(e)}",
            name="Erreur de capture",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.fixture(autouse=True)
def setup_allure_environment():
    """
    Fixture pour configurer l'environnement Allure
    """
    # Ajouter des informations d'environnement
    allure.dynamic.tag("automated")
    allure.dynamic.label("framework", "playwright-pytest")
    
    yield


# Fixtures personnalisées pour Allure
@pytest.fixture
def allure_step():
    """
    Fixture pour ajouter des étapes personnalisées
    """
    def step(title):
        return allure.step(title)
    return step


# Configuration des catégories d'erreurs pour Allure
def pytest_configure(config):
    """
    Configuration des catégories d'erreurs Allure
    """
    # Créer le répertoire allure-results s'il n'existe pas
    allure_dir = config.getoption("--alluredir")
    if allure_dir and not os.path.exists(allure_dir):
        os.makedirs(allure_dir)
    
    # Créer le fichier categories.json pour Allure
    if allure_dir:
        categories_path = os.path.join(allure_dir, "categories.json")
        categories_content = '''[
  {
    "name": "Erreurs de navigation",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*navigation.*|.*timeout.*|.*page.*"
  },
  {
    "name": "Erreurs d'éléments",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*element.*|.*selector.*|.*locator.*"
  },
  {
    "name": "Erreurs d'assertion",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*assert.*|.*expect.*"
  },
  {
    "name": "Erreurs de réseau",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*network.*|.*connection.*|.*ssl.*"
  }
]'''
        try:
            with open(categories_path, 'w', encoding='utf-8') as f:
                f.write(categories_content)
        except Exception as e:
            print(f"Impossible de créer categories.json: {e}")


# Hook pour personnaliser les rapports de test
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """
    Hook exécuté avant chaque test
    """
    # Ajouter des informations de démarrage
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    allure.attach(
        f"Démarrage du test: {start_time}",
        name="Heure de démarrage",
        attachment_type=allure.attachment_type.TEXT
    )
    
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    """
    Hook exécuté après chaque test
    """
    yield
    
    # Ajouter des informations de fin
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    allure.attach(
        f"Fin du test: {end_time}",
        name="Heure de fin",
        attachment_type=allure.attachment_type.TEXT
    )
