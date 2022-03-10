# -*- coding: utf-8 -*-
import datetime
import time
from json import JSONDecodeError
import phonenumbers
import json
import re

import requests
import scrapy
from scrapy import Selector
from ..items import FbaboutItem2


listcount = []


class FBBOOK(scrapy.Spider):
    name = 'FBBOOK'
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'Docdash.pipelines.GRAVVISOFT_LEADSDB_Pipeline': 100,
            # 'Docdash.pipelines.PhonyDuplicatesPipeline': 200,
            # 'Docdash.pipelines.BRIANSCHULLERCityFilterPipeline': 300,

        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_crawlera.CrawleraMiddleware': 610,

            ## User agent
            # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # need pip install scrapy_fake_useragent  (in conda)
            # 'scrapy_fake_useragent.middlewares.RandomUserAgentMiddleware': 400,
            ## Proxy (privoxy + tor)
            # cf https://trevsewell.co.uk/scraping/anonymous-scraping-scrapy-tor-polipo/
            # activate http proxy (turn on proxy)
            # 'scrapy_fb.middlewares.UserAgentRotatorMiddlware': 110,
            # call the middleware to customize the http proxy  (set proxy to 'http://127.0.0.1:8118')
            # 'scrapy_fb.middlewares.ProxyMiddleware': 100,


        },
        "EXTENSIONS" : {
        # 'scrapy.extensionsa.enpxxtensions.TorRenewIdentity': 1,
        'scrapy.extensionsa.enpxxtensions.SpiderOpenCloseLogging': 50
    },

    "RETRY_HTTP_CODES": [500, 502, 503, 504, 400, 401, 403, 404, 405, 406, 407, 408, 409, 410, 429],
        "CRAWLERA_URL": "gravvisoft.crawlera.com:8010",
        "CRAWLERA_APIKEY": "c79ed6d3bb814597b4b26b17dfa299d5",
        "CRAWLERA_ENABLED": True,
        "CRAWLERA_DOWNLOAD_TIMEOUT": 200,
        'CONCURRENT_REQUESTS': 32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,
        },
    #     #
    #     'CONCURRENT_REQUESTS': 1,
    #     'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    #     # 'TOR_RENEW_IDENTITY_ENABLED': True,
    #     # 'TOR_ITEMS_TO_SCRAPE_PER_IDENTITY': 5
    #     # "MYEXT_ENABLED": True,
    #     # "ROTATING_PROXY_LIST_PATH": 'proxy-list.txt',
        # "ROTATING_PROXY_PAGE_RETRY_TIMES": 5
    #


    # def __init__(self, name=None, **kwargs):
    #     super().__init__(name=None, **kwargs)
    #     self.request = None

    def start_requests(self):

        global city, industry, cityyo, cityies, proxiyo2

        indlist = []

        industrylist1 = getattr(self, "industrylist1", "")
        industrylist1_admin = getattr(self, "industrylist1_admin", "")
        industrylistwhatwhat = f'{industrylist1}{industrylist1_admin}'
        # print(industrylistwhatwhat)
        ind = industrylistwhatwhat.split("|")
        for indus in ind:
            if "" != indus:
                indlist.append(indus)
        # print(cit)

        indjoin = "|".join(indlist)
        industry = indjoin.split("|")

        stateies = getattr(self, "stateslist1", "")
        cityyo = getattr(self, "citylist1", "")
        citylist = []

        if stateies:
            cityyo = f"{cityyo}{stateies}"

        cit = cityyo.split("|")
        for c in cit:
            if "" != c:
                citylist.append(c)

        cityjoin = "|".join(citylist)
        city = cityjoin.split("|")

        global link1
        self.start_urls = ["https://scrapethissite.com/pages/simple/"]
        for ind in industry:
            for key in city:
                for n in range(0, 5, 1):

                    link2 = f'https://www.google.com/search?q="{key}"+{ind}+{n}+&start=0&num=100'
                    link3 = f'https://www.google.com/search?q={key}+{ind}+{n}+&start=0&num=100'
                    link4 = f'https://www.google.com/search?q={ind}+{key}+{n}+&start=0&num=100'

                    self.start_urls.append(link2)
                    self.start_urls.append(link3)
                    self.start_urls.append(link4)
                    self.start_urls.append("https://scrapethissite.com/pages/simple/")
        #
        # proxy = FreeProxy(elite=True, https=True, timeout=5).get()
        # print(proxy)
        # yield scrapy.Request(url="http://scrapethissite.com/pages/simple/", callback=self.parse)

        # # initialize some
        # # holding variables
        # oldIP = "0.0.0.0"
        # newIP = "0.0.0.0"
        #
        # # how many IP addresses
        # # through which to iterate?
        # nbrOfIpAddresses = 3
        #
        # # seconds between
        # # IP address checks
        # secondsBetweenChecks = 2
        # session = requests.session()
        #
        # # TO Request URL with SOCKS over TOR
        # session.proxies = {}
        # session.proxies['http'] = 'socks5h://localhost:9050'
        # session.proxies['https'] = 'socks5h://localhost:9050'
        # try:
        #     r = session.get('http://httpbin.org/ip')
        # except Exception as e:
        #     print(str(e))
        # else:
        #     proxiyo = r.text
        #     proxiyo2 = json.loads(proxiyo)
        #     print(proxiyo2)
        #     if proxiyo2:
        #         with Controller.from_port(port=9051) as controller:
        #             controller.authenticate(password="16:7A0120469C58F8B860F85FAB0FE00F3774E6FF1F7C313F7C1DFDC70667#D")
        #             print("Success!")
        #             controller.signal(Signal.NEWNYM)
        #             print("New Tor connection processed")
        #             for link in self.start_urls:
        #                 yield scrapy.Request(url=link, callback=self.parse, meta={'proxy': proxiyo2['origin']})
        #             controller.close()
        #         print(proxiyo2)
        #     else:
        #         print(proxiyo2['origin'])
        #         pass
        # time.sleep(5)
        for link in self.start_urls:
        #     yield scrapy.Request(url=link, callback=self.parse)
        #     # middleware will process the request
        #     yield scrapy.Request(url=url, callback=self.parse)

        # check if Tor has changed IP
            yield scrapy.Request(url=link, callback=self.parse)

    #
    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     print('\n\nSpider: Start')
    #     print('Is proxy in response.meta?: ', response.meta)
    #     print ("user_agent is: ", response.request.headers['User-Agent'])
    #     print('\n\n Spider: End')
    #     # self.log('Saved file  ---  %s' % filename)
    #
    #
    # def is_tor_and_privoxy_used(self, response):
    #     print('\n\nSpider: Start')
    #     print("My IP is : " + str(response.body))
    #     print("Is proxy in response.meta?: ", response.meta)  # not header dispo
    #     print('\n\nSpider: End')
        # self.log('Saved file %s' % filename)


    def parse(self, response, **kwargs):
        # print("My IP is : " + str(response.body))
        # print ("user_agent is: ", response.request.headers['User-Agent'])
        #
        # print(response.headers.get('Set-Cookie'))
        # proxy = response.meta
        # print(proxy)
        gitit = response.xpath("//span[text()='View all']").extract()
        # print(gitit)

        if gitit:
            requesturl1 = f'{response.request.url}{gitit[0]}'

            yield scrapy.Request(
                url=requesturl1,
                callback=self.parse_result, )

        gitit2 = response.xpath("//span[text()='More businesses']/ancestor-or-self::a[1]/@href").extract()
        print(gitit2)
        if gitit2:
            requesturl2 = f'{response.request.url}{gitit2[0]}'
            print(requesturl2)
            if requesturl2:
                yield scrapy.Request(
                    url=requesturl2,
                    callback=self.parse_result)

    def parse_result(self, response):
        item = FbaboutItem2()

        time.sleep(5)

        def FindIndustry(string):
            iindustrylist = []
            industrylist1 = getattr(self, "industrylist1", "")
            industrylist1_admin = getattr(self, "industrylist1_admin", "")
            industrylistwhatwhat = f'{industrylist1}{industrylist1_admin}'
            ind = industrylistwhatwhat.split("|")
            for i in ind:
                if "" != i:
                    iindustrylist.append(i)

            indjoin = "|".join(iindustrylist)
            injoin = indjoin.replace("-", " ")

            indies3 = injoin.replace("|", r"\b|\b")

            regexind = fr'\b{indies3}\b'
            industryyoo = re.findall(regexind, string)
            return [x for x in industryyoo]

        def FindCity(string):
            citylist = []
            stateies = getattr(self, "stateslist1", "")
            cityies = getattr(self, "citylist1", "")

            if stateies:
                cityies = f"{cityies}{stateies}"

            cit = cityies.split("|")
            for c in cit:
                if "" != c:
                    citylist.append(c)

            citjoin = "|".join(citylist)
            cijoin = citjoin.replace("-", " ")
            # print(citjoin)

            cityies3 = cijoin.replace("|", r"\b|\b")

            regex_city = fr'\b{cityies3}\b'
            ciityyoo = re.findall(regex_city, string)
            return [x for x in ciityyoo]

        citytesty = response.xpath("//div[contains(@id,'tsu')]").extract()
        for ct in citytesty:
            # print(ct)
            ctsel = Selector(text=ct)
            ctsel_links = ctsel.xpath("//div[text()='Directions']/ancestor::a/@data-url").extract()
            print(ctsel_links)

            # COMPANY
            if ctsel_links:

                site = ctsel.xpath("//div[text()='Website']/ancestor::a/@href").extract()
                print(site)

                textit = ctsel.xpath("//div[@class='rllt__details']//text()").extract()
                print(textit)
                divheading = ctsel.xpath("//div[@class='rllt__details']/preceding::div[1]/text()[1]").extract()
                print(f'THIS IS THE DIVHEAD:   {divheading}')
                # place("+", " ")
                # print(selecter_citylinks3)
                # CITY
                selecter_citylinks2 = ctsel_links[0]
                selecter_citylinks3 = selecter_citylinks2
                foundcity2 = FindCity(f'{selecter_citylinks3}{" ".join(textit)}')
                print(f'FOUNDCIIIIIIIITTTTYYYY:     {foundcity2}')
                if foundcity2:
                    item['city'] = foundcity2[0]
                    found_industry1 = FindIndustry(" ".join(textit).title())
                    print(found_industry1)
                    if found_industry1:
                        item['industry'] = found_industry1[0]
                        item['city'] = foundcity2[0]

                        # COMPANY
                        if ctsel_links:
                            lineline2 = ctsel_links[0]
                            lineline4 = lineline2.split(",")[0]
                            line5yo = lineline4.replace("/maps/dir//", "")
                            line6 = line5yo.replace("+", " ")
                            print(line6)
                            item['company'] = line6

                        for match in phonenumbers.PhoneNumberMatcher(" ".join(textit), "US"):
                            phoneage = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL)
                            phone_found = phoneage
                            if phoneage:
                                item['phone'] = phoneage
                                print(phone_found)
                            else:
                                pass

                            if site:
                                item['url'] = site[0]  # data_id = data['id']
                                yield scrapy.Request(url=item['url'], callback=self.email_parse_result, meta={
                                    'city': item["city"],
                                    'company': item["company"],
                                    'industry': item["industry"],
                                    'phone': item['phone'],
                                    'url': item['url'],
                                    # "data_id": data_id,
                                })

                            else:
                                item["url"] = None
                                item['email'] = None
                                # item["valid_email"] = None
                                # item['free_email'] = None
                                # item["email_drop"] = None
                                yield item
                                print(f'FOUND BOTH THE INDUSTRY AND CITY: {item["city"]} {item["industry"]}')
                                urlccciittyy = 'https://www.gravvisoft.com/api/lead/'

                                itemcity = {
                                    "user_id": getattr(self, 'user_id', ''),
                                    "date": str(datetime.date.today()),
                                    'city': item["city"],
                                    'company': item["company"],
                                    'industry': item["industry"],
                                    'phone': item['phone'],
                                    # "email": item['email'],

                                    # 'valid_email': item['valid_email'],
                                    # "free_email": item['free_email'],
                                    # "email_drop": item["email_drop"],
                                }
                                x = requests.post(urlccciittyy, data=itemcity)
                                x_yo = x.content
                                print(x_yo)
                                yield item

            nextlink = response.xpath("//span[text()='Next']").extract()
            if nextlink:
                nextlink_url = response.xpath("//span[text()='Next']/ancestor-or-self::a[1]/@href").extract()
                nextlink_url_full = f'{response.request.url}{nextlink_url[0]}'
                print(nextlink_url_full)
                yield scrapy.Request(
                    url=nextlink_url_full,
                    callback=self.parse_result,
                )

    def email_parse_result(self, response):
        global datadebounce
        item = FbaboutItem2()
        city = response.meta['city']
        industry = response.meta['industry']
        phone = response.meta['phone']
        company = response.meta['company']
        url = response.meta['url']

        # data_id = response.meta['data_id']
        # print(f'THIS IS THE META DATA: {data_id}')
        bodytext = response.xpath('//body//text()').extract()
        bodyjoin = " ".join(bodytext)
        # print(bodyjoin)
        emailfind = re.findall(
            "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",
            bodyjoin)
        print(emailfind)
        if emailfind:
            item['email'] = emailfind[0]

            ademail = getattr(self, 'klentymail', '')
            adklentyapikey = getattr(self, 'klentyapikey', '')
            adcadenceName = getattr(self, 'klentyCadence', '')
            ### EMAIL API
            try:
                addprospect = requests.post(
                    f"https://api.debounce.io/v1/?api=5f43170b7690e&email={item['email']}")
                datadebounce = json.loads(addprospect.content)
            except JSONDecodeError:
                pass
            if not datadebounce:
                item['free_email'] = None
                item['valid_email'] = None
                item['email_drop'] = None

            if datadebounce:
                print(datadebounce['debounce']['send_transactional'])
                processemail = datadebounce['debounce']['send_transactional']

                item['free_email'] = datadebounce['debounce']['send_transactional']
                item['valid_email'] = datadebounce['debounce']['reason']

                if processemail != "1":
                    item['email_drop'] = None

                elif processemail == "1":
                    item["email_drop"] = "Valid"

                    addprospect = requests.post(
                        f'https://app.klenty.com/apis/v1/user/{ademail}/prospects',
                        json={"Email": f"{item['email']}",
                              "Company": f"{company}",
                              "City": f"{city}",
                              "Department": f"{industry}",
                              "Phone": f"{phone}",
                              },
                        headers={'x-api-key': adklentyapikey})
                    try:
                        data = json.loads(addprospect.content)
                        print(data)
                    except JSONDecodeError:
                        pass
                    addtocadence = requests.post(
                        f'https://app.klenty.com/apis/v1/user/{ademail}/startcadence',
                        json={"Email": f"{item['email']}",
                              "cadenceName": adcadenceName},
                        headers={'x-api-key': adklentyapikey})
                    try:
                        data2 = json.loads(addtocadence.content)
                        print(data2)
                    except JSONDecodeError:
                        pass

            # yield item
            print(f'FOUND BOTH THE INDUSTRY AND CITY: {city} {industry}')
            urlccciittyy = 'https://www.gravvisoft.com/api/lead/'

            itemcity2 = {
                "user_id": getattr(self, 'user_id', ''),
                "date": str(datetime.date.today()),
                'city': city,
                'company': company,
                'industry': industry,
                'url': url,
                'email': item['email'],
                'phone': phone,
                'valid_email': item['valid_email'],
                "free_email": item['free_email'],
                "email_drop": item["email_drop"],
            }
            print(itemcity2)
            x2 = requests.post(urlccciittyy, data=itemcity2)
            print(x2.content)
            yield item
