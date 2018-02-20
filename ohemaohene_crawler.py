from urllib2 import urlopen
import string 
from bs4 import BeautifulSoup
from collections import defaultdict
import os 
import uuid

home_url = "https://ohemaohene.com/" 
id_tag = "oo"
images_count = 0 
products_count = 0 
scraped = []
scraped_image = []



def make_soup(url):
	page = urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	return soup

def extract_images(product_url, path_prefix):

	# get a product id 
	global scraped_image
	global scraped
	global id_tag
	product_soup = make_soup(home_url + product_url)
	
	product_review = product_soup.find('div', {"id": "shopify-product-reviews"})
	product_id = product_review.get("data-id") + id_tag
	print product_id

	if product_id in scraped: return 
	else: scraped.append(product_id)

	i = 0
	product_photos = product_soup.findAll('div', {"class": "mthumb"})

	for img in product_photos: 
		temp = img.find('img').get("src")
		image_url = "https:" + temp	
		
		
		if not image_url in scraped_image :
				
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
	products = page_soup.findAll('div', {"class": "prod-container"})
	
	for product in products:
		
		product_url = product.find('a').get('href')
		
		page_urls.append(product_url)
		extract_images(product_url, path_prefix)

	return page_urls

if __name__ == '__main__':


	# page_soup = "/products/yellow-dashiki-boom-dress?variant=22439851716"
	# path_prefix = "data/women/skirt"   

	# extract_images(page_soup, path_prefix)

	women_list =["dresses", "jackets-blazers", "jumpsuits-playsuits", "tops", "skirts", "trousers-shorts", "african-print-two-piece"]
	men_list = ["blazers", "trousers-shorts-1", "sweaters-cardigans", "shirts", "accessories"]
	shoes_list = ["espadrilles", "hitops", "canvas-sneakers", "ladies-shoes"]

	women_list += shoes_list

	for category in women_list:

		category_name = ""
		if "tops" in category or "shirts" in category and category != "hitops":
			category_name = "women-tops"
		elif "skirt" in category :
			category_name = "women-skirts"
		elif "dress" in category:
			category_name = "women-dresses"
		elif "pants" in category or "trousers" in category:
			category_name = "women-pants-and-shorts"

		elif "jumpsuit" in category:
			category_name = "women-jumpsuits"
		elif "sets" in category or "seperates" in category or "piece" in category:
			category_name = "women-matching-sets"
		elif "swimwear" in category:
			category_name = "women-swimwear"
		elif "jacket" in category:
			category_name = "women-jackets"
		elif "men" in category:
			category_name = "men-tops"
		elif category in shoes_list:
			category_name = "shoes"
		else:
			category_name = category

		

		if not "shoes" in category_name:
			path_prefix = "data/women/" + category_name 
		else: 
			path_prefix = "data/others/shoes" 

		page = 1
		category_url = home_url + "/collections/" + category + "?page="

		while(True):
			page_soup = make_soup(category_url + str(page))
			page_products = get_products(page_soup, path_prefix)
			print "category: "+ category + "page " + str(page) + " :" + str(len(page_products)) + " products"
			if len(page_products) == 0: break 
			page += 1 
			
	######	
	for category in men_list:
		if "blazers" in category: 
			category_name = "men-blazers"

		elif "trousers-shorts-1" in category :
			category_name = "men-bottoms"

		elif "sweaters-cardigans" in category:
			category_name = "men-sweaters-cardigans"

		elif "shirts" in category:
			category_name = "men-tops"


		path_prefix = "data/men/" + category_name 

	######


		page = 1
		category_url = home_url + "/collections/" + category + "?page="

		while(True):
			page_soup = make_soup(category_url + str(page))
			page_products = get_products(page_soup, path_prefix)
			print "category: "+ category + "page " + str(page) + " :" + str(len(page_products)) + " products"
			if len(page_products) == 0: break 
			page += 1 



	print "NUM_PRODUCTS: ", len(scraped)
	print "NUM_IMGS: ", len(scraped_image)
	

	

#product-id product-6740089861
# https://omiwoods.com/collections/dresses/products/the-amaka-bell-sleeve-wrap-dress-in-classic-mudcloth


