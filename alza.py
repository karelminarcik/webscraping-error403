from bs4 import BeautifulSoup
import requests

# URL of the page to scrape
url = 'https://www.alza.cz/32-tcl-32s5400af-d7598541.htm'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'cs-CZ,cs;q=0.9,en-US;q=0.8,en;q=0.7',
}

def clean_price(price_str):
    """
    Cleans the price string by removing unwanted characters.
    
    Args:
        price_str (str): The raw price string to be cleaned.
        
    Returns:
        str: The cleaned price string with unwanted characters removed.
    """
    replacements = {
        ",-": "",
        '\xa0': ' ',  # Non-breaking space to regular space
        " ": "",       # Remove all spaces
        "Kč": ""
    }
    for old, new in replacements.items():
        price_str = price_str.replace(old, new)
    return price_str

def send_request_get(url, headers):
    """
    Sends a GET request to the provided URL and returns the response text and URL.

    Args:
        url (str): The URL to which the GET request is sent.
        headers (dict): The headers to include in the GET request.

    Returns:
        tuple: A tuple containing the response text and the URL.
    """
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure the request was successful
    return response.text, url

def parse_response(response, url):
    """
    Parses the HTML response using BeautifulSoup.

    Args:
        response (str): The HTML response to be parsed.
        url (str): The URL of the response.

    Returns:
        tuple: A tuple containing the BeautifulSoup object and the URL.
    """
    soup = BeautifulSoup(response, "html.parser")
    return soup, url
def fetch_price(url, headers):
    try:
        # Send request and parse response
        response_text, response_url = send_request_get(url, headers)
        alza_soup, _ = parse_response(response_text, response_url)

        # Find the price element
        price_wrap = alza_soup.find(name="div", class_="price-box__body")

        # print(price_wrap)

        if price_wrap:
            # Extract the price text and clean it
            price = price_wrap.get_text(strip=True)
            price = clean_price(price)
            
            try:
                # Convert the cleaned price string to an integer
                price = int(price)
                print('Price:', price)
            except ValueError:
                print('Could not convert price to integer:', price)
        else:
            print('Price element not found')
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    
    finally:
        print("Program finished")


fetch_price(url, headers)

if __name__ == "__main__":
    fetch_price(url, headers) 