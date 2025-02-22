from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# DRIVER_PATH = '/usr/local/bin/chromedriver'
# # Set up Chrome WebDriver
# driver = webdriver.Chrome(service=Service(executable_path=DRIVER_PATH))

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to Hacker News
driver.get("https://news.ycombinator.com/")

# Retrieve the page source
html = driver.page_source

# Close the driver
driver.quit()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all 'tr' elements with class 'athing' which contain the news titles
titles = soup.find_all('tr', class_='athing')

# Loop through each title and print it
for title in titles:
    # Find the <a> tag within the 'titleline' span inside a 'td' with class 'title'
    title_link = title.find('td', class_='title').find('span', class_='titleline').find('a')
    title_text = title_link.get_text()  # Extract the text of the title
    print(title_text)