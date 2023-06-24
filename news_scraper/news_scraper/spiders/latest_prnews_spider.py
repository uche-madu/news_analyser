import scrapy
import re

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', raw_html)
    return clean_text

class LatestPrnewsSpider(scrapy.Spider):
    name = "latest_prnews"
    start_urls = [
        "https://www.prnewswire.com/news-releases/news-releases-list/?page=1&pagesize=100",
    ]

    def parse(self, response):

        news = response.css("div.row.arabiclistingcards")
        for new in news:
            href = new.css("a::attr(href)").get()
            news_url = f"https://www.prnewswire.com{href}"

            yield response.follow(news_url, callback=self.parse_news_page)

        next_page = response.css("ul.pagination  a::attr(href)")[-1].get()
        if next_page is not None:
            next_page_url = "https://www.prnewswire.com/news-releases/news-releases-list/" + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_news_page(self, response):
        dirty_article = response.css("div.col-lg-10.col-lg-offset-1 p").getall()
        headline = response.css("h1::text").get()

        clean_article = ""
        for dirt in dirty_article:
            clean_article += clean_html(dirt) + "\n\n"
        
        yield {
            "published_on": response.xpath("//p[@class='mb-no']/text()").get(),
            "news_provided_by": response.xpath("//p[@class='meta']/following-sibling::a/strong/text()").get(),
            "headline": headline,
            "article": clean_article,
            "url": response.url,
            
        }
        
