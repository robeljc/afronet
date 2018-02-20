from urllib2 import urlopen
import string 
from bs4 import BeautifulSoup
from collections import defaultdict
import os 
import uuid

home_url = "https://wrenfashion.com/" 
id_tag = "wf"
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
	thumb_tags = "product-single__photo js-zoom-enabled product-single__photo--has-thumbnails hide"
	featured_tags = "product-single__photo js-zoom-enabled product-single__photo--has-thumbnails"
	thumb_imgs = product_soup.findAll('div', {"class": thumb_tags})	
	featured_img = product_soup.find('div', {"class": featured_tags})
	thumb_imgs.append(featured_img)

	if thumb_imgs[0] == None:
		print ("NO IMAGE FOR "), product_url
		no_thumb_tag = "product-single__photo js-zoom-enabled"
		thumb_imgs = product_soup.findAll('div', {"class": no_thumb_tag})	

	
	for img in thumb_imgs:
		temp = img.get("data-zoom")
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
		else: 
			no_thumb_tag = "product-single__photo js-zoom-enabled"
			no_thumb_img = product_soup.find('div', {"class": no_thumb_tag})	

			

def get_products(page_soup, path_prefix):
	page_urls = []
	products = page_soup.findAll('div', {"class": "grid__item grid__item--collection-template small--one-half medium-up--one-third"})
	
	for product in products:
		product_url = product.find('a').get('href')
		page_urls.append(product_url)
		extract_images(product_url, path_prefix)

	return page_urls

if __name__ == '__main__':


	# page_soup = "/products/yellow-dashiki-boom-dress?variant=22439851716"
	# path_prefix = "sample/women/skirt"   

	# extract_images(page_soup, path_prefix)

	category_list = [ "dresses", "pants", "shirts", "skirts", "jackets", "jumpsuit-and-romper", "men"]
	#category_list = ["shirts"]
	for category in category_list:

		category_name = ""
		if "tops" in category or "shirts" in category:
			category_name = "women-tops"
		if "skirt" in category :
			category_name = "women-skirts"
		if "dress" in category:
			category_name = "women-dresses"
		if "pants" in category:
			category_name = "women-pants-and-shorts"

		if "jumpsuit" in category:
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


