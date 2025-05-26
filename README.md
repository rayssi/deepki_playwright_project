# deepki_playwright_project

pour lancer les tests en local
# Exécuter le test avec Allure
pytest tests/ --alluredir=allure-results --browser firefox --headed
pytest tests/test_organsierDemo.py tests/testSASSolution.py --alluredir=allure-results --browser firefox --headed


# Générer le rapport HTML
allure generate allure-results --clean -o allure-report

# Ouvrir le rapport
allure serve allure-results      
allure open allure-report