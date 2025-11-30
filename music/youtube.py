import yt_dlp

def yt_search(query: str):
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        try:
            result = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
            return result["webpage_url"], result["title"]
        except:
            return None, None
