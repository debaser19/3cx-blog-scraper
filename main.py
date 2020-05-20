from selenium import webdriver

DRIVER_PATH = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://3cx.com/blog')

content = driver.find_element_by_class_name('fusion-read-more')
content.click()

driver.implicitly_wait(10)
title = driver.find_element_by_class_name('fusion-post-title')
title = title.get_attribute('outerHTML')
print(title)

post = driver.find_element_by_class_name('post-content')
post = post.get_attribute('outerHTML')
print(str(post))

# write to a file
# f = open("test.html", "w")
# f.write(post)
# f.close