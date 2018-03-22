from urllib2 import urlopen
import string 
from bs4 import BeautifulSoup
from collections import defaultdict
import os 
import uuid

home_url = "https://www.afrikrea.com/en" 
id_tag = "afrikrea"
images_count = 0 
products_count = 0 
scraped = []
scraped_image = []
scraped_product = []



def make_soup(url):
	page = urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	return soup

def extract_images(product_url, path_prefix):

	# get a product id 
	global scraped_image
	global scraped
	global id_tag
	
	if product_url in scraped_product: 
		print "repeated product: ",  product_url
		return 
	else: scraped_product.append(product_url)
	product_soup = make_soup(product_url)
	
	product_details = product_soup.find('div', {"id": "product-details-images"})
	#product_id = product_review.get("data-id") + id_tag
	#print product_id

	#if product_id in scraped: return 
	#else: scraped.append(product_id)

	i = 0
	#product_photos = product_soup.findAll('div', {"class": "mthumb"})
	image_div = product_details.find("img")
	if image_div == None: return 
	image_url = image_div.get("data-large")
	id_len = 8
	index_suffix = image_url.index("-large")
	product_id = image_url[index_suffix-id_len:index_suffix] + id_tag
	if product_id in scraped: 
		print "PRODUCT REPEAT: ", product_id
		return 
	else: scraped.append(product_id)
	print product_id

	for img in product_details.findAll("img"): 
		image_url = img.get("data-large")
		
		if not image_url in scraped_image:
			print image_url
			scraped_image.append(image_url)
			
			dir_name = path_prefix + "/" + product_id 
			if not os.path.exists(dir_name): os.makedirs(dir_name)
			filename = dir_name + "/" + str(i) + product_id
			imagefile = open(filename+ '.jpeg', 'wb')
			imagefile.write(urlopen(image_url).read())
			imagefile.close()
			i += 1	

			
			

def get_products(page_soup, path_prefix):
	page_urls = []
	products = page_soup.findAll('div', {"class": "card card-product"})
	
	for product in products:
		product_url = product.get('data-url')
		
		page_urls.append(product_url)
		extract_images(product_url, path_prefix)

	return page_urls

if __name__ == '__main__':


	#zuvaa_list =["jackets", "jumpsuits", "dresses", "two-piece-sets", "tops", "pants", "jewlery", "athleisure", "bags"]	

	cat_list = ["skirts", "dresses-tunic", "shorts", "trousers", "jackets-coats", "swimsuits", "jumpsuits-overalls"]
	
	# category: jackets-coatspage 4 :72 products

	#NUM_PRODUCTS:  3390
	# NUM_IMGS:  9110
	
	# NUM_PRODUCTS:  275
	# NUM_IMGS:  704


	#category: jackets-coatspage 12 :72 products

	# 	NUM_PRODUCTS:  411
	# NUM_IMGS:  1107


	# FINAL_NUM_PRODUCTS:  170
	# FINAL_NUM_IMGS:  458
	#Skipped = "t-shirts-crop-tops-tank-tops", "shirts"


	for category in cat_list:

		category_name = ""
		if "tops" in category or "shirts" in category:
			category_name = "women-tops"
		elif "skirt" in category :
			category_name = "women-skirts"
		elif "dress" in category:
			category_name = "women-dresses"
		elif "pants" in category or "trousers" in category or "shorts" in category:
			category_name = "women-pants-and-shorts"
		elif "jumpsuit" in category:
			category_name = "women-jumpsuits"
		elif "sets" in category or "seperates" in category or "piece" in category:
			category_name = "women-matching-sets"
		elif "swim" in category:
			category_name = "women-swimwear"
		elif "jacket" in category:
			category_name = "women-jackets"
		elif "men" in category:
			category_name = "men-tops"
		elif category in shoes_list:
			category_name = "shoes"
		else:
			category_name = category

		
		if "jewlery" in category_name:
			path_prefix = "data/others/jewlery" 
		elif "bags" in category_name:
			path_prefix = "data/others/bags"  
		else: 
			path_prefix = "data/women/" + category_name 

		page = 13
		
		while(True):
			category_url = home_url + "/categories/"+ category + "?page="   + str(page) 
			
			page_soup = make_soup(category_url)
			page_products = get_products(page_soup, path_prefix)
			print "category: "+ category + "page " + str(page) + " :" + str(len(page_products)) + " products"
			print "NUM_PRODUCTS: ", len(scraped)
			print "NUM_IMGS: ", len(scraped_image)
			if len(page_products) == 0: break 
			page += 1 
		
			

	print "FINAL_NUM_PRODUCTS: ", len(scraped)
	print "FINAL_NUM_IMGS: ", len(scraped_image)
	

	

#product-id product-6740089861
# https://omiwoods.com/collections/dresses/products/the-amaka-bell-sleeve-wrap-dress-in-classic-mudcloth


