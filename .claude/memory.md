# FatvoAI - Islomiy fatvo AI yordamchisi

## Maqsad
7 ta islomiy fatvolar kitobiga asoslangan AI yordamchi. Foydalanuvchi savol beradi, AI javob beradi.

## Tech Stack
- **Framework:** Streamlit (Python)
- **AI:** OpenAI Assistant API
- **Transliteration:** UzTransliterator (lotin ↔ kiril)
- **Deploy:** Vercel / Streamlit Cloud

## Arxitektura
```
app.py              — Streamlit ilova (chat interfeys)
requirements.txt    — streamlit, openai, python-dotenv, UzTransliterator
env.example         — API key va Assistant ID
README.md           — Setup va deploy
```

## Muhim logika
- OpenAI Assistant API bilan multi-turn suhbat
- Avtomatik o'zbek transliteratsiya (lotin ↔ kiril)
- Session state bilan chat tarixini saqlash
- Thread management va error handling
