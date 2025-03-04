# Scraper - Google & Buscapé

This project is a web scraper that collects product information from Google Shopping and Buscapé, aggregating offers into a table and (optionally) sending it via email.

## Description

The project automates the search for products on price comparison websites, allowing you to quickly and efficiently find the best deals. It uses the Selenium and Pandas libraries to navigate the websites, extract the data, and organize it into an Excel file.

## Prerequisites

*   Python 3.6 or higher
*   Python Libraries:
    *   selenium
    *   webdriver-manager
    *   pandas
    *   openpyxl
    *   pywin32
*   Google Chrome installed

## Installation

1.  Clone this repository (if you're using Git):

    ```bash
    git clone <repository URL>
    ```

2.  Navigate to the project folder:

    ```bash
    cd "Scraper - Google & Buscapé"
    ```

3.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    ```

4.  Activate the virtual environment:

    ```bash
    .\venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

5.  Install the dependencies:

    ```bash
    pip install selenium webdriver-manager pandas openpyxl pywin32
    ```

## Usage

1.  **Configure the Project:**
    *   Edit the `config/config.py` file to define:
        *   `GOOGLE_URL`: The URL of Google Shopping.
        *   `BUSCAPE_URL`: The URL of Buscapé.
        *   `EXCEL_FILE`: The name of the Excel file that will be used to store the results (e.g., `"buscas.xlsx"` or `"data/buscas.xlsx"`).
    *   (Optional) If you are going to use email sending, configure the email information in `config/config.py` (specific details will depend on the email sending implementation).

2.  **Prepare the Product List:**
    *   Create (or edit) the Excel file specified in `config/config.py` (`buscas.xlsx` by default).
    *   The Excel file should contain a spreadsheet with the products you want to search for. The columns can include:
        *   `product`: The name of the product to be searched.
        *   `banned`: Keywords that should be excluded from the search results.
        *   `preco_min`: The desired minimum price (optional).
        *   `preco_max`: The desired maximum price (optional).

3.  **Run the Script:**
    *   In the terminal, navigate to the project folder (if you are not already there).
    *   Make sure the virtual environment is activated.
    *   Run the main script:

        ```bash
        python main.py
        ```

4.  **Check the Results:**
    *   After the script runs, the search results will be saved to the Excel file specified in `config/config.py`.
    *   (Optional) If email sending is configured, you will receive an email with the results table.

## Chrome Profile Configuration (Optional)

The script uses a specific Google Chrome profile to maintain sessions and cookies. If you want to use your own profile, follow these steps:

1.  **Locate Your Profile Folder:**
    *   Open Chrome and type `chrome://version` in the address bar.
    *   Look for the line "Profile Path". The value on this line is the path to your profile folder.

2.  **Update the `config/config.py` File:**
    *   Locate the `CHROME_PROFILE_PATH` variable (if it doesn't exist yet, add it).
    *   Set the value of this variable to the path of your Chrome profile folder. For example:

        ```python
        CHROME_PROFILE_PATH = "C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data\Default"
        ```

    *   **Important:** Make sure to use double backslashes (`\`) in the path, as Python interprets a single backslash (`\`) as an escape character.

If you do not configure the profile path, the script will use a temporary profile, which will be deleted at the end of execution.

## Project Structure
Scraper - Google & Buscapé/ ├── venv/ # Virtual environment (dependencies) ├── core/ # (May contain core project logic) ├── scrapers/ # (May contain specific modules for each website) ├── config/ # Project settings │ └── config.py # Main configuration file ├── data/ # (Optional) Folder to store data │ └── buscas.xlsx # Excel file with the product list ├── main.py # Main script └── README.md # This file


## Contribution

Contributions are welcome! Follow the code conventions and submit pull requests with tests and documentation.

