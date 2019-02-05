from library import *

amazon_db = TinyDB('amazon.json')
ebay_db = TinyDB('ebay.json')

amazon_db.purge()
print(amazon_db.all())

ebay_db.purge()
print(ebay_db.all())