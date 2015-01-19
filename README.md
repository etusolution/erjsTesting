# ER/EI End-to-End Test

Welcome to Etu Insight! This document will show you how to use `python + selenium + phantomjs` to simulating user behavior and verify the whole software functionality.

- ## Enviorment Setup
	- python
	```
	# install homebrew first
	ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	export PATH=/usr/local/bin:/usr/local/sbin:$PATH

	# install python via homebrew
	brew install python
	```

	- selenium
	```
	pip install selenium
	```

	- Firefox (default bouwser driver in selenium)
	```
	# install brew-cask first
	brew tap phinze/homebrew-cask
	brew install brew-cask

	# install firefox via brew-cask
	brew cask install firefox
	```

	- phantomjs (quick and lightweight alternative)
	```
	brew update && brew install phantomjs
	```

- ## Test Data Preparation
	- input: csv files which describe actions for each robot.

	- example: 

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

- ## How to use test python codes
