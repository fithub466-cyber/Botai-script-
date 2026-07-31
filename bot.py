import os
from google import genai
from google.genai import types

# ตั้งค่า Client โดยใช้ API Key จาก Environment Variable
# (แนะนำให้ตั้งค่าตัวแปร GEMINI_API_KEY ในเครื่องของคุณก่อนรัน)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def chat_with_bot():
    print("🤖 บอทส่วนตัวพร้อมทำงานแล้วครับ (พิมพ์ 'exit' หรือ 'quit' เพื่อออก)")
    
    # สร้างบทสนทนาแบบต่อเนื่อง (Chat Session) เพื่อให้บอทจำข้อความก่อนหน้าได้เหมือนคุยกันจริงๆ
    chat = client.chats.create(
        model="gemini-3.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="คุณคือผู้ช่วยส่วนตัวอัจฉริยะ คอยให้คำปรึกษา ช่วยเหลือ และพูดคุยกับผู้ใช้ด้วยความเป็นกันเอง เป็นประโยชน์ และตรงประเด็น",
            temperature=0.7,
        )
    )
    
    while True:
        user_input = input("\nคุณ: ")
        if user_input.lower() in ["exit", "quit", "ออก"]:
            print("🤖 บอท: ไว้คุยกันใหม่นะครับ สวัสดีครับ!")
            break
            
        if not user_input.strip():
            continue
            
        try:
            # ส่งข้อความหาบอทและรอรับคำตอบ
            response = chat.send_message(user_input)
            print(f"\n🤖 บอท: {response.text}")
        except Exception as e:
            print(f"\n❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    # ตรวจสอบว่าใส่ API Key หรือยัง
    if not os.environ.get("GEMINI_API_KEY"):
        print("⚠️ คำเตือน: ยังไม่ได้ตั้งค่าตัวแปรสิ่งแวดล้อม GEMINI_API_KEY")
        print("💡 วิธีตั้งค่า (บน Command Line/Terminal):")
        print("   - Windows (CMD): set GEMINI_API_KEY=คีย์ของคุณ")
        print("   - Mac/Linux: export GEMINI_API_KEY='คีย์ของคุณ'")
    else:
        chat_with_bot()
