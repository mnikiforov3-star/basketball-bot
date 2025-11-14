import requests, json, datetime as dt
from bs4 import BeautifulSoup
import config

LEAGUES = {
    "Евролига": "euroleague",
    "Еврокубок": "eurocup",
    "Лига чемпионов": "basketball-champions-league",
    "Лига А Италия": "italy-lega-a",
    "Единая лига ВТБ": "russia-vtb-united-league",
    "Суперлига Турция": "turkey-bsl",
    "АКБ Испания": "spain-acb",
    "ЛНБ Франция": "france-lnb",
    "ББЛ Германия": "germany-bbl",
    "ЛКЛ Литва": "lithuania-lkl",
    "Высшая лига Словакия": "slovakia-sbl",
    "Высшая лига Финляндия": "finland-korisliiga",
    "Премьер-лига Хорватия": "croatia-premijer-liga",
    "Высшая лига Австрия": "austria-bundesliga",
    "Латвийско-эстонская лига": "latvia-estonia-lbl",
    "Адриатическая лига": "adriatic-league",
    "Высшая лига Норвегия": "norway-bln",
}

def get_today_home_matches(max_odds=1.40):
    matches = []
    for league, slug in LEAGUES.items():
        url = f"https://www.flashscore.com/basketball/{slug}/fixtures/"
        html = requests.get(url, headers=config.HEADERS).text
        soup = BeautifulSoup(html, "lxml")
        for row in soup.select("div.event__match"):
            home = row.select_one(".event__home").text
            away = row.select_one(".event__away").text
            is_home = True  # фильтруем ниже
            odds = float(row.select_one(".event__odd")["data-odd"])  # пример
            if is_home and odds <= max_odds:
                matches.append({
                    "league": league,
                    "home": home,
                    "away": away,
                    "odds": odds,
                    "url": "https://www.flashscore.com" + row["data-id"]
                })
    return matches
