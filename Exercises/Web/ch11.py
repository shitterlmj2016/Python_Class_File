from selenium import webdriver
browser = webdriver.Chrome()
browser.get('http://inventwithpython.com')
linkElem = browser.find_element_by_link_text('More Info')
print(type(linkElem))
linkElem.click()  # follows the "Read It Online" link
