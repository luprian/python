#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import logging
import logging.handlers
import os

from bs4 import BeautifulSoup

smtp_handler = logging.handlers.SMTPHandler(mailhost=("relay.foobar.local", 25),
                                            fromaddr="AzureIPUpdate@foobar.org",
                                            toaddrs=["test1@foobar.org",
                                                     "test2@foobar.org"],
                                            subject=u"Azure IP Script update completion status.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(smtp_handler)

namelist = ["AzureCloud.australiacentral", "AzureCloud.australiacentral2",
            "AzureCloud.australiaeast", "AzureCloud.australiasoutheast"]
baseurl = 'https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519'

with requests.Session() as session:
    response = session.get(baseurl)
try:
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    downloadurl = soup.find('span', class_='file-link-view1').find('a')['href']
    response = session.get(downloadurl)
    response.raise_for_status()
    json = response.json()
    if os.path.exists("C:\Test.txt"):
        os.remove("C:\Test.txt")
    for n in json['values']:
        if n['name'] in namelist:
            for ap in n['properties']['addressPrefixes']:
                if ":" not in ap:
                    with open('C:\Test.txt', 'a') as file:
                        file.write(ap + "\n")
except requests.exceptions.HTTPError as e:
    logger.exception(
        "URL is no longer valid, please check the URL that's defined in this script with MS, as this may have changed.\n\n")
except Exception as e:
    logger.exception("Unknown error has occured, please review script")
else:
    logger.info("Script has run successfully! Azure IPs have been updated.")
