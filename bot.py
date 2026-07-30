@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # เช็คว่าพิมพ์อยู่ในห้องชื่อ "bot-chat" หรือไม่ (เปลี่ยนชื่อห้องตามต้องการได้เลย)
    if message.channel.name != 'bot-chat':
        return  # ถ้าไม่ใช่ห้องนี้ บอทจะไม่สนใจและไม่ตอบกลับ

    # โค้ดเดิมสำหรับคุยกับ Gemini
    if client.user.mentioned_in(message):
        user_message = message.content.replace(f'<@{client.user.id}>', '').strip()
        response = model.generate_content(user_message)
        await message.channel.send(response.text)
