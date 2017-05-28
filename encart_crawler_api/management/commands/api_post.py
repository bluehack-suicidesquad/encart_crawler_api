# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import requests
import json
import base64

class HTTPElasticsearchPost(Exception):

    def __init__(self, message, *args, **kwargs):
        super(HTTPElasticsearchPost, self).__init__(*args, **kwargs)
        self.message = message

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **kwargs):
        data = open('/Users/tcruz/Developer/IBM/encart_crawler_api/encart_crawler_api/product_list.json', 'r')
        json_data = json.loads(data.read())
        url = "http://bluemix:73de6dc581b6d56cbf95111f252ca3bb@nori-us-east-1.searchly.com/products/product"

        # headers = ("Authorization", "Basic " + btoa('bluemix' + ":" + '73de6dc581b6d56cbf95111f252ca3bb'))
        # headers.append("content-type", "application/json")

        authorizarition = base64.b64encode("bluemix:" + ":" + "73de6dc581b6d56cbf95111f252ca3bb")
        headers = {"content-type": "application/json", "Authorization": "Basic" + authorizarition}

        self.send_request(url=url, data=json_data, headers=headers)


    def send_request(self, url, method='POST', data={}, headers={}):

        if method == 'POST':
            for k in data:
                category = k['category']
                image = k['image']
                price = k['price']
                name = k['name']
                market = k['market']

                data = {"root":[

                    {
                            "category": category,
                            "image": image,
                            "price": price,
                            "name": name,
                            "market": market,
                    }
                ]}

                print data
                response = requests.request(method, url, headers=headers, data=data)
                print response.content

            if not response.ok:
                if response.status_code == 404:
                    print ("Resource not found: {0}".format(response.content))
                    raise HTTPElasticsearchPost(message="Resource not found: {0}".format(response.content))
                elif response.status_code == 400:
                    print ("Bad Request: {0}".format(response.content))
                    raise HTTPElasticsearchPost(message="Bad Request: {0}".format(response.content))
                elif response.status_code == 403:
                    print ("Unauthorized: {0}".format(response.content))
                    raise HTTPElasticsearchPost(message="Unauthorized: {0}".format(response.content))
                elif response.status_code == 500:
                    print ("Internal Server Error: {0}".format(response.content))
                    raise HTTPElasticsearchPost(message="Internal Server Error: {0}".format(response.content))