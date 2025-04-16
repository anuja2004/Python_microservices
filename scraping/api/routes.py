from fastapi import APIRouter
import requests  # Import requests library

router = APIRouter()

@router.get("/posts")
def get_all_posts():
    # Fetch data from the external API
    api_url = "https://api.apify.com/v2/datasets/ebqwfF7B4cNgONFEx/items?token=apify_api_k3ZwhjGdkpkm0YHiScPBaLWzy2VfsI03zktp"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for HTTP errors
        data = response.json()  # Parse the JSON response
    except requests.RequestException as e:
        return {"error": f"Failed to fetch data from API: {str(e)}"}

    # Extract and normalize the data
    all_posts = []
    try:
        top_posts = data[1]["topPosts"]  # Access the second index and its "topPosts"
        for post in top_posts:
            # Extract required fields
            media = None
            if post.get("type") == "Video":
                media = post.get("videoUrl")
            elif post.get("type") == "Sidecar":
                media = post.get("displayUrl")  # Get the first image if available
            elif post.get("type") == "Image":
                media = post.get("displayUrl")

            normalized_post = {
                "id": post.get("id"),
                "type": post.get("type"),
                "caption": post.get("caption"),
                "media": media,
                "url": post.get("url")  # Include the URL field
            }
            all_posts.append(normalized_post)
    except (IndexError, KeyError) as e:
        return {"error": f"Failed to process data: {str(e)}"}

    return {"posts": all_posts}
