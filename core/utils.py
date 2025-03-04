

def has_banned_terms(product_name, banned_term_list):
    """
    Checks if a product name contains any banned terms.

    Args:
        product_name (str): The name of the product to check.
        banned_term_list (list): A list of terms that are not allowed in the product name.

    Returns:
        bool: True if the product name contains any banned terms, False otherwise.
    """
    has_banned_terms = False #Flag to see if the name has any term
    for term in banned_term_list: #Loop to read each term of the list
        if term in product_name: #Check if the current term is in the name
            has_banned_terms = True #Setting the flag to True if finds the term
    return has_banned_terms


def has_all_required_words(product_name, required_word_list):
    """
    Checks if a product name contains all the required words.

    Args:
        product_name (str): The name of the product to check.
        required_word_list (list): A list of words that must be present in the product name.

    Returns:
        bool: True if the product name contains all the required words, False otherwise.
    """
    has_all_required_words = True #Flag to see if the name has all required words
    for word in required_word_list: #Loop to read each word of the list
        if word not in product_name: #Check if the current word is in the name
            has_all_required_words = False #Setting the flag to False if doesn't find the word
    return has_all_required_words