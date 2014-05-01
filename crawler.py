#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Copyright 2014 Yuan Li, liyuan@villagel.com
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import re
import urllib # urllib is an easy way to download the link 
import csv
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


# Prepare Stock ID List
idFirm = []
idYear = []
csvsource = csv.reader(file("SSE.csv", "rb"))
for line in csvsource:
  idFirm.append(line[0])
  idYear.append(line[1])


# Crawling Reports
browser = webdriver.Firefox()

BASEURL1 = ("http://www.sse.com.cn/assortment/stock/list/"
            "stockdetails/announcement/index.shtml?COMPANY_CODE=")
BASEURL2 = ("&reportType=YEARLY&reportType2=定期公告&reportType=YEARLY&"
            "moreConditions=true")

for n in range(0,50):
  stockID = idFirm[n]
  yearS = int(idYear[n])
  
  if os.path.exists(stockID):
    print stockID + " is already downloaded!"
    continue
  else:
    os.mkdir(stockID)
    os.chdir(stockID)
  
  while (yearS < 2015):
    time.sleep(1)
    yearE = yearS + 3
    url = (BASEURL1 + stockID + "&startDate=" + str(yearS) + "-01-01&endDate="
           + str(yearE) + "-01-01&productID=" + stockID + BASEURL2)
    print "Downloading reports for firm " + stockID + " from " + str(yearS)
    browser.get(url)
    nFile = 0
    try:
      elem = WebDriverWait(browser, 10).until(lambda x: x.find_elements_by_partial_link_text("年报"))
      nFile = len(elem) # Number of links 
    except:
      print "Seems no file on this page"

    if nFile > 0:
      for i in range(nFile):
        # Downloading the file
        toDL = elem[i].get_attribute("href")
        pt = re.compile(stockID + ".*" + ".pdf")
        fName = re.findall(pt, toDL)
        if len(fName) > 0:
          fName = fName[0]
          urllib.urlretrieve(toDL, fName)
          time.sleep(1)
          if not os.path.isfile(fName):
            print "Error: Not Downloaded!"
          else:
            print "Successfully Downloaded " + fName
    yearS = yearS + 3

  os.chdir("..")
  
browser.close()
print "Mission Accomplished!"
