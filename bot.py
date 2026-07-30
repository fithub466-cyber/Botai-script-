import os
import discord
import google.generativeai as genai
from keep_alive import keep_alive # นำเข้าโค้ดปลุกบอท

# ดึงรหัสจากระบบของ Render
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

genai.configure(api_key=GEMINI_API_KEY)
instruction = """คุณคือ AI ผู้เชี่ยวชาญด้านการเขียนสคริปต์ Roblox... (ใส่แบบเดิม)"""
model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instruction)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

chat_sessions = {}

@client.event
async def on_ready():
    print(f'ล็อกอินสำเร็จ! บอท {client.user} พร้อมทำงานแล้ว')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        user_text = message.content.replace(f'<@{client.user.id}>', '').strip()
        if not user_text:
            await message.reply("มีสคริปต์อะไรให้ผมช่วยเขียนไหมครับ?")
            return
        try:
            if message.author.id not in chat_sessions:
                chat_sessions[message.author.id] = model.start_chat(history=[])
            chat = chat_sessions[message.author.id]
            async with message.channel.typing():
                response = chat.send_message(user_text)
                if len(response.text) > 2000:
                    for chunk in [response.text[i:i+2000] for i in range(0, len(response.text), 2000)]:
                        await message.reply(chunk)
                else:
                    await message.reply(response.text)
        except Exception as e:
            await message.reply(f"เกิดข้อผิดพลาด: {str(e)}")

# สั่งให้เว็บจำลองทำงานก่อนรันบอท
keep_alive()
client.run(DISCORD_TOKEN)
