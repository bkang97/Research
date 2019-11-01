
from bs4 import BeautifulSoup
# from requests_html import AsyncHTMLSession
import requests
import json
import time

import pickle

cookie = """bcLightView=true; market=eyJpdiI6IjdSbDhyQ2syK1hlN2ZMdU9CUHUxcmc9PSIsInZhbHVlIjoiQmliXC83d0hSK2VQYnlHcUF4TThreXc9PSIsIm1hYyI6IjU3ZjNkMDgzMzQ2Nzg5Y2YwN2JhNWY3MGVkNzA0ZGU5NTlmN2E5ZGM1NTAyZDRkZTUwNTYyYTkwNzIyNTI1YzMifQ%3D%3D; XSRF-TOKEN=eyJpdiI6IkhnWXRLVWdTUit6V2NcL3IrWjBYaGZnPT0iLCJ2YWx1ZSI6IlJxN0MwU2ZxdWxIUWR0THplb0ZqSExyRDdrbzREKzd6cnlxQjRicDFZYmd3dlNjeEdLY251XC9nS2RHVWFtNUxaIiwibWFjIjoiMmVkY2ZmZGJlOGFlNDQ4Y2RjZjVkNmU1Y2ZiNTE5MWQzNzNmYTY0YzQxNDZiNGZmMWJlNjViYWJjM2I0N2I2ZSJ9; laravel_session=eyJpdiI6Iklsd2RHV2lvaFlEQWViVDkwRjlxaFE9PSIsInZhbHVlIjoiOVU4RjR0bkk5VWR3ZE5LOTZrbjVtT3JxTkhQNTJPWGFYZDFRNTBEdGszZzFoOHZpUGtFbDhUWWI4WVwvSVM4eVkiLCJtYWMiOiI2NzkxNTFlNmE1ZWQzYWY0MjhlODc5ZTI1OWE4OTI2ZTM1NDBmYzY1OTU5ZTA2OGVhOTQ1NzExN2VmN2M5MTlmIn0%3D"""

xsrf = """eyJpdiI6IkhnWXRLVWdTUit6V2NcL3IrWjBYaGZnPT0iLCJ2YWx1ZSI6IlJxN0MwU2ZxdWxIUWR0THplb0ZqSExyRDdrbzREKzd6cnlxQjRicDFZYmd3dlNjeEdLY251XC9nS2RHVWFtNUxaIiwibWFjIjoiMmVkY2ZmZGJlOGFlNDQ4Y2RjZjVkNmU1Y2ZiNTE5MWQzNzNmYTY0YzQxNDZiNGZmMWJlNjViYWJjM2I0N2I2ZSJ9"""

url = "https://www.barchart.com/proxies/core-api/v1/quotes/get?" \
      "lists=stocks.sectors.sic.us&orderDir=asc&fields=symbol," \
      "sicIndustry,weightedAlpha,weightedAlphaChange,numberOfStocks," \
      "symbolCode,symbolType,lastPrice,dailyLastPrice&orderBy=symbol" \
      "&meta=field.shortName,field.type," \
      "field.description"

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                         "77.0.3865.120 Safari/537.36",
           'Origin': 'https://www.barchart.com',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Referer': 'https://www.barchart.com/stocks/sectors/'
                      'industry-rankings/sic?orderBy=symbol&orderDir=asc',
           'X-xsrf-token':xsrf,
           "cookie":cookie}

res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.content, 'html')
formatted = json.loads(soup.find('p').text)
symbol_list = [formatted['data'][n]['symbol'] for n in range(formatted['count'])]



finallist = []

for symbol in symbol_list:
    print(symbol)
    url = "https://www.barchart.com/proxies/core-api/v1/quotes/get?" \
          "lists=stocks.inSector.by_sic_code(" + symbol + ")&f" \
                                                          "ields=symbol%2CsicIndustry%2CweightedAlpha%2CweightedAlphaChange%2C" \
                                                          "numberOfStocks%2CsymbolCode%2CsymbolType%2ClastPrice%2CdailyLastPrice%2C" \
                                                          "hasOptions&orderBy=weightedAlpha&orderDir=desc&meta=field.shortName%2C" \
                                                          "field.type%2Cfield.description&hasOptions=true&gt(numberOfStocks%2C0)=&raw=1"
    # url = "https://www.barchart.com/proxies/core-api/v1/quotes/get?" \
    #                   "lists=stocks.inSector.all(" + symbol + ")&fields=symbol%2C" \
    #                   "symbolName%2CweightedAlpha%2ClastPrice%2CpriceChange%2C" \
    #                   "percentChange%2ChighPrice1y%2ClowPrice1y%2CpercentChange1y%2C" \
    #                   "tradeTime%2CsymbolCode%2CsymbolType%2ChasOptions&orderBy" \
    #                   "=weightedAlpha&orderDir=desc&meta=field.shortName%2Cfield." \
    #                   "type%2Cfield.description&hasOptions=true&raw=1"

    true_false = True
    while true_false:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html')
        true_false = soup.find('title') != None
        if not true_false:
            break
        time.sleep(5)

    try:
        formatted = json.loads(soup.find('p').text)
        symbol_list2 = [formatted['data'][n]['symbol'] for n in range(formatted['count'])]


        def getSymbol(symbol_list2):
            time.sleep(1)
            for symbol2 in symbol_list2:
                print(symbol2)
                url = "https://www.barchart.com/proxies/core-api/v1/quotes/get?" \
                      "lists=stocks.inSector.by_sic_code(" + symbol2 + ")&f" \
                                                                       "ields=symbol%2CsicIndustry%2CweightedAlpha%2CweightedAlphaChange%2C" \
                                                                       "numberOfStocks%2CsymbolCode%2CsymbolType%2ClastPrice%2CdailyLastPrice" \
                                                                       "%2C" \
                                                                       "hasOptions&orderBy=weightedAlpha&orderDir=desc&meta=field." \
                                                                       "shortName%2C" \
                                                                       "field.type%2Cfield.description&hasOptions=true&gt(numberOfStocks%2C0)" \
                                                                       "=&raw=1"
                url2 = "https://www.barchart.com/proxies/core-api/v1/quotes/get?" \
                       "lists=stocks.inSector.all(" + symbol2 + ")&fields=symbol%2C" \
                                                                "symbolName%2CweightedAlpha%2ClastPrice%2CpriceChange%2C" \
                                                                "percentChange%2ChighPrice1y%2ClowPrice1y%2CpercentChange1y%2C" \
                                                                "tradeTime%2CsymbolCode%2CsymbolType%2ChasOptions&orderBy" \
                                                                "=weightedAlpha&orderDir=desc&meta=field.shortName%2Cfield." \
                                                                "type%2Cfield.description&hasOptions=true&raw=1"

                true_false = True
                while true_false:
                    res2 = requests.get(url2, headers=headers)
                    soup2 = BeautifulSoup(res2.content, 'html')
                    true_false = soup2.find('title') != None
                    if not true_false:
                        break
                    time.sleep(5)
                found = soup2.find('p')
                if found != None:
                    formatted2 = json.loads(found.text)
                    if json.loads(soup.find('p').text)['count'] == 0:
                        true_false = True
                        while true_false:
                            res2 = requests.get(url, headers=headers)
                            soup2 = BeautifulSoup(res2.content, 'html')
                            true_false = soup2.find('title') != None
                            if not true_false:
                                break
                            time.sleep(5)
                        formatted2 = json.loads(soup2.find('p').text)
                    symbol_list3 = [formatted2['data'][n]['symbol']
                                    for n in range(formatted2['count'])]
                    if (symbol_list3[0][0] != '-'):
                        finallist.append(symbol_list3)
                    elif len(symbol_list3) > 0:
                        getSymbol(symbol_list3)
                    else:
                        print('ERROR')
                else:
                    print('Error')


        getSymbol(symbol_list2)
    except:
        pass

with open('groupedStocks.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(finallist, filehandle)
with open('dump.txt','w') as file:
    for listitem in finallist:
        file.write('%s\n' % listitem)