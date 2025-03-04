import time
import pandas as pd
import win32com.client as win32
from core.driver_setup import create_driver
from scrapers.google_shopping import google_shopping_search, process_google_shopping_results
from scrapers.buscape import buscape_shopping, buscape_process_search_results
from config.config import EXCEL_FILE, GOOGLE_URL, BUSCAPE_URL


def navigate_to_url(driver, url):
    driver.get(url)


# Create a Chrome WebDriver instance
driver = create_driver()

# Initialize an empty DataFrame to store the aggregated offers
offer_table = pd.DataFrame()

product_table = pd.read_excel(EXCEL_FILE)

# Iterate through each row in the product table
for row_index in product_table.index:
    # Extract data for the current product from the product table
    product = product_table.loc[row_index, 'Nome']
    banned_term = product_table.loc[row_index, 'Termos banidos']
    min_price = product_table.loc[row_index, 'Preço mínimo']
    max_price = product_table.loc[row_index, 'Preço máximo']

    # ----------------------- Google Shopping -----------------------
    # Navigate to Google
    navigate_to_url(driver, GOOGLE_URL)
    # Perform a search on Google Shopping
    google_shopping_search(driver, product)
    time.sleep(2)
    # Process the search results
    google_results = process_google_shopping_results(driver, product, banned_term, min_price, max_price)

    # If results were found, create a DataFrame and add them to the offer table
    if google_results:
        google_df = pd.DataFrame(google_results, columns=['Produto', 'Descrição', 'Preço', 'Link'])
        offer_table = pd.concat([offer_table, google_df])
    else:
        google_df = None

    # ----------------------- Buscapé Shopping -----------------------
    # Navigate to Buscapé
    navigate_to_url(driver, BUSCAPE_URL)
    # Perform a search on Buscapé
    buscape_shopping(driver, product)
    time.sleep(2)
    # Process the search results
    buscape_results = buscape_process_search_results(driver, product, banned_term, min_price, max_price)

    # If results were found, create a DataFrame and add them to the offer table
    if buscape_results:
        buscape_df = pd.DataFrame(buscape_results, columns=['Produto', 'Descrição', 'Preço', 'Link'])
        offer_table = pd.concat([offer_table, buscape_df])
    else:
        buscape_df = None

# Display the aggregated offer table
print(offer_table)

# Send email with offers if any offers were found
if len(offer_table) > 0:
    # Export the offer table to an Excel file
    offer_table.to_excel('Tabela de Ofertas.xlsx', index=False)

    # Configure Outlook to send the email with the offer table
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'raphael-sapia@hotmail.com'
    mail.HTMLBody = f'''
    <p>Segue tabela de ofertas!</p>
    {offer_table.to_html(index=False)}
    <p>Att.</p>
    '''
    mail.Send()

# Close the WebDriver
driver.quit()