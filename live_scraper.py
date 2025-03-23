from bs4 import BeautifulSoup
import requests

def get_live_score():
    url = "https://www.cricapi.com/"  
    response = requests.get(url)

    if response.status_code != 200:
        return "Error fetching live score"

    soup = BeautifulSoup(response.text, "html.parser")
    score_element = soup.find("div", class_="live-score")

    if score_element:
        return score_element.text.strip()
    else:
        return "Live score not available"
