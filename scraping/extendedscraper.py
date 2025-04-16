import asyncio
import json
from playwright.async_api import async_playwright
from serpapi import GoogleSearch
import os

# Synchronous Google data fetcher using SerpApi
def fetch_google_data(query="Water Conservation Techniques", num_results=5):
    params = {
        "engine": "google",
        "q": query,
        "num": num_results,
        "api_key": os.getenv("SERPAPI_KEY")
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    
    data = []
    for result in organic_results:
        data.append({
            "title": result.get("title", "N/A"),
            "link": result.get("link", "N/A"),
            "snippet": result.get("snippet", "N/A")
        })
    return data

# Dummy async YouTube scraper for context (you already have your own logic)
async def fetch_youtube_data(page, query="Water Conservation"):
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    print(f"🎬 Visiting YouTube: {search_url}")
    await page.goto(search_url, wait_until="networkidle")
    await page.wait_for_selector("ytd-video-renderer", timeout=15000)
    
    video_elements = await page.query_selector_all("ytd-video-renderer")
    print(f"🎥 Found {len(video_elements)} YouTube video results")
    videos = []
    for video in video_elements:
        try:
            title_el = await video.query_selector("#video-title")
            title = await title_el.get_attribute("title")
            video_url = await title_el.get_attribute("href")
            if video_url and not video_url.startswith("https://"):
                video_url = "https://www.youtube.com" + video_url
            thumbnail_el = await video.query_selector("img")
            thumbnail_url = await thumbnail_el.get_attribute("src")
            videos.append({
                "title": title,
                "video_url": video_url,
                "thumbnail_url": thumbnail_url
            })
        except Exception as e:
            print(f"❌ Error parsing a YouTube video: {e}")
            continue
    return videos

async def main_extended():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        youtube_data = await fetch_youtube_data(page)
        google_data = fetch_google_data()  # Synchronous call

        # Combine results into a dictionary
        combined_data = {
            "youtube": youtube_data,
            "google": google_data,
        }

        # Save combined data to a JSON file
        with open("extended_data.json", "w", encoding="utf-8") as f:
            json.dump(combined_data, f, indent=2, ensure_ascii=False)

        print("✅ Saved extended data to extended_data.json")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main_extended())


