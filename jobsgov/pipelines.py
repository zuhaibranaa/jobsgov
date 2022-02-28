# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class JobsgovPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'mongodb://localhost:27017/*' 
        )
        self.db = self.conn['jobs_gov']
        self.collection = self.db['jobs_list']
    
    def process_item(self, item, spider):
        try:
            self.collection.insert_one(dict(item))
        except:
            return {'message': 'Item Already Exists'}
        return item
