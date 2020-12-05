from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.pccasegear.com/products/52597/asus-geforce-rtx-3060-ti-dual-oc-8gb")
el = driver.find_element_by_type_name('submit')
str1=el.text 
print(str1.find("In stock"))
if(str1.find("In stock") == -1):
    print("Sadge")
else: 
    print("ryzen AVAILABLE PogU")
driver.close()