from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from trie import *
def scroll_all(driver):
	SCROLL_PAUSE_TIME = 5
	last_height = driver.execute_script("return document.body.scrollHeight")
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(SCROLL_PAUSE_TIME)
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height


# def scroll_once(driver , no):
# 	Y = no*1080
# 	driver.execute_script("""window.scrollTo(0, console.log(Y));""")
# 	time.sleep(7)

def friends_of_friends(driver , friends):

	visited_friends = TrieNode('*')
	for one in friends:
		if find(visited_friends,one) == True:
			continue
		else:
			insert(visited_friends,one)
		driver.get(one)
		time.sleep(7)
		print 
		print
		print one
		friend_page = driver.find_elements_by_class_name("_6-6")
		for a in friend_page:
			link = a.get_attribute("href")
			print link
			if link == None:
				continue
			elif "friends" in link:
				driver.get(link)	
				all_links = driver.find_elements_by_tag_name("a")
				for link in all_links:
					check_link = link.get_attribute("href")
					#print check_link
					if check_link == None:
						continue
					elif check_link.endswith("friends_tab"):
						#print check_link
						print link.get_attribute("text")
				#driver.execute_script("window.history.go(-1)")
				#time.sleep(7)
				break
		#driver.execute_script("window.history.go(-1)")


def my_friends(driver):
	friends = []
	form_element = driver.find_element_by_xpath("//*[@id='u_0_a']/div[1]/div[1]/div/a")
	form_element.click()
	time.sleep(7)
	friend_page = driver.find_element_by_xpath("//*[@id='u_fetchstream_2_9']/li[3]/a")
	#print friend_page
	friend_page.click()
	time.sleep(7)
	no = 1
	#scroll_all(driver)
	all_links = driver.find_elements_by_tag_name("a")
	for link in all_links:
		check_link = link.get_attribute("href")
		#print check_link
		if check_link == None:
			continue
		elif check_link.endswith("friends_tab"):
			#print check_link
			friends.append(check_link)
			print link.get_attribute("text")

	friends_of_friends(driver,friends)


def login():
	email = ""
	password = ""

	chrome_options = webdriver.ChromeOptions()
	prefs = {"profile.default_content_setting_values.notifications" : 2}
	chrome_options.add_experimental_option("prefs",prefs)
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.get("https://www.facebook.com/")
	#assert "Facebook" in driver.title
	elem = driver.find_element_by_id("email")
	elem.send_keys(email)
	elem = driver.find_element_by_id("pass")	
	elem.send_keys(password)
	elem.send_keys(Keys.RETURN)
	time.sleep(5)
	#driver.get("https://www.facebook.com/ravdeep.singh.180072?fref=pb&hc_location=friends_tab")
	my_friends(driver)
	#print form_element
	time.sleep(10)
	#driver.close()

login()
