import os
import discord
from discord import app_commands
import google.generativeai as genai

# กำหนดค่า API Key ของ Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# ตั้งค่าบอท Discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ชื่อห้องที่อนุญาตให้ใช้คำสั่ง (เปลี่ยนเป็นชื่อห้องของคุณได้เลย)
ALLOWED_CHANNEL_NAME = "bot-chat"

@client.event
async def on_ready():
    # ซิงค์คำสั่ง Slash Command เข้ากับ Discord
    await tree.sync()
    print(f"Logged in as {client.user} (Slash Commands Synced)")

# สร้างคำสั่ง /ask สำหรับเขียนสคริปต์หรือถามคำถาม
@tree.command(name="ask", description="ถาม AI หรือให้ช่วยเขียนสคริปต์ Roblox")
@app_commands.describe(prompt="ใส่คำสั่งหรือสิ่งที่คุณต้องการให้ AI ช่วย")
async def ask(interaction: discord.Interaction, prompt: str):
    # เช็คว่าใช้ในห้องที่อนุญาตไหม
    if interaction.channel.name != ALLOWED_CHANNEL_NAME:
        await interaction.response.send_message(
            f"❌ คำสั่งนี้ใช้ได้เฉพาะในห้อง #{ALLOWED_CHANNEL_NAME} เท่านั้นครับ!", 
            ephemeral=True
        )
        return

    # แจ้งสถานะกำลังคิด
    await interaction.response.defer(thinking=True)

    try:
        # ให้ Gemini ประมวลผลข้อความ
        response = model.generate_content(prompt)
        reply_text = response.text

        # Discord จำกัดความยาวข้อความต่อ 1 บล็อก ถ้าเกินให้ตัดแบ่งส่ง
        if len(reply_text) > 1900:
            chunks = [reply_text[i:i+1900] for i in range(0, len(reply_text), 1900)]
            await interaction.followup.send(chunks[0])
            for chunk in chunks[1:]:
                await interaction.followup.send(chunk)
        else:
            await interaction.followup.send(reply_text)

    except Exception as e:
        await interaction.followup.send("เกิดข้อผิดพลาดในการประมวลผลครับ ลองใหม่อีกครั้งนะ")

# รันบอท
client.run(os.environ["DISCORD_TOKEN"])
