import pyarrow as pa
import pyarrow.parquet as pq
from itemadapter import ItemAdapter
from datetime import datetime
import pytz
from google.cloud import storage
import os
import time
import pandas as pd

class NewsScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # convert published_on to daylight savings aware UTC time 
        time_zone = pytz.timezone('US/Eastern')
        value = adapter.get("published_on")
        # Replace "ET" with the corresponding time zone offset
        value = value.replace('ET', '-0400')
        datetime_object = datetime.strptime(value, '%d %b, %Y, %H:%M %z').astimezone(time_zone)
        adapter["published_on"] = datetime_object
        
        # remove whitespace from texts
        text_fields = ["news_provided_by", "headline", "article"]
        for text_field in text_fields:
            value = adapter.get(text_field)
            adapter[text_field] = value.strip()

        return item

class GCSStoragePipeline:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.file_rows = []

    @classmethod
    def from_crawler(cls, crawler):
        bucket_name = crawler.settings.get('GCS_BUCKET_NAME')
        return cls(bucket_name)

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        # Generate a unique file name for the session
        timestamp = time.strftime('%Y%m%d%H%M%S')
        file_name = f'latest_prnews/data_{timestamp}.parquet'

        # Save content to a local Parquet file
        local_file_name = f'{spider.name}_{timestamp}.parquet'
        df = pd.DataFrame(self.file_rows)

        # Add a dummy column to the DataFrame
        # This ensures that the resulting Parquet file will have at least  
        # one non-root column, avoiding the ValueError when reading it.
        df["dummy_column"] = ""

        table = pa.Table.from_pandas(df)
        pq.write_table(table, local_file_name)

        # Upload the file to GCS
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(local_file_name)
        spider.logger.info(f'Saved {file_name} to GCS bucket {self.bucket_name}')

        # Delete the local file
        os.remove(local_file_name)

    def process_item(self, item, spider):
        self.file_rows.append(dict(item))
        return item