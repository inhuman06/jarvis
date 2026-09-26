# test_keys.py
import os
from dotenv import load_dotenv
from groq import Groq
from google import genai

print("=== STARTING API VALIDATION DIAGNOSTIC ===")

# 1. Test .env file reading
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

print(f"Reading .env file...")
print(f"-> GROQ_API_KEY detected: {'✅ YES' if groq_key else '❌ NO (Check .env file name and location)'}")
print(f"-> GEMINI_API_KEY detected: {'✅ YES' if gemini_key else '❌ NO (Check .env file name and location)'}")
print("-" * 50)

# 2. Test Live Groq Key Connection
if groq_key:
    print("Testing Groq Cloud Server Connection...")
    try:
        groq_client = Groq(api_key=groq_key)
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Respond with the word 'SUCCESS'"}],
            max_tokens=10
        )
        response_text = completion.choices[0].message.content.strip()
        print(f"-> Groq API Status: 🎉 WORKING! Server says: '{response_text}'")
    except Exception as e:
        print(f"-> Groq API Status: ❌ FAILED! Error returned:\n   {e}")
else:
    print("Skipping Groq test due to missing key.")

print("-" * 50)

# 3. Test Live Gemini Key Connection
if gemini_key:
    print("Testing Google Gemini Cloud Server Connection...")
    try:
        gemini_client = genai.Client(api_key=gemini_key)
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents="Respond with the word 'SUCCESS'",
        )
        response_text = response.text.strip()
        print(f"-> Gemini API Status: 🎉 WORKING! Server says: '{response_text}'")
    except Exception as e:
        print(f"-> Gemini API Status: ❌ FAILED! Error returned:\n   {e}")
else:
    print("Skipping Gemini test due to missing key.")

print("==========================================")