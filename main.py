from selenium import webdriver
from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods import posts
import creds

def grabLatestPost():
    # define webdriver and blog url
    DRIVER_PATH = 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get('https://3cx.com/blog')

    # search for the read more link and click it
    content = driver.find_element_by_class_name('fusion-read-more')
    content.click()

    # wait for page to load and grab the title
    driver.implicitly_wait(10)
    title = driver.find_element_by_class_name('fusion-post-title')
    title = title.get_attribute('innerHTML')

    # grab the content of the post
    post = driver.find_element_by_class_name('post-content')
    post = post.get_attribute('outerHTML')

    return post, title

def writeToFile():
    # set post and encode in utf-8 to handle unicode characters when writing
    post = grabLatestPost()
    filename = str(post[1])+'.html'
    with open(filename, 'wb') as f:
        f.write(post[0].encode('utf-8'))
        f.close()

def sendToWP():
    url = creds.creds['url']
    user = creds.creds['user']
    pwd = creds.creds['pwd']


    client = Client(url, user, pwd)

    post = grabLatestPost()
    wppost = WordPressPost()
    wppost.title = post[1]
    wppost.content = post[0]
    wppost.id = client.call(posts.NewPost(wppost))

    wppost.post_status = 'draft'
    client.call(posts.EditPost(wppost.id, wppost))


# writeToFile()
sendToWP()