from dexscreener import DexscreenerClient
import asyncio


def format_token_info(token_info):
    output = []
    output.append(f"Token Address: {token_info.token_address}")
    output.append(f"Chain ID: {token_info.chain_id}")
    output.append(f"URL: {token_info.url}")
    output.append(f"Description: {token_info.description}")
    output.append(f"Amount: {token_info.amount}")
    output.append(f"Total Amount: {token_info.total_amount}")
    output.append(f"Icon: {token_info.icon}")
    
    if token_info.links:
        output.append("Links:")
        for link in token_info.links:
            link_label = link.label if link.label else "Link"
            output.append(f"  - {link_label}: {link.url}")
    
    output.append("\n")  # Add a newline for better separation
    return "\n".join(output)

tokens = []

async def main():
    client = DexscreenerClient()

    token_profiles = client.get_latest_token_profiles()



   
    for token in token_profiles:
        tokens.append(format_token_info(token))
        if token.chain_id == "solana":
            print(token.chain_id,token.description, token.token_address)
    
            
asyncio.get_event_loop().run_until_complete(main())
