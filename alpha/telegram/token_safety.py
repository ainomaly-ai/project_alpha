import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

# Replace with your own API ID and API hash from my.telegram.org
api_id = os.getenv("TELE_API_ID")  
api_hash = os.getenv("TELE_API_HASH") 
session_path = os.getenv("TELE_SESSION_PATH")  # Path for session file


group_chat_ids = ["BananaGun_bot", "fluxbeam_bot", "solana_trojanbot", "TrenchScannerBot", "Phanes_bot", "SyraxScannerBot"] 

# # Create the Telegram client
# client = TelegramClient(session_name, api_id, api_hash)


async def main():
    """
    Connects to Telegram, send and starts listening for new messages, and keeps the connection alive.
    """
    async with TelegramClient(session_path, api_id, api_hash) as client:
    
        await client.connect()

        for group_id in group_chat_ids:
            await client.send_message(group_id, "8Yb3LKFK5ftyTWRJJ6VsZufoZvHCYAKim8MDRzkspump")
        await client.send_message("th_sol_scanner_bot", "/thp 8Yb3LKFK5ftyTWRJJ6VsZufoZvHCYAKim8MDRzkspump") 
        
        print(f"Message sent to groups")



        print("Listening for new messages...")

        @client.on(events.NewMessage())
        async def my_new_message_handler(event):
            """
            This function is called whenever a new message is received.
            """
            sender = await event.get_sender()
            chat = await event.get_chat()
            message_text = event.message.message

            chat_id = event.chat.id
            
            if chat.id in group_chat_ids:
                print(f"New message from  ({sender.username}) in : {message_text}")

        
        # Keep the client running until manually stopped
        await client.run_until_disconnected()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())