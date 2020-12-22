import scrapy
import webbrowser
from time import sleep
from colorama import Fore
from colorama import Style
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process

i = 0

class MySpider(scrapy.Spider):
    name = "CPU"
    start_urls = ["https://www.pccasegear.com/products/52254/amd-ryzen-5-5600x-with-wraith-stealth","https://www.ple.com.au/Products/643561/AMD-Ryzen-5-5600X-37Ghz-6-Core-12-Thread-AM4---With-Wraith-Stealth-Cooler","https://www.centrecom.com.au/amd-ryzen-5-5600x-460ghz-6-cores-12-threads-am4-desktop-processor",]
    
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }
    
   
    def parse(self, response):
        checktxt = ["In stock", "In Stock", "in stock"]
        pccg = response.xpath("//div[@class='price-box']//text()").getall()
        ple = response.xpath("//div[@class='viewItemAvailabilityStatusWrapper']//text()").getall()
        ccom = response.xpath("//div[@class='prod_right']//text()").getall()  
        global i
        global start_urls
        i = i + 1
       
        j = 0

        if i == 1:
            
            for stock in pccg:
                j = j + 1
                
                if checktxt[0] in stock:
                    print(f"{Fore.BLUE}5600X @ PCCG::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                
                    webbrowser.open('https://www.pccasegear.com/products/52254/amd-ryzen-5-5600x-with-wraith-stealth')

                    break

                elif j == len(pccg):
                    print(f"{Fore.BLUE}5600X @ PCCG::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                    start_urls = []
                    
                    
        elif i == 2:
            
            for stock in ple:
                j = j + 1
                
                if checktxt[0] in stock:
                    
                    print(f"{Fore.BLUE}5600X @ PLE::{Fore.GREEN}In Stock{Style.RESET_ALL}")

                    webbrowser.open('https://www.ple.com.au/Products/643561/AMD-Ryzen-5-5600X-37Ghz-6-Core-12-Thread-AM4---With-Wraith-Stealth-Cooler')

                    break

                elif j == len(ple):
                    print(f"{Fore.BLUE}5600X @ PLE::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                    start_urls = []


        elif i == 3:
             
            for stock in ccom:
                j = j + 1
                
                if checktxt[0] in stock:
                    print(f"{Fore.BLUE}5600X @ Centrecom::{Fore.GREEN}In Stock{Style.RESET_ALL}")

                    webbrowser.open('https://www.centrecom.com.au/amd-ryzen-5-5600x-460ghz-6-cores-12-threads-am4-desktop-processor')

                    break

                elif j == len(ccom):
                    print(f"{Fore.BLUE}5600X @ Centrecom::{Fore.RED}Out of Stock{Style.RESET_ALL}")

                    
        


       
#threading.Timer(10,CheckStock).start()
def CheckStock():
    process = CrawlerProcess()
    process.crawl(MySpider)   
    process.start()
    #sleep(900)

CheckStock()    


