#*******************************************
#Copyright@Sellermania Services Pvt. Ltd.
#Version: 2.0
#Author: Dipankar Nalui, QA Tester, Selermania 
#*******************************************
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os, sys
from time import sleep					
def productApi():
	global driver,base_url, browser, email, pwd, z
	base_url = "http://preprod2.sellermania.com"
	print "Preprod-FR: URL= " + base_url
	print "Choose Your Browser: 1. Firefox 2. Google Chrome "
	browser=input('Your Answer = ')
	email=raw_input('Enter the Email: ')
	pwd=raw_input('Enter the password: ')
	if browser == 1 :
		driver = webdriver.Firefox()
		driver.maximize_window() #To maximize the browser
		print "Browser Maximized"
	else :
		chromedriver = "/home/bala/Desktop/chromedriver"
		os.environ["webdriver.chrome.driver"] = chromedriver
		driver = webdriver.Chrome(chromedriver)
	z = unittest.TestCase('run') #required for z.assertEqual
	driver.implicitly_wait(30)	
	verificationErrors = []
	accept_next_alert = True	
	driver.get(base_url + "/login") #Navigating to login page	
	driver.find_element_by_id("seller_login_loginName").clear()	
	driver.find_element_by_id("seller_login_loginName").send_keys(email)
	driver.find_element_by_id("seller_login_password").send_keys(pwd)
	driver.find_element_by_css_selector("span.metrics").click()
	sleep(4)
	driver.get(base_url + "/language/en") #To display webpage in English
	print "Displaying in English"			
	driver.get(base_url + "/inventory/obo/add_onebyone") #product search page
	#ASIN = B00JVOIRPG
	ASIN_EAN=raw_input('Enter ASIN/EAN = ')
	driver.find_element_by_id("seller_inventory_add_product_onebyone_inputSearchEan").send_keys(ASIN_EAN)
	driver.find_element_by_id("inventory_obosearch_go_item_lookup").click()
	sku=raw_input('Enter SKU = ')
	driver.find_element_by_id("seller_inventory_obo_sku").clear()
	driver.find_element_by_id("seller_inventory_obo_sku").send_keys(sku)#sku
	driver.find_element_by_id("seller_inventory_obo_quantity").clear()
	driver.find_element_by_id("seller_inventory_obo_quantity").send_keys("1")# QTY =1
	driver.find_element_by_id("seller_inventory_obo_offerTags").clear()
	driver.find_element_by_id("seller_inventory_obo_offerTags").send_keys(sku) #Tag
	driver.find_element_by_id("seller_inventory_obo_mkpMatch_description").clear()
	driver.find_element_by_id("seller_inventory_obo_mkpMatch_description").send_keys("Do not buy this product. This is for test.") #Description
	driver.find_element_by_id("seller_inventory_obo_mkpMatch_wishedPrice").clear()
	driver.find_element_by_id("seller_inventory_obo_mkpMatch_wishedPrice").send_keys("999999") #Top price=999999
	driver.find_element_by_id("seller_inventory_obo_mkpMatch_bottomPrice").clear()
	driver.find_element_by_id("seller_inventory_obo_mkpMatch_bottomPrice").send_keys("88888") #bottom price=88888
	sleep(2)
	driver.find_element_by_css_selector("span.metrics").click()
	sleep(3)
	try:	
		success_url= base_url + "/inventory/obo/add_onebyone/inventory.searchProduct.oboSuccessMessage"
		print "checking success/fail..."
		sleep(2)
		if driver.current_url == success_url : #checking if login error
			print 'Item added to your inventory'
			driver.get("http://preprod2.sellermania.com/inventory/")#inventory page
			print 'Navigated to inventory page'
			driver.execute_script("window.scrollTo(0, 500)") #scroll down to adjust viewport height
			print 'Scrolling down to find SKU'
			sleep(2)
			try:
				z.assertEqual(sku,driver.find_element_by_xpath("//*[@id='inventory_table_row_0']/td[3]/div[23]").text)
				print "Success: SKU is displayed in Inventory Page"
			except:
				print "FAILED: OBO - item creation"
		else:
			print "FAILED: Check your input and try again"			
	except:
		print 'Error!'
	

productApi()		
