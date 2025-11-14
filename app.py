# chatbot_ui.py
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from UzTransliterator import UzTransliterator

# .env faylini yuklash (local development uchun)
load_dotenv()

# OpenAI client - API key ni olish
# Streamlit Cloud da st.secrets, local da .env fayl
try:
    # Streamlit Cloud Secrets (production)
    api_key = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    # Local development (.env fayl)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ OPENAI_API_KEY topilmadi!")
        st.info("💡 **Local development:** `.env` fayl yaratib, ichiga quyidagini yozing:\n`OPENAI_API_KEY=sk-...`\n\n"
                "💡 **Streamlit Cloud:** App Settings > Secrets bo'limida quyidagini yozing:\n"
                "```toml\nOPENAI_API_KEY = \"sk-...\"\n```")
        st.stop()

try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    error_msg = str(e)
    if "401" in error_msg or "invalid_api_key" in error_msg or "Incorrect API key" in error_msg:
        st.error("❌ **API Key noto'g'ri yoki eskirgan!**")
        st.info("💡 Iltimos, quyidagilarni tekshiring:\n"
                "1. `.env` faylda API key to'g'ri yozilganmi?\n"
                "2. API key hali ham faolmi? (https://platform.openai.com/account/api-keys)\n"
                "3. API key to'liq ko'chirilganmi? (boshlanishi `sk-` bilan)")
    else:
        st.error(f"❌ Xatolik: {error_msg}")
    st.stop()

transliterator = UzTransliterator.UzTransliterator()

# Assistant ID ni olish
# Streamlit Cloud da st.secrets, local da .env fayl
try:
    # Streamlit Cloud Secrets (production)
    ASSISTANT_ID = st.secrets["OPENAI_ASSISTANT_ID"]
except (KeyError, FileNotFoundError):
    # Local development (.env fayl)
    ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
    if not ASSISTANT_ID:
        st.error("❌ **Assistant ID topilmadi!**")
        st.info("💡 **Local development:** `.env` faylda quyidagini yozing:\n`OPENAI_ASSISTANT_ID=asst-...`\n\n"
                "💡 **Streamlit Cloud:** App Settings > Secrets bo'limida quyidagini yozing:\n"
                "```toml\nOPENAI_ASSISTANT_ID = \"asst-...\"\n```")
        st.stop()

# Sahifa sozlamalari
st.set_page_config(
    page_title="Fatvo Maslahatchi",
    page_icon="🕌",
    layout="centered"
)

# Sarlavha
st.title("🕌 Fatvo Maslahatchi")
st.caption("Islomiy fatvolar bo'yicha AI yordamchi")

# Tarjima funktsiyalari
def preprocess_question(question):
    """
    Savolni qayta ishlash: har doim lotin → kiril konversiya qiladi
    """
    try:
        # Har doim lotin → kiril konversiya qilish
        question_cyr = transliterator.transliterate(
            question, 
            from_="lat", 
            to="cyr"
        )
        return question_cyr, "converted"
    except Exception as e:
        st.warning(f"⚠️ Transliteration xatolik: {e}")
        return question, "failed"

def postprocess_response(response):
    """
    Javobni qayta ishlash: har doim kiril → lotin konversiya qiladi
    """
    try:
        # Har doim kiril → lotin konversiya qilish
        response_lat = transliterator.transliterate(
            response,
            from_="cyr",
            to="lat"
        )
        return response_lat, "converted"
    except Exception as e:
        st.warning(f"⚠️ Javob konversiya xatolik: {e}")
        return response, "failed"

# Thread yaratish funktsiyasi
def get_or_create_thread():
    """
    Thread yaratish yoki mavjud threadni qaytarish
    """
    if 'thread_id' not in st.session_state or not st.session_state.thread_id:
        try:
            thread = client.beta.threads.create()
            st.session_state.thread_id = thread.id
            return thread.id
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "invalid_api_key" in error_msg or "Incorrect API key" in error_msg:
                st.error("❌ **API Key noto'g'ri!** Thread yaratib bo'lmadi.")
                st.info("💡 Iltimos, `.env` fayldagi API keyni tekshiring.")
            else:
                st.error(f"❌ Thread yaratishda xatolik: {error_msg}")
            return None
    return st.session_state.thread_id

# Session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
# Thread lazy loading - faqat kerak bo'lganda yaratiladi

# Chat tarixini ko'rsatish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Agar konversiya bo'lgan bo'lsa, ko'rsatish
        if message.get("converted"):
            st.caption(f"🔄 Lotin: {message['original']}")

# Savol kiritish
if prompt := st.chat_input("Savolingizni yozing (lotin yozuvda)..."):
    # Original savolni saqlash
    original_prompt = prompt
    
    # Foydalanuvchi savolini ko'rsatish (original)
    st.session_state.messages.append({
        "role": "user", 
        "content": original_prompt,
        "original": original_prompt
    })
    with st.chat_message("user"):
        st.markdown(original_prompt)
    
    # Savolni pre-process qilish (lotin → kiril)
    processed_prompt, status = preprocess_question(original_prompt)
    
    # Agar konversiya bo'lgan bo'lsa, xabar ko'rsatish
    if status == "converted":
        st.info(f"🔄 Kiril yozuvga o'girildi: {processed_prompt}")
    
    # Assistant javobini olish
    with st.chat_message("assistant"):
        with st.spinner("Javob tayyorlanmoqda..."):
            try:
                # Thread yaratish yoki olish
                thread_id = get_or_create_thread()
                if not thread_id:
                    st.error("❌ Thread yaratib bo'lmadi. Iltimos, API keyni tekshiring.")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "❌ Thread yaratib bo'lmadi. Iltimos, API keyni tekshiring."
                    })
                    st.stop()
                
                # PROCESSED savolni yuborish (kiril)
                client.beta.threads.messages.create(
                    thread_id=thread_id,
                    role="user",
                    content=processed_prompt  # ← MUHIM: Kiril savol!
                )
            
                # Assistant ni ishga tushirish (timeout 90 soniya - ko'p user uchun)
                run = client.beta.threads.runs.create_and_poll(
                    thread_id=thread_id,
                    assistant_id=ASSISTANT_ID,
                    timeout=90
                )
                
                # Javobni olish
                if run.status == 'completed':
                    messages = client.beta.threads.messages.list(
                        thread_id=thread_id
                    )
                    
                    # Eng oxirgi javob (assistant) - kiril yozuvda
                    response_cyr = messages.data[0].content[0].text.value
                    
                    # Javobni lotin yozuvga o'girish (kiril → lotin)
                    response_lat, response_status = postprocess_response(response_cyr)
                    
                    # Javobni ko'rsatish (lotin yozuvda)
                    st.markdown(response_lat)
                    
                    # Session ga saqlash
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_lat,  # Lotin yozuvda saqlanadi
                        "converted": response_status == "converted",
                        "original": response_cyr if response_status == "converted" else None  # Kiril versiyasi
                    })
                elif run.status == 'failed':
                    error_msg = f"❌ Xatolik yuz berdi: {run.last_error.message if run.last_error else run.status}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                elif run.status == 'requires_action':
                    st.warning("⚠️ Assistant qo'shimcha ma'lumot so'ramoqda. Iltimos, qayta urinib ko'ring.")
                else:
                    error_msg = f"⏳ Javob kutayapti: {run.status}. Iltimos, biroz kuting va qayta urinib ko'ring."
                    st.warning(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
            except Exception as e:
                error_msg = f"❌ Xatolik: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Sidebar - Ma'lumot
with st.sidebar:
    st.header("📚 Haqida")
    st.write("""
    **Fatvo Maslahatchi** - 7 ta islomiy fatvolar 
    kitobiga asoslangan AI yordamchi.
    
    **Imkoniyatlar:**
    - ✅ O'zbek tili (lotin yozuv - kirilga o'giriladi va javob lotinda qaytariladi)
    - ✅ 7 ta fatvolar kitobidan qidiruv
    - ✅ Aniq manbalar bilan javob
    - ✅ 24/7 ishlash
    
    **Qanday ishlatish:**
    1. Savolingizni yozing
    2. Javobni kuting
    3. Kerak bo'lsa qo'shimcha savol bering
    """)
    
    st.divider()
    
    st.header("⚙️ Sozlamalar")
    if st.button("🗑️ Suhbatni tozalash"):
        st.session_state.messages = []
        try:
            thread = client.beta.threads.create()
            st.session_state.thread_id = thread.id
            st.success("✅ Yangi suhbat boshlandi!")
            st.rerun()
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "invalid_api_key" in error_msg:
                st.error("❌ API Key noto'g'ri! Yangi thread yaratib bo'lmadi.")
            else:
                st.error(f"❌ Xatolik: {error_msg}")
    
    st.divider()
    
    thread_id = get_or_create_thread()
    if thread_id:
        st.caption(f"Thread ID: `{thread_id}`")
    st.caption(f"Xabarlar: {len(st.session_state.messages)}")
    
    st.divider()
    
    st.header("🔧 Texnik ma'lumot")
    st.caption("✅ Multi-user support: Har bir foydalanuvchi o'z thread ID bilan ishlaydi")
    st.caption("✅ Tarjima: Lotin → Kiril (savol), Kiril → Lotin (javob)")
    st.caption("✅ Error handling: Xatoliklarni to'g'ri boshqarish")
