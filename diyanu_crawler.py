from urllib2 import urlopen
import string 
from bs4 import BeautifulSoup
from collections import defaultdict
import os 



#print (soup.title.text)

#all links on the website 
#for link in soup.findAll('a'):
	#print (link.get('href'))
	#print (link.text) (name)

# soup = make_soup(diyanu_url)
# i = 0
# for img in soup.findAll('img'):

# 	temp = img.get('src')
# 	print temp
# 	image = "https:" + temp

# 	nametemp = img.get('alt')

# 	if nametemp == None or len(nametemp) == 0:
# 		filename = str(i)
# 		i = i +1 
# 	else: 
# 		exclude = set(string.punctuation)
# 		filename = ''.join(ch for ch in nametemp if ch not in exclude and ch != " ")

# 	imagefile = open(filename + '.jpeg', 'wb')
# 	imagefile.write(urlopen(image).read())
# 	imagefile.close()


# a product will have four pictures 

# dump all images in one dir 
# gender/high-level-type/product file 


#check product id 

# collections/women
	#/women/tops...
# collections/men
	#collections/men-... (based on string)
	# for each product  (collections/mens-african-print-bottoms/products/*)
		# extract all product images and locate in a folder 
			# textfile of all: r
				# product-id
				# Tags
				# related product names 
				# price 
				# rating 
				# Description


#category 
	# nav: nav-bar:: ul: site-nav: ul: dropdown> 
home_url = "https://www.diyanu.com" 
gender_urls = ["/collections/men/?page=", "/collections/women/?page="]

#product-url to product_id dict 
product_url_to_id = defaultdict(int)
product_id_to_category = defaultdict(str)
images_count = 0 

scraped = []
categorized = []

def make_soup(url):
	page = urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	return soup

def extract_categories():

	women_categories = ["skirts", "dresses", "womens-tops", "pants-and-shorts", "outerwear"] 

	for category in women_categories:
		category_url = home_url + "/collections/" + category +  "?page="
		category_soup = make_soup(category_url)
		page = 1
		while(True):
			page_soup = make_soup(category_url+ str(page))	
			product_count = 0
			

			for box_product in page_soup.findAll('div', {"class": "box product"}):
					figcaption  = box_product.find('figcaption').find('div')
					if figcaption != None: 
						product_id= figcaption.get('data-product-id')

						if not product_id in categorized:
							if category == "womens-tops":
								product_id_to_category[product_id]= "women-tops"
							else: 
								product_id_to_category[product_id]= "women-"+category
							product_count += 1 
						
			print "category: " + category + "page " + str(page) + " :" + str(product_count) + " products"
			if product_count == 0: break 
			page += 1



	mens_categories = ["mens-jacket", "short-sleeve-t-shirts", "long-sleeve-t-shirts", "mens-african-print-bottoms", "tanks", "mens-swimwear"]
	
	for category in mens_categories:
		category_url = home_url + "/collections/" + category +  "?page="

		category_soup = make_soup(category_url)
		page = 1
		while(True):
			page_soup = make_soup(category_url+ str(page))	
			product_count = 0

			for box_product in page_soup.findAll('div', {"class": "box product"}):
					figcaption  = box_product.find('figcaption').find('div')
					if figcaption != None: 
						product_id= figcaption.get('data-product-id')
						if not product_id in categorized:
							if (category == "short-sleeve-t-shirts" or category == "long-sleeve-t-shirts" or category == "tanks"):
								product_id_to_category[product_id]= "mens-tops"
							elif ((category == "mens-african-print-bottoms" or category == "mens-swimwear")):
								product_id_to_category[product_id]= "mens-bottoms"
							elif (category == "mens-jacket"):
								product_id_to_category[product_id]= "mens-outwear"
							product_count += 1 
						
			print "category: " + category + "page " + str(page) + " :" + str(product_count) + " products"
			if product_count == 0: break 
			page += 1



def get_products(page_soup):
	page_urls = []
	for box_product in page_soup.findAll('div', {"class": "box product"}):
		figcaption  = box_product.find('figcaption').find('div')
		if figcaption != None: 
			product_id= figcaption.get('data-product-id')

			if not product_id in scraped:
				product_url_to_id[figcaption.get('data-url')] = product_id
				scraped.append(product_id)
				page_urls.append(box_product.find('a').get('href'))
	return page_urls

def extract_urls(gender_url):
	page = 1
	product_urls = []
	while(True):
		page_soup = make_soup(home_url + gender_url + str(page))	
		page_products = get_products(page_soup)
		print "page " + str(page) + " :" + str(len(page_products)) + " products"
		if len(page_products) == 0: break 
		product_urls += page_products
		page += 1
	return product_urls



def save_image(img, image_url, i, product_id):	
	global images_count 
	images_count += 1

	# nametemp = img.get('alt')

	# if nametemp == None or len(nametemp) == 0:
	# 			filename = str(i)
	# else: 
	# 	exclude = set(string.punctuation)
	# 	filename = ''.join(ch for ch in nametemp if ch not in exclude and ch != " ")
	# 	filename = str(i) + filename

	# category = product_id_to_category[product_id]
	# print product_id, category
	# if "women" in category:
	# 	dir_name = "women/" + category + "/" + product_id
	# else: 
	# 	dir_name = "men/" + category + "/" + product_id
	
	# if not os.path.exists(dir_name): os.makedirs(dir_name)
	# filename = dir_name + "/" + filename 

	# imagefile = open(filename + '.jpeg', 'wb')
	# imagefile.write(urlopen(image_url).read())
	# imagefile.close()	


	# textfilename 
	# fh = open("hello.txt", "w")
	# lines_of_text = ["a line of text", "another line of text", "a third line"]
	# fh.writelines(lines_of_text)
	# fh.close()


def extract_images(product_soup):
	
	product_id = product_soup.find('div', {"class": "product-title"}).find('div').get("data-product-id")
	



	images = product_soup.find('div', {"class": "product-images"})
	thumbnails = images.find('div', {"class": "thumbnails"})
	i = 0
	if thumbnails != None: 
	
		for img in thumbnails.findAll("img"):
			temp=img.get("data-highres")
			image_url = "https:" + temp			
			
			save_image(img, image_url, i, product_id)
			i += 1 
	else: 
		# only one image product
		img = images.find('img')
		temp = img.get('data-zoom-image')
		image_url = "https:" + temp 
		save_image(img, image_url, i, product_id)

	# Note: requires selenium to extract related fields as they are generated by JS 


	#find('ul', {"class": "cross-sell"})
	#print related_list
	# if related_list != None:
	# 	for item in related_list.findAll('li'):
	# 		product_url= item.find('div', {"class": "producttitle"}).find('a').get('href')
	# 		print product_url
	# 		print product_listing[home_url + product_url] 



if __name__ == '__main__':
	
	#extract_categories()
	#print ("******************* CATEGORIZED PRODUCTS *******************")
	#product_soup = make_soup("https://www.diyanu.com/collections/skirts/products/limited-amsa-african-print-midi-skirt-with-sash-blue-lime-green")
	#extract_images(product_soup)


	for gender_url in gender_urls:

		products_urls = extract_urls(gender_url)
		print "scrapped: ", scraped
		print ("******************* EXTRACTED URLS *******************")
	# 	for product_url in products_urls:

	# 		product_soup = make_soup(home_url + product_url)
	# 		extract_images(product_soup)
	# print images_count

			# images = product_soup.find('div', {"class": "product-images"})
			# for img in images.findAll("img"):
			# 	print img.get("src")

			# TODO: make a category foldera
			# TODO: dump in main dir





		

















####################################################################################################################################
####################################################################################################################################
# col_str = '/collections'
# collections_links = []
# 
#exclude_collections = ["/collections/all","/collections/clearance", "/collections/new-arrivals", "/collections/men", "/collections/women"]
# for link in soup.findAll('a'):
# 	link_ref = link.get('href')
# 	if (link_ref).find(col_str,0, len(col_str)) != -1 and not link_ref in collections_links and not link_ref  in exclude_collections:
# 		collections_links.append(link_ref)
# 		print link_ref[len(col_str): ]






# if not os.path.exists(directory):
#     os.makedirs(directory)


