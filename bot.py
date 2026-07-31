import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def chat_with_bot():
    print("Bot is ready. Type exit or quit to stop.")
    
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="คุณคือผู้ช่วยส่วนตัวอัจฉริยะ คอยให้คำปรึกษา ช่วยเหลือ และพูดคุยกับผู้ใช้ด้วยความเป็นกันเอง เป็นประโยชน์ และตรงประเด็น",
            temperature=0.7,
        )
    )
    
    while True:
        try:
            user_input = input("\nคุณ: ")
        except EOFError:
            break
            
        if user_input.lower() in ["exit", "quit", "ออก"]:
            print("บอท: ไว้คุยกันใหม่นะครับ สวัสดีครับ!")
            break
            
        if not user_input.strip():
            continue
            
        try:
            response = chat.send_message(user_input)
            print(f"\nบอท: {response.text}")
        except Exception as e:
            print(f"\nเกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    if not os.environ.get("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY is missing.")
    else:
        chat_with_bot()
