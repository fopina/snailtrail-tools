from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

ff_driver = webdriver.Firefox()
ff_driver.get('https://api.snailtrail.art/graphql')
sleep(2)
x = ff_driver.execute_script(r'''
return fetch("https://api.snailtrail.art/graphql/", {
    "credentials": "omit",
    "headers": {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.5",
        "content-type": "application/json",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    },
    "referrer": "https://api.snailtrail.art/graphql/",
    "body": "{\"operationName\":\"getM\",\"variables\":{},\"query\":\"query getM {\\n  marketplace_stats_promise(market: 1) {\\n    __typename\\n  }\\n}\\n\"}",
    "method": "POST",
    "mode": "cors"
}).then(data => data.json());
''')
print(x)