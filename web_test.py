from selenium import webdriver

# url = "https://shopping.udn.com/mall/Cc1a00.do"
url = "https://"

for x in testbot:
	for action in act_list:
		driver = webdriver.PhantomJS()
		driver.set_window_size(1120, 550)
		driver.get(url)
		driver.find_element_by_id().send_keys()
		driver.find_element_by_id().click()
		driver.quit()

