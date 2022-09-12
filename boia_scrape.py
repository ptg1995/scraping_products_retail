import requests
import json
import csv


class BoiaScraper:
    NUMBER_OF_PAGES = 40
    headers = {
        'x-api-key': 'KhMO3jH1hsjvSRzQXNfForv5FrnfSpX6StdqMmjncjGivPBj3MS4kFzRWn2j7MPn',
        'x-app-token': 'eyJraWQiOiJLZ1NcLytSZFlwVWJYTkJzbUs0NXNJS0poZjQwUmVoNndhQWtYSW1COGNVZz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI5MzE4NzZhZS0yN2NhLTQ2ODMtOTFkNy1hZjIzMzExYTI4M2EiLCJhdWQiOiIzZms4aGg1aHA4NTRyaGNiaG1wMjQxbGRwMSIsImV2ZW50X2lkIjoiZDA2YzU3Y2MtOWI1MC00YmIyLWJlZGItMTI4NmViNzAwYTc0IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2NjMwMjE3MzcsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX1V1ZkUySFlXayIsIm5hbWUiOiJFLWNvbW1lcmNlIFdFQiAtIFBSRCIsIm5pY2tuYW1lIjoiYmY2MGNiOTEtYTg2ZC00YTY4LTg2ZWItNDY4NTViNDczOGM4IiwiY29nbml0bzp1c2VybmFtZSI6IjV0cVoyS0p2YlRld1dsOGpCYVU4OFVXeEJxZU5DR01RIiwiZXhwIjoxNjYzMDI1MzM3LCJpYXQiOjE2NjMwMjE3Mzd9.Iu-W9Y7UwrQp4ofqLGRx_lQYasbl5OgnpTpqjJEymxkNZ_w7Rjm3ZjELs23OMasZCrnQuD5AjrhBOoqeRRWVIdNIEUBk3bdsoao3AwgBAH4tIzQ7i8KJ4_2BF49SUHs1sLS22DQoYDN-FBQZNopcAnRVy3lmaRFS__VtEhlM9X2TnZSJBCOGdiOtKzD2Wa0xJoZOA7a8GMEzNIauh3CtQ6sh8wDRxqlGMvz89UY20nwTO0XtW00GEhm0XkVtkPcklz1Cty3hxZWO1Yw5QubLlhEQLQVxZXlwRy45nXz9-hojLVBzavTdNqhS4ZJqSHaAML2OFD6l1ggf2TtpYjSM_Q',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
    }
    RIACHUELO_URL = "https://www.riachuelo.com.br/campanha/r/artistasbrasileiros/incerti"
    URL = "https://api-dc-rchlo-prd.riachuelo.com.br/ecommerce-web-catalog/v2/products"

    def __init__(self):
        self.save_sku_list()

    @staticmethod
    def create_payload_dict(page_number: str | int):
        return json.dumps({
            "includeFilters": False,
            "category": [
                "campanha/r/artistasbrasileiros/incerti"
            ],
            "attributes": {},
            "price": [],
            "page": page_number,
            "soldOut": False
        })

    def get_api_key_and_token(self):
        """Esse metodo deve conseguir pegar o x-api-key e x-api-token"""
        # request = requests.request("GET", self.RIACHUELO_URL)
        pass

    def do_request(self, page_number):
        payload = self.create_payload_dict(page_number)
        request = requests.request("POST", self.URL, headers=self.headers, data=payload)
        return request

    def handle_request(self):
        for i in range(self.NUMBER_OF_PAGES):
            request = self.do_request(i)
            if request.status_code != 200:
                break
            response = self._read_response(request)
            products_response = response['products']
            for product in products_response:
                yield product['sku']

    @staticmethod
    def _read_response(response):
        return json.loads(response.text)

    def save_sku_list(self):
        with open('boia.csv', mode='a') as f:
            writer = csv.writer(f)
            for row in self.handle_request():
                writer.writerow([row])


b = BoiaScraper()
