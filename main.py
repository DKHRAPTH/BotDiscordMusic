import discord
import os
from discord.ext import commands
from discord import app_commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='=', intents=intents)
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} is online!')

@bot.tree.command(name="play_yt", description="Play music from Youtube")
@app_commands.describe(yt_url="ใส่ url เพลงที่ต้องการจะฟัง")
async def play_yt(interaction:discord.Interaction, yt_url: str):
    if not interaction.user.voice:
        await interaction.response.send_message("🤖 เข้าห้องเสียงก่อน! ❌", ephemeral=True)
        return
    else:
        await interaction.user.voice.channel.connect(timeout=60)
        await interaction.response.send_message(f'🤖 กำลังโหลดเพลง ⚪', ephemeral=True)
        audio,title = extrct_url(yt_url)
        vc = interaction.guild.voice_client
        vc.play(FFmpegPCMAudio(audio, options='-vn -b:a 128k -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'))
        await interaction.followup.send(f"🤖 กำลังเล่นเพลง {title}")
@bot.tree.command(name="leave", description="Bot leave channel")
async def leave(interaction:discord.Integration):
    await interaction.guild.voice_client.disconnect()
def extrct_url(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'socket_timeout': 10,
        'retries': 3,
        'quiet': True,
        'extract_flat': False,
        'compat_opts': ['no-simulcast'],
        }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url=url, download=False)#แปลงเสียง
        audio = info['url']
    return audio, info.get('title')
bot.run(TOKEN)
