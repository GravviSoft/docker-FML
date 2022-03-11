# -*- coding: utf-8 -*-
import ssl
from json import JSONDecodeError
import datetime
import itertools
import json
import phonenumbers
import pymongo
import requests
from bson import ObjectId

import scrapy

from pymongo.errors import DuplicateKeyError

from ..items import FbaboutItem2, Zyte

class ZYTEGRAVVIDBSpider(scrapy.Spider):
    name = 'ZYTE_GRAVVI_DB'
    start_urls = ['https://scrapethissite.com/pages/simple/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'Docdash.pipelines.GravviPipeline': 100,
            # 'Docdash.pipelines.PhonyDuplicatesPipeline': 200,
            # 'Docdash.pipelines.BRIANSCHULLERCityFilterPipeline': 300
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_crawlera.CrawleraMiddleware': 610,

        },

        "RETRY_HTTP_CODES": [500, 502, 503, 504, 400, 401, 403, 404, 405, 406, 407, 408, 409, 410, 429],
        "CRAWLERA_URL": "gravvisoft.crawlera.com:8010",
        "CRAWLERA_APIKEY": "c79ed6d3bb814597b4b26b17dfa299d5",
        "CRAWLERA_ENABLED": True,
        "CRAWLERA_DOWNLOAD_TIMEOUT": 200,
        'CONCURRENT_REQUESTS': 32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,

    }

    def parse(self, response, **kwargs):
        global emailwhatwhat, datadebounce, phoneage, phoneage2, leads2, leads
        item = FbaboutItem2()
        zitems = Zyte()
        user_id = getattr(self, "user_id", "")

        # return zitems

        id_start = getattr(self, "id_start", "")
        id_end = getattr(self, "id_end", "")
        # user_id = getattr(self, "user_id", "")
        # zitems['user__id'] = user_id
        conn2 = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster0.kuvzf.mongodb.net",  tls=True)
        db2 = conn2["GRAVVIBOY"]
        collection2 = db2['LEADS']
        collectionyo = db2["users_profile"]

        # for dbases in collectionyo.find({"user_id": int(user_id)}, batch_size=20):
        for dbases in itertools.islice(collectionyo.find(), int(id_start), int(id_end)):

            if dbases["active_client"] == True:

                zitems["databasename"] = dbases["databasename"]
                zitems["klentyemail"] = dbases["klentyemail"]
                zitems["klenty_api_key"] = dbases["klenty_api_key"]
                zitems["cadence_name"] = dbases["cadence_name"]
                zitems["databasename"] = dbases["databasename"]
                zitems["ringlessvm_id"] = dbases["ringlessvm_id"]
                zitems["databasename"] = dbases["databasename"]

                industrylist1 = dbases['industrylist1']
                industrylist1_admin = dbases['industrylist1_admin']

                zitems["industrylist1"] = industrylist1 + industrylist1_admin

                if industrylist1 == None:
                    print("databasename")
                cust_industries = []
                cust_cities = []

                industrylistwhatwhat = industrylist1_admin.replace("-", " ")
                ind = industrylistwhatwhat.split("|")
                for i in ind:
                    if "" != i:
                        cust_industries.append(i)

                citylistwhatwhat = dbases['citylist1'].replace("-", " ")
                #         s2city = cityyo.replace(',-', " ")
                #         s3city = s2city.replace('- ', " ")
                cit = citylistwhatwhat.split("|")
                for c in cit:
                    if "" != c:
                        cust_cities.append(c.strip())
                print(cust_industries, cust_cities)


               # itemkip = int(dbases["vmd_leads_loaded"]) - int(dbases["vmd_leads_remaining"])
                # print(leadstoskip)
                # conn1 = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster0.kuvzf.mongodb.net",
                #                             ssl_cert_reqs=ssl.CERT_NONE)
                # db1 = conn1[f'{dbases["databasename"]}']
                conn2 = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster0.kuvzf.mongodb.net", tls=True)


                db2 = conn2[f"GRAVVIBOY"]

                collection2 = db2['LEADS']


                for leads in collection2.find({ '$and': [ {"industry": { "$in": cust_industries }, "city": { "$in": cust_cities }}]}):

                    zitems['city']= leads['city'],
                    zitems['company']= leads["company"],
                    zitems['email']= leads['email'],
                    zitems['industry']= leads['industry'],

                    for match in phonenumbers.PhoneNumberMatcher(leads["phone"], "US"):
                        phonage = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL)
                        zitems["phone"] = phonage

                        url_gravvisoft = 'https://www.gravvisoft.com/api/lead/'
                        try:
                            itemcity = {
                                "user_id": dbases["user_id"],
                                "date": str(datetime.date.today()),
                                'city': leads['city'],
                                'company': leads["company"],
                                'email': leads['email'],
                                'industry': leads['industry'],
                                'lead_source': "",
                                'phone': zitems["phone"],
                                "phone_carrier": "",
                                "phone_type": "",
                                'rvm_drop': "",
                                'email_drop': "",
                                "free_email": "",
                                "valid_email": "",
                                'url': "",
                                'dnc_email': False,
                                'dnc_phone': False,
                                'notes': "",
                                "tags": "",
                                "facebook": "",
                                "houzz": "",
                                "yelp": "",
                                "bbb": "",
                                "yp": "",
                                "instagram": "",
                                "linkedin": "",
                                "twitter": "",
                                "whatsapp": "",
                                "otherlinks": "",
                                "zillow": "",
                                "realtor": "",
                                "google": "",
                                "first_name": "",
                                "cadence_name": "",
                                "opens": "",
                                "clicks": "",
                                "replies": "",
                                "unsubscribes": "",
                                "rvm_sent": False,
                                "rvm_lead_id": "",
                                "rvm_message": "",

                            }
                            print(itemcity)


                            gravvi = requests.post(url_gravvisoft, data=itemcity)
                            gravvi_data = gravvi.json()
                            print(gravvi_data)

                        except JSONDecodeError:
                            pass

                    ademail = dbases["klentyemail"]
                    adklentyapikey = dbases["klenty_api_key"]
                    adcadenceName = dbases["cadence_name"]
                    ### EMAIL API

                    if ["email"]:
                        try:
                            addprospect = requests.post(
                                f"https://api.debounce.io/v1/?api=5f43170b7690e&email={leads['email']}")
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

                            # item['free_email'] = datadebounce['debounce']['free_email']
                            # item['valid_email'] = datadebounce['debounce']['reason']
                            try:
                                emailurl1 = f'https://www.gravvisoft.com/api/lead/phone/{zitems["phone"]}/'
                                emaildata1 = {
                                    "free_email": datadebounce['debounce']['free_email'],
                                    "valid_email": datadebounce['debounce']['reason'],
                                }
                                email_y = requests.patch(emailurl1, data=emaildata1)
                                print(email_y)

                                # data2 = json.loads(y)
                                print(email_y.json())
                            except JSONDecodeError:
                                pass



                            if processemail != "1":
                                pass

                            elif processemail == "1":
                                # item["email_drop"] = "Valid"



                                try:
                                    emailurl2 = f'https://www.gravvisoft.com/api/lead/phone/{zitems["phone"]}/'
                                    emaildata2 = {
                                        "email_drop": "Valid",
                                    }
                                    email_y2 = requests.patch(emailurl2, data=emaildata2)
                                    print(email_y2)

                                    # data2 = json.loads(y)
                                    print(email_y2.json())
                                except JSONDecodeError:
                                    pass


                                addprospect = requests.post(
                                    f'https://app.klenty.com/apis/v1/user/{ademail}/prospects',
                                    json={"Email": f"{leads['email']}",
                                          "Company": f"{leads['company']}",
                                          "City": f"{leads['city']}",
                                          "Phone": f"{leads['phone']}",
                                          },
                                    headers={'x-api-key': adklentyapikey})
                                try:
                                    data = json.loads(addprospect.content)
                                    print(data)
                                except JSONDecodeError:
                                    pass
                                addtocadence = requests.post(
                                    f'https://app.klenty.com/apis/v1/user/{ademail}/startcadence',
                                    json={"Email": f"{leads['email']}",
                                          "cadenceName": adcadenceName},
                                    headers={'x-api-key': adklentyapikey})
                                try:
                                    data2 = json.loads(addtocadence.content)
                                    print(data2)
                                except JSONDecodeError:
                                    pass


                    # conn2 = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster0.kuvzf.mongodb.net",
                    #                             ssl_cert_reqs=ssl.CERT_NONE)
                    # db2 = conn2[f"GRAVVIBOY"]
                    #
                    # collection2 = db2['LEADS']
                #
                conn1 = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster1.9f0gx.mongodb.net", tls=True)


                db1 = conn1[f"GRAVVISOFT"]
                collection = db1['LEADS']

                for leads2 in collection.find(
                        {'$and': [{"industry": {"$in": cust_industries}, "city": {"$in": cust_cities}}]}).noCursorTimeout():
                    # print(leads)

                    for match in phonenumbers.PhoneNumberMatcher(leads2["phone"], "US"):
                        phoneage = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL)

                        url_gravvisoft = 'https://www.gravvisoft.com/api/lead/'
                        try:
                            itemcity = {
                                "user_id": dbases["user_id"],
                                "date": str(datetime.date.today()),
                                'city': leads2['city'],
                                'company': leads2["company"],
                                'email': leads2['email'],
                                'industry': leads2['industry'],
                                'lead_source': "",
                                'phone': phoneage,
                                "phone_carrier": "",
                                "phone_type": "",
                                'rvm_drop': "",
                                'email_drop': "",
                                "free_email": "",
                                "valid_email": "",
                                'url': "",
                                'dnc_email': False,
                                'dnc_phone': False,
                                'notes': "",
                                "tags": "",
                                "facebook": "",
                                "houzz": "",
                                "yelp": "",
                                "bbb": "",
                                "yp": "",
                                "instagram": "",
                                "linkedin": "",
                                "twitter": "",
                                "whatsapp": "",
                                "otherlinks": "",
                                "zillow": "",
                                "realtor": "",
                                "google": "",
                                "first_name": "",
                                "cadence_name": "",
                                "opens": "",
                                "clicks": "",
                                "replies": "",
                                "unsubscribes": "",
                                "rvm_sent": False,
                                "rvm_lead_id": "",
                                "rvm_message": "",

                            }
                            print(itemcity)

                            gravvi = requests.post(url_gravvisoft, data=itemcity)
                            gravvi_data = gravvi.json()
                            print(gravvi_data)

                        except JSONDecodeError:
                            pass

                    ademail = dbases["klentyemail"]
                    adklentyapikey = dbases["klenty_api_key"]
                    adcadenceName = dbases["cadence_name"]
                    ### EMAIL API

                    if ["email"]:
                        try:
                            addprospect = requests.post(
                                f"https://api.debounce.io/v1/?api=5f43170b7690e&email={leads2['email']}")
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

                            # item['free_email'] = datadebounce['debounce']['free_email']
                            # item['valid_email'] = datadebounce['debounce']['reason']
                            try:
                                emailurl1 = f'https://www.gravvisoft.com/api/lead/phone/{phoneage}/'
                                emaildata1 = {
                                    "free_email": datadebounce['debounce']['free_email'],
                                    "valid_email": datadebounce['debounce']['reason'],
                                }
                                email_y = requests.patch(emailurl1, data=emaildata1)
                                print(email_y)

                                # data2 = json.loads(y)
                                print(email_y.json())
                            except JSONDecodeError:
                                pass

                            if processemail != "1":
                                pass

                            elif processemail == "1":
                                # item["email_drop"] = "Valid"

                                try:
                                    emailurl2 = f'https://www.gravvisoft.com/api/lead/phone/{phoneage}/'
                                    emaildata2 = {
                                        "email_drop": "Valid",
                                    }
                                    email_y2 = requests.patch(emailurl2, data=emaildata2)
                                    print(email_y2)

                                    # data2 = json.loads(y)
                                    print(email_y2.json())
                                except JSONDecodeError:
                                    pass

                                addprospect = requests.post(
                                    f'https://app.klenty.com/apis/v1/user/{ademail}/prospects',
                                    json={"Email": f"{leads2['email']}",
                                          "Company": f"{leads2['company']}",
                                          "City": f"{leads2['city']}",
                                          "Phone": f"{leads2['phone']}",
                                          },
                                    headers={'x-api-key': adklentyapikey})
                                try:
                                    data = json.loads(addprospect.content)
                                    print(data)
                                except JSONDecodeError:
                                    pass
                                addtocadence = requests.post(
                                    f'https://app.klenty.com/apis/v1/user/{ademail}/startcadence',
                                    json={"Email": f"{leads2['email']}",
                                          "cadenceName": adcadenceName},
                                    headers={'x-api-key': adklentyapikey})
                                try:
                                    data2 = json.loads(addtocadence.content)
                                    print(data2)
                                except JSONDecodeError:
                                    pass

                conn1.close()
                conn2.close()
        connyo.close()
                    # conn1 = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster1.9f0gx.mongodb.net",
                    #                             ssl_cert_reqs=ssl.CERT_NONE)
                    # db1 = conn1[f"GRAVVISOFT"]
                    #
                    # ph_list = []
                    # collection = db1['LEADS']
                    # conn2 = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster0.kuvzf.mongodb.net",
                    #                            ssl_cert_reqs=ssl.CERT_NONE)
                    # db2 = conn2[f"GRAVVIBOY"]
                    # ph_list = []
                    # collection2 = db2['LEADS']
                    # collection2.update_many({}, {'$rename': {"date_of_pull": "date"}})
                    # collection2.update_many({'date': {'$exists': False}}, {'$set': {"date": str(datetime.date.today())}})
                    # collection2.update_many({'email': {'$exists': False}}, {'$set': {"email": None}})
                    # collection2.update_many({'email': ""}, {'$set': {"email": None}})
                    # collection2.update_many({'lead_source': {'$exists': False}}, {'$set': {"lead_source": None}})
                    # collection2.update_many({'phone': {'$exists': False}}, {'$set': {"phone": None}})
                    # collection2.update_many({'phone': ""}, {'$set': {"phone": None}})
                    #
                # for leads2 in collection2.find(
                #         {'$and': [{"industry": {"$in": cust_industries}, "city": {"$in": cust_cities}}]}):
                #     # print(leads)
                #
                #     for match in phonenumbers.PhoneNumberMatcher(leads2["phone"], "US"):
                #         phoneage2 = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL)
                #
                #     url_gravvisoft2 = 'https://www.gravvisoft.com/api/leadmaster/'
                #     try:
                #         itemcity2 = {
                #             "user_id": "0",
                #             "date": str(datetime.date.today()),
                #             'city': leads2['city'],
                #             'company': leads2["company"],
                #             'email': leads2['email'],
                #             'industry': leads2['industry'],
                #             'lead_source': "",
                #             'phone': phoneage2,
                #             "phone_carrier": "",
                #             "phone_type": "",
                #             'rvm_drop': "",
                #             'email_drop': "",
                #             "free_email": "",
                #             "valid_email": "",
                #             'url': "",
                #             'dnc_email': "False",
                #             'dnc_phone': "False",
                #             'notes': "",
                #             "tags": "",
                #             "facebook": "",
                #             "houzz": "",
                #             "yelp": "",
                #             "bbb": "",
                #             "yp": "",
                #             "instagram": "",
                #             "linkedin": "",
                #             "twitter": "",
                #             "whatsapp": "",
                #             "otherlinks": "",
                #             "zillow": "",
                #             "realtor": "",
                #             "google": "",
                #             "first_name": "",
                #             "cadence_name": "",
                #             "opens": "",
                #             "clicks": "",
                #             "replies": "",
                #             "unsubscribes": "",
                #             "rvm_sent": False,
                #             "rvm_lead_id": "",
                #             "rvm_message": "",
                #
                #         }
                #         print(itemcity2)
                #
                #         gravvi2 = requests.post(url_gravvisoft2, data=itemcity2)
                #         gravvi_data2 = gravvi2.json()
                #         print(gravvi_data2)
                #
                #     except JSONDecodeError:
                #         pass


                    #
                    #
                    # ademail = dbases["klentyemail"]
                    # adklentyapikey = dbases["klenty_api_key"]
                    # adcadenceName = dbases["cadence_name"]
                    # ### EMAIL API
                    #
                    # if ["email"]:
                    #     try:
                    #         addprospect = requests.post(
                    #             f"https://api.debounce.io/v1/?api=5f43170b7690e&email={leads['email']}")
                    #         datadebounce = json.loads(addprospect.content)
                    #     except JSONDecodeError:
                    #         pass
                    #     if not datadebounce:
                    #         item['free_email'] = None
                    #         item['valid_email'] = None
                    #         item['email_drop'] = None
                    #
                    #     if datadebounce:
                    #         print(datadebounce['debounce']['send_transactional'])
                    #         processemail = datadebounce['debounce']['send_transactional']
                    #
                    #         # item['free_email'] = datadebounce['debounce']['free_email']
                    #         # item['valid_email'] = datadebounce['debounce']['reason']
                    #         try:
                    #             emailurl1 = f'https://www.gravvisoft.com/api/lead/phone/{phoneage}/'
                    #             emaildata1 = {
                    #                 "free_email": datadebounce['debounce']['free_email'],
                    #                 "valid_email": datadebounce['debounce']['reason'],
                    #             }
                    #             email_y = requests.patch(emailurl1, data=emaildata1)
                    #             print(email_y)
                    #
                    #             # data2 = json.loads(y)
                    #             print(email_y.json())
                    #         except JSONDecodeError:
                    #             pass
                    #
                    #
                    #         if processemail != "1":
                    #             pass
                    #
                    #         elif processemail == "1":
                    #             # item["email_drop"] = "Valid"
                    #
                    #
                    #
                    #             try:
                    #                 emailurl2 = f'https://www.gravvisoft.com/api/lead/phone/{phoneage}/'
                    #                 emaildata2 = {
                    #                     "email_drop": "Valid",
                    #                 }
                    #                 email_y2 = requests.patch(emailurl2, data=emaildata2)
                    #                 print(email_y2)
                    #
                    #                 # data2 = json.loads(y)
                    #                 print(email_y2.json())
                    #             except JSONDecodeError:
                    #                 pass
                    #
                    #
                    #             addprospect = requests.post(
                    #                 f'https://app.klenty.com/apis/v1/user/{ademail}/prospects',
                    #                 json={"Email": f"{leads['email']}",
                    #                       "Company": f"{leads['company']}",
                    #                       "City": f"{leads['city']}",
                    #                       "Phone": f"{leads['phone']}",
                    #                       },
                    #                 headers={'x-api-key': adklentyapikey})
                    #             try:
                    #                 data = json.loads(addprospect.content)
                    #                 print(data)
                    #             except JSONDecodeError:
                    #                 pass
                    #             addtocadence = requests.post(
                    #                 f'https://app.klenty.com/apis/v1/user/{ademail}/startcadence',
                    #                 json={"Email": f"{leads['email']}",
                    #                       "cadenceName": adcadenceName},
                    #                 headers={'x-api-key': adklentyapikey})
                    #             try:
                    #                 data2 = json.loads(addtocadence.content)
                    #                 print(data2)
                    #             except JSONDecodeError:
                    #                 pass


                    #
                    #
                    #
                    #
                    #
                    # if phoneage:
                    #     api_key = "e2e6bf6c93bc7431aa243fade9af49b20665656c"
                    #     check_duplicate = "CHECK_DUPLICATE_IN_LIST"
                    #     Integration_Key = "e2e6bf6c93bc7431aa243fade9af49b20665656c"
                    #     Encoded_Integration_Key = "f66e83d5f117f20a778a7c3647609e65"
                    #     #     phone_number = "8018150852"
                    #     #
                    #     #     # IF NO DUPLICATE PHONE IN MONGO + THE CITY IS IN THE LIST OF CITIES THEN PROCESS THE PHONE NUMBER.  SEND THE PHONE NUMBER INTO THE CLIENTS VOICEMAIL DROP API
                    #     #     vmdapi = "692074"
                    #
                    #     url_lr = "https://s2.leadsrain.com/ringless/api/add_posted_lead.php"
                    #     myobj = {
                    #         'api_key': api_key,
                    #         'username': "23100",
                    #         'list_id': int(dbases["ringlessvm_id"]),
                    #         'check_duplicate': check_duplicate,
                    #         'phone_number': phoneage,
                    #
                    #     }
                    #     try:
                    #         x = requests.post(url_lr, data=myobj)
                    #         data = x.json()
                    #         print(data)
                    #         print(data["lead_id"])
                    #         print(data["message"])
                    #         rvm_message1 = data["message"]
                    #
                    #
                    #         if "Duplicate Phone Number" in rvm_message1:
                    #
                    #
                    #             url1 = f'https://www.gravvisoft.com/api/lead/phone/{phoneage}/'
                    #             data1 = {
                    #                 "rvm_sent": True,
                    #             }
                    #             y = requests.patch(url1, data=data1)
                    #             print(y)
                    #             # data2 = json.loads(y)
                    #             print(y.json())
                    #
                    #
                    #         elif "Lead Successfully added" in rvm_message1:
                    #             url2 = f'https://www.gravvisoft.com/api/lead/phone/{phoneage}/'
                    #             data2 = {
                    #                 "rvm_sent": True,
                    #                 "rvm_message": data["message"]
                    #
                    #             }
                    #             y2 = requests.patch(url2, data=data2)
                    #             print(y2)
                    #             # data2 = json.loads(y)
                    #             print(y2.json())
                    #
                    #         else:
                    #             url3 = f'https://www.gravvisoft.com/api/lead/phone/{phoneage}/'
                    #             data3 = {
                    #                 "rvm_sent": False,
                    #                 "rvm_message": data["message"]
                    #
                    #             }
                    #             y3 = requests.patch(url3, data=data3)
                    #             print(y3)
                    #             # data2 = json.loads(y)
                    #             print(y3.json())
                    #     except JSONDecodeError:
                    #         pass

                # { '$and': [ {"industry": { "$in":['Boat Dealership', 'Appliance Repair Service', 'Appliance Sales', 'Appliance Installation',
                #  'Appliance Repair', 'Cooktop, Range & Stove Installation', 'Oven Installation',
                #  'Range Hood Installation', 'Appliance Removal', 'Oven Repair', 'Cooktop, Range & Stove Repair',
                #  'Dishwasher Installation', 'Architectural Designer', 'Cabinets', 'Custom Kitchen Cabinets',
                #  'Custom Cabinets', 'Custom Bathroom Vanities', 'Custom Cabinet Doors', 'Custom Built ins',
                #  'Cabinet Installation', 'Cabinet Sales', 'Custom Entertainment Centers', 'Custom Bookcases',
                #  'Custom Pantries', 'Carpenter', 'Handyman', 'Carpentry', 'Custom Built ins', 'Custom Shelving',
                #  'Custom Bookcases', 'Custom Cabinets', 'Finish Carpentry', 'Custom Furniture',
                #  'Custom Entertainment Centers', 'Custom Pantries', 'Custom Fireplace Mantels', 'Carpet Cleaner',
                #  'Chimney Sweeper', 'Cleaning Service', 'Commercial Cleaning', 'House Cleaning', 'Concrete Contractor',
                #  'Concrete Sales', 'Patio Construction', 'Hardscaping', 'Stone Masonry', 'Retaining Wall Construction',
                #  'Paver Installation', 'Masonry', 'Concrete Construction', 'Stone Installation',
                #  'Concrete Driveway Installation', 'Driveway Sealing', 'Concrete Driveway Installation',
                #  'Concrete Construction', 'Hardscaping', 'Driveway Repair', 'Driveway Resurfacing', 'Asphalt Paving',
                #  'Land Leveling & Grading', 'Paver Installation', 'Masonry', 'Construction Company', 'Contractor',
                #  'General Contracting', 'Home Remodeling', 'Kitchen Remodeling', 'Bathroom Remodeling',
                #  'Home Additions', 'Home Extensions', 'Custom Homes', 'New Home Construction', 'Basement Remodeling',
                #  'Deck Building', 'Kitchen Design', 'Bathroom Design', 'Custom Cabinets', 'Custom Kitchen Cabinets',
                #  'Custom Bathroom Vanities', 'Custom Countertops', '3D Rendering', 'Custom Pantries', 'Home Additions',
                #  'Custom Walk in Closets', 'Countertops', 'Custom Countertops', 'Tile Sales', 'Countertop Sales',
                #  'Countertop Installation', 'Backsplash Installation', 'Tile Installation', 'Natural Stone Countertops',
                #  'Quartz Countertops', 'Granite Countertops', 'Marble Countertops', 'Damage Restoration Service',
                #  'Deck & Patio Builder', 'Pergola Construction', 'Deck Building', 'Patio Construction',
                #  'Porch Design & Construction', 'Gazebo Design & Construction', 'Sunroom Design & Construction',
                #  'Deck Design', 'Trellis Construction', 'Patio Design', 'Pool Deck Design & Construction', 'Doors',
                #  'Door Dealer', 'Custom Exterior Doors', 'Door Sales', 'Exterior Door Installation',
                #  'Custom Interior Doors', 'Custom Folding Doors', 'Interior Door Installation',
                #  'Sliding Door Installation', 'Bifold Doors', 'Custom Retractable Screens', 'Door Repair',
                #  'Electrician', 'Electricians', 'Electrical Installation', 'Electrical Repair', 'Electrical Inspection',
                #  'Circuit Breaker Installation & Repair', 'Lighting Design',
                #  'Electrical Outlet & Light Switch Installation', 'Exhaust Fan Installation', 'House Wiring',
                #  'Deck Lighting Installation', 'Home Energy Audit', 'Elevator Service', 'Fence & Gate Contractor',
                #  'Fence Contractors', 'Driveway Gate Installation', 'Fence Installation', 'Gate Installation',
                #  'Fence Repair', 'Chain Link Fence Installation', 'Gate Repair', 'Fence Sales',
                #  'Wrought Iron Fence Installation', 'Aluminum Fence Installation', 'Wood Fence Installation',
                #  'Fireplaces', 'Fireplace Installation', 'Fireplace Sales', 'Custom Fireplaces',
                #  'Gas Fireplace Installation', 'Custom Fireplace Mantels', 'Custom Fire Pits',
                #  'Wood Stove Installation', 'Electric Fireplace Installation', 'Outdoor Fireplace Construction',
                #  'Fireplace Repair', 'Flooring', 'Carpet Installation', 'Carpet Sales', 'Custom Rugs',
                #  'Custom Flooring', 'Carpet Repair', 'Carpet Stretching', 'Rug Cleaning', 'Carpet Cleaning',
                #  'Flooring Installation', 'Laminate Flooring Installation', 'Custom Flooring',
                #  'Wood Floor Installation', 'Vinyl Flooring Installation', 'Wood Flooring Sales', 'Flooring Sales',
                #  'Tile Installation', 'Laminate Flooring Sales', 'Vinyl Flooring Sales', 'Stair Installation',
                #  'Railing Installation', 'Baluster Installation', 'Staircase Design', 'Railing Repair', 'Stair Repair',
                #  'Glass Railings', 'Furniture', 'Antique Restoration', 'Furniture Refinishing', 'Upholstery Repair',
                #  'Custom Upholstery', 'Custom Furniture', 'Furniture Repair', 'Wall Upholstery', 'Custom Drapery',
                #  'Leather Repair', 'Upholstery Cleaning', 'Furniture Repair & Upholstery Service', 'Custom Furniture',
                #  'Pool Table Repair', 'Furniture Repair', 'Furniture Refinishing', 'Upholstery Repair',
                #  'Antique Restoration', 'Custom Tables', 'Sandblasting', 'Furniture Sales', 'Custom Furniture',
                #  'Outdoor Furniture Sales', 'Furniture Delivery', 'Custom Rugs', 'Custom Tables', 'Lighting Sales',
                #  'Custom Pool Tables', 'Antique Furniture Sales', 'Custom Framing', 'Garage Door Service',
                #  'Garage Door Installation', 'Garage Door Repair', 'Garage Door Installation', 'Garage Door Repair',
                #  'Garage Door Sales', 'Custom Garage Doors', 'Gardener', 'Glass Service', 'Shower Door Installation',
                #  'Shower Door Sales', 'Mirror Installation', 'Glass Installation', 'Shower Door Repair',
                #  'Stained Glass Repair & Design', 'Window Installation', 'Glass Cutting', 'Glass Repair',
                #  'Window Repair', 'Gutter Cleaning Service', 'Handyman', 'Closet Design', 'Custom Walk in Closets',
                #  'Closet Organization', 'Space Planning', 'Custom Cabinets', 'Professional Organizing',
                #  'Garage Storage', 'Decluttering', 'Custom Storage', 'Sports Equipment Storage', 'Kitchen Design',
                #  'Bathroom Design', 'Custom Cabinets', 'Custom Kitchen Cabinets', 'Custom Bathroom Vanities',
                #  'Custom Countertops', '3D Rendering', 'Custom Pantries', 'Home Additions', 'Custom Walk in Closets',
                #  'Heating Ventilating & Air Conditioning Service', 'Air Conditioning & Heating',
                #  'Heating & Cooling Sales & Repair', 'HVAC', 'Air Conditioning Installation', 'Heat Pump Installation',
                #  'HVAC Installation', 'Air Conditioning Repair', 'Furnace Installation', 'Oil to Gas Conversion',
                #  'HVAC Inspection', 'Heating System Installation', 'Ventilation Installation & Repair',
                #  'Thermostat Repair', 'Home Remodeling', 'Kitchen & Bath Contractor', 'Custom Homes', 'Home Remodeling',
                #  'New Home Construction', 'Home Additions', 'Kitchen Remodeling', 'Home Extensions',
                #  'Bathroom Remodeling', 'Architectural Design', 'Kitchen Design', 'Bathroom Design',
                #  'Kitchen Remodeling', 'Bathroom Remodeling', 'Home Remodeling', 'Home Additions',
                #  'Cabinet Installation', 'Custom Cabinets', 'Custom Kitchen Cabinets', 'Home Extensions',
                #  'Custom Bathroom Vanities', 'Custom Countertops', 'Home Improvement', 'Home Security Company',
                #  'House Painting', 'Custom Artwork', 'Texture Painting', 'Decorative Painting', 'Mural Painting',
                #  'Wall Stenciling', 'Faux Painting', 'Stained Glass Repair & Design', 'Custom Framing',
                #  'Art Installation', 'Custom Furniture', 'Interior Design Studio', 'Home Staging',
                #  'Furniture Selection', 'Space Planning', 'Color Consulting', 'Decluttering', 'Downsizing',
                #  'Art Selection', 'Furniture Rental', 'Holiday Decorating', 'Feng Shui Design', 'Interior Design',
                #  'Kitchen Design', 'Bathroom Design', 'Bedroom Design', 'Living Room Design', 'Space Planning',
                #  'Color Consulting', 'Furniture Selection', 'Kids Bedroom Design', 'Dining Room Design', 'Landscaping',
                #  'Landscape Company', 'Landscape Architects & Landscape Designers', 'Landscape Contractors',
                #  'Gardeners & Lawn Care', 'Landscape Construction', 'Hardscaping', 'Landscape Maintenance',
                #  'Garden Design', 'Patio Construction', 'Custom Fire Pits', 'Custom Water Features',
                #  'Paver Installation', 'Outdoor Fireplace Construction', 'Pool Landscaping', 'Planting', 'Lawn Care',
                #  'Irrigation System Installation', 'Weed Control', 'Tree Pruning', 'Brush Clearing',
                #  'Drought Tolerant Landscaping', 'Lawn Aeration', 'Yard Waste Removal', 'Drip Irrigation Installation',
                #  'Lighting', 'Lighting Sales', 'Lighting Design', 'Outdoor Lighting Design', 'Lighting Installation',
                #  'Outdoor Lighting Installation', 'Landscape Lighting Installation', 'Deck Lighting Installation',
                #  'Recessed Lighting Installation', 'Ceiling Fan Installation', 'Pool Lighting Installation',
                #  'Outdoor Lighting Installation', 'Landscape Lighting Installation', 'Lighting Installation',
                #  'Deck Lighting Installation', 'Outdoor Lighting Design', 'Lighting Design', 'Lighting Sales',
                #  'Home Automation', 'Pool Lighting Installation', 'Outdoor Audio Installation', 'Masonry Contractor',
                #  'Moving Service', 'Piano Moving', 'Local Moving', 'Long Distance Moving', 'Painters', 'Painting',
                #  'Door Painting', 'Drywall Repair', 'Interior Painting', 'Drywall Texturing', 'Baseboard Installation',
                #  'Interior Door Installation', 'Door Repair', 'Ceiling Painting', 'Paint Removal',
                #  'Backsplash Installation', 'Paint Sales', 'Wallcovering Sales', 'Paving & Asphalt Service',
                #  'Pest Control Service', 'Plumbing Service', 'Plumbers', 'Plumber', 'Faucet Installation',
                #  'Emergency Plumbing', 'Faucet Repair', 'Water Heater Repair', 'Plumbing Repair', 'Drain Cleaning',
                #  'Garbage Disposal Repair', 'Garbage Disposal Installation', 'Water Heater Installation',
                #  'Tankless Water Heater Installation', 'Water Heater Installation & Repair Service', 'Roofing Service',
                #  'Roof Replacement', 'Gutter Installation', 'Roof Installation', 'Asphalt Shingle Roofing',
                #  'Roof Repair', 'Metal Roofing', 'Roof Inspection', 'Composition Roofing', 'Gutter Repair',
                #  'Soffit Installation', 'Swimming Pool & Hot Tub Service', 'Swimming Pool Cleaner',
                #  'Hot Tub Installation', 'Hot Tub Sales', 'Custom Hot Tubs', 'Sauna Installation', 'Sauna Sales',
                #  'Sauna Repair', 'Pool Liner Replacement', 'Pool and Spa Repair', 'Pool Cleaning & Maintenance',
                #  'Sauna Repair', 'Solar Pool Heating', 'Aboveground Pools', 'Aboveground Pool Liner Replacement',
                #  'Pool Covers', 'Natural Swimming Pools', 'Swimming Pool Design', 'Swimming Pool Construction',
                #  'Pool Deck Design & Construction', 'Pool Lighting Installation', 'Pool Remodeling', 'Custom Hot Tubs',
                #  'Natural Swimming Pools', 'Hot Tub Installation', 'Pond Construction', 'Sauna Installation',
                #  'Tiling Service', 'Tree Cutting Service', 'Tree Pruning', 'Tree Removal', 'Stump Removal',
                #  'Tree Planting', 'Wood Chipping', 'Stump Grinding', 'Hedge Trimming', 'Mulching', 'Land Clearing',
                #  'Window Services', 'Window Replacement', 'Window Installation', 'Custom Windows', 'Window Sales',
                #  'Window Repair', 'Egress Windows', 'Bifold Windows', 'Trim Work', 'Skylight Installation',
                #  'Window Screen Installation', 'Window Installation Service', 'Home Window Service',
                #  'Custom Blinds & Shades', 'Motorized Blinds', 'Blinds & Shades Sales', 'Custom Drapery',
                #  'Blind Installation', 'Plantation Shutters', 'Interior Shutters', 'Custom Retractable Screens',
                #  'Exterior Shades', 'Exterior Shutters', 'Boat / Sailing Instructor', 'Cruise Line', 'Limo Service',
                #  'Private Plane Charter', 'Travel Company', 'Tour Agency', 'Architectural Tour Agency',
                #  'Art Tour Agency', 'Sightseeing Tour Agency', 'Tour Guide', 'Travel Agency', 'Cruise Agency',
                #  'Travel Service'] }, "city": { "$in": ['Gwynn Oak, MD', 'Lutherville Timonium, MD', 'Linthicum Heights, MD', 'Hydes, MD', 'Reisterstown, MD', 'Laurel, MD', 'Fallston, MD', 'Baltimore, MD', 'Clarksville, MD', 'Elkridge, MD', 'Pasadena, MD', 'Monkton, MD', 'Highland, MD', 'Baldwin, MD', 'Phoenix, MD', 'Randallstown, MD', 'Arnold, MD', 'Nottingham, MD', 'Severn, MD', 'Fort George G Meade, MD', 'Savage, MD', 'Jessup, MD', 'Rosedale, MD', 'Essex, MD', 'Crownsville, MD', 'Kingsville, MD', 'Finksburg, MD', 'Columbia, MD', 'Perry Hall, MD', 'Gunpowder, MD', 'Fork, MD', 'Halethorpe, MD', 'Ellicott City, MD', 'Sparks Glencoe, MD', 'Annapolis Junction, MD', 'White Marsh, MD', 'Crofton, MD', 'Millersville, MD', 'Pikesville, MD', 'Hunt Valley, MD', 'Parkville, MD', 'Hanover, MD', 'Sparrows Point, MD', 'Windsor Mill, MD', 'Glen Arm, MD', 'Burtonsville, MD', 'Curtis Bay, MD', 'Edgewood, MD', 'Abingdon, MD', 'Upper Falls, MD', 'Joppa, MD', 'Gambrills, MD', 'Annapolis, MD', 'Middle River, MD', 'Cockeysville, MD', 'Odenton, MD', 'Dundalk, MD', 'Owings Mills, MD', 'Towson, MD', 'Glen Burnie, MD', 'Fulton, MD', 'Severna Park, MD', 'Catonsville, MD'] }}]}

                # cursor = collection.update_many({'rvm_lead_id': {'$exists': False}}, {'$set': {"rvm_lead_id": ""}}).limit(10000)
                # cursor = collection.update_many({'rvm_message': {'$exists': False}}, {'$set': {"rvm_message": ""}}).limit(10000)
                # cursor = collection.update_many({'rvm_sent': {'$exists': False}}, {'$set': {"rvm_sent": False}}).limit(10000)
                # cursor = collection.update_many({'dnc_phone': {'$exists': False}}, {'$set': {"dnc_phone": "False"}}).limit(10000)
                # cursor = collection.update_many({'dnc_email': {'$exists': False}}, {'$set': {"dnc_email": "False"}}).limit(10000)

                # CHECK FOR UNSENT RVM LEADS
                # DELETE_DUPLICATE_PHONE_NUM
                # phone_list = []
                # duplicate_ids = []
                #
                # for dupphone in collection.find():
                #     try:
                #         for match in phonenumbers.PhoneNumberMatcher(dupphone["phone"], "US"):
                #             phoneage = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL)
                #             if phoneage not in phone_list:
                #                 phone_list.append(phoneage)
                #             else:
                #                 duplicate_ids.append(dupphone["_id"])
                #     except KeyError:
                #         pass
                # print(phone_list)
                # print(duplicate_ids)
                #
                # collection.delete_many({"_id": {"$in": duplicate_ids}})
                # collection.update_many({'rvm_sent': {'$exists': False}}, {'$set': {"rvm_sent": False}})
                # collection.update_many({'dnc_phone': {'$exists': False}}, {'$set': {"dnc_phone": "False"}})
                # # collection.update_many({'lead_id': {'$exists': False}}, {'$set': {"lead_id": ""}})
                # # collection.update_many({'lead_message': {'$exists': False}}, {'$set': {"lead_message": ""}})
                # collection.update_many({'rvm_lead_id': {'$exists': False}}, {'$set': {"rvm_lead_id": ""}})
                # collection.update_many({'rvm_message': {'$exists': False}}, {'$set': {"rvm_message": ""}})

                # for c in collection.find():
                #     # for c in collection.find( {"dnc_phone": "False"}):
                #
                #     print(c)
                #     # print(c["_id"])
                #     print(c["phone"])



