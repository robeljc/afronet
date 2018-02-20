from urllib2 import urlopen
import string 
from bs4 import BeautifulSoup
from collections import defaultdict
import os 


home_url = "https://www.grass-fields.com/" 
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
	product_soup = make_soup(home_url + product_url)

	product_review = product_soup.find('div', {"id": "shopify-product-reviews"})
	product_id = product_review.get("data-id")

	if product_id in scraped: return 
	else: scraped.append(product_id)

	i = 0

	for img in product_soup .findAll('img'):
		temp = img.get("src")
		image_url = "https:" + temp	
		
		if not image_url in scraped_image and "/products" in image_url and not "youtube" in image_url:
			print image_url
			scraped_image.append(image_url)
			
			dir_name = path_prefix + "/" + product_id 
			if not os.path.exists(dir_name): os.makedirs(dir_name)
			filename = dir_name + "/" + str(i) + product_url[len("/products/"):]
			imagefile = open(filename+ '.jpeg', 'wb')
			imagefile.write(urlopen(image_url).read())
			imagefile.close()
			i += 1	

def get_products(page_soup, path_prefix):
	page_urls = []
	products = page_soup.findAll('div', {"class": "velaProBlock product-section-effect col-sp-12 col-xs-6 col-md-4"})

	for product in products:
		page_urls.append(product.find('a').get('href'))
		product_url = product.find('a').get('href')
		extract_images(product_url, path_prefix)

	return page_urls

if __name__ == '__main__':


	# page_soup = "/products/yellow-dashiki-boom-dress?variant=22439851716"
	# path_prefix = "sample/women/skirt"   

	# extract_images(page_soup, path_prefix)

	category_list = [ "dashiki-shirts", "african-print-tops", "african-jumpsuits", "matching-sets", "african-print-pants", "african-print-skirts", "african-dresses"]

	for category in category_list:

		category_name = ""
		if category in ["dashiki-shirts", "african-print-tops"]:
			category_name = "women-tops"
		if category in ["african-print-skirts"]:
			category_name = "women-skirts"
		if category in ["african-dresses"]:
			category_name = "women-dresses"
		if category in ["african-jumpsuits"]:
			category_name = "women-jumpsuits"
		if category in ["matching-sets"]:
			category_name = "women-matching-sets"
		if category in ["african-print-pants"]:
			category_name = "women-pants-and-shorts"

		
		path_prefix = "data/women/" + category_name 
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
	


