ER End-to-End Test
===

Welcome to Etu Recommander/Insight! This document will show you how to use `python + selenium + phantomjs` to simulating user behavior and verify the whole software functionality.

- ## Enviorment Setup

	- python
	```
	### install homebrew first
	$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	$ export PATH=/usr/local/bin:/usr/local/sbin:$PATH

	### install python via homebrew
	$ brew install python
	```

	- selenium
	```
	$ pip install selenium
	```

	- firefox (default bouwser driver in selenium)
	```
	### install brew-cask first
	$ brew tap phinze/homebrew-cask
	$ brew install brew-cask

	### install firefox via brew-cask
	$ brew cask install firefox
	```

	- phantomjs (quick and lightweight alternative)
	```
	$ brew update && brew install phantomjs
	```

- ## Test Data Preparation

	- Input: 
		- csv files `web_test_[camp/cat/src/funnel].csv` which describe actions for each robot.
		- python script `web_test.py` which control the robots.
		
		Put them all together under your test project directory.

	- Format: 

	| Field | Type | Description |
	|---|---|---|
	| date | timestamp | Date of action |
	| Time | timestamp | Time of action |
	| ssid | string | Session ID |
	| uid | string | User ID |
	| eruid | string | Tracking UID |
	| lo | boolean | Login flag |
	| act | string | Action |
	| cat | string | Category (view) |
	| pid | string | Product ID (view) |
	| pcat | string | Category (payment) |
	| paypid | string | Product ID (payment) |
	| qty | int | Order quantity |
	| unit_price | int | Price of each product |
	| oid | string | Order ID |
	| amt | int | Total amount of payment |
	| ERCAMP | string | Campaign ID |
	| ERAD | string | Advertising ID |

	- Example: [web_test_funnel.csv](https://github.com/suensummit/erjsTesting/blob/gh-pages/web_test_funnel.csv)

	| date | Time | ssid | uid | eruid | lo | act | cat | pid | pcat | paypid | qty | unit_price | oid | amt | ERCAMP | ERAD |
	|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
	| 1201 | 11:10 | S01 | U01 | ERU01 | 0 | VIEW | "CAT01_1,CAT01_2,CAT01_3,CAT01_4,CAT01_5" | PID01 |  |  |  |  |  |  | CAMP1 | AD1.1 |
	| 1201 | 11:30 | S02 | U02 | ERU02 | 0 | VIEW | "CAT02_1,CAT02_2,CAT02_3,CAT02_4,CAT02_5" | PID02 |  |  |  |  |  |  | CAMP2 | AD2.1 |
	| 1201 | 11:50 | S03 |  | ERU03 | 0 | VIEW | "CAT03_1,CAT03_2,CAT03_3,CAT03_4,CAT03_5" | PID03 |  |  |  |  |  |  | CAMP1 | AD1.2 |
	| 1201 | 12:10 | S04 |  | ERU04 | 0 | VIEW | "CAT04_1,CAT04_2,CAT04_3,CAT04_4,CAT04_5" | PID04 |  |  |  |  |  |  | CAMP2 | AD2.1 |
	| 1201 | 12:30 | S05 |  | ERU05 | 0 | VIEW | "CAT01_1,CAT01_2,CAT01_3,CAT01_4,CAT01_5" | PID01 |  |  |  |  |  |  | CAMP2 | AD2.1 |
	| 1201 | 12:50 | S06 |  | ERU06 | 0 | VIEW | "CAT02_1,CAT02_2,CAT02_3,CAT02_4,CAT02_5" | PID02 |  |  |  |  |  |  | CAMP2 | AD2.3 |
	| 1201 | 13:10 | S07 |  | ERU07 | 0 | VIEW | "CAT03_1,CAT03_2,CAT03_3,CAT03_4,CAT03_5" | PID03 |  |  |  |  |  |  | CAMP2 | AD2.2 |
	| 1201 | 13:30 | S08 | U08 | ERU08 | 0 | VIEW | "CAT04_1,CAT04_2,CAT04_3,CAT04_4,CAT04_5" | PID04 |  |  |  |  |  |  | CAMP1 | AD1.3 |
	| 1201 | 13:50 | S08 | U08 | ERU08 | 0 | VIEW | "CAT01_1,CAT01_2,CAT01_3,CAT01_4,CAT01_5" | PID04 |  |  |  |  |  |  | CAMP1 | AD1.3 |
	| 1201 | 14:10 | S09 | U09 | ERU09 | 1 | VIEW | "CAT01_1,CAT01_2,CAT01_3,CAT01_4,CAT01_5" | PID01 |  |  |  |  |  |  | CAMP2 | AD2.2 |
	| 1201 | 14:30 | S10 | U10 | ERU10 | 1 | VIEW | "CAT01_1,CAT01_2,CAT01_3,CAT01_4,CAT01_5" | PID01 |  |  |  |  |  |  | CAMP2 | AD2.2 |
	| 1201 | 14:50 | S11 | U11 | ERU11 | 1 | VIEW | "CAT02_1,CAT02_2,CAT02_3,CAT02_4,CAT02_5" | PID02 |  |  |  |  |  |  | CAMP1 | AD1.2 |
	| 1201 | 15:10 | S12 | U12 | ERU12 | 1 | VIEW | "CAT03_1,CAT03_2,CAT03_3,CAT03_4,CAT03_5" | PID03 |  |  |  |  |  |  |  |  |
	| 1201 | 15:30 | S13 | U13 | ERU13 | 1 | VIEW | "CAT04_1,CAT04_2,CAT04_3,CAT04_4,CAT04_5" | PID04 |  |  |  |  |  |  |  |  |
	| 1201 | 15:50 | S14 | U14 | ERU14 | 1 | VIEW | "CAT01_1,CAT01_2,CAT01_3,CAT01_4,CAT01_5" | PID01 |  |  |  |  |  |  |  |  |
	| 1201 | 16:10 | S15 | U15 | ERU15 | 1 | VIEW | "CAT02_1,CAT02_2,CAT02_3,CAT02_4,CAT02_5" | PID02 |  |  |  |  |  |  |  |  |
	| 1201 | 16:30 | S09 | U09 | ERU09 | 1 | CART |  |  | "CAT01_1,CAT01_2,CAT01_3,CAT01_4,CAT01_5" | PID01 | 2 | 100 |  | 200 |  |  |
	| 1201 | 16:50 | S10 | U10 | ERU10 | 1 | CART |  |  | "CAT01_1,CAT01_2,CAT01_3,CAT01_4,CAT01_5" | PID01 | 1 | 100 |  | 100 |  |  |
	| 1201 | 17:10 | S11 | U11 | ERU11 | 1 | CART |  |  | "CAT02_1,CAT02_2,CAT02_3,CAT02_4,CAT02_5" | PID02 | 1 | 200 |  | 200 |  |  |
	| 1201 | 17:30 | S12 | U12 | ERU12 | 1 | CART |  |  | "CAT03_1,CAT03_2,CAT03_3,CAT03_4,CAT03_5" | PID03 | 1 | 300 |  | 300 |  |  |
	| 1201 | 17:50 | S13 | U13 | ERU13 | 1 | CART |  |  | "CAT04_1,CAT04_2,CAT04_3,CAT04_4,CAT04_5" | PID04 | 1 | 400 |  | 400 |  |  |
	| 1201 | 18:10 | S09 | U09 | ERU09 | 1 | ORDER |  |  | "CAT01_1,CAT01_2,CAT01_3,CAT01_4,CAT01_5" | PID01 | 2 | 100 | O01 | 200 |  |  |

- ## Usage

	```
	### run the python script under project folder 
	$ python web_test.py
	```

- ## Lookup Python Script Step-by-step

	- Import dependency libraries
	```
	from selenium import webdriver
	from pandas import *
	import csv
	import time
	```

	- Load test csv data for different scenario
	```
	#with open('web_test_cat.csv', 'rb') as f: 
	#with open('web_test_src.csv', 'rb') as f:
	#with open('web_test_funnel.csv', 'rb') as f:
	with open('web_test_camp.csv', 'rb') as f:
	reader = csv.reader(f)
	testbot_raw = list(reader)
	```

	- Build up well-structured robot dataframe
	```
	testbot = sorted(testbot_raw, key=lambda testbot_raw: testbot_raw[2])
	df = DataFrame(testbot, columns = testbot[len(testbot)-1])
	```

	- Target url setting and initializing web browser driver(s)
	```
	url = "http://localhost/"
	#url = "file:///Users/summitsuen/Documents/erjsTesting/index.html"
	#url = "https://suensummit.github.io/erjsTesting/"

	# initialize drivers
	driver = {}
	k = 0
	ssid = df.ssid.unique()
	while k < len(ssid)-1:
		key = ssid[k]
		value = webdriver.PhantomJS()
		#value = webdriver.Firefox()
		driver[key] = value
		k += 1
	```

	- Send actions from robot dataframe
	```
	# send actions from testbot
	for k in range(len(df)-2):
		driver[df.ssid[k]].get(url)
		driver[df.ssid[k]].find_element_by_id('agroup').send_keys("ER")
		driver[df.ssid[k]].find_element_by_id('acid').send_keys("ER_web_testing")
		driver[df.ssid[k]].find_element_by_id('auid').send_keys(df.uid[k])
		if df.lo[k] == '0':
			driver[df.ssid[k]].find_element_by_id('auid').send_keys("")
			pass
		driver[df.ssid[k]].find_element_by_id('aact').send_keys(df.act[k])
		driver[df.ssid[k]].find_element_by_id('acat').send_keys(df.cat[k])
		driver[df.ssid[k]].find_element_by_id('apid').send_keys(df.pid[k])
		driver[df.ssid[k]].find_element_by_id('apcat').send_keys(df.pcat[k])
		driver[df.ssid[k]].find_element_by_id('apaypid').send_keys(df.paypid[k])
		driver[df.ssid[k]].find_element_by_id('aunit_price').send_keys(df.unit_price[k])
		#driver[df.ssid[k]].find_element_by_id('apmk').send_keys(df.pmk[k])
		driver[df.ssid[k]].find_element_by_id('aqty').send_keys(df.qty[k])
		driver[df.ssid[k]].find_element_by_id('aercamp').send_keys(df.ERCAMP[k])
		driver[df.ssid[k]].find_element_by_id('aerad').send_keys(df.ERAD[k])
		#print 'It is the ' + str(k+1) + 'th testbot\n'
		driver[df.ssid[k]].find_element_by_id('custom-click').click()
		# Take screenshot for verify
		#driver[df.ssid[k]].save_screenshot('screenshot_' + str(k+1) + '.png')

	# close jobs
	for k in range(len(ssid)-1):
		driver[ssid[k]].quit
	```

---
2015-01-20 last edited by [Summit Suen](https://github.com/suensummit)