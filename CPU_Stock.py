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
    start_urls=["https://www.pccasegear.com/products/52254/amd-ryzen-5-5600x-with-wraith-stealth"]
    
    def parse(self, response):
        checktxt = ["In stock", "In Stock", "in stock", "Call"]
        stores = ["Online","Bundoora"]
        global i
        
        j = 0
        
        if i == 0:
            
            pccg = response.xpath("//div[@class='price-box']//text()").getall()
            for stock in pccg:
                j = j + 1
                
                if checktxt[0] in stock:
                    print(f"{Fore.BLUE}5600X @ PCCG::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                
                    webbrowser.open('https://www.pccasegear.com/products/52254/amd-ryzen-5-5600x-with-wraith-stealth')

                    break

                elif j == len(pccg): #2nd last element in list will be ignored due to array indexing from 1 instead of 0
                    print(f"{Fore.BLUE}5600X @ PCCG::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                    i = i + 1
                    yield scrapy.Request("https://www.ple.com.au/Products/643561/AMD-Ryzen-5-5600X-37Ghz-6-Core-12-Thread-AM4---With-Wraith-Stealth-Cooler",callback=self.parse)

        elif i == 1:
            
            ple = response.xpath("//div[@class='viewItemAvailabilityStatusWrapper']//text()").getall()
            for stock in ple:
                j = j + 1
                
                if checktxt[0] in stock:
                    
                    print(f"{Fore.BLUE}5600X @ PLE::{Fore.GREEN}In Stock{Style.RESET_ALL}")

                    webbrowser.open('https://www.ple.com.au/Products/643561/AMD-Ryzen-5-5600X-37Ghz-6-Core-12-Thread-AM4---With-Wraith-Stealth-Cooler')

                    break

                elif j == len(ple): 
                    print(f"{Fore.BLUE}5600X @ PLE::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                    i = i + 1
                    yield scrapy.Request("https://www.centrecom.com.au/amd-ryzen-5-5600x-460ghz-6-cores-12-threads-am4-desktop-processor",callback=self.parse)


        elif i == 2:
            ccom = response.xpath("//div[@class='prod_right']//text()").getall()
            a = False #boolean for cases when one with status call
            b = False
            for stock in ccom:
                j = j + 1
                if stores[0] in stock:
                    if checktxt[0] in ccom[j]:
                        print(f"{Fore.BLUE}5600X @ Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.GREEN}In Stock{Style.RESET_ALL}")

                        webbrowser.open('https://www.centrecom.com.au/amd-ryzen-5-5600x-460ghz-6-cores-12-threads-am4-desktop-processor')
                        break

                        

                    elif checktxt[3] in ccom[j]:
                        print(f"{Fore.BLUE}5600X @ Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.YELLOW}Call{Style.RESET_ALL}")
                        a = True
                        b = False
                elif stores[1] in stock:
                    if checktxt[0] in ccom[j]:
                        print(f"{Fore.BLUE}5600X @ Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                        break
                        

                    elif checktxt[3] in ccom[j]:
                        print(f"{Fore.BLUE}5600X @ Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.YELLOW}Call{Style.RESET_ALL}")
                        a = False
                        b = True
                       
                elif j == len(ccom):
                    break
                   
            if a == False and b == False: # Both Out of Stock
                print(f"{Fore.BLUE}5600X @ Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                print(f"{Fore.BLUE}5600X @ Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")

            elif a == True and b == False: #
                print(f"{Fore.BLUE}5600X @ Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")

            elif a == False and b == True:
                print(f"{Fore.BLUE}5600X @ Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")
           
def CheckStock():
    process = CrawlerProcess()
    process.crawl(MySpider)   
    process.start()
    #sleep(900)

CheckStock()    


