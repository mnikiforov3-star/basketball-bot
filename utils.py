# utils.py
# Вспомогательные функции для бота (Win 7 / Python 3.8)

import os
import pickle
import requests
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


# 1. Базовый путь к файлам (рядом с bot.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# 2. Загрузка/сохранение pickle-объектов (модель, словари)
def load_pickle(filename):
    """Безопасно загружает pickle из папки BASE_DIR"""
    path = os.path.join(BASE_DIR, filename)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Файл {filename} не найден!")
    with open(path, "rb") as f:
        return pickle.load(f)


def save_pickle(obj, filename):
    """Сохраняет объект в pickle"""
    path = os.path.join(BASE_DIR, filename)
    with open(path, "wb") as f:
        pickle.dump(obj, f)
    print(f"[utils] Сохранено: {path}")


# 3. Простой парсер травм Flashscore (Selenium-версия ниже)
def get_injuries_flashscore(team_name):
    """Возвращает кол-во травмированных игроков команды (заглушка)"""
    # Пока возвращаем 0, ниже будет полный код под Win7 + Selenium
    return 0


# 4. Парсим реальные коэффициенты с the-odds-api (500 запросов/мес бесплатно)
ODDS_API_KEY = "ВСТАВЬТЕ_КЛЮЧ"   # берём на https://the-odds-api.com/
ODDS_URL = "https://api.the-odds-api.com/v4/sports/basketball_euroleague/odds"


def fetch_odds(home, away, regions="eu", markets="h2h"):
    """Возвращает коэфф. home_win для домашней команды"""
    if ODDS_API_KEY == "ВСТАВЬТЕ_КЛЮЧ":
        return 1.25  # заглушка
    params = {"apiKey": ODDS_API_KEY, "regions": regions, "markets": markets}
    r = requests.get(ODDS_URL, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    for game in data:
        if home in game["home_team"] and away in game["away_team"]:
            for bookmaker in game["bookmakers"]:
                for outcome in bookmaker["markets"][0]["outcomes"]:
                    if outcome["name"] == home:
                        return float(outcome["price"])
    return 1.25


# 5. Kelly-criterion (оптимальный % ставки)
def kelly_stake(prob, odds, k=0.25):
    """Возвращает рекомендованный % банка (0-1)"""
    if odds <= 1:
        return 0.0
    q = 1 - prob
    bp = odds - 1
    kelly = (bp * prob - q) / bp
    return max(0.0, kelly * k)   # дробный Kelly (защита)


# 6. Утилита: последние 5 матчей (заглушка, можно заменить CSV)
def last5_win_pct(team, games_df):
    """Считает % побед за 5 последних матчей"""
    last5 = games_df[games_df["team"] == team].tail(5)
    if last5.empty:
        return 0.5
    return last5["win"].mean()


# 7. Считаем средний счёт 1-й четверти (заглушка)
def avg_q1_score(team, games_df):
    """Возвращает средний счёт 1-й четверти команды"""
    sub = games_df[games_df["team"] == team]
    return sub["q1_score"].mean() if not sub.empty else 20.0


# 8. Проверка ОС (Win7-friendly)
def is_win7():
    """True если Windows 7"""
    ver = os.sys.getwindowsversion()
    return ver.major == 6 and ver.minor == 1


# 9. Быстрый лог (в файл)
def log(msg):
    log_path = os.path.join(BASE_DIR, "logs", "bot.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S}  {msg}\n")


# 10. Словарь лиг → Flashscore slug (дополняйте при необходимости)
LEAGUE_SLUGS = {
    "Евролига": "euroleague",
    "Единая лига ВТБ": "russia-vtb-united-league",
    "АКБ Испания": "spain-acb",
    "Суперлига Турция": "turkey-bsl",
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
