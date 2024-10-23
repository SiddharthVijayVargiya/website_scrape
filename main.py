'''from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd

# Configure Chrome webdriver using webdriver-manager to automatically manage the driver
options = webdriver.ChromeOptions()
# Uncomment this line if you want to run headless (without GUI)
# options.add_argument('--headless')

# Use ChromeDriverManager to install the correct driver and create a Service object
service = Service(ChromeDriverManager().install())

# Initialize the WebDriver with Service and Options
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)  # Implicit wait for 10 seconds

# Navigate to the page with the table
url = 'https://eb.du.ac.in/web/book-details/index'
driver.get(url)

# Function to scrape data from the table
def scrape_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'table-striped'})
    
    # Extract table rows (excluding header)
    rows = table.find_all('tr')[2:]  # Skip header and filter rows
    data = []
    for row in rows:
        cells = row.find_all('td')
        # Extract ISBN, Title, Author, etc.
        row_data = {
            'S.No': cells[0].text.strip(),
            'ISBN': cells[1].text.strip(),
            'Title': cells[2].text.strip(),
            'Author': cells[3].text.strip(),
            'Year': cells[4].text.strip(),
            'Publisher': cells[5].text.strip(),
            'Link': cells[6].find('a')['href']  # URL in the 'Go' button
        }
        data.append(row_data)
    return data

# Function to click the "Next" button and go to the next page
def click_next_button():
    try:
        next_button = driver.find_element(By.LINK_TEXT, '»')
        next_button.click()
        time.sleep(2)  # Wait for the page to load
        return True
    except:
        return False  # No more pages

# Loop through all pages and scrape data
all_data = []
while True:
    # Scrape the current page's table
    page_html = driver.page_source
    data = scrape_table(page_html)
    all_data.extend(data)
    
    # Check if there's a next page
    if not click_next_button():
        break  # Exit loop if no more pages

# Save data to an Excel sheet using pandas
df = pd.DataFrame(all_data)
df.to_excel('scraped_data.xlsx', index=False)  # Save without the DataFrame index

# Quit the driver
driver.quit()

print("Data has been successfully saved to 'scraped_data.xlsx'")
'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# Configure Chrome webdriver
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Uncomment to run headless
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)

# Navigate to the page with the table
url = 'https://eb.du.ac.in/web/book-details/index'
driver.get(url)

# Wait until the table is present on the page
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-striped')))
    print("Table loaded successfully.")
except Exception as e:
    print("Error: Table not found.")
    driver.quit()
    exit()

# Function to scrape data from the table
def scrape_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'table-striped'})
    
    # Ensure the table exists before proceeding
    if table is None:
        print("Table not found in HTML.")
        return []
    
    rows = table.find_all('tr')[2:]  # Skip header
    data = []
    for row in rows:
        cells = row.find_all('td')
        row_data = {
            'S.No': cells[0].text.strip(),
            'ISBN': cells[1].text.strip(),
            'Title': cells[2].text.strip(),
            'Author': cells[3].text.strip(),
            'Year': cells[4].text.strip(),
            'Publisher': cells[5].text.strip(),
            'Link': cells[6].find('a')['href']  # URL in the 'Go' button
        }
        data.append(row_data)
    return data

# Function to click the "Next" button and go to the next page
def click_next_button():
    try:
        next_button = driver.find_element(By.LINK_TEXT, '»')
        next_button.click()
        return True
    except Exception as e:
        return False  # No more pages

# Loop through all pages and scrape data
all_data = []
try:
    while True:
        # Scrape the current page's table
        page_html = driver.page_source
        data = scrape_table(page_html)
        all_data.extend(data)

        # Check if there's a next page
        if not click_next_button():
            break  # Exit loop if no more pages
except Exception as e:
    print(f"An error occurred during scraping: {e}")

# Save data to an Excel sheet using pandas
try:
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_excel('scraped_data.xlsx', index=False)
        print("Data has been successfully saved to 'scraped_data.xlsx'")
    else:
        print("No data scraped.")
except Exception as e:
    print(f"Error saving data: {e}")

# Quit the driver
driver.quit()
