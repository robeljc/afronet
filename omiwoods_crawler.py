from urllib2 import urlopen
import string 
from bs4 import BeautifulSoup
from collections import defaultdict
import os 
import uuid

home_url = "https://omiwoods.com" 
id_tag = "ow"
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
	
	product_div = product_soup.find('div', {"class": "desktop-10 main-product-image"})
	product_id = product_div.find('img').get("id") + id_tag
	print product_id
	

	if product_id in scraped: return 
	else: scraped.append(product_id)

	i = 0
	product_photos = product_soup.find('div', {"id": "product-photos"})

	for img in product_photos.findAll('img'):
		temp = img.get("src")
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
	products = page_soup.findAll('div', {"class": "ci"})
	
	for product in products:
		
		product_url = product.find('a').get('href')
		
		page_urls.append(product_url)
		extract_images(product_url, path_prefix)

	return page_urls

if __name__ == '__main__':


	# page_soup = "/products/yellow-dashiki-boom-dress?variant=22439851716"
	# path_prefix = "data/women/skirt"   

	# extract_images(page_soup, path_prefix)

	category_list =["dresses", "jewelry", "jackets", "jumpsuitsandpants", "maxi-dresses", "skirts", "tops", "two-piece-sets"] 

	for category in category_list:

		category_name = ""
		if "tops" in category or "shirts" in category:
			category_name = "women-tops"
		elif "skirt" in category :
			category_name = "women-skirts"
		elif "dress" in category:
			category_name = "women-dresses"
		elif "pants" in category:
			category_name = "women-pants-and-shorts"

		elif "jumpsuit" in category:
			category_name = "women-jumpsuits"
		elif "sets" in category or "seperates" in category:
			category_name = "women-matching-sets"
		elif "swimwear" in category:
			category_name = "women-swimwear"
		elif "jackets" in category:
			category_name = "women-jackets"
		elif "men" in category:
			category_name = "men-tops"
		else:
			category_name = category

		path_prefix = "data/women/" + category_name 
		if not "women" in category_name:
			if not "men" in category_name:
				path_prefix = "data/others/" + category_name 
			else:
				path_prefix = "data/men/" + category_name 
		
		

				

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


