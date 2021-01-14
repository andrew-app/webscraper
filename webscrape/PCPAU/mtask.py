import scrapy
import time
from colorama import Fore, Style
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
from em_service import sendemail
import datetime
import pickle

urls = ["https://www.pccasegear.com/products/52254/amd-ryzen-5-5600x-with-wraith-stealth",
        "https://www.ple.com.au/Products/643561/AMD-Ryzen-5-5600X-37Ghz-6-Core-12-Thread-AM4---With-Wraith-Stealth-Cooler",
        "https://www.centrecom.com.au/amd-ryzen-5-5600x-460ghz-6-cores-12-threads-am4-desktop-processor"]
i = 0
store1 = False  # pccg stock flag
store2 = False  # ple '' ''
checktxt = ["In stock", "In Stock", "in stock", "Call"]
stores = ["Online", "Bundoora"]
inv = {
    "PCCG": "Out of Stock",
    "PLE": "Out of Stock",
    "CCOM": "Out of Stock"
}
body = []


class MySpider(scrapy.Spider):
    name = "PCPAU"
    start_urls = ["https://www.pccasegear.com/products/52254/amd-ryzen-5-5600x-with-wraith-stealth"]
    custom_settings = {
        'LOG_ENABLED': 'False',
    }

    def parse(self, response):

        global i, store1, store2, checktxt, stores, inv

        j = 0
        MySpider.test = 5
        if i == 0:

            pccg = response.xpath("//div[@class='price-box']//text()").getall()
            for stock in pccg:
                j = j + 1

                if checktxt[0] in stock:
                    print(f"{Fore.BLUE}@PCCG::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                    inv["PCCG"] = "In Stock"
                    store1 = True
                elif j == len(
                        pccg):  # 2nd last element in list will be ignored due to array indexing from 1 instead of 0
                    if store1 is False:
                        print(f"{Fore.BLUE}@PCCG::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                    i = i + 1
                    yield scrapy.Request(urls[1], callback=self.parse)


        elif i == 1:

            ple = response.xpath("//div[@class='viewItemAvailabilityStatusWrapper']//text()").getall()

            for stock in ple:
                j = j + 1

                if checktxt[0] in stock:

                    print(f"{Fore.BLUE}@PLE::{Fore.GREEN}In Stock{Style.RESET_ALL}")

                    MySpider.inv["PLE"] = "In Stock"
                    store2 = True



                elif j == len(ple):
                    if store2 is False:
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
                    if checktxt[1] in ccom[j]:
                        print(
                            f"{Fore.BLUE}@Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                        inv["CCOM"] = "In Stock"
                        a = True

                    elif checktxt[3] in ccom[j]:
                        print(
                            f"{Fore.BLUE}@Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.YELLOW}Call{Style.RESET_ALL}")
                        a = True


                elif stores[1] in stock:
                    if checktxt[1] in ccom[j]:
                        print(
                            f"{Fore.BLUE}@Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                        inv["CCOM"] = "In Stock"
                        b = True

                    elif checktxt[3] in ccom[j]:
                        print(
                            f"{Fore.BLUE}@Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.YELLOW}Call{Style.RESET_ALL}")

                        b = True

                if j == len(ccom):
                    break

            if a == False and b == False:  # Both Out of Stock
                print(
                    f"{Fore.BLUE}@Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                print(
                    f"{Fore.BLUE}@Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")

            elif a == True and b == False:  # Online in stock
                print(
                    f"{Fore.BLUE}@Centrecom{Fore.WHITE}(Bundoora){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")

            elif a == False and b == True:  # Bundoora in stock
                print(
                    f"{Fore.BLUE}@Centrecom{Fore.WHITE}(online){Fore.BLUE}::{Fore.RED}Out of Stock{Style.RESET_ALL}")

            # ADD MSY
            # response.xpath("//div[@class='product-specs-box']//tr[@class='odd']//td[@class='spec-value ui-table-text-center color-green']//text()").get()


def CheckStock():
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
    time.sleep(60)
    body.append([inv, urls])
    with open(status, 'wb') as fi:
        pickle.dump(inv, fi)


if __name__ == '__main__':
    check_time = time.strftime("%H:%M:%S", time.gmtime(1800))
    start_time = time.time()
    status = "data.pk"


    while True:
        p = Process(target=CheckStock)
        p.start()
        p.join()

        current_time = time.time()
        elapsed_time = current_time - start_time
        t = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        print("Uptime: ", t)
        if t > check_time:  # email sent every 15 minutes when in stock
            h, m, s = check_time.split(":")
            check_time_u = int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())
            check_time = check_time_u + 1800
            check_time = time.strftime("%H:%M:%S", time.gmtime(check_time))
            with open(status, 'rb') as fi:
                inv = pickle.load(fi)
            print(inv)
            if checktxt[1] in inv.values():
                print("email sent")
                sendemail("Product Status", body)


