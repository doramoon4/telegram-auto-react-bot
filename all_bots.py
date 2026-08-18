import asyncio
import http.server
import random
import socketserver
import threading
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

api_id = 31216176
api_hash = "afb77871e67a499d6fa9660dbb830269"

CHANNEL_IDS = [
    -1003972207620,
    -1003919304525,
    -1004220190063,
    -1003988666924,
    -1003987223858,
    -1003713815674,
    -1003640692235,
    -1003975845100,
    -1003749731711,
]

# Random ပေးမည့် Emoji ၁၁ ခု
REACTION_EMOJIS = [
    "❤️",
    "👍",
    "🎉",
    "🔥",
    "🥰",
    "💯",
    "🏆",
    "💋",
    "😇",
    "🤝",
    "😘",
]

# သင့်မှာရှိတဲ့ Bot Token တွေ
BOT_TOKENS = [
    "8533233484:AAEUs_NARjPJ1O4akKH2tHMmmpWqiIid-Lc",
    "8883643062:AAHecUg1GY264VnQuHIBX2ln30St2kJ46PU",
    "8966013905:AAFEg1SuzVJN_S1PzPM72yccAkrwz3ktURQ",
    "8762822746:AAHOoE29uuB7kQLbmox0l2xeiZ0zuCgUDRg",
    "8563429096:AAE8o62UxQyLwwEmS2OyDJj-0oFXEnt2gqQ",
    "8635956850:AAHOz_4czg9DCvJiKezyhbyATW301ThDnTQ",
    "8799893710:AAEZGu6hngkjPMDMLWZdv5ZAjrSrYC7758U",
]


# ==========================================
# Render အတွက် Port 10000 ဖွင့်ပေးမယ့် Mini Web Server
# ==========================================
PORT = 10000


class Handler(http.server.SimpleHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Bot is active and running!")


def run_server():
  with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"HTTP Server running on port {PORT}")
    httpd.serve_forever()


# ==========================================
# Telegram Bot Logic
# ==========================================
async def run_single_bot(token, index):
  client = TelegramClient(f"bot_session_{index}", api_id, api_hash)

  @client.on(events.NewMessage(chats=CHANNEL_IDS))
  async def handler(event):
    try:
      await asyncio.sleep(index * 0.1)
      selected_emoji = random.choice(REACTION_EMOJIS)
      await client(
          SendReactionRequest(
              peer=event.chat_id,
              msg_id=event.id,
              reaction=[ReactionEmoji(emoticon=selected_emoji)],
          )
      )
      print(f"Bot {index} ({selected_emoji}) Reaction ပေးလိုက်ပါပြီ။")
    except Exception as e:
      print(f"Bot {index} Error: {e}")

  await client.start(bot_token=token)
  print(f"Bot {index} အလုပ်လုပ်နေပါပြီ...")
  await client.run_until_disconnected()


async def main():
  # HTTP Server ကို Background မှာ စတင် Run ပေးခြင်း
  server_thread = threading.Thread(target=run_server, daemon=True)
  server_thread.start()

  # Bot အားလုံးကို တစ်ပြိုင်နက် အလုပ်လုပ်စေရန်
  tasks = [
      run_single_bot(token, i + 1) for i, token in enumerate(BOT_TOKENS)
  ]
  await asyncio.gather(*tasks)


if __name__ == "__main__":
  asyncio.run(main())
