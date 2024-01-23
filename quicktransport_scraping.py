import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import requests
from time import sleep
from pymongo import MongoClient


class online():
    def __init__(self) -> None:
        client = MongoClient("mongodb+srv://franciscob:salve@salve-ai.xpisp3m.mongodb.net/")
        db = client['quicktransport_scraping']
        self.mongo_quicktransports = db["quicktransport"]


class quicktransportsolutions():
    def __init__(self) -> None:
        self.base_link = 'https://www.quicktransportsolutions.com/carrier/'
        self.headers = {
    'authority': 'www.quicktransportsolutions.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'es-ES,es;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://www.quicktransportsolutions.com/',
    'sec-ch-ua': '"Opera";v="103", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0',
}
    
        
    def get_states(self):
        
        response = requests.get('https://www.quicktransportsolutions.com/carrier/usa-trucking-companies.php', headers=self.headers)
        
        print(response.status_code)

        soup = BeautifulSoup(response.content, 'html.parser')

        states = []
        counter = 0
        for link in soup.find_all('a'):
            link = link.get('href')
            if 'trucking-' in link and 'quicktransportsolutions' not in link:
                link = urljoin(self.base_link, link)
                counter += 1
                if counter < 4:
                    continue
                states.append(link)
        return states

    def get_cities(self, state):
        cities = []
        response = requests.get(state, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        for city in soup.find_all('td', {'align': '10%'}):
            link_city = city.find('a').get('href')
            city_url = urljoin(state, link_city)
            cities.append(city_url)
        return cities

    def get_companies(self, city):
        companies = []
        response = requests.get(city, headers=self.headers)
        if response.status_code == 520:
            sleep(10)
            return self.get_companies(city)
        
            
        soup = BeautifulSoup(response.content, 'html.parser')
        for info in soup.find_all('div', {'itemtype': 'https://schema.org/Organization'}):
            link_company = info.find('a').get('href')
            companies.append(link_company)
        return companies
    
    
    def company_contac_info(self, company):
        
        response = requests.get(company, headers=self.headers)
        if response.status_code == 520:
            print('sleeping')
            sleep(10)
            return self.company_contac_info(company)
        soup = BeautifulSoup(response.content, 'html.parser')
        company_dict = {}
        contact_info = soup.find('address')
        if contact_info is None:
            return None
        name = contact_info.find('span', {'itemprop': 'name'}) 
        address = contact_info.find('span', {'itemprop': 'streetAddress'})
        city = contact_info.find('span', {'itemprop': 'addressLocality'})
        state = contact_info.find('span', {'itemprop': 'addressRegion'})
        zipcode = contact_info.find('span', {'itemprop': 'postalCode'})
        phone = contact_info.find('span', {'itemprop': 'telephone'})
        company_dict['name'] = name.text if name else None
        company_dict['address'] = address.text if address else None
        company_dict['city'] = city.text if city else None
        company_dict['state'] = state.text if state else None
        company_dict['zipcode'] = zipcode.text if zipcode else None
        company_dict['phone'] = phone.text if phone else None
        return company_dict

    
Object = quicktransportsolutions()
db = online()

companies = []
for state in Object.get_states():
    print(state)
    for city in Object.get_cities(state):
        print(city)
        for company in Object.get_companies(city):
            print(company)
            company_info = Object.company_contac_info(company)
            if company_info is None:
                continue
            print(company_info)
            companies.append(company_info)

            db.mongo_quicktransports.insert_one(company_info)

exit()

companies = []

headers = {
    'authority': 'www.quicktransportsolutions.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'es-ES,es;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://www.quicktransportsolutions.com/',
    'sec-ch-ua': '"Opera";v="103", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0',
}

response = requests.get('https://www.quicktransportsolutions.com/carrier/usa-trucking-companies.php', headers=headers)

print(response.status_code)

soup = BeautifulSoup(response.content, 'html.parser')

base_link = 'https://www.quicktransportsolutions.com/carrier/'

counter = 0
for link in soup.find_all('a'):
    link = link.get('href')
    if 'trucking-' in link and 'quicktransportsolutions' not in link:
        link = urljoin(base_link, link)
        counter += 1
        if counter < 4:
            continue

    
        headers2 = {
            'authority': 'www.quicktransportsolutions.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'es-ES,es;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Opera";v="103", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0',
        }
        # print(link)
        
        response = requests.get(link, headers=headers2)
        # print(response.text)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for city in soup.find_all('td', {'align': '10%'}):
            link_city = city.find('a').get('href')
            # print(link_city)
            city_url = urljoin(link, link_city)
            # print(city_url)
            
            headers3 = {
                    'authority': 'www.quicktransportsolutions.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'es-ES,es;q=0.9',
                    'cache-control': 'max-age=0',
                    'sec-ch-ua': '"Opera";v="103", "Not;A=Brand";v="8", "Chromium";v="117"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0',
                }

            
            response = requests.get(city_url, headers=headers3)

            # print(response.status_code)

            soup = BeautifulSoup(response.content, 'html.parser')
            
            for info in soup.find_all('div', {'itemtype': 'https://schema.org/Organization'}):
                # print(info)
                

                headers4 = {
                    'authority': 'www.quicktransportsolutions.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'es-ES,es;q=0.9',
                    'cache-control': 'max-age=0',
                    'sec-ch-ua': '"Opera";v="103", "Not;A=Brand";v="8", "Chromium";v="117"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0',
                }

                link_company = info.find('a').get('href')
                
                response = requests.get(link_company, headers=headers4)
                print(response.text)
                print(link_company)
                print(response.status_code)
                
                soup = BeautifulSoup(response.content, 'html.parser')
                company_dict = {}
                contact_info = soup.find('address')
                # print('contact info:', contact_info)
                name = contact_info.find('span', {'itemprop': 'name'})
                address = contact_info.find('span', {'itemprop': 'streetAddress'})
                city = contact_info.find('span', {'itemprop': 'addressLocality'})
                state = contact_info.find('span', {'itemprop': 'addressRegion'})
                zipcode = contact_info.find('span', {'itemprop': 'postalCode'})
                phone = contact_info.find('span', {'itemprop': 'telephone'})
                
                company_dict['name'] = name.text if name else None
                company_dict['address'] = address.text if address else None
                company_dict['city'] = city.text if city else None
                company_dict['state'] = state.text if state else None
                company_dict['zipcode'] = zipcode.text if zipcode else None
                company_dict['phone'] = phone.text if phone else None
                companies.append(company_dict)


                
                # if 'address' in contact_info:
                #     print('contact info:', contact_info)
                #     exit()
                
with open('quicktransportsolutions.json', 'w') as f:
    json.dump(companies, f)