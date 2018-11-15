#*******************************************
#Sellermania Webpage Navigation Script
#Copyright@Sellermania Services Pvt. Ltd.
#Version: 5.0
#Author: Dipankar Nalui, QA Tester, Selermania 
#*******************************************
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os, sys
from time import sleep
from bs4 import BeautifulSoup #html parser

# To print in red color if any testing faliure 
def red(name):
    print ("\033[91m {}\033[00m" .format(name)) #added by dipankar

def browser_open():
	global driver,base_url, browser, website, z, email, pwd
	#---------------input from User at run time-------------
	red('WARNING: DO NOT TOUCH MOUSE AND KEYBOARD ONCE THE BROWSERS ARE OPENED')
	print "This script checks only the webpage/weblink navigations. It does not check any functionality."
	red('Choose Your Browser: 1. Firefox 2. Google Chrome') 
	browser=input('Your Answer = ')
	red('Which Website do you want to test?')
	print "1. Preprod-FR 2. Test.Preprod-FR 3. Production-FR"	
	website=input('Your Answer = ')
	email=raw_input('Enter the Email: ')
	pwd=raw_input('Enter the password: ')
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
		driver.maximize_window() #To maximize the browser
		print "Browser Maximized"
	else :
		chromedriver = "/home/bala/Desktop/chromedriver"
		os.environ["webdriver.chrome.driver"] = chromedriver
		driver = webdriver.Chrome(chromedriver)
			
	#driver.set_page_load_timeout(30)		
	z = unittest.TestCase('run') #required for z.assertEqual
	driver.implicitly_wait(30)	
	verificationErrors = []
	accept_next_alert = True
	#----------------Openning the login page-----------------
	driver.get(base_url + "/login") #Navigating to login page	
def check_login():
	#-------------Enter Email and password-----------------
	driver.find_element_by_id("seller_login_loginName").clear()	
	driver.find_element_by_id("seller_login_loginName").send_keys(email)
	driver.find_element_by_id("seller_login_password").send_keys(pwd)
	driver.find_element_by_css_selector("span.metrics").click()				
def main():
	browser_open()	
	check_login()
	login_url= base_url + "/login"
	print "URL= " + driver.current_url
	print "checking login..."
	sleep(4)
	try:
		z.assertEqual(u"LOGIN - IDENTIFICATION",driver.find_element_by_tag_name("h3").text)
		red("Login Error!")
	except: 
		driver.get(base_url + "/language/en") #To display webpage in English
		print "Displaying webpage in English"	
		page_source=driver.page_source
		soup = BeautifulSoup(page_source,'html.parser') #parsing the html page
		navi_all = soup.find_all(id=re.compile("^navbar_"))
		a= re.compile('navbar_(.*?)"')
		navi = a.findall('%s'%navi_all)
		for j in navi:
			print j
			driver.find_element_by_id("navbar_%s"%j).click()
			sleep(2)
			func = 'display_%s_page()'%j
			print func
			eval(func)
			print ("Successfully navigated to %s Page"%j)
		print "DONE."		
def display_home_page():
	print "Checking the contents of the Navigation bar"	
	try:		
		driver.find_element_by_id("nav")
	except: 
		red("Failure: Navigation bar")
	try:
		z.assertEqual(u"Home",driver.find_element_by_id("navbar_home").text)
	except: 
		red("Failure: Home")
	try:
		z.assertEqual(u"Orders",driver.find_element_by_id("navbar_orders").text)
	except:
		red("Failure: Orders")
	try:
		z.assertEqual(u"Inventory",driver.find_element_by_id("navbar_inventory_button").text)
	except:
		red("Failure: Inventory")
	try:
		z.assertEqual(u"Analytics",driver.find_element_by_id("navbar_stats").text)
	except:
		red("Failure: Analytics")
	try:
		z.assertEqual(u"Mapper",driver.find_element_by_id("navbar_mapper").text)#This differs from DE and UK 
	except:
		red("Failure: Mapper")
	try:
		z.assertEqual(u"Strategy",driver.find_element_by_id("navbar_pricing").text) #This differs from DE and UK 
	except:
		red("Failure: Strategy")
	try:
		z.assertEqual(u"Settings",driver.find_element_by_id("navbar_settings").text)
	except:
		red("Failure: Settings")
	try:
		z.assertEqual(u"Your account",driver.find_element_by_id("navbar_account").text)
	except:
		red("Failure: Your Accounts")
	print "HOME PAGE: Navigation Bar and its contexts are good"
	print "================================================================================================="
	print "                                          HOME PAGE                                              "
	print "================================================================================================="
	print "----------------------------------Manage your inventory Box--------------------------------------"	
	try:
		z.assertEqual(u"Home",driver.find_element_by_id("page_title").text)
	except: 
		red("Failure: Home Page Title")
	try:
		z.assertEqual(u"MANAGE YOUR INVENTORY\nAdd single items\nSearch by title or bar code and add items.\nUpload a txt file\nUpload your whole inventory in a single text file.\nImport your Amazon listings directly and automatically\nClick a button and import your inventory effortlessly into Sellermania.\nDisplay your inventory\nDisplay your inventory of out-of-stock items\nCheck the success of your inventory uploads",driver.find_element_by_id("manage_inventory").text)
		
		print "Success:Manage your inventory Box"
	except: 
		red("Failure: Manage your Inventory box")	
	#------------------------ checking obo link from home---------------------------	
	driver.find_element_by_id("home_add_one_by_one").click()
	print "Manage your Inventory box:: Clicked: Add single items " 
	sleep(2)
	try:		
		z.assertEqual(u"Add an item to your inventory",driver.find_element_by_tag_name("h1").text) 
		print "Navigated To --> Add an item to your inventory"
	except: 
		red("Failure:: Add single items")
	sleep(2)
	driver.find_element_by_id("navbar_home").click() #To go back to home
	print "<---Going back to home page"
	#----------------------- checking file upload link from home----------------------------------
      	driver.find_element_by_id("home_send_txt_file").click()
	print "Manage your Inventory box:: Clicked: Upload a txt file"
	sleep(2)
	try:		
		z.assertEqual(u"Upload an inventory file",driver.find_element_by_tag_name("h1").text) #Upload an inventory file == h1 = html tag
		print "Navigated To --> Upload an inventory file"		 
	except: 
		red("Failure:: Upload a txt file")
	sleep(2)
	driver.find_element_by_id("navbar_home").click() # go back to home
	print "<--Going back to home page"
	#-------------------------------checking import link from home---------------------
	driver.find_element_by_id("home_import").click() 
	print "Manage your Inventory box:: Clicked: Import your Amazon listings directly and automatically "  		
	sleep(2)	
	try:
		z.assertEqual(u"Choose your import options into Sellermania",driver.find_element_by_tag_name("h1").text) 
		print "Navigated To --> Choose your import options into Sellermania"
	except: 
		red("Failure: Import your Amazon listings directly and automatically")
	sleep(2)
	driver.find_element_by_id("navbar_home").click() #go back to home
	print "<---Going back to home page" 
	#------------------------------checking inventory link from home------------------
	driver.find_element_by_id("home_see_inventory").click() 
	print "Manage your Inventory box:: Clicked: Display your inventory"
	sleep(2)	
	try:			
		z.assertEqual(u"Your inventory",driver.find_element_by_tag_name("h1").text) 
		print "Navigated To -->  Your inventory"
	except:
		red("Failure: Display your inventory")
	sleep(2)
	driver.find_element_by_id("navbar_home").click()
	print "<--Going back to home page" 
	#------------------------------checking out-of-stock link from home-----------------
	driver.find_element_by_id("home_see_out_of_stock").click()
	print "Manage your Inventory box:: Clicked: Display your inventory of out-of-stock items"
	sleep(2)
	try:
		z.assertEqual(u"Your items out of stock",driver.find_element_by_tag_name("h1").text)
		print "Navigated To --> Your items out of stock"
	except: 
		red("Faliure: Your items out of stock")		
	sleep(9)
	try:		
		z.assertEqual(u"Listing of your out of stock items",driver.find_element_by_tag_name("h1").text)
		print "Navigated To --> Listing of your out of stock items"
	except: 
		red("Faliure: TIME OUT ERROR: Listing of your out of stock items")
	sleep(2)
	driver.find_element_by_id("navbar_home").click()
	print "<---Going back to home page" 
	#----------------------------checking check-load link from home-----------------
	driver.find_element_by_id("home_verify_uploaded_files").click()
	print "Manage your Inventory box:: Clicked: Check the success of your inventory uploads"
	sleep(2)	
	try:
		z.assertEqual(u"Check the success of your inventory uploads",driver.find_element_by_tag_name("h1").text)
		print "Navigated To --> Check the success of your inventory uploads"		
	except: 
		red("Failure: check-load link from home")
	sleep(2)
	driver.find_element_by_id("navbar_home").click()
	print "<---Going back to home page" 
	print "----------------------------------Manage your Orders Box--------------------------------------"
	try:	
		sleep(2)
		z.assertEqual(u"MANAGE YOUR ORDERS\nCheck your orders\nChange the status of your customer orders, send confirmation emails, print packing slips...\nConfirm your orders\nLoad a confirmation or cancellation order file, with your tracking numbers.\nSee and edit your settings\nCreate email templates, set your packing slips settings, upload your logo...",driver.find_element_by_id("manage_orders").text)
		print "Success: Manage your Orders< box"
	except:
		red("Failure: Manage your Orders")
	#------------------------------Check your orders--------------------
	sleep(2)
	driver.find_element_by_id("home_see_order_page").click()
	print "Manage your Orders box:: Clicked: Check your orders"
	sleep(2)
	try:
		z.assertEqual(u"Your Orders",driver.find_element_by_tag_name("h1").text)
		print "Navigated To --> Your Orders"
	except:
		red("Failure: Manage your Orders box:: Check your orders")
	sleep(2)	
	driver.find_element_by_id("navbar_home").click()
	print "<---Going back to home page" 
	sleep(2)
	#----------------Confirm your orders------------------
	driver.find_element_by_id("home_orders_followup").click()
	print "Manage your Orders box:: Clicked: Confirm your orders"
	sleep(2)
	try:			
		z.assertEqual(u"Order handling",driver.find_element_by_tag_name("h1").text)
		print "Navigated To --> Order handling"		
	except:
		red("Failure: Manage your Orders box:: Confirm your orders")
	sleep(2)
	driver.find_element_by_id("navbar_home").click()
	print "<---Going back to home page"
	sleep(2)
	#------------------------See and edit your settings---------------------
	driver.find_element_by_id("home_see_settings").click()
	print "Manage your Orders box:: Clicked: See and edit your settings"
	sleep(2)
	try:			
		z.assertEqual(u"Your preferences",driver.find_element_by_tag_name("h1").text)
		print "Success: Manage your Orders box:: See and edit your settings"
	except:
		red("Failure: Manage your Orders box:: See and edit your settings")
	sleep(2)	
	driver.find_element_by_id("navbar_home").click()
	print "<---Going back to home page" 
	sleep(2)
	#------------------------MANAGE YOUR PRICE STRATEGY BOX---------------------
	print "-----------------------------------MANAGE YOUR PRICE STRATEGY BOX-------------------------------"
	try:			
		z.assertEqual(u"MANAGE YOUR PRICE STRATEGY\nDisplay and modify your price strategy\nSet your pricing strategy, depending on your competitors and your item conditions.",driver.find_element_by_id("manage_strategy").text)
	except:
		red("Failure: MANAGE YOUR PRICE STRATEGY BOX: Display and modify your price strategy")
	driver.find_element_by_id("home_see_strategy").click()
	print "Manage your Orders box:: Clicked: Display and modify your price strategy"
	sleep(2)
	try:
		z.assertEqual(u"Choose Your Price Strategy",driver.find_element_by_tag_name("h1").text)	
		print "Navigated to ----> Choose Your Price Strategy"	
	except: 
		red("Failure: Manage your Orders box:: Display and modify your price strategy")
	sleep(2)
	driver.find_element_by_id("navbar_home").click()
	print "<---Going back to home page"
	sleep(2)

	#-------------------MANAGE YOUR ACCOUNT Box----------------
	print "--------------------------------------MANAGE YOUR ACCOUNT Box------------------------------------"
	try: 		
		z.assertEqual(u"MANAGE YOUR ACCOUNT\nDisplay and modify your account information\nUpdate your email address, password, ID information for marketplaces",driver.find_element_by_id("manage_account").text)
		print "Success: MANAGE YOUR ACCOUNT Box Contents"
	except:
		print "Faliure: MANAGE YOUR ACCOUNT Box Contents"
	sleep(2)
	#driver.find_element_by_id("home_your_account").click() 
	print "MANAGE YOUR ACCOUNT Box:: Clicked: Display and modify your account information"
	sleep(2)	
	try:
		#z.assertEqual(u"Your Account",driver.find_element_by_tag_name("h1").text)
		print "Success: MANAGE YOUR ACCOUNT BOX:: Display and modify your account information"		
	except:
		red("Faliure: MANAGE YOUR ACCOUNT BOX:: Display and modify your account information")
	sleep(2)		
	driver.find_element_by_id("navbar_home").click()
	print "<---Going back to home page" 
	sleep(2)
	#-------------------Messages and alerts----------------
	print "-----------------------------------Messages and alerts Box----------------------------------------"
	z.assertEqual(u"MESSAGES AND ALERTS",driver.find_element_by_xpath("//*[@id='bulletinBoardSmallExt']/h3").text)
	print "WARNING :: Only the presence of this box is tested not the content displayed inside"
	#-------------------ANALYTICS BOX----------------
	print "--------------------------------------ANALYTICS BOX-----------------------------------------------"
	try:
		z.assertEqual(u"ANALYTICS\nYour business overview\nYour replenishment analytics\nYour sales (value) over the last 6 months\nYour sales (quantity) over the last 6 months\nYour sales :\n- today's sales vs yesterday's\n- this week's sales vs last week's\n- this month's sales vs last month's",driver.find_element_by_id("analytics_acc").text)
		print "Success: Contents of Analytics box"
	except:
		red("Faliure: Analytics")
	sleep(2)
	#------------Your business overview-------------------------
	driver.find_element_by_id("home_analytics").click()
	print "ANALYTICS BOX:: Clicked: Your business overview"
	sleep(2)	
	try:
		z.assertEqual(u"Analytics",driver.find_element_by_tag_name("h1").text)
		print "Success: ANALYTICS BOX:: Your business overview"		
	except:
		red("Faliure: ANALYTICS BOX:: Your business overview")
	sleep(2)		
	driver.find_element_by_id("navbar_home").click()
	print "<---Going back to home page" 
	sleep(2)
	#----------------Your replenishment analytics------------
	driver.find_element_by_id("home_reassort").click()
	print "ANALYTICS BOX:: Clicked: Your replenishment analytics"
	sleep(2)	
	try:
		z.assertEqual(u"Your bestsellers and items with slow turnover",driver.find_element_by_tag_name("h1").text)
		print "Success: ANALYTICS BOX:: Your replenishment analytics"		
	except:
		red("Faliure: ANALYTICS BOX:: Your replenishment analytics")
	sleep(2)		
	driver.find_element_by_id("navbar_home").click()
	print "<---Going back to home page" 
	sleep(2)
	#Your sales (value) over the last 6 months
	driver.find_element_by_id("home_sales_GMV").click()
	print "ANALYTICS BOX:: Clicked: Your sales (value) over the last 6 months"
	sleep(2)	
	try:
		z.assertEqual(u"Analytics",driver.find_element_by_tag_name("h1").text)
		print "Success: ANALYTICS BOX:: Your sales (value) over the last 6 months"		
	except:
		red("Faliure: ANALYTICS BOX:: Your sales (value) over the last 6 months")
	sleep(2)		
	driver.find_element_by_id("navbar_home").click()
	print "<---Going back to home page" 
	sleep(2)
	#Your sales (quantity) over the last 6 months
	driver.find_element_by_id("home_sales_quantity").click()
	print "ANALYTICS BOX:: Clicked: Your sales (quantity) over the last 6 months"
	sleep(2)	
	try:
		z.assertEqual(u"Analytics",driver.find_element_by_tag_name("h1").text)
		print "Success: ANALYTICS BOX:: Your sales (quantity) over the last 6 months"		
	except:
		red("Faliure: ANALYTICS BOX:: Your sales (quantity) over the last 6 months")
	sleep(2)		
	driver.find_element_by_id("navbar_home").click()
	print "<---Going back to home page" 
	sleep(2)
	#Your sales
	driver.find_element_by_id("home_see_more_stats").click()
	print "ANALYTICS BOX:: Clicked: Your sales"
	sleep(2)	
	try:
		z.assertEqual(u"SEE YOUR SALES FOR A SPECIFIC DATE",driver.find_element_by_css_selector("h3").text) #differs from UK and DE
		print "Success: ANALYTICS BOX:: Your sales"		
	except:
		red("Faliure: ANALYTICS BOX:: Your sales")
	sleep(2)		
	driver.find_element_by_id("navbar_home").click()
	print "<---Going back to home page" 
	sleep(2)
	print "Home Page Completed"
def display_orders_page():
	print "================================================================================================="
	print "                                          ORDERS PAGE                                            "
	print "================================================================================================="
	try:	
		z.assertEqual(u"Your Orders",driver.find_element_by_tag_name("h1").text) #differes from DE and UK
		print "Success: Your Orders"
		z.assertEqual(u"SEARCH AND FILTER",driver.find_element_by_css_selector("h3").text)
		print "Success: SEARCH AND FILTER BOX"
		#z.assertEqual(u"SALES SUMMARY",driver.find_element_by_xpath("//*[@id='stats']/h3").text)
		#print "Success: SALES SUMMARY BOX"		
	except:
		red("Faliure: ORDER PAGE Contents")
	driver.find_element_by_xpath("//*[@id='idaucun']").click()
	print "ORDER PAGE:: 'All Orders' clicked"
	sleep(5)
	try:
		driver.find_element_by_class_name("table_row_head").is_displayed()
		print "Success: Order Result Table is displayed"
	except:
		print "ORDER PAGE:: Order Result Table is not displayed"	
def display_inventory_button_page():
	print "================================================================================================="
	print "                                          INVENTORY PAGE                                         "
	print "================================================================================================="
	try:	
		z.assertEqual(u"Your inventory",driver.find_element_by_id("page_title").text)	
		print "Success: Your inventory"
		driver.find_element_by_link_text("Add one item").is_enabled()
		print "Success: Add one item"
		driver.find_element_by_link_text("Load file").is_enabled()
		print "Success: Load file"
		driver.find_element_by_link_text("Check loads").is_enabled()
		print "Success: Check loads"
		driver.find_element_by_link_text("Out of Stock").is_enabled()
		print "Success: Out of Stock"
		driver.find_element_by_id("inventory_default_priceCalculation")
		print "Success: Price Calculation"
		driver.find_element_by_id("inventory_marketplaces_box")
		print "Success: inventory_marketplaces_box"
		driver.find_element_by_id("inventory_default_statistics")
		print "Success: Statistics"
		driver.find_element_by_id("inventory_default_searchAndFilter")
		print "Success: Analytics"
	except: 
		red("Faliure: INVENTORY PAGE")
	try:
		driver.find_element_by_id("navbar_inventory_button").click()
		print "inventory button clicked"
	except:
		red("INVENTORY BUTTON click") 
	#sleep(2)
	try:
		driver.find_element_by_xpath("//*[@id='main']/div[3]/ul/li[2]/a").click() 
		print "INVENTORY PAGE:: Clicked: Add one item --- 1"
	except:
		red("INVENTORY PAGE:: Clicked: Add one item --- 1")
	#-----------------------Add one item-----------------------------------------------
	try:
		driver.find_element_by_xpath("//*[@id='inventory_addProduct_OneByOne_content']/p[1]/a").click() 
		print "INVENTORY PAGE:: Clicked: Add one item --- 2"	
	except:
		red("INVENTORY PAGE:: Clicked: Add one item --- 2")
	sleep(3)	
	try:
		z.assertEqual(u"Add an item to your inventory",driver.find_element_by_tag_name("h1").text) ####-----------------problem here
		print "Navigated to Product Search Page"
	except:
		red("Faliure: Product Search Page")
	sleep(2)	
	#----------------------Add an item to your inventory-------------------------------
	print "**********************************************************************************************"
	print "                       Product API :: Search by keyword(s)  and  Search by EAN                             "
	print "**********************************************************************************************"   
	try:	
		driver.find_element_by_id("seller_inventory_add_product_onebyone_inputSearchProduct").clear()	
		driver.find_element_by_id("seller_inventory_add_product_onebyone_inputSearchProduct").send_keys("Mobile") #search a product by keyword = 'Mobile'
		driver.find_element_by_id("inventory_obosearch_go_item_search").click()
	except:
		red("Faliure: INVENTORY PAGE:: Search by keyword(s) ")
	sleep(2)
	try:
		z.assertEqual(u"Find the article you want to sell",driver.find_element_by_xpath("//*[@id='main']/div[1]/h1").text)
	except:
		red("Faliure: Product API :: Find the article you want to sell ")
	sleep(2)
	#-----------------------Find the article you want to sell--------------------------
	try:	
		driver.find_element_by_id("sell_yours1").click()
		sleep(2)
		try:
			z.assertEqual(u"Add this listing",driver.find_element_by_xpath("//*[@id='obo_page']/div[1]/h1").text)
			print "Success: Navigated to Product API page"
		except: 
			red("Faliure:: Product API : Add this listing")
	except:
		red("Faliure: clicking sell_yours does not navigate to Product API page ")
	
def display_stats_page():
	driver.find_element_by_id("navbar_stats").click()
	print "================================================================================================="
	print "                                          ANALYTICS PAGE                                         "
	print "================================================================================================="
	try:	
		z.assertEqual(u"BUSINESS OVERVIEW",driver.find_element_by_tag_name("h3").text)
		print "Success: Analytics"
		z.assertEqual(u"BUSINESS OVERVIEW",driver.find_element_by_tag_name("h3").text)	
		print "Success: BUSINESS OVERVIEW"
		driver.find_element_by_id("stats_graph").is_displayed()
		print "Success: stats_graph"
	except:
		red("Faliure: Analytics page")

def display_mapper_page():
	#This differs from DE and UK 
	print "================================================================================================="
	print "                                          MAPPER PAGE                                         "
	print "================================================================================================="
	try:	
		z.assertEqual(u"Welcome",driver.find_element_by_class_name("section_head_top").text)
		driver.find_element_by_link_text("INSERT YOUR SOURCE FILE").is_enabled()
		print "Success: MAPPER PAGE: INSERT YOUR SOURCE FILE"
		driver.find_element_by_class_name("headerStepLink").click()
	except:
		red("Faliure: mapper_page")	
	
def display_pricing_page():#This line and also the following lines differ from DE and UK 
	driver.find_element_by_id("navbar_pricing").click()
	print "================================================================================================="
	print "                                          STRATEGY PAGE                                         "
	print "================================================================================================="
	try:		
		#z.assertEqual(u"Choose Your Price Strategy",driver.find_element_by_css_selector("h1").text)
		z.assertEqual(u"Choose Your Price Strategy",driver.find_element_by_class_name("section_head").text) #differs in UK and DE
		#z.assertEqual(u"CHOOSE YOUR PRICE STRATEGY",driver.find_element_by_css_selector("h3").text)
		print "Success: Choose Your Price Strategy"
	except:
		red("Faliure:  STRATEGY PAGE ")
	try:	
		driver.find_element_by_id("Amazon_All_New").is_enabled() #This differs from DE and UK 
		print "Success: STRATEGY PAGE: Amazon"
	except:
		red("Faliure:  STRATEGY PAGE: Amazon ")
	try:	
		driver.find_element_by_id("Fnac_All_New").is_enabled()
		print "Success: STRATEGY PAGE: FNAC"
	except:
		red("Faliure:  STRATEGY PAGE: FNAC ")
	try:	
		driver.find_element_by_id("PriceMinister_All_New").is_enabled()
		print "Success: STRATEGY PAGE: PriceMinister"
	except:
		red("Faliure:  STRATEGY PAGE: PriceMinister ")
	try:	
		driver.find_element_by_id("Cdiscount_All_New").is_enabled()
		print "Success: STRATEGY PAGE: Cdiscount"
	except:
		red("Faliure:  STRATEGY PAGE: Cdiscount ")
	try:	
		driver.find_element_by_id("Darty_All_New").is_enabled()
		print "Success: STRATEGY PAGE: Darty"
	except:
		red("Faliure:  STRATEGY PAGE: Darty ")		
def display_settings_page():
	driver.find_element_by_xpath("//*[@id='navbar_settings']").click() #settings button click
	print "================================================================================================="
	print "                                          SETTINGS PAGE                                          "
	print "================================================================================================="	
	try:
		z.assertEqual(u"Your preferences",driver.find_element_by_class_name("section_head").text)
	except:
		red("Faliure: SETTINGS PAGE CONTENTS: Your preferences")
	try:
		z.assertEqual(u"SEE YOUR SELLER PROFILE",driver.find_element_by_xpath("//*[@id='profil_seller']/h3").text)
	except:
		red("Faliure: SETTINGS PAGE CONTENTS: SEE YOUR SELLER PROFILE")
	try:
		z.assertEqual(u"SEE YOUR ORDER PREFERENCES",driver.find_element_by_xpath("//*[@id='pref_order_treatment']/h3").text)#differs from DE and UK
	except:
		red("Faliure: SETTINGS PAGE CONTENTS: SEE YOUR ORDER PREFERENCES")
	try:
		z.assertEqual(u"SEE YOUR SCHEDULE PREFERENCES",driver.find_element_by_xpath("//*[@id='pref_schedule']/h3").text)
	except:
		red("Faliure: SETTINGS PAGE CONTENTS: SEE YOUR SCHEDULE PREFERENCES")
	#SEE YOUR ORDER PREFERENCES
	try: 
		driver.find_element_by_xpath("//*[@id='pref_order_treatment_content']/a").click()   
		print "SETTINGS PAGE:: Clicked: See your order preferences"
		sleep(2)	
		try:
			z.assertEqual(u"Your order preferences",driver.find_element_by_css_selector("h1").text)
			print "Navigated to ----> Your order preferences"
		except:
			red("Faliure: SETTINGS PAGE: Your order preferences")
		sleep(2)		
		driver.find_element_by_css_selector("span.metrics_back").click()
		print "<---Going back to SETTINGS page"
	except:
		red("Faliure:: SETTINGS PAGE:: See your order preferences") 
	sleep(2)
	#SEE YOUR SELLER PROFILE
	driver.find_element_by_xpath("//*[@id='profil_seller_content']/a").click()
	print "SETTINGS PAGE:: Clicked: SEE YOUR SELLER PROFILE"
	sleep(2)	
	try:
		z.assertEqual(u"Your seller profile",driver.find_element_by_css_selector("h1").text)
		print "Navigated to ----> SEE YOUR SELLER PROFILE"
	except:
		red("Faliure: SETTINGS PAGE: SEE YOUR SELLER PROFILE")
	sleep(2)		
	driver.find_element_by_css_selector("span.metrics_back").click()
	print "<---Going back to SETTINGS page" 
	sleep(2)
	#SEE YOUR SCHEDULE PREFERENCES
	#See your pricing preferences
	driver.find_element_by_xpath("//*[@id='pref_schedule']/a[1]").click()
	print "SETTINGS PAGE:: Clicked: See your pricing preferences"
	sleep(2)	
	try:
		z.assertEqual(u"Define your pricing schedule",driver.find_element_by_css_selector("h1").text)
		print "Navigated to ----> Define your pricing schedule"
	except:
		red("Faliure: SETTINGS PAGE: See your pricing preferences")
	sleep(2)		
	driver.find_element_by_css_selector("span.metrics_back").click()
	print "<---Going back to SETTINGS page" 
	sleep(2)
	#See your push preferences
	driver.find_element_by_xpath("//*[@id='pref_schedule']/a[2]").click()
	print "SETTINGS PAGE:: Clicked: See your push preferences"
	sleep(2)	
	try:
		#z.assertEqual(u"Define your push schedule",driver.find_element_by_xpath("//*[@id='main']/div[2]/h1").text) #differs in UK and DE
		z.assertEqual(u"Define your push schedule",driver.find_element_by_css_selector("h1").text)
		print "Navigated to ----> Define your push schedule"
		print "*********************************************"
	except:
		red("Faliure: SETTINGS PAGE: See your push preferences")
	sleep(2)		
	driver.find_element_by_css_selector("span.metrics_back").click()
	print "<---Going back to SETTINGS page" 
	sleep(2)
def display_account_page():
	driver.find_element_by_id("navbar_account").click() #your account button click	
	print "================================================================================================="
	print "                                          YOUR ACCOUNTS PAGE                                     "
	print "================================================================================================="
	try:
		print "Please wait... Your account page is too slow!"
		z.assertEqual(u"Your Account",driver.find_element_by_class_name("section_head").text)
		#--------------------Your customer accesss settings-------------------
		try: 
			driver.find_element_by_xpath("//*[@id='account_page_customer_account']").click()
			print "YOUR ACCOUNTS PAGE:: Clicked: Your customer accesss settings"
		except:
			red("Faliure:: YOUR ACCOUNTS PAGE:: Clicked: Your customer accesss settings")
		sleep(2)	
		try:
			z.assertEqual(u"Your customer accesss settings",driver.find_element_by_css_selector("h1").text)
			print "Navigated to ----> Your customer accesss settings"
		except:
			red("Faliure: YOUR ACCOUNTS PAGE: Your customer accesss settings")
		sleep(2)		
		driver.find_element_by_xpath("//*[@id='main']/div[6]/a").click()
		print "<---Going back to YOUR ACCOUNTS PAGE" 
		sleep(2)
		#------------------------------Your main account details-----------------
		driver.find_element_by_xpath("//*[@id='account_page_main_details']").click()
		print "YOUR ACCOUNTS PAGE:: Clicked: Your main account details"
		sleep(2)	
		try:
			z.assertEqual(u"Your main account details",driver.find_element_by_css_selector("h1").text)
			print "Navigated to ----> Your main account details"
		except:
			red("Faliure: YOUR ACCOUNTS PAGE: Your main account details")
		sleep(2)		
		driver.find_element_by_xpath("//*[@id='main']/div[6]/a").click()
		print "<---Going back to YOUR ACCOUNTS PAGE" 
		sleep(2)
		#------------------------Your billing details----------------------------
		driver.find_element_by_xpath("//*[@id='account_page_billing_details']").click()
		print "YOUR ACCOUNTS PAGE:: Clicked: Your billing details"
		sleep(2)	
		try:
			z.assertEqual(u"Your billing details",driver.find_element_by_css_selector("h1").text)
			print "Navigated to ----> Your billing details"
		except:
			red("Faliure: YOUR ACCOUNTS PAGE: Your billing details")
		sleep(2)		
		driver.find_element_by_xpath("//*[@id='main']/div[6]/a").click()
		print "<---Going back to YOUR ACCOUNTS PAGE" 
		sleep(2)
		#----------------------Your Payment Method------------------------
		driver.find_element_by_xpath("//*[@id='account_page_payment_method']").click()
		print "YOUR ACCOUNTS PAGE:: Clicked: Your Payment Method"
		sleep(2)	
		try:
			z.assertEqual(u"Your Payment Method",driver.find_element_by_css_selector("h1").text)
			print "Navigated to ----> Your Payment Method"
		except:
			red("Faliure: YOUR ACCOUNTS PAGE: Your Payment Method")
		sleep(2)		
		driver.find_element_by_xpath("//*[@id='main']/div[6]/a").click()
		print "<---Going back to YOUR ACCOUNTS PAGE" 
		sleep(2)		
		#--------------------Your subscription---------------------
		driver.find_element_by_xpath("//*[@id='account_page_subscription']").click()
		print "YOUR ACCOUNTS PAGE:: Clicked: Your subscription"
		sleep(2)	
		try:
			z.assertEqual(u"Your subscription",driver.find_element_by_css_selector("h1").text)
			print "Navigated to ----> Your subscription"
		except:
			red("Faliure: YOUR ACCOUNTS PAGE: Your subscription")
		sleep(2)		
		driver.find_element_by_xpath("//*[@id='main']/div[6]/a").click()
		print "<---Going back to YOUR ACCOUNTS PAGE" 
		sleep(2)
		#---------------------Your invoices---------------------
		driver.find_element_by_xpath("//*[@id='account_page_invoices']").click()
		print "YOUR ACCOUNTS PAGE:: Clicked: Your invoices"
		sleep(2)	
		try:
			z.assertEqual(u"Your list of bills",driver.find_element_by_css_selector("h1").text)
			print "Navigated to ----> Your list of bills"
		except:
			red("Faliure: YOUR ACCOUNTS PAGE: Your invoices")
		sleep(2)		
		driver.find_element_by_css_selector("span.metrics_back").click()
		print "<---Going back to YOUR ACCOUNTS PAGE" 
		sleep(2)
		#-------------Look up and update your marketplace connections----------------------------
		driver.find_element_by_xpath("//*[@id='account_page_marketplaces']").click()
		print "YOUR ACCOUNTS PAGE:: Clicked: Look up and update your marketplace connections"
		sleep(2)	
		try:
			z.assertEqual(u"Look up and update your marketplace connections",driver.find_element_by_css_selector("h1").text)
			print "Navigated to ----> Look up and update your marketplace connections"
		except:
			red("Faliure: YOUR ACCOUNTS PAGE: Look up and update your marketplace connections")
		sleep(2)		
		driver.find_element_by_xpath("//*[@id='main']/div[6]/a").click() 
		print "<---Going back to YOUR ACCOUNTS PAGE" 
		sleep(2)
	except: 
		red("FAILED:: Your Account page is too slow to load. Test this page manually")	
		
main()		
