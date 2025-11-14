import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression

def get_team_stats(team):
    # парсим последние 5 матчей, % побед, средний счёт 1-й четверти
    return {
        "last5_win": 0.8,
        "avg_q1_for": 22.3,
        "avg_q1_against": 19.1,
        "injuries": 0,
        "h2h_q1": 0.6  # % побед в 1-й четверти личных встреч
    }

def predict_q1(home, away):
    h = get_team_stats(home)
    a = get_team_stats(away)
    features = np.array([[h["last5_win"], h["avg_q1_for"], h["avg_q1_against"],
                          a["last5_win"], a["avg_q1_for"], a["avg_q1_against"],
                          h["h2h_q1"], h["injuries"]]])
    model = LogisticRegression()  # обученная модель (сохраняйте в .pkl)
    prob = model.predict_proba(features)[0][1]  # вероятность победы дома
    score_home = int(h["avg_q1_for"] * 0.9 + a["avg_q1_against"] * 0.1)
    score_away = int(a["avg_q1_for"] * 0.9 + h["avg_q1_against"] * 0.1)
    return prob, f"{score_home}:{score_away}"
