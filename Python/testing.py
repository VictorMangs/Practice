import requests
from bs4 import BeautifulSoup
import re
import yaml

def get_bestbuy_product_info(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(product_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    price_element = soup.find('div', {'class': 'priceView-hero-price'})
    sale_element = soup.find('div', {'class': 'priceView-customer-price'})


    if price_element and sale_element:
        sale_price = sale_element.span.text.strip()
        price = price_element.span.text.strip()
        if sale_price==price:
            sum_up = soup.find("div", {"class": "priceView-price"}).get_text()
            
            if 'Was' in sum_up:
                pattern = re.compile(r'(?<=Was )\$\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?')
                price = re.findall(pattern, sum_up)[0]
        else:
            price = price_element.span.text.strip()
            
        return price, sale_price

    return None, None

# Example usage
file = "./Yaml/pricingYaml.yml"

with open(file,'r') as yf:
    data = yaml.safe_load(yf)

for shop in data:
    for item in data[shop]:
        if item:
            print('\n')
            print(item)
            price, sale_price = get_bestbuy_product_info(item)
            if price and sale_price:
                if float(price.replace('$','').replace(',','')) > float(sale_price.replace('$','').replace(',','')):
                    print(f"Regular price: {price}")
                    print(f"Sale price: {sale_price}")
                    print(f"Sale amount: ${round(float(price.replace('$','').replace(',',''))-float(sale_price.replace('$','').replace(',','')),2)}")
                    print("This product is on sale!")
                # elif price:
                #     print(f"Regular price: {price}")
                #     print("This product is not on sale.")
                else:
                    print("Price in not noteworthy")

            else:
                    print("Failed to retrieve product information")