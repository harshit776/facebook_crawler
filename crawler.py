from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from trie import *
import urllib
from selenium.webdriver.support.wait import WebDriverWait

#-----------------------------------------
#-----------------------------------------

def new_window(driver):
	
	#To switch to a new window in order to save state on present window ( required to avoid stale element reference exception)
	WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
	driver.switch_to_window(driver.window_handles[1])
	time.sleep(7)


#------------------------------------------
def old_window(driver):

	# To switch back to previous state
	driver.switch_to_window(driver.window_handles[0])
	time.sleep(10)

#------------------------------------------
def scroll_all(driver , scrolls = 1000):

	# To scroll a page a specific number of times controlled by scrolls
	SCROLL_PAUSE_TIME = 5
	count = 0
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		count += 1
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(SCROLL_PAUSE_TIME)
		new_height = driver.execute_script("return document.body.scrollHeight")

		if new_height == last_height:
			break
		if count == scrolls:
			break

		last_height = new_height


# def scroll_once(driver , no):
# 	Y = no*1080
# 	driver.execute_script("""window.scrollTo(0, console.log(Y));""")
# 	time.sleep(7)

# ------------------------------------
def images(driver , friends):
	
	# To download images of all your friends

	# loc = location to store images of your friends (specify this)
	loc=""
	
	print
	print "---------------Getting images of Friends--------------------"
	for one in friends:
		driver.get(one)
		time.sleep(7)

		friend_image = driver.find_elements_by_tag_name("img")
		for image in friend_image:
			if image.get_attribute("class") == "_11kf img":
				image_link = image.get_attribute("src")
				break

		friend_name = driver.find_elements_by_tag_name("a")
		for friend in friend_name:
			if friend.get_attribute("class") == "_2nlw _2nlv":
				image_name = friend.get_attribute("text")
				break

		image_name = "/" + image_name +".jpg"
		image_loc = loc + image_name

		urllib.urlretrieve(image_link,image_loc)

	
# --------------------------------------
def friends_of_friends(driver , friends):

	# To check friends of all your connections
	print
	print "---------------Getting details of friends of all connections--------------------"
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
				break
		#driver.execute_script("window.history.go(-1)")

# ---------------------------------------------
def timeline_images(driver):
	
	# loc = place to store downloaded images (specify this)
	loc=""
	
	print
	print "---------------Downloading timeline images of user--------------------"
	cnt = 1

	scroll_all(driver,3)
	all_anchor = driver.find_elements_by_tag_name("a")
	for anchor in all_anchor:

		link = anchor.get_attribute("href")

		if link == None:
			continue

		rel_atr = anchor.get_attribute("rel")

		if rel_atr == "theater":
			new_window(driver)
			driver.get(link)
			time.sleep(7)
			wall_image = driver.find_elements_by_tag_name("img")

			for image in wall_image:
				image_class = image.get_attribute("class")

				if image_class == "spotlight":
					src = image.get_attribute("src")
					image_loc = loc+"/"+ str(cnt) +".png"
					#print link
					urllib.urlretrieve(src,image_loc)
					cnt += 1

			old_window(driver)
			break
			time.sleep(7)


# --------------------------------------------
def my_friends(driver):

	# To store links of all friends of a user
	friends = []

	# To go on main page of a user
	form_element = driver.find_element_by_xpath("//*[@id='u_0_a']/div[1]/div[1]/div/a")
	form_element.click()
	time.sleep(7)

	# To go on friends page of user
	friend_page = driver.find_elements_by_class_name("_6-6")

	# To download recent images on timeline of user
	timeline_images(driver)

	# Finding all friends and saving their links

	print
	print "---------------Getting Friends--------------------"

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
				
				if check_link == None:
					continue
				elif check_link.endswith("friends_tab"):
					
					friends.append(check_link)
					print link.get_attribute("text")
			break

	# To get images of all friends and dowloading them
	images(driver,friends)

	# To check friends of all your connections
	friends_of_friends(driver,friends)


# ------------------------------------
def login():

	# To login to Facebook enter your email and password in email and password variable
	print
	print "---------------Logging In--------------------"
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

	# To check all connections of an user 
	my_friends(driver)
	
	driver.close()

# -----------------------------------------
login()