#*******************************************
##Export Order parallel
#Copyright@Sellermania Services Pvt. Ltd.
#Version: 4
#Author: Dipanakr Nalui, QA Tester, Selermania 
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
from selenium.webdriver.common.action_chains import ActionChains
from multiprocessing import Process

# To print in red color if any testing faliure 
def red(name):
    print ("\033[91m {}\033[00m" .format(name)) 
def open_new_browser(email,pwd,caid):
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
        driver.maximize_window()
	print "Browser Window Maximized" + ", CAID = " + caid 
	driver.find_element_by_id("seller_login_loginName").send_keys(email) #email
	driver.find_element_by_id("seller_login_password").send_keys(pwd) #password
	sleep(2)
	driver.find_element_by_css_selector("span.metrics").click() #login button click
	print "Logged in... Email = " + email + ", CAID = " + caid 	
	sleep(2)
	driver.get(base_url + "/language/en") # display webpage in English
	print "Displaying page in English" + ", CAID = " + caid 
	sleep(2)
	#--------------order page ----------------------------------------
	driver.get(base_url + "/orders/search/firstFilter") #Order page # All orders
	print "Navigated to Order Page" + ", CAID = " + caid 
	sleep(2)
	driver.find_element_by_id("idaucun").click()
	print "Clicked: All Orders" + ", CAID = " + caid 
	sleep(3)
	driver.find_element_by_xpath("//*[@id='selectAll']/span").click() #checkbox to select all orders
	print "Checkbox: checked"  + ", CAID = " + caid 
	sleep(3)
	driver.execute_script("window.scrollTo(0, 300)") #scroll down to adjust viewport height
	print "Order Page (All orders): Scrolling down to adjust viewport"  + ", CAID = " + caid 
	sleep(2)
	element_to_hover_over = driver.find_element_by_xpath("//*[@id='orders_menu']/div/div/ul/li/a") #select what you want to do
	print "Mouse Hover: Select what you want to do" + ", CAID = " + caid 
	hover = ActionChains(driver).move_to_element(element_to_hover_over)
	hover.perform()
	sleep(2)
	element_to_hover_over = driver.find_element_by_xpath("//*[@id='orders_menu']/div/div/ul/li/ul/li[8]/a") #Export Orders
	hover = ActionChains(driver).move_to_element(element_to_hover_over)
	hover.perform()
	print "Mouse Hover: Export Orders" + ", CAID = " + caid 
	sleep(2)
	element_to_hover_over = driver.find_element_by_xpath("//*[@id='orders_menu']/div/div/ul/li/ul/li[8]/ul/li[1]/a") #Export Orders to Excel * Hover
	hover = ActionChains(driver).move_to_element(element_to_hover_over)
	hover.perform()
	sleep(2)
	driver.find_element_by_xpath("//*[@id='orders_menu']/div/div/ul/li/ul/li[8]/ul/li[1]/a").click() #click Export Orders to Excel
	print "Order Exported to excel file. Please save the file"  + ", CAID = " + caid 

def main():
	global driver,base_url, browser, website, z
	#---------------input from User at run time-------------	
	if len(sys.argv) > 1: #command line argument
	    	customerFile = sys.argv[1] #customer Details file
    		red('WARNING: DO NOT TOUCH MOUSE AND KEYBOARD ONCE THE BROWSERS ARE OPENED') 
		red('Choose Your Browser: 1. Firefox 2. Google Chrome') 
		browser=input('Your Answer = ')
		red('Which Website do you want to test?')
		print "1. preprod 2. test.prepreprod 3. production" 	
		website=input('Your Answer = ')		
		processes = []	
		for line in open(customerFile): #read customer details from file
			caid,email,pwd=line.split(',',4)
			#print "Checking Main()... Email = " + email + ", CAID = " + caid + ",PWD= " + pwd		
			p=Process(target=open_new_browser, args=(email,pwd,caid)) 
			p.start()
			processes.append(p)
		for p in processes:
			p.join()
		print "finished"
	else: 
		print "Usage: Enter the input file as Command line argument" 
		print "Example: $python test.py customer.txt"
main()


	
    		
		



