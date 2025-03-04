import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from core.utils import has_banned_terms, has_all_required_words

def buscape_shopping(driver, product):
    """
    Enters a product name into the search box on the Buscapé website and presses ENTER.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        product (str): The name of the product to search for.

    Returns:
        None
    """
    # Insert the product and press ENTER on the SEARCH element
    search_box = driver.find_element(By.XPATH, '//*[@id="new-header"]/div[1]/div/div/div[3]/div/div/div[2]/div/div[1]/input')
    search_box.send_keys(product, Keys.ENTER)


def buscape_process_search_results(driver, product, banned_term, min_price, max_price):
    """
    Processes the search results on Buscapé, filtering products based on specified criteria.

    Args:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        product (str): The product name to search for.
        banned_term (str): Terms to exclude from product names.
        min_price (float): The minimum acceptable price.
        max_price (float): The maximum acceptable price.

    Returns:
        list: A list of tuples, where each tuple contains the name, description, price, and URL of a product that meets the criteria.
    """
    product = product.lower() #Convert product to lowercase
    required_word_list = product.split() #Split product name into a list of words

    banned_term = banned_term.lower() #Convert banned term to lowercase
    banned_term_list = banned_term.split() #Split banned term into a list of words

    product_list = [] #Create a list to store the filtered products

    # Wait for the product cards to load
    product_cards = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ProductCard_ProductCard_Inner__gapsh')))

    # Iterate through each product card
    for card in product_cards:
        name = card.find_element(By.CLASS_NAME, 'ProductCard_ProductCard_NameWrapper__45Z01').text #Get the product name
        name = name.lower() #Convert product name to lowercase

        #Check if the product name contains any banned terms
        has_banned_terms_flag = has_banned_terms(name, banned_term_list)

        #Check if the product name contains all the required words
        has_all_required_words_flag = has_all_required_words(name, required_word_list)

        #Continue processing if the product meets the criteria
        if not has_banned_terms_flag and has_all_required_words_flag:
            try:
                description = card.find_element(By.TAG_NAME, 'h3').text #Get the product description
            except:
                description = '--'

            #Find the URL of the product
            url_element = card.find_element(By.CLASS_NAME, 'ProductCard_ProductCard_Body__bnVUn')
            url = url_element.find_element(By.XPATH, '..').get_attribute('href')

            #Extract and process the price
            price_text = card.find_element(By.CLASS_NAME, 'Text_Text__ARJdp.Text_MobileHeadingS__HEz7L').text
            price_text = re.sub(r'[^0-9.,]', '', price_text)
            price_text = price_text.replace('.','').replace(',','.')
            price = float(price_text) if price_text else 0.0

            #Check if the price is within the specified range
            if min_price < price < max_price:
                product_list.append((name, description, price, url))

    return product_list