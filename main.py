from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

URL = "https://www.drivendata.org/competitions/66/flu-shot-learning/leaderboard/"

def scrape_website():

    list_of_teams = ['computofilos','happy beavers', 'gatopizza','cross validation uclm','ml and prolog enjoyers','covid-24']
    i = 1
    data = []
    url = URL

    while True:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(options=options)
            
            driver.get(url)
            
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, "leaderTable")))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            table = soup.find('table', id='leaderTable')
            rows = table.find_all('tr')
            
            for row in rows[1:]:
                cols = row.find_all('td')
                if cols:
                    entry = {
                        'rank': cols[0].text.strip(),
                        'team': cols[2].find('div').find('div').find('div').text.strip().lower(),
                        'score': cols[3].text.strip(),
                        # 'entries': cols[3].text.strip(),
                        # 'last_submission': cols[4].text.strip()
                    }

                    if entry['team'] in list_of_teams:
                        data.append(entry)
                        list_of_teams.remove(entry['team'])
                        if not list_of_teams:
                            driver.quit()
                            return data

            i += 1
            print(i)
            url = "https://www.drivendata.org/competitions/66/flu-shot-learning/leaderboard/" + f"?page={i}"  
            if i > 25 :
                driver.quit()
                return data      
        except Exception as e:
            print(f"Error: {e}")
            return None

def main():
    results = scrape_website()
    
    if results:
        for entry in results:
            print(f"Rank: {entry['rank']}")
            print(f"Team: {entry['team']}")
            print(f"Score: {entry['score']}")
            # print(f"Entries: {entry['entries']}")
            # print(f"Last Submission: {entry['last_submission']}")
            print("-" * 50)

if __name__ == "__main__":
    main()