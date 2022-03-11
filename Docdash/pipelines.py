import datetime
import json
import ssl
from json import JSONDecodeError

import phonenumbers
import pymongo
import requests


class GravviPipeline(object):
    #
    # def __init__(self):
    #     self.conn = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster1.9f0gx.mongodb.net", ssl_cert_reqs=ssl.CERT_NONE)
    #     db = self.conn["GRAVVISOFT"]
    #     self.collection = db['LEADS']
    #
    #     self.conn2 = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster0.kuvzf.mongodb.net",
    #                                      ssl_cert_reqs=ssl.CERT_NONE)
    #     self.db2 = self.conn2["GRAVVIBOY"]
    #     self.collection2 = self.db2['LEADS']
    #     self.users_profile = self.db2["users_profile"]

    def process_item(self, zitems, spider):
        global datadebounce

        conn = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster1.9f0gx.mongodb.net", ssl_cert_reqs=ssl.CERT_NONE)
        db = conn["GRAVVISOFT"]
        collection = db['LEADS']

        conn2 = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster0.kuvzf.mongodb.net",
                                         ssl_cert_reqs=ssl.CERT_NONE)
        db2 = conn2["GRAVVIBOY"]
        collection2 = db2['LEADS']
        users_profile = db2["users_profile"]
        # cursor = ({'active_client': {'$exists': False}}, {'$set': {"active_client": False}}
        #
        # id_start = getattr(self, "id_start", "")
        # id_end = getattr(self, "id_end", "")
        # user_id = getattr(self, "user_id", "")

        for dbases in users_profile.find(zitems['user__id']):
            # for dbases in itertools.islice(collectionyo.find(batch_size=20), int(id_start), int(id_end)):
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

                zitems["cust_industries"] = cust_industries
                zitems["cust_cities"] = cust_cities

                # leadstoskip = int(dbases["vmd_leads_loaded"]) - int(dbases["vmd_leads_remaining"])
                # print(leadstoskip)
                # conn1 = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster0.kuvzf.mongodb.net",
                #                             ssl_cert_reqs=ssl.CERT_NONE)
                # db1 = conn1[f'{dbases["databasename"]}']
                conn2 = pymongo.MongoClient("mongodb+srv://benslow:Grannyboy1@cluster0.kuvzf.mongodb.net",
                                            ssl_cert_reqs=ssl.CERT_NONE)

                db2 = conn2[f"GRAVVIBOY"]

                collection2 = db2['LEADS']

                for leads in collection2.find(
                        {'$and': [{"industry": {"$in": cust_industries}, "city": {"$in": cust_cities}}]}):

                    # zitems['city'] = leads['city'],
                    # zitems['company'] = leads["company"],
                    # zitems['email'] = leads['email'],
                    # zitems['industry'] = leads['industry'],

                    for match in phonenumbers.PhoneNumberMatcher(leads["phone"], "US"):
                        zitems["phone"] = phonenumbers.format_number(match.number,
                                                                     phonenumbers.PhoneNumberFormat.NATIONAL)

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
                            return gravvi_data

                        except JSONDecodeError:
                            pass

                    ademail = dbases["klentyemail"]
                    adklentyapikey = dbases["klenty_api_key"]
                    adcadenceName = dbases["cadence_name"]
                    ### EMAIL API
                    if not ['email']:
                        return zitems

                    elif ["email"]:
                        try:
                            addprospect = requests.post(
                                f"https://api.debounce.io/v1/?api=5f43170b7690e&email={leads['email']}")
                            datadebounce = json.loads(addprospect.content)
                        except JSONDecodeError:
                            pass
                        if not datadebounce:
                            zitems['free_email'] = None
                            zitems['valid_email'] = None
                            zitems['email_drop'] = None

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

        return zitems
