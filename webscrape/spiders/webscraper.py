import scrapy

class GPUSpider(scrapy.Spider):
    name = "GPU"
    start_urls = ["https://www.pccasegear.com/category/193_2145/graphics-cards/geforce-rtx-3060-ti"]
    
    def parse(self, response):
        cstock = response.xpath("//a//text()").extract()
        i = 0
        a = "In stock"

        for stock in cstock:
            if a in stock:
                i = i + 1
        
        print("No. of GPUs in stock PCCG: ", i)




