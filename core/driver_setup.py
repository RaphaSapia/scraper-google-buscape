from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def get_default_chrome_options():
    """
    Configures the default options for the Chrome browser to optimize web scraping performance
    and reduce the chance of detection.

    Returns:
        Options: An instance of ChromeOptions with the configured settings.
    """
    options = Options()

    # Run in headless mode to improve performance
    options.headless = True

    # Set window size to a standard resolution
    options.add_argument("--window-size=1920,1080")

    # Reduce automation detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Disable images to improve performance
    prefs = {
        "profile.default_content_settings": {"images": 2},
        "profile.managed_default_content_settings": {"images": 2}
    }
    options.add_experimental_option("prefs", prefs)

    # Prevent unnecessary logs in the console
    options.add_argument("--log-level=3")
    options.add_argument("--silent")

    # Suppress driver error messages
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Use a custom User-Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36")

    # User data directory for session persistence
    options.add_argument(r"user-data-dir=C:\Users\RaphaelSapia\AppData\Local\Google\Chrome\User Data\Selenium Profile")

    return options


def create_driver():
    """
    Creates and configures a Chrome WebDriver instance with the default options.

    Returns:
        webdriver.Chrome: A Chrome WebDriver instance ready for web scraping.
    """
    options = get_default_chrome_options()  # Get the default options
    service = Service(ChromeDriverManager().install()) #Installs the ChromeDriverManager
    driver = webdriver.Chrome(service=service, options=options) #Create the webdriver

    # Set implicit wait time for page elements
    driver.implicitly_wait(10)
    return driver


def navigate_to_url(driver, url):
    """
    Navigates the Chrome WebDriver to the specified URL.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance to use.
        url (str): The URL to navigate to.

    Returns:
        None
    """
    driver.get(url)
