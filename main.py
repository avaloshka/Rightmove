import requests
from bs4 import BeautifulSoup
import csv
import time
import pandas as pd


class Rightmove:
    results = []
    void = False
    # Change the number in production for actual number of pages that needs to be scraped
    total_pages = 8

    def fetch(self, url):
        print(f"HTTP request to URL: {url}", end="")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        print(f" | Status code : {response.status_code}")
        return response

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')

        titles = [title.text.strip() for title in content.findAll('h2', {'class': 'propertyCard-title'})]
        addresses = [address.text.strip() for address in content.findAll('address', {'class': 'propertyCard-address'})]
        descriptions = [description.text.strip() for description in content.findAll('span', {'itemprop': 'description'})]
        prices = [price.text.strip() for price in content.findAll('div', {'class': 'propertyCard-rentalPrice-primary'})]
        for price in prices:
            print(price)
        dates = [date.text.split() for date in content.findAll('span', {'class': 'propertyCard-branchSummary-addedOrReduced'})]
        # split dates and get last value in the list- the actual date
        d = []
        for date in dates:
            if date != []:
                d.append(date[-1])
            else:
                d.append('None')
        dates = d

        # Seller
        sellers = [seller.text.split('by')[-1] for seller in content.findAll('span', {'class': 'propertyCard-branchSummary-branchName'})]

        #images
        images = [image['src'] for image in content.findAll('img', {'itemprop': 'image'})]

        for index in range(0, len(titles)):
            item = {
                'title': titles[index],
                'address': addresses[index],
                'description': descriptions[index],
                'price': prices[index],
                'date': dates[index],
                'seller': sellers[index],
                'image': images[index],
            }
            self.results.append(item)
        print('Items are written to self.results')

    def to_csv(self):
        df = pd.DataFrame(self.results)
        df.to_csv("rightmove.csv")
        print("Saved to csv")

    def run(self):

        for page in range(0, self.total_pages):
            try:
                index = page * 24
                # url = f'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&sortType=1&index={index}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords='
                # url = 'https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E182&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&includeSSTC=true&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false'
                url = f'https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E182&index={index}&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare='
                response = self.fetch(url)

                self.parse(response.text)

                self.to_csv()

                time.sleep(1)
            except:

                break


if __name__ == '__main__':
    scraper = Rightmove()
    scraper.run()


