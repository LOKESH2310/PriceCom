from autoscraper import AutoScraper
import pandas as pd

search="iphones"
amazon_url="https://www.amazon.in/s?k={}&ref=nb_sb_noss_2".format(search)
print(amazon_url)
wanted_list=["https://m.media-amazon.com/images/I/71i2XhHU3pL._AC_UY218_.jpg","New Apple iPhone 11 (64GB) - Black","51,999"]

scraper=AutoScraper()

result=scraper.build(amazon_url,wanted_list)
#print(result)
data=scraper.get_result_similar(amazon_url,grouped=True)
print(data)

keys=list(data.keys())
print(keys)

scraper.set_rule_aliases({str(keys[0]):"ImageUrl",str(keys[2]):'Title',str(keys[4]):'Price'})
scraper.save("amazon.json")
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

