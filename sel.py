from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from trie import *
import urllib


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

def images(driver , friends):
	
	loc="location to download images"
	for one in friends:
		driver.get(one)
		time.sleep(7)

		friend_image = driver.find_elements_by_tag_name("img")
		for image in friend_image:
			if image.get_attribute("class") == "_11kf img":
				image_link = image.get_attribute("src")
				break

		#print image_link

		friend_name = driver.find_elements_by_tag_name("a")
		for friend in friend_name:
			if friend.get_attribute("class") == "_2nlw _2nlv":
				image_name = friend.get_attribute("text")
				break

		#print image_name

		image_name = "/" + image_name +".jpg"
		image_loc = loc + image_name

		urllib.urlretrieve(image_link,image_loc)
		#print image_loc

	

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
			#print link
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
	#//*[@id="u_0_g"]/div[1]/div[1]/div/a
	form_element.click()
	time.sleep(7)
	friend_page = driver.find_elements_by_class_name("_6-6")
	for a in friend_page:
		link = a.get_attribute("href")
		#print link
		if link == None:
			continue
		elif "friends" in link:
			driver.get(link)	
			time.sleep(7)
			scroll_all(driver)
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
			break

	images(driver,friends)
	friends_of_friends(driver,friends)


def login():
<<<<<<< HEAD
	email = ""
	password = ""
=======
	email = "facebook_id"
	password = "facebook_password"
>>>>>>> Download images of friends!

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
	my_friends(driver)
	# friends = []
	# friends.append("https://www.facebook.com/akhilsingla97?fref=pb&hc_location=friends_tab")
	# images(driver,friends)
	time.sleep(10)
	#driver.close()

login()
