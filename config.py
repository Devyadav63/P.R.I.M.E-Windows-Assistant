import requests
from bs4 import BeautifulSoup

def get_live_scores():
    url = "https://www.espncricinfo.com/live-cricket-score"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    live_matches = soup.find_all(class_="match-info")
    
    if not live_matches:
        print("No live matches available.")
        return
    
    print("Live Matches:")
    
    for match in live_matches:
        match_title = match.find(class_="match-title").text.strip()
        team_scores = match.find(class_="teamscores").text.strip()
        status = match.find(class_="status").text.strip()
        
        print("Match:", match_title)
        print("Score:", team_scores)
        print("Status:", status)
        print("-------------------------")

def main():
    get_live_scores()

if __name__ == "__main__":
    main()
