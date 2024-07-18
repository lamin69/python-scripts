import asyncio
import httpx
import re
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_content(url, progress_callback):
    progress_callback(0, f"Fetching content from {url}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            progress_callback(10, f"Content fetched from {url}")
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            progress_callback(10, f"Error fetching {url}: {str(e)}")
            return ""

async def verify_stream(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.head(url, timeout=5.0)
            return response.status_code == 200
        except:
            return False

def extract_channel_name(info):
    patterns = [
        r'tvg-name="([^"]*)"',
        r'group-title="([^"]*)"',
        r',(.+)$'
    ]
    for pattern in patterns:
        match = re.search(pattern, info)
        if match and match.group(1):
            return match.group(1).strip()
    return "Unknown Channel"

async def process_m3u(content, progress_callback):
    progress_callback(20, "Processing as M3U file")
    matches = re.findall(r'(#EXTINF:-1[^\n]*)\n(https?://[^\s]+)', content)
    all_streams = {url: (extract_channel_name(info), info) for info, url in matches}
    progress_callback(30, f"Found {len(all_streams)} potential streams in M3U format")
    return all_streams

async def process_html(content, progress_callback):
    progress_callback(20, "Processing as HTML")
    soup = BeautifulSoup(content, 'html.parser')
    all_streams = {}
    for a in soup.find_all('a', href=True):
        if a['href'].endswith(('.m3u8', '.m3u')):
            all_streams[a['href']] = (a.text.strip() or "Unknown Channel", f"#EXTINF:-1,{a.text.strip()}")
    progress_callback(30, f"Found {len(all_streams)} potential streams in HTML format")
    return all_streams

async def process_raw_links(content, progress_callback):
    progress_callback(20, "Processing as raw text for links")
    matches = re.findall(r'(https?://[^\s]+\.(?:m3u8|m3u))', content)
    all_streams = {url: ("Unknown Channel", f"#EXTINF:-1,Unknown Channel") for url in matches}
    progress_callback(30, f"Found {len(all_streams)} potential streams as raw links")
    return all_streams

async def process_playlist(url, progress_callback):
    content = await fetch_content(url, progress_callback)
    if not content:
        return []

    processing_methods = [
        process_m3u,
        process_html,
        process_raw_links
    ]

    all_streams = {}
    for method in processing_methods:
        all_streams = await method(content, progress_callback)
        if all_streams:
            break

    verified_streams = []
    total = len(all_streams)
    
    progress_callback(40, f"Verifying {total} potential streams")
    for i, (url, (name, info)) in enumerate(all_streams.items()):
        if await verify_stream(url):
            verified_streams.append((name, url, info))
        progress = 40 + int((i + 1) / total * 50)
        progress_callback(progress, f"Verified {i + 1}/{total} streams")
    
    progress_callback(90, f"Found {len(verified_streams)} valid streams from {url}")
    return verified_streams

async def run_channel_scrapper_script_async(website_urls, progress_callback):
    all_verified_streams = []
    total_urls = len(website_urls)
    
    for i, url in enumerate(website_urls):
        progress_callback(0, f"Processing website {i + 1}/{total_urls}: {url}")
        verified_streams = await process_playlist(url, progress_callback)
        all_verified_streams.extend(verified_streams)
        overall_progress = int((i + 1) / total_urls * 100)
        progress_callback(overall_progress, f"Processed {i + 1}/{total_urls} websites")
    
    m3u_content = "#EXTM3U\n"
    for name, url, info in all_verified_streams:
        m3u_content += f"{info}\n{url}\n"
    
    return {'progress': 100, 'message': f'Channels successfully scraped with {len(all_verified_streams)} verified streams', 'content': m3u_content}

def run_channel_scrapper_script(website_urls, progress_callback):
    return asyncio.run(run_channel_scrapper_script_async(website_urls, progress_callback))
