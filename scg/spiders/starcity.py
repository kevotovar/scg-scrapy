import scrapy

class SimpleScrapper(scrapy.Spider):
    name = "simple"

    def start_requests(self):
        urls = [
            'http://www.starcitygames.com/catalog/category/Kaladesh',
            'http://www.starcitygames.com/catalog/category/Aether%20Revolt',
            'http://www.starcitygames.com/catalog/category/Amonkhet',
            'http://www.starcitygames.com/catalog/category/Hour%20of%20Devastation',
            'http://www.starcitygames.com/catalog/category/Explorers%20of%20Ixalan',
            'http://www.starcitygames.com/catalog/category/Rivals%20of%20Ixalan',
            'http://www.starcitygames.com/catalog/category/Dominaria',
            'http://www.starcitygames.com/catalog/category/Core%20Set%202019'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.css('.deckdbbody_row, .deckdbbody2_row')
        for item in items:
            name = item.css('.search_results_1 a::text').extract_first()
            if name:
                try:
                    expansion = (
                        item.css('.search_results_2 a::text').extract_first().rstrip()
                    )
                    name = name.replace('\n', '')
                    price = item.css('.search_results_9::text').extract_first().replace('$', '')
                    price = float(price)
                    yield(dict(
                        name=name,
                        expansion=expansion,
                        price=price,
                        mxn_regular=price * 16,
                        mxn_client=price * 15
                    ))
                except Exception as e:
                    print("Card couldn't be processed")
        next_page_xpath = response.xpath('//*[@id="content"]/div[3]/a')[-1]
        next_page_text = next_page_xpath.css('::text').extract_first()
        if next_page_text == ' - Next>> ':
            next_page = next_page_xpath.css('::attr(href)').extract_first()
            yield response.follow(next_page, callback=self.parse)
