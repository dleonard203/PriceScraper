from library import *

with open('config.json', 'r') as j_in:
	config_data = json.load(j_in)

sleep_minutes = config_data['sleep_minutes']
amazon_db = TinyDB('amazon.json')
#ebay_db = TinyDB('ebay.json')

#database storage
#{{item:string, prices:[[dt, price], [dt, price]]}, {item:string, prices:[[dt, price], [dt, price]]}}


def pretty_date_time():
	raw = str(datetime.datetime.now())
	return raw[:len(raw)-7]


def insert_into(item, price, db):
	question = Query()
	result = db.search(question.item == item)
	#not in database (yet)
	exists = True
	if result == []:
		exists = False
	if not exists:
		price_list = []
	else:
		price_list = result[0]["prices"]

	dt = pretty_date_time()
	price_list.append([dt, price])
	if exists:
		db.update({"prices": price_list}, question.item == item)
	else:
		db.insert({"item":item, "prices":price_list})


# for _ in range(10):
# 	insert_into("ssbm", 324.21, amazon_db)

count = 0
while True:
	if count % 5 == 0:
		print("current amazon db:\n")
		print(amazon_db.all())
	for item in config_data["items"]:
		try:
			price = float(scrape_amazon_for(item))
			insert_into(item, price, amazon_db)
		except Exception as e:
			print("got error: " + str(e) + "\nNot updating dbs...\n")
	time.sleep(sleep_minutes*60)
	count += 1