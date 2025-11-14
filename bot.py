# 1. ИМПОРТЫ (добавляем сюда)
import config
from utils import fetch_odds, kelly_stake, log, LEAGUE_SLUGS
from telegram import Bot

# 2. ОСНОВНОЙ КОД
bot = Bot(config.BOT_TOKEN)

def job():
    matches = parser.get_matches()
    for m in matches:
        # пример использования функций из utils
        odds   = fetch_odds(m["home"], m["away"])
        prob   = 0.65                       # заглушка
        stake  = kelly_stake(prob, odds)
        log(f"{m['home']} odds={odds} stake={stake:.2f}")

        text = f"""🏀 {m['liga']}
{m['home']} – {m['away']} (дома)
Коэффициент: {odds}
Вероятность: {prob:.1%}
Kelly-ставка: {stake:.1%} банка"""
        bot.send_message(chat_id=config.CHAT_ID, text=text)

if __name__ == "__main__":
    job()
