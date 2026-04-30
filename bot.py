import discord
import aiohttp
import os

# 환경변수에서 설정값 가져오기
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
APPS_SCRIPT_URL = os.environ.get('APPS_SCRIPT_URL')  # /exec URL
CHANNEL_ID = int(os.environ.get('DISCORD_CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'봇 실행 중: {client.user}')

@client.event
async def on_message(message):
    # 봇 자신의 메시지 무시
    if message.author == client.user:
        return

    # 지정된 채널에서만 반응
    if message.channel.id != CHANNEL_ID:
        return

    content = message.content.strip()

    # 숫자 입력 감지 (1~7)
    if content.isdigit() and 1 <= int(content) <= 7:
        await message.channel.send(f'✅ **{content}번** 선택! 콘텐츠 생성 중... (1~2분 걸려요 ☕)')

        # Apps Script 웹앱 호출
        url = f'{APPS_SCRIPT_URL}?action=select&number={content}'
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, allow_redirects=True, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    print(f'Apps Script 호출 완료: {resp.status}')
        except Exception as e:
            print(f'Apps Script 호출 오류: {e}')

client.run(DISCORD_BOT_TOKEN)
