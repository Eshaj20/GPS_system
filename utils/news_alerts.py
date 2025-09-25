import requests
import os

# NewsAPI key (set as env var or fallback hardcoded key)
NEWS_API_KEY = os.getenv("NEWS_API_KEY") 

def fetch_road_alerts(cities):
    """
    Fetch traffic/road alerts for intermediate cities only.
    cities: list of city names (make sure source and destination are excluded before passing)
    """
    if isinstance(cities, str):
        cities = [cities]

    alerts = []

    include_keywords = ["accident", "jam", "congestion", "crash", "roadblock", "closure", "traffic", "delay"]
    exclude_keywords = ["airport", "flight", "airline", "runway", "terminal", "salary", "pay", "hike"]

    for city in cities:
        query = f"{city} AND (traffic OR accident OR jam OR congestion OR crash OR roadblock OR closure OR delay)"
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={requests.utils.quote(query)}&"
            f"apiKey={NEWS_API_KEY}&pageSize=10&language=en&sortBy=publishedAt"
        )

        try:
            response = requests.get(url, timeout=10)
            print(f"📡 NewsAPI response for {city}: {response.status_code}")
            data = response.json()

            if data.get("status") == "ok":
                for article in data["articles"]:
                    title = (article.get("title") or "").lower()
                    description = (article.get("description") or "").lower()

                    if (
                        any(kw in title or kw in description for kw in include_keywords)
                        and not any(bad_kw in title or bad_kw in description for bad_kw in exclude_keywords)
                    ):
                        alerts.append(
                            (
                                city,
                                {
                                    "title": article.get("title"),
                                    "url": article.get("url"),
                                    "publishedAt": article.get("publishedAt"),
                                    "source": article["source"].get("name"),
                                },
                            )
                        )
        except Exception as e:
            print(f"❌ Error fetching news for {city}: {e}")

    # Group & sort alerts by recency
    grouped_alerts = {}
    for city, alert in sorted(alerts, key=lambda x: x[1]["publishedAt"], reverse=True):
        grouped_alerts.setdefault(city, []).append(alert)

    return grouped_alerts

