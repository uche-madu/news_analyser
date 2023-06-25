# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import pytz


class NewsScraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # convert published_on to daylight savings aware UTC time 
        time_zone = pytz.timezone('US/Eastern')
        value = adapter.get("published_on")
        # Replace "ET" with the corresponding time zone offset
        value = value.replace('ET', '-0400')
        datetime_object = datetime.strptime(value , '%d %b, %Y, %H:%M %z').astimezone(time_zone)
        adapter["published_on"] = datetime_object
        
        # remove whitespace from texts
        text_fields = ["news_provided_by", "headline", "article"]
        for text_field in text_fields:
            value = adapter.get(text_field)
            adapter[text_field] = value.strip()

        return item
