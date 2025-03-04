import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from core.utils import has_banned_terms, has_all_required_words

def google_shopping_search(driver, product):
    """
    Enters a product name into the search box on Google Shopping and presses ENTER.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        product (str): The name of the product to search for.

    Returns:
        None
    """
    # Insert the product and press ENTER on the SEARCH element
    search_box = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
    search_box.send_keys(product, Keys.ENTER)

    # Wait until the result elements are present
    try:
        # Use WebDriverWait to wait for the search result elements to be present
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'nPDzT.T3FoJb'))
        )

        for element in elements:
            time.sleep(1)  # A short pause may help in specific environments
            if 'Shopping' in element.text:
                try:
                    # Check if the element is clickable and click
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, 'nPDzT.T3FoJb'))
                    )
                    element.click()
                    break
                except Exception as e_click:
                    print(f"Error clicking the element: {e_click}")
            else:
                print('NOK')

    except Exception as e:
        print(f"An error occurred while locating elements: {e}")


def process_google_shopping_results(driver, product, banned_term, min_price, max_price):
    """
    Processes the search results on Google Shopping, filtering products based on specified criteria.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        product (str): The product name to search for.
        banned_term (str): Terms to exclude from product names.
        min_price (float): The minimum acceptable price.
        max_price (float): The maximum acceptable price.

    Returns:
        list: A list of tuples, where each tuple contains the name, description, price, and URL of a product that meets the criteria.
    """
    product = product.lower()  # Convert product to lowercase
    required_word_list = product.split()  # Split product name into a list of words

    banned_term = banned_term.lower()  # Convert banned term to lowercase
    banned_term_list = banned_term.split()  # Split banned term into a list of words

    product_list = []  # Create a list to store the filtered products

    links = driver.find_elements(By.CLASS_NAME, 'i0X6df')  # -----------Find each Item from the search

    # Analisa cada item da busca encotrado para adicionar a lista final
    for link in links:
        name = link.find_element(By.CLASS_NAME, 'EI11Pd').text
        name = name.lower()

        # Check if the product name contains any banned terms
        has_banned_terms_flag = has_banned_terms(name, banned_term_list)

        # Check if the product name contains all the required words
        has_all_required_words_flag = has_all_required_words(name, required_word_list)

        # Continue processing if the product meets the criteria
        if not has_banned_terms_flag and has_all_required_words_flag:
            try:
                description = link.find_element(By.CLASS_NAME, 'dWRflb').text
            except:
                description = '--'

            url_element = link.find_element(By.CLASS_NAME, 'mnIHsc')  # Elemento pai do elemento URL
            url = url_element.find_element(By.XPATH, './*').get_attribute('href')

            # Extract and process the price
            price_text = link.find_element(By.CLASS_NAME, 'a8Pemb.OFFNJ').text
            price_text = re.sub(r'[^0-9.,]', '', price_text)
            price_text = price_text.replace('.', '').replace(',', '.')
            price = float(price_text) if price_text else 0.0

            # Check if the price is within the specified range
            if min_price < price < max_price:
                product_list.append((name, description, price, url))
    return product_list