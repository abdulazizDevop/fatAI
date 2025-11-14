# 🕌 Fatvo Maslahatchi

Islomiy fatvolar bo'yicha AI yordamchi - 7 ta islomiy fatvolar kitobiga asoslangan Streamlit ilovasi.

## ✨ Imkoniyatlar

- ✅ O'zbek tili qo'llab-quvvatlash (lotin yozuv)
- ✅ 7 ta fatvolar kitobidan qidiruv
- ✅ Aniq manbalar bilan javob
- ✅ Avtomatik yozuv konversiyasi (lotin ↔ kiril)
- ✅ Multi-user support (8-10 foydalanuvchi bir vaqtda)
- ✅ 24/7 ishlash

## 🚀 O'rnatish

### 1. Loyihani klonlash

```bash
git clone <repository-url>
cd fatvoAI
```

### 2. Virtual environment yaratish

```bash
python -m venv venv
```

### 3. Virtual environmentni faollashtirish

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Kerakli paketlarni o'rnatish

```bash
pip install -r requirements.txt
```

### 5. Environment variable sozlash

1. `env.example` faylini `.env` nomiga o'zgartiring:
   ```bash
   copy env.example .env  # Windows
   # yoki
   cp env.example .env     # Linux/Mac
   ```

2. `.env` faylini oching va OpenAI API keyingizni yozing:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```

3. API key olish:
   - https://platform.openai.com/account/api-keys ga kiring
   - "Create new secret key" tugmasini bosing
   - API keyni ko'chirib, `.env` faylga yozing

### 6. Dasturni ishga tushirish

```bash
streamlit run app.py
```

Brauzerda avtomatik ochiladi: http://localhost:8501

## ☁️ Streamlit Cloud ga Deploy qilish

### 1. GitHub ga yuklash

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Streamlit Cloud ga ulash

1. https://share.streamlit.io ga kiring
2. "New app" tugmasini bosing
3. GitHub reponi tanlang
4. Branch va main file ni tanlang (`app.py`)

### 3. Secrets sozlash

Streamlit Cloud da **App Settings > Secrets** bo'limida quyidagi formatda yozing:

```toml
OPENAI_API_KEY = "sk-proj-your-api-key-here"
OPENAI_ASSISTANT_ID = "asst_***"
```

**Muhim:**
- TOML formatida yozing (qo'shtirnoq ichida)
- `=` belgisi atrofida bo'sh joy bo'lishi kerak
- Qo'shtirnoqlar ichida API key va Assistant ID yoziladi

### 4. Deploy

"Deploy" tugmasini bosing. Bir necha daqiqadan keyin ilova ishga tushadi!

## 📋 Talablar

- Python 3.8+
- OpenAI API key
- Internet ulanishi

## 🔧 Texnik ma'lumotlar

- **Framework:** Streamlit
- **AI:** OpenAI Assistants API
- **Tarjima:** UzTransliterator
- **Multi-user:** Streamlit session state

## 📝 Foydalanish

1. Dasturni ishga tushiring
2. Savolingizni lotin yozuvda yozing
3. Javobni kuting (avtomatik lotin yozuvda ko'rsatiladi)
4. Qo'shimcha savollar bering

## ⚠️ Eslatmalar

- `.env` fayl hech qachon Git ga yuklanmaydi (`.gitignore` da)
- API keyni hech kimga ko'rsatmang
- Har bir foydalanuvchi o'z thread ID bilan ishlaydi

## 📄 Litsenziya

MIT

## 👤 Muallif

Abdulaziz Olimov

