import scrapy
import webbrowser
class GPUSpider(scrapy.Spider):
  
    name = "CPU"
    start_urls = ["https://www.pccasegear.com/category/193_2145/graphics-cards/geforce-rtx-3060-ti"]
        
    
    def parse(self, response):
        
        cstock = response.xpath("//a//text()").extract()
        i = 0    

        a = "In stock"

        text = "BUY NOW"
    
        
        for stock in cstock:
            if a in stock:
                i = i + 1
        
        print("No. of CPUs in stock PCCG: ", i)

        if i > 0:
            
            print(text)
            webbrowser.open("https://www.pccasegear.com/category/193_2145/graphics-cards/geforce-rtx-3060-ti")
       




