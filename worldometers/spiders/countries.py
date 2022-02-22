# -*- coding: utf-8 -*-
import scrapy
import logging 

class CountriesSpider(scrapy.Spider):
    name = 'countries' # name of the spider
    allowed_domains = ['www.worldometers.info'] # domain link never ever include htt protocol inn allowed_domains
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/'] # website we gonna scrap from

    def parse(self, response): # parse is to catch the response
        # title = response.xpath("//h1/text()").get() 
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # absolute_url = "https://www.worldometers.info" + link  # or use fstrings in python
            # absolute_url = f"https://www.worldometers.info{link}"
            
            # fancy of way by using .urljoin()
            # absolute_url = response.urljoin(link)
            
            # yield scrapy.Request(url=absolute_url)
            
            # Sending the request can use the relative url without use of absolute url
            yield response.follow(url=link, callback=self.parse_country, meta={'country_name':name})

            # returning the scrapy data
            # yield {
            #     'country_name': name,
            #     'country_link': link
            # }
            
            
    # receiving the response
    def parse_country(self, response):
        # logging.info(response.url)
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {
                'country_name': name,
                'year': year,
                'population': population
            }
                
                