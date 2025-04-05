import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY") or "2fab7d696ae74f1194aeead67a029740"

def fetch_road_alerts(city_or_list):
    if isinstance(city_or_list, str):
        cities = [city_or_list]
    else:
        cities = city_or_list

    alerts = []

    # Keywords to include/exclude
    include_keywords = ["accident", "jam", "congestion", "crash", "roadblock", "closure", "traffic", "delay"]
    exclude_keywords = ["airport", "flight", "airline", "runway", "terminal", "salary", "pay", "hike"]

    for city in cities:
        # Smart query for better matching
        query = f"{city} AND (traffic OR accident OR jam OR congestion OR crash OR roadblock OR closure OR delay)"
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={requests.utils.quote(query)}&"
            f"apiKey={NEWS_API_KEY}&pageSize=10&language=en&sortBy=publishedAt"
        )

        try:
            response = requests.get(url)
            print(f"📡 NewsAPI response for {city}: {response.status_code}")
            data = response.json()

            if data.get("status") == "ok":
                for article in data["articles"]:
                    title = (article.get("title") or "").lower()
                    description = (article.get("description") or "").lower()

                    if (
                        any(kw in title or kw in description for kw in include_keywords) and
                        not any(bad_kw in title or bad_kw in description for bad_kw in exclude_keywords)
                    ):
                        alert = {
                            "title": article["title"],
                            "url": article["url"],
                            "publishedAt": article["publishedAt"],
                            "source": article["source"]["name"]
                        }
                        alerts.append((city, alert))
        except Exception as e:
            print(f"❌ Error fetching news for {city}: {e}")

    # Group and sort alerts by city and recency
    grouped_alerts = {}
    for city, alert in sorted(alerts, key=lambda x: x[1]["publishedAt"], reverse=True):
        grouped_alerts.setdefault(city, []).append(alert)

    return grouped_alerts
