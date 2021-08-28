from autoscraper import AutoScraper
import pandas as pd

search="iphones"
flipkart_url="https://www.flipkart.com/search?q={}".format(search)
print(flipkart_url)
wanted_list=["https://rukminim1.flixcart.com/image/312/312/kg8avm80/mobile/r/h/z/apple-iphone-12-dummyapplefsn-original-imafwg8dqgncgbcb.jpeg?q=70","APPLE iPhone 12 (Black, 128 GB)","₹71,999"]

scraper=AutoScraper()

result=scraper.build(flipkart_url,wanted_list)
#print(result)
data=scraper.get_result_similar(flipkart_url,grouped=True)
print(data)

keys=list(data.keys())
print(keys)

scraper.set_rule_aliases({str(keys[0]):"ImageUrl",str(keys[3]):'Title',str(keys[5]):'Price'})
scraper.save("flipkart.json")
# print(scraper)
# amazon_scraper=AutoScraper()
# amazon_scraper.load('amazon.json')
#
# search="oppo"
# amazon_url="https://www.amazon.in/s?k={}&s=price-desc-rank".format(search)
#
# data=amazon_scraper.get_result_similar(amazon_url,group_by_alias=True)
# search_data=tuple(zip(data['Title'],data['ImageUrl'],data['Price'],data['Reviews']))
#
# df=pd.DataFrame(columns=['Query','Title','Price','Reviews','ImageUrl'])
# for i in range(len(search_data)):
#     df.loc[len(df)]=[search,search_data[i][0],search_data[i][2],search_data[i][3],search_data[i][1]]

#print(df.shape)
#print(df)

