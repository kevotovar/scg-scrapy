import scrapy
import collections

class SimpleScrapper(scrapy.Spider):
    name = "simple"

    def start_requests(self):
        urls = [
            'http://www.starcitygames.com/catalog/category/Rivals%20of%20Ixalan',
            'http://www.starcitygames.com/catalog/category/Dominaria',
            'http://www.starcitygames.com/catalog/category/Core%20Set%202019',
            'http://www.starcitygames.com/catalog/category/Guilds%20of%20Ravnica',
            'http://www.starcitygames.com/catalog/category/Ixalan',
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
                    rarity = item.css('.search_results_6::text').extract_first()
                    if rarity in ['R', 'M']:
                        id = item.css('.search_results_1 b a::attr(href)').extract_first().replace('http://www.starcitygames.com/catalog/magic_the_gathering/product/', '')
                        if '/' in id:
                            id = id.split('/')[0]
                        name = name.replace('\n', '')
                        price = item.css('.search_results_9::text').extract_first().replace('$', '')
                        price = float(price)
                        data = collections.OrderedDict()
                        data['id'] = id
                        data['name'] = name
                        data['expansion'] = expansion
                        data['rarity'] = rarity
                        data['price'] = price
                        data['mxn_regular'] = price * 17
                        data['mxn_client'] = price * 16
                        data['width'] = 8.8
                        data['height'] = .1
                        data['length'] = 6.3
                        data['weight'] = .001
                        yield(data)
                except Exception as e:
                    pass
        next_page_xpath = response.xpath('//*[@id="content"]/div[3]/a')[-1]
        next_page_text = next_page_xpath.css('::text').extract_first()
        if next_page_text == ' - Next>> ':
            next_page = next_page_xpath.css('::attr(href)').extract_first()
            yield response.follow(next_page, callback=self.parse)
