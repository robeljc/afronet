from urllib2 import urlopen
import string 
from bs4 import BeautifulSoup
from collections import defaultdict
import os 
import uuid





home_url = "https://zabbadesigns.com/" 
id_tag = "zd"
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
	

	product_header = product_soup.find('div', {"class": "breadcrumb breadcrumb_text product_breadcrumb"})
	product_id_tag = product_header.findAll('div')[1].get('id')
	product_id = product_id_tag[len("secomapp-fg-image-"):] + id_tag
	

	if product_id in scraped: return 
	else: scraped.append(product_id)

	i = 0

	product_list = product_soup.find('div', {"class": "flexslider-container ten columns alpha"})

	for img in product_list .findAll('img'):
		temp = img.get("src")
		image_url = "https:" + temp	
		
		
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
	products = page_soup.findAll('div', {"itemprop": "itemListElement"})
	
	for product in products:
		product_url = product.find('a').get('href')
		page_urls.append(product_url)
		extract_images(product_url, path_prefix)

	return page_urls

if __name__ == '__main__':


	# page_soup = "/products/yellow-dashiki-boom-dress?variant=22439851716"
	# path_prefix = "sample/women/skirt"   

	# extract_images(page_soup, path_prefix)

	category_list = [ "african-tops-and-blouses", "african-dresses", "formal-african-dresses", "african-inspired-dressy-seperates", "african-jackets-and-outerwear", "maxi-skirts-pants", "african-mens-clothing"]

	for category in category_list:

		category_name = ""
		if "tops" in category:
			category_name = "women-tops"
		if "skirt" in category :
			category_name = "women-skirts"
		if "dresses" in category:
			category_name = "women-dresses"
		if "jumpsuits" in category:
			category_name = "women-jumpsuits"
		if "sets" in category or "seperates" in category:
			category_name = "women-matching-sets"
		if "swimwear" in category:
			category_name = "women-swimwear"
		if "jackets" in category:
			category_name = "women-jackets"

		
		path_prefix = "data/women/" + category_name 

		if "men" in category:
			category_name = "men-tops"
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
	

	
#product-id div-secomapp-fg-image-215295917


