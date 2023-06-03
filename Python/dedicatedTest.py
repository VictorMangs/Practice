import requests
from bs4 import BeautifulSoup

def get_product_name(url):
    # Send a GET request to the provided URL
    response = requests.get(url)
    
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the element containing the product name
    product_name_element = soup.find('h1', class_='heading-5 v-fw-regular')
    
    # Extract the product name
    if product_name_element:
        product_name = product_name_element.text.strip()
        return product_name
    
    # Return None if the product name is not found
    return None

# Example usage
product_url = 'https://www.bestbuy.com/site/company-of-heroes-3-launch-edition-playstation-5/6543762.p?skuId=6543762' #'https://www.bestbuy.com/site/samsung-65-class-q60a-series-4k-uhd-tv-smart-led-with-hdr/6455363.p?skuId=6455363'
product_name = get_product_name(product_url)

if product_name:
    print("Product Name:", product_name)
else:
    print("Product name not found.")
