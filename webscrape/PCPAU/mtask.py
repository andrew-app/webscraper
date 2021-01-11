import scrapy
import time
from colorama import Fore, Style
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
from em_service import sendemail
import settings
import pymongo
urls = ["https://www.pccasegear.com/products/52254/amd-ryzen-5-5600x-with-wraith-stealth",
        "https://www.ple.com.au/Products/643561/AMD-Ryzen-5-5600X-37Ghz-6-Core-12-Thread-AM4---With-Wraith-Stealth-Cooler",
        "https://www.centrecom.com.au/amd-ryzen-5-5600x-460ghz-6-cores-12-threads-am4-desktop-processor"]
i = 0

class MySpider(scrapy.Spider):
    name = "CPU"
    start_urls = ["https://www.pccasegear.com/products/46835/amd-ryzen-5-3600-with-wraith-stealth"]
    custom_settings = {
        'LOG_ENABLED': 'False',
    }

    def parse(self, response):

        global i, start_time, start_time, check_time
        checktxt = ["In stock", "In Stock", "in stock", "Call"]
        stores = ["Online", "Bundoora"]

        j = 0

        if i == 0:

            pccg = response.xpath("//div[@class='price-box']//text()").getall()
            for stock in pccg:
                j = j + 1

                if checktxt[0] in stock:
                    print(f"{Fore.BLUE}@PCCG::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                    settings.inv["PCCG"] = "In Stock"
                elif j == len(pccg):  # 2nd last element in list will be ignored due to array indexing from 1 instead of 0

                    print(f"{Fore.BLUE}@PCCG::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                    i = i + 1
                    yield scrapy.Request(urls[1], callback=self.parse)


        elif i == 1:

            ple = response.xpath("//div[@class='viewItemAvailabilityStatusWrapper']//text()").getall()

            for stock in ple:
                j = j + 1

                if checktxt[0] in stock:

                    print(f"{Fore.BLUE}@PLE::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                    settings.inv["PLE"] = "In Stock"




                elif j == len(ple):

                    print(f"{Fore.BLUE}@PLE::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                    i = i + 1
                    yield scrapy.Request(urls[2], callback=self.parse)


        elif i == 2:
            ccom = response.xpath("//div[@class='prod_right']//text()").getall()
            a = False  # boolean for cases when one with status 'call'
            b = False
            for stock in ccom:
                j = j + 1
                if stores[0] in stock:
                    if checktxt[0] in ccom[j]:
                        print(
                            f"{Fore.BLUE}@Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                        settings.inv["CCOM"] = "In Stock"


                    elif checktxt[3] in ccom[j]:
                        print(
                            f"{Fore.BLUE}@Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.YELLOW}Call{Style.RESET_ALL}")
                        a = True
                        b = False

                elif stores[1] in stock:
                    if checktxt[0] in ccom[j]:
                        print(f"{Fore.BLUE}@Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                        settings.inv["CCOM"] = "In Stock"


                    elif checktxt[3] in ccom[j]:
                        print(
                            f"{Fore.BLUE}@Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.YELLOW}Call{Style.RESET_ALL}")

                        a = False
                        b = True

                elif j == len(ccom):

                    break
            if a == False and b == False:  # Both Out of Stock
                print(f"{Fore.BLUE}@Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                print(f"{Fore.BLUE}@Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")

            elif a == True and b == False:  # Online in stock
                print(
                    f"{Fore.BLUE}@Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")

            elif a == False and b == True:  # Bundoora in stock
                print(f"{Fore.BLUE}@Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")





def CheckStock():
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
    time.sleep(15)


if __name__ == '__main__':
    start_time = time.time()
    check_time = time.strftime("%H:%M:%S", time.gmtime(30))
    settings.init()
    print(settings.inv)
    print(settings.body)

    while True:
        p = Process(target=CheckStock)
        p.start()
        p.join()
        current_time = time.time()
        elapsed_time = current_time - start_time
        t = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(t)
        if t > check_time:  # email sent every 15 minutes when in stock

            start_time = time.time()

            if settings.body:
                print("email sent")
                sendemail("Product Status", settings.body)
                settings.body = []

























