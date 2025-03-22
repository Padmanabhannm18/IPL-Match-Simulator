import requests
from bs4 import BeautifulSoup

def get_live_score():
    url = "https://www.espncricinfo.com/live-cricket-score"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    score = soup.find("div", class_="live-score").text.strip()
    return score
