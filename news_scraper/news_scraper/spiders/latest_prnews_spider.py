import scrapy
import re
import random
from news_scraper.items import NewsScraperItem

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', raw_html)
    return clean_text

class LatestPrnewsSpider(scrapy.Spider):
    name = "latest_prnews"
    start_urls = [
        "https://www.prnewswire.com/news-releases/news-releases-list/?page=1&pagesize=100",
    ]
    # override FEEDS in settings.py
    custom_settings = {
        'FEEDS': {
            'data/%(name)s/%(name)s_%(time)s.jsonl': {'format': 'jsonlines'},
            'data/%(name)s/%(name)s_%(time)s.csv': {'format': 'csv',}
        }
    
    }

    # user_agent_list = [
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    # 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    # 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    # ]

    def parse(self, response):

        news = response.css("div.row.arabiclistingcards")
        for new in news:
            href = new.css("a::attr(href)").get()
            news_url = f"https://www.prnewswire.com{href}"

            yield response.follow(
                news_url, 
                callback=self.parse_news_page,
                # headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]}
                )

        next_page = response.css("ul.pagination  a::attr(href)")[-1].get()
        if next_page is not None:
            next_page_url = "https://www.prnewswire.com/news-releases/news-releases-list/" + next_page
            yield response.follow(
                next_page_url, 
                callback=self.parse,
                # headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]}
                )

    def parse_news_page(self, response):
        dirty_article = response.css("div.col-lg-10.col-lg-offset-1 p").getall()
        headline = response.css("h1::text").get()

        clean_article = ""
        for dirt in dirty_article:
            clean_article += clean_html(dirt) + "\n\n"
        
        news_item = NewsScraperItem()
        
        news_item["published_on"] = response.xpath("//p[@class='mb-no']/text()").get()
        news_item["news_provided_by"] = response.xpath("//p[@class='meta']/following-sibling::a/strong/text()").get()
        news_item["headline"] = headline
        news_item["article"] = clean_article
        news_item["url"] = response.url
        
        yield news_item
    
        
