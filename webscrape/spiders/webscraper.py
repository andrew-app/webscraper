import scrapy
import webbrowser
from colorama import Fore
from colorama import Style

i = 0
class CPUSpider(scrapy.Spider):
  
    name = "CPU"
    start_urls = ["https://www.pccasegear.com/products/52254/amd-ryzen-5-5600x-with-wraith-stealth","https://www.ple.com.au/Products/643561/AMD-Ryzen-5-5600X-37Ghz-6-Core-12-Thread-AM4---With-Wraith-Stealth-Cooler"]
    print(start_urls)    
    
    def parse(self, response):
        checktxt = ["In stock", "In Stock", "in stock"]

        global i

        buy = "PogU BUY NOW"
        
        
        

        i = i + 1
       
        case = True
        j = 0

        pccg = response.xpath("//a//text()").getall()
        ple = response.xpath("//div[@class='viewItemAvailabilityStatusWrapper']//text()").getall()   

        if i == 1:
            
            for stock in pccg:
                if checktxt[0] in stock:
                    print(f"{Fore.YELLOW}5600X In stock at PCCG {buy}{Style.RESET_ALL}")
                
                    webbrowser.open('https://www.pccasegear.com/products/52254/amd-ryzen-5-5600x-with-wraith-stealth')

                    case = False

                    break

        elif i == 2:
            
            for stock in ple:
                j = j + 1
                if checktxt[0] in stock:
                    print(f"{Fore.YELLOW}5600X In stock at PLE {buy}{Style.RESET_ALL}")

                    webbrowser.open('https://www.ple.com.au/Products/643561/AMD-Ryzen-5-5600X-37Ghz-6-Core-12-Thread-AM4---With-Wraith-Stealth-Cooler')

                    case = False

                    break

                if j == len(ple):
                    print(f"{Fore.YELLOW}NO CPU sadge{Style.RESET_ALL}")

        

                    
                  
        



        




