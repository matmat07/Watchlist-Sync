import requests
import json
import logging
import asyncio
import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Placeholder API URLs and keys (replace with actual ones)
PLEX_API_URL = "https://plex.tv/api/"
PLEX_API_KEY = "your_plex_api_key"
LETTERBOXD_API_URL = "https://api.letterboxd.com/v0/"
LETTERBOXD_API_KEY = "your_letterboxd_api_key"

# Fetch Plex watchlist
async def fetch_plex_watchlist(session):
    url = f"{PLEX_API_URL}watchlist"
    headers = {
        "X-Plex-Token": PLEX_API_KEY
    }
    async with session.get(url, headers=headers) as response:
        response.raise_for_status()
        return await response.json()

# Fetch Letterboxd watchlist
async def fetch_letterboxd_watchlist(session):
    url = f"{LETTERBOXD_API_URL}watchlist"
    headers = {
        "Authorization": f"Bearer {LETTERBOXD_API_KEY}"
    }
    async with session.get(url, headers=headers) as response:
        response.raise_for_status()
        return await response.json()

# Compare watchlists
def compare_watchlists(plex_watchlist, letterboxd_watchlist):
    plex_set = set(plex_watchlist)
    letterboxd_set = set(letterboxd_watchlist)
    
    to_add_to_plex = list(letterboxd_set - plex_set)
    to_add_to_letterboxd = list(plex_set - letterboxd_set)
    
    return to_add_to_plex, to_add_to_letterboxd

# Update Plex watchlist
async def update_plex_watchlist(session, to_add):
    url = f"{PLEX_API_URL}watchlist"
    headers = {
        "X-Plex-Token": PLEX_API_KEY
    }
    for item in to_add:
        payload = {"item": item}
        async with session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            logger.info(f"Added {item} to Plex watchlist")

# Update Letterboxd watchlist
async def update_letterboxd_watchlist(session, to_add):
    url = f"{LETTERBOXD_API_URL}watchlist"
    headers = {
        "Authorization": f"Bearer {LETTERBOXD_API_KEY}"
    }
    for item in to_add:
        payload = {"item": item}
        async with session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            logger.info(f"Added {item} to Letterboxd watchlist")

# Main function
async def sync_watchlists():
    async with aiohttp.ClientSession() as session:
        plex_watchlist = await fetch_plex_watchlist(session)
        letterboxd_watchlist = await fetch_letterboxd_watchlist(session)
        
        to_add_to_plex, to_add_to_letterboxd = compare_watchlists(plex_watchlist, letterboxd_watchlist)
        
        await update_plex_watchlist(session, to_add_to_plex)
        await update_letterboxd_watchlist(session, to_add_to_letterboxd)
        logger.info("Watchlists have been synchronized")

# Run the main function
if __name__ == "__main__":
    asyncio.run(sync_watchlists())
