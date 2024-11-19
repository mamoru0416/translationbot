import discord
import deepl
import os
from langdetect import detect
from dotenv import load_dotenv

#.envファイルの読み込み
load_dotenv()

# DeepL APIキー
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')

# Discord Botのトークン
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# 翻訳元チャンネルIDと翻訳結果投稿先チャンネルID
SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID'))
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))

# DeepL翻訳クライアントの初期化
translator = deepl.Translator(DEEPL_API_KEY)

# Discordクライアントの設定
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author == client.user:
        return

    # 指定されたチャンネルからのメッセージのみ処理
    if message.channel.id == SOURCE_CHANNEL_ID:
        text = message.content

        # 言語検出
        try:
            detected_lang = detect(text)
        except Exception as e:
            print(f'言語検出エラー: {e}')
            return

        # 翻訳処理
        if detected_lang == 'ko':
            # 韓国語から日本語へ翻訳
            try:
                result = translator.translate_text(text, source_lang='KO', target_lang='JA')
                translated_text = result.text
                notice = "KR to JP:"
            except Exception as e:
                print(f'翻訳エラー: {e}')
                return
        elif detected_lang == 'ja':
            # 日本語から韓国語へ翻訳
            try:
                result = translator.translate_text(text, source_lang='JA', target_lang='KO')
                translated_text = result.text
                notice = "JP to KR:"
            except Exception as e:
                print(f'翻訳エラー: {e}')
                return
        else:
            # 韓国語でも日本語でもない場合
            translated_text = "対応していない言語です。"
            notice = ""

        # 翻訳結果を指定されたチャンネルに送信
        target_channel = client.get_channel(TARGET_CHANNEL_ID)
        if target_channel:
            await target_channel.send(f"{notice}\n{translated_text}")

# Botの実行
client.run(DISCORD_BOT_TOKEN)