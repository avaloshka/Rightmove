import requests
from bs4 import BeautifulSoup
import csv
import time


class Rightmove:
    results = []
    void = False
    # Change the number in production for actual number of pages that needs to be scraped
    total_pages = 1

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
        descriptions = [description.text for description in content.findAll('span', {'itemprop': 'description'})]
        prices = [price.text.strip() for price in content.findAll('div', {'class': 'propertyCard-priceValue'})]
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

    def to_csv(self):
        with open('rightmove.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())

            for row in self.results:
                writer.writerow(row)
            print('Results are stored in "rightmove.csv" ')

    def run(self):

        for page in range(0, self.total_pages):
            try:
                index = page * 24
                url = f'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&sortType=1&index={index}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords='

                response = self.fetch(url)

                self.parse(response.text)

                self.to_csv()

                time.sleep(1)
            except:

                break


if __name__ == '__main__':
    scraper = Rightmove()
    scraper.run()