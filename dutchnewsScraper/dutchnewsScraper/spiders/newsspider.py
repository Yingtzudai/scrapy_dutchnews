import scrapy


class NewsspiderSpider(scrapy.Spider):
    name = "newsspider"
    allowed_domains = ["dutchnews.nl"]
    start_urls = ["https://www.dutchnews.nl/category/environment/"]

    def parse(self, response):
        all_news = response.css("div.col-12")
        for news in all_news:
            yield{
                'title':news.css('a.text-reset.text-decoration-none::text').get(),
                # This targets the <a> tag with the specific classes text-reset and text-decoration-none.
                # ::text >>This pseudo-selector extracts the visible text content from the selected elements.
                'url': news.css('a::attr(href)').get(),

            }
        
        next_page = response.css('li.page-item.next a.page-link::attr(href)').get()
        if next_page is not None:
            next_page_url = "https://www.dutchnews.nl" + next_page
            yield response.follow(next_page_url, callback = self.parse)
