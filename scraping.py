import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import random

def scrape_listings():

    data_dictionary = {
        "links": [],
        "addresses": [],
        "descriptions": [],
        "prices": [],
    }

    AREA_CODES = {
        "Sheffield": "5E1195"
    }

# "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E1195&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
# "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E1195&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

    AREA_NAME = "Sheffield"
    AREA_CODE = AREA_CODES[AREA_NAME]

    global_listing_index = 0
    for page_index in range(1):

        print({f"processing page {page_index}"})

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }

        if global_listing_index == 0:
            rightmove_url = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{AREA_CODE}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
        else:
            rightmove_url = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{AREA_CODE}&index={page_index * 24}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
        print(f"rightmove URL for area {AREA_NAME}: \n{rightmove_url}")

        print(f"making GET request for area {AREA_NAME}")
        response = requests.get(rightmove_url, headers=headers)

        response.raise_for_status()

        response_text = response.text
        print(f"response received")
        print(f"length of response: {len(response_text)}")

        # print("\n------response html------\n")
        # print(response_text)

        with open("latest_response.html", "w") as f:
            f.write(response_text)

        # print("\n-------------------------\n")

        soup = BeautifulSoup(response_text, "html.parser")

        # Fetch the number of listings that displays at the top of the page
        number_of_listings = soup.find("span", {"class": "searchHeader-resultCount"}).get_text()
        # Delete commas
        number_of_listings = int(number_of_listings.replace(",", ""))
        print(f"total number of listings found: {number_of_listings}")

        # Search for divs with the class "l-searchResult is-list"
        # each result is an individual search result, showing a house
        page_listings = soup.find_all("div", class_="l-searchResult is-list")
        print(f"number of listings for this page: {len(page_listings)}")

        # collect all the links to the houses
        for page_listing_index in range(len(page_listings)):

            print(f"processing listing {page_listing_index} for page {page_index}")

            listing_div = page_listings[page_listing_index]

            # add link to the house to the list of links
            house_info_link = listing_div.find("a", class_="propertyCard-link")
            house_relative_link = house_info_link.attrs["href"]

            # create link to the house page. the link is incomplete, eg: "/properties/12345678#/?channel=RES_BUY".
            # we need to prepend rightmove.co.uk to it
            house_url = "https://www.rightmove.co.uk" + house_relative_link
            data_dictionary["links"].append(house_url)

            # get house id
            house_id = listing_div.find("a", class_="propertyCard-anchor")
            house_id = house_id['id']
            print(f"house id: {house_id}")

            # add house address to list of addresses
            house_address = house_info_link.find("address", class_="propertyCard-address")
            house_address = house_address.get_text().strip()
            data_dictionary["addresses"].append(house_address)
            print(f"house address found")

            # add house description to list of descriptions
            house_description = house_info_link.find("h2", class_="propertyCard-title")
            house_description = house_description.get_text().strip()
            data_dictionary["descriptions"].append(house_description)
            print(f"house description found")

            # add price to the list of prices
            house_price = listing_div.find("div", class_="propertyCard-priceValue")
            house_price = house_price.get_text().strip()
            data_dictionary["prices"].append(house_price)
            print(f"house price found")

            global_listing_index += 1

            print(f"finished processing listing {page_listing_index}")

            print("\n")

        print(f"scraped {page_index + 1} pages of listings")
        print(f"total listings: {number_of_listings}")
        print(f"listings processed: {page_listing_index + 1}")
        print("\n\n\n==============================================\n\n\n")

        time.sleep(random.random() * 3 + 1)

        if global_listing_index > number_of_listings:
            break

    # convert the data to dataframe and save to csv
    df = pd.DataFrame(data_dictionary)
    df.to_csv("house_listings.csv", encoding="utf-8", header="true", index=False)



if __name__ == "__main__":
    scrape_listings()

        

