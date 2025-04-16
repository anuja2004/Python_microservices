import asyncio
import json
import csv
from playwright.async_api import async_playwright

# ------------------------
# 🧱 Website 1: Jal Shakti
# ------------------------

async def fetch_schemes(page, page_num):
    url = f"https://www.jalshakti-dowr.gov.in/offerings?page={page_num}"
    print(f"🌐 Visiting: {url}")
    await page.goto(url, wait_until='networkidle')
    await page.wait_for_selector("div.col-md-6 > div.scheme-card", timeout=10000)

    schemes = []
    cards = await page.query_selector_all("div.col-md-6 > div.scheme-card")
    print(f"📦 Found {len(cards)} schemes")

    for card in cards:
        title_el = await card.query_selector(".scheme-title.h3")
        desc_el = await card.query_selector(".scheme-intro.h4")
        img_el = await card.query_selector("img")

        title = await title_el.inner_text() if title_el else "N/A"
        desc = await desc_el.inner_text() if desc_el else "N/A"
        img_url = await img_el.get_attribute("src") if img_el else "N/A"

        schemes.append({
            "scheme_name": title.strip(),
            "description": desc.strip(),
            "image_url": img_url
        })

    return schemes


# -------------------------
# 🌿 Website 2: NWM - Best Practices
# -------------------------
async def fetch_best_practices(context):
    best_practices = []
    base_url = "https://nwm.gov.in"

    for page_num in range(33, 45):  # Pages 33 to 44 inclusive
        url = f"{base_url}/bestpractice/{page_num}"
        print(f"📁 Visiting best practice list page: {url}")
        
        try:
            page = await context.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        except Exception as e:
            print(f"❌ Could not open page {url}: {e}")
            continue

        try:
            await page.wait_for_selector("table.views-table", timeout=10000)
        except Exception:
            print(f"⚠️ Table not found on {url}")
            await page.close()
            continue

        rows = await page.locator("table.views-table tbody tr").all()
        print(f"🔍 Found {len(rows)} practices on page {page_num}")

        for i, row in enumerate(rows):
            detail_page = None
            try:
                # Get the "View Details" link; use the second link in the row
                link_locator = row.locator("a")
                if await link_locator.count() < 2:
                    print(f"⚠️ Row {i} on page {page_num} has less than 2 links, skipping")
                    continue

                detail_href = await link_locator.nth(1).get_attribute("href")
                if not detail_href:
                    print(f"⚠️ No href found in row {i} on page {page_num}, skipping")
                    continue

                full_detail_url = f"{base_url}{detail_href}"

                # Open detail page in a new tab
                detail_page = await context.new_page()
                await detail_page.goto(full_detail_url, wait_until="domcontentloaded", timeout=30000)

                # Wait for the detail content container to be visible
                await detail_page.wait_for_selector("article.node-best-practice", timeout=30000)

                # Extract the title specifically using the page title element
                detail_title = await detail_page.locator("h1#page-title").text_content()
                detail_title = detail_title.strip() if detail_title else "Untitled"

                # Extract full content from the article element
                detail_content = await detail_page.locator("article.node-best-practice").inner_text()
                detail_content = detail_content.strip() if detail_content else "No content available"

                # Extract image URLs from within the article
                img_elements = await detail_page.locator("article.node-best-practice img").all()
                image_urls = []
                for img in img_elements:
                    src = await img.get_attribute("src")
                    if src and src.startswith("https://"):
                        image_urls.append(src)

                best_practices.append({
                    "page": page_num,
                    "title": detail_title,
                    "url": full_detail_url,
                    "content": detail_content,
                    "image_urls": image_urls
                })

            except Exception as e:
                print(f"❌ Error parsing a row on page {url}: {e}")
                if detail_page:
                    await detail_page.screenshot(path=f"error_page_{page_num}_{i}.png")
                continue
            finally:
                if detail_page:
                    await detail_page.close()

        await page.close()

    # Save results to JSON
    with open("best_practices.json", "w", encoding="utf-8") as f:
        json.dump(best_practices, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(best_practices)} best practices to best_practices.json")

    return best_practices







# -------------------------
# 🚀 Main Orchestrator
# -------------------------

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # 📦 Scrape Website 1
        all_schemes = []
        for page_num in range(1, 2):  # Adjust page range as needed
            schemes = await fetch_schemes(page, page_num)
            all_schemes.extend(schemes)

        with open("schemes.json", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["scheme_name", "description", "image_url"])
            writer.writeheader()
            writer.writerows(all_schemes)

        print(f"\n✅ Saved {len(all_schemes)} schemes to schemes.json")

        # 🌿 Scrape Website 2
        best_practices = await fetch_best_practices(context)

        # Save to JSON
        with open("best_practices.json", "w", encoding="utf-8") as f:
            json.dump(best_practices, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {len(best_practices)} best practices to best_practices.json")

        await browser.close()


if __name__ == "__main__":
<<<<<<< HEAD
    asyncio.run(main())
=======
    asyncio.run(main())
>>>>>>> main
