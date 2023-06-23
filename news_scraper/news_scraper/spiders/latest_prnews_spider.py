import scrapy
import re

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', raw_html)
    return clean_text

class LatestPrnewsSpider(scrapy.Spider):
    name = "latest_prnews"
    # allowed_domains = ["https://www.prnewswire.com"]
    start_urls = [
        "https://www.prnewswire.com/news-releases/news-releases-list/?page=1&pagesize=100",
    ]

    def parse(self, response):

        news = response.css("div.row.arabiclistingcards")
        for new in news:
            href = new.css("a::attr(href)").get()
            news_url = f"https://www.prnewswire.com{href}"

            # lang = new.css("div::attr(lang)").get()
            # title = new.css("h3::text")[1].get()

            # yield {
            #     "lang": lang,
            #     "title": title,
            #     "url": news_url,
            # }

            yield response.follow(news_url, callback=self.parse_news_page)

        next_page = response.css("ul.pagination  a::attr(href)")[-1].get()
        if next_page is not None:
            next_page_url = "https://www.prnewswire.com/news-releases/news-releases-list/" + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_news_page(self, response):
        dirty = response.css("div.col-lg-10.col-lg-offset-1 p")[1:].getall()
        subhead = response.css("p.prntac i::text").getall()
        headline = response.css("h1::text").get()

        clean_subhead = ""
        for i in subhead:
            clean_subhead += clean_html(i)

        clean_article = ""
        for dirt in dirty:
            clean_article += clean_html(dirt) + "\n\n"
        
        yield {
            "headline": headline,
            "subhead": subhead,
            "article": clean_article,
            "url": response.url
        }
        
