import os, sys, time, shutil, datetime
from getpass import getpass
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
from telethon.tl.types import InputPeerChannel

# ==== Dizayn moduli ====
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def vibrate(duration_ms=300):
    os.system(f'termux-vibrate -d {duration_ms}')

def moving_matrix_line(repeat=80, delay=0.015):
    charset = '01'
    width = shutil.get_terminal_size().columns
    matrix = ''.join(charset[i % 2] for i in range(width * 2))
    for i in range(repeat):
        line = matrix[i:i + width]
        sys.stdout.write("\r\033[32m" + line + "\033[0m")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def framed_banner():
    width = min(80, shutil.get_terminal_size().columns - 4)
    lines = [
        "🛠 Developed by @originalprofil",
        "📢 Telegram kanalimiz: @originalprofil",
        "✉ Savol va takliflar uchun shu akkauntga yozing"
    ]
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print("\033[92m╔" + "═" * width + "╗")
    print("║" + " " * width + "║")
    for i, line in enumerate(lines):
        centered = line.center(width)
        print(f"\033[9{1 + i % 6}m║{centered}║\033[0m")
    print("║" + " " * width + "║")
    print("╚" + "═" * width + "╝\033[0m")
    print(f"\033[90m{now.rjust(width + 2)}\033[0m\n")

def type_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def full_intro():
    clear_screen()
    moving_matrix_line()
    vibrate()
    framed_banner()
    moving_matrix_line()
    type_text("🚀 Dastur ishga tushirilmoqda...")

# ==== Telegram qismini boshlaymiz ====

api_id = int(input("API ID ni kiriting: "))
api_hash = input("API Hash ni kiriting: ")
phone = input("Telefon raqamingizni kiriting (+998...): ")
password = getpass("2-bosqichli parol (agar mavjud bo‘lsa): ")

group_count = int(input("Nechta guruh ochilsin (0–100): "))
assert 0 <= group_count <= 100, "Faqat 0 dan 100 gacha son kiriting!"

# Botlar (doimiy)
BOT_USERNAMES = ["Join_Dalet_Bot", "SuperDefenderBot"]

client = TelegramClient(f"session_{phone.replace('+','')}", api_id, api_hash)

async def create_groups():
    await client.start(phone=phone, password=lambda: password)
    full_intro()

    for i in range(group_count):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = f"AutoGroup {now}"
        about = "@originalprofil"

        result = await client(CreateChannelRequest(
            title=title,
            about=about,
            megagroup=True
        ))

        channel = result.chats[0]
        peer = InputPeerChannel(channel.id, channel.access_hash)

        # Botlarni admin qilish
        for bot in BOT_USERNAMES:
            try:
                entity = await client.get_entity(bot)
                await client(InviteToChannelRequest(
                    channel=peer,
                    users=[entity]
                ))
                print(f"✅ @{bot} guruhga qo‘shildi")
            except Exception as e:
                print(f"⚠️ @{bot} ni qo‘shishda xatolik: {e}")

        print(f"✅ Guruh #{i+1} yaratildi: {title}\n")
        time.sleep(3)

    print("🎉 Barcha guruhlar yaratildi!")

with client:
    client.loop.run_until_complete(create_groups())
  
