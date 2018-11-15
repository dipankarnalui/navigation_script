#*******************************************
#Sellermania: inventory file upload Script
#Copyright@Sellermania Services Pvt. Ltd.
#Version: 2.0
#Author: Dipankar Nalui, QA Tester, Selermania 
#*******************************************
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os, sys
from time import sleep
from multiprocessing import Process

# To print in red color if any testing faliure 
def red(name):
    print ("\033[91m {}\033[00m" .format(name)) #added by dipankar
def open_new_browser(email,pwd,caid,csvFile):
	#-----------------Selection of website------------	
	if website==1 :
		base_url = "https://preprod2.sellermania.com"
	elif website==2 :			
		base_url = "http://test.preprod2.sellermania.com"
	elif website==3 :
		base_url = "https://membres.sellermania.com"
	else:
		red('Invalid Input! Please try again...')
	#-----------------Selection of browser------------
	if browser == 1 :
		driver = webdriver.Firefox()
	else :
		chromedriver = "/home/bala/Desktop/chromedriver"
		os.environ["webdriver.chrome.driver"] = chromedriver
		driver = webdriver.Chrome(chromedriver)		
	z = unittest.TestCase('run')
	driver.implicitly_wait(30)	
	verificationErrors = []
	accept_next_alert = True
	#----------------Openning the login page and Enter Email & password--------------------
	driver.get(base_url + "/login")
	driver.find_element_by_id("seller_login_loginName").send_keys(email) #email
	driver.find_element_by_id("seller_login_password").send_keys(pwd) #password
	sleep(3)
	driver.find_element_by_css_selector("span.metrics").click() #login button click
	print "Logged in... Email = " + email + ", CAID = " + caid 
	sleep(3)
	driver.get(base_url + "/language/en") # display webpage in English	
	sleep(3)
	driver.get( base_url + "/inventory/send_txt_file") #inventory file upload page
	print "Navigated to 'Upload an inventory file' page"
	sleep(3)
	filePath=os.path.abspath(csvFile) #csv file        
	driver.find_element_by_id("seller_inventory_add_product_sendtxtfile_uploadTxtFile").send_keys(filePath)
	sleep(3)
	driver.find_element_by_xpath("//*[@id='inventorySendTxtFileFormSubmit']/span[2]/span").click() #submit
	print "File received, waiting for import"
	sleep(3)
	driver.close()
def main():
	global driver,base_url, browser, website, z, csvFile, currentTime
	customer_account_id =''
	print "Timestamp: " + time.strftime('%Y-%m-%d %H:%M:%S')
	#---------------input from User at run time-------------	
	if len(sys.argv) > 2: #command line argument
	    	customerFile = sys.argv[1] #customer Details file
		csvFile = sys.argv[2] #inventory csv file
    		red('WARNING: DO NOT TOUCH MOUSE AND KEYBOARD ONCE THE BROWSERS ARE OPENED') 
		red('Choose Your Browser: 1. Firefox 2. Google Chrome') 
		browser=input('Your Answer = ')
		red('Which Website do you want to test?')
		print "1. preprod 2. test.prepreprod 3. production" 	
		website=input('Your Answer = ')		
		processes = []			
		for line in open(customerFile): #read customer details from file
			caid,email,pwd=line.split(',',4)
			customer_account_id= customer_account_id +","+ caid				
			p=Process(target=open_new_browser, args=(email,pwd,caid,csvFile)) 
			p.start()
			processes.append(p)
		for p in processes:
			p.join()
		print "finished"
		red('Run the following SQL Query to fetch the result data')
		print "select inventory_upload_id,customer_account_id,inventory_upload_type, inventory_upload_status,upload_date,last_update,original_file_name from  inventory_upload where customer_account_id  in (" + customer_account_id + ")  ORDER BY inventory_upload_id desc limit 8;"	
	else: 
		red('Usage: Enter the input file as Command line argument')
		print "Example: $python test.py customer.txt inventory_upload_sku.csv"
main()

