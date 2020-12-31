import scrapy
import webbrowser
import time
from colorama import Fore, Style
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
from email_service import sendemail


i = 0
urls = ["https://www.pccasegear.com/products/52254/amd-ryzen-5-5600x-with-wraith-stealth","https://www.ple.com.au/Products/643561/AMD-Ryzen-5-5600X-37Ghz-6-Core-12-Thread-AM4---With-Wraith-Stealth-Cooler","https://www.centrecom.com.au/amd-ryzen-5-5600x-460ghz-6-cores-12-threads-am4-desktop-processor"]

emf = False
s1 = False #flags for in stock at stores
s2 = False
s3 = False
body = []
class MySpider(scrapy.Spider):
    name = "CPU"
    start_urls=["https://www.pccasegear.com/products/46835/amd-ryzen-5-3600-with-wraith-stealth"]
    
    custom_settings = {
        'LOG_ENABLED': 'False',
    }

    def parse(self, response):
    
        checktxt = ["In stock", "In Stock", "in stock", "Call"]
        stores = ["Online","Bundoora"]
        global i,s1,s2,s3,body
        
        
        j = 0
        
        if i == 0:
            
            pccg = response.xpath("//div[@class='price-box']//text()").getall()
            for stock in pccg:
                j = j + 1
                
                if checktxt[0] in stock:
                    print(f"{Fore.BLUE}@PCCG::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                    s1 = True
                    
                elif j == len(pccg): #2nd last element in list will be ignored due to array indexing from 1 instead of 0
                    if s1 == False:
                        print(f"{Fore.BLUE}@PCCG::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                    i = i + 1
                    yield scrapy.Request("https://www.ple.com.au/Products/643561/AMD-Ryzen-5-5600X-37Ghz-6-Core-12-Thread-AM4---With-Wraith-Stealth-Cooler",callback=self.parse)

        elif i == 1:
            
            ple = response.xpath("//div[@class='viewItemAvailabilityStatusWrapper']//text()").getall()
            for stock in ple:
                j = j + 1
                
                if checktxt[0] in stock:
                    
                    print(f"{Fore.BLUE}@PLE::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                    s2 = True
                   

                    

                elif j == len(ple): 
                    if s2 == False:
                        print(f"{Fore.BLUE}@PLE::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                    i = i + 1
                    yield scrapy.Request("https://www.centrecom.com.au/amd-ryzen-5-5600x-460ghz-6-cores-12-threads-am4-desktop-processor",callback=self.parse)


        elif i == 2:
            ccom = response.xpath("//div[@class='prod_right']//text()").getall()
            a = False #boolean for cases when one with status 'call'
            b = False
            for stock in ccom:
                j = j + 1
                if stores[0] in stock:
                    if checktxt[0] in ccom[j]:
                        print(f"{Fore.BLUE}@Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                        s3 = True
                        
                        
                    elif checktxt[3] in ccom[j]:
                        print(f"{Fore.BLUE}@Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.YELLOW}Call{Style.RESET_ALL}")
                        a = True
                        b = False

                elif stores[1] in stock:
                    if checktxt[0] in ccom[j]:
                        print(f"{Fore.BLUE}@Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                        s3 = True
                        

                    elif checktxt[3] in ccom[j]:
                        print(f"{Fore.BLUE}@Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.YELLOW}Call{Style.RESET_ALL}")
                        
                        a = False
                        b = True
                       
                elif j == len(ccom):
                    break
                   
            if a == False and b == False: # Both Out of Stock
                print(f"{Fore.BLUE}@Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                print(f"{Fore.BLUE}@Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")

            elif a == True and b == False: #Online in stock
                print(f"{Fore.BLUE}@Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")

            elif a == False and b == True:#Bundoora in stock
                print(f"{Fore.BLUE}@Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")
            
             
            if t > check_time or emf == False: #email sent every 15 minutes when in stock
               
                if s1 == True and s2 == True and s3 == True:
                    body = ["In stock @ PCCG,PLE & Centrecom: ", urls]
                    
                elif s1 == True and s2 == False and s3 == False:
                    body = ["In stock @ PCCG: ", urls[0]]

                elif s1 == False and s2 == True and s3 == False:
                    body = ["In stock @ PLE: ", urls[1]]
                
                elif s1 == False and s2 == False and s3 == True:
                    body = ["In stock @ Centrecom: ", urls[2]]
                
                elif s1 == True and s2 == True and s3 == False:
                    body = ["In stock @ PCCG & PLE: ", urls[0][1]]
                
                elif s1 == True and s2 == False and s3 == True:
                    body = ["In stock @ PCCG & Centrecom: ", urls[0][2]]

                elif s1 == False and s2 == True and s3 == True:
                    body = ["In stock @ PLE & Centrecom: ", urls[1][2]]

            
   

    

def CheckStock():

    process = CrawlerProcess()
    process.crawl(MySpider)   
    process.start()
    time.sleep(15)          
                
            
if __name__ == '__main__':
    start_time = time.time()
    check_time = time.strftime("%H:%M:%S",time.gmtime(30))
    while True:
        p = Process(target=CheckStock)
        p.start()
        p.join()
        current_time = time.time()
        elapsed_time = current_time-start_time
        
        t = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(t)
        if body:
            print("email sent")
            sendemail("Product Status",body)
            start_time = time.time()
            emf = True


        
                   

           

    
    


