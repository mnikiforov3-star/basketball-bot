from telegram import Bot
import config, parser, analyzer, datetime as dt

bot = Bot(token=config.BOT_TOKEN)

def job():
    matches = parser.get_today_home_matches()
    for m in matches:
        prob, score = analyzer.predict_q1(m["home"], m["away"])
        text = f"""🏀 <b>{m['league']}</b>
📍 <b>{m['home']} – {m['away']}</b> (дома)
💰 Кэф: {m['odds']}
🎯 1-я четверть: <b>{m['home']}</b> победит с вероятностью {prob:.1%}
📊 Пример счёт: {score}
        """
        bot.send_message(chat_id=config.CHAT_ID, text=text, parse_mode="HTML")

if __name__ == "__main__":
    job()
