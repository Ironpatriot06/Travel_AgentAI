from agents.blog_agent import ingest_multiple_blogs_to_vectorstore

blog_urls = [
    "https://lifewithbugo.com/travel-guide-to-dubai/",
    "https://veerasundar.com/blog/traveling-to-dubai-from-india-as-tourist",
    "https://myprettytravels.com/asia/uae/dubai-best-things/",
    "https://www.akbartravels.com/in/blogs/planning-your-dubai-travel-itinerary-a-holistic-guide/",
    "https://wanderon.in/blogs/things-to-do-in-dubai",
    "https://traveltriangle.com/blog/free-things-to-do-in-dubai/",
    "https://myvintagemap.com/7-day-dubai-itinerary/",
    "https://www.bruisedpassports.com/wheres/offbeat-dubai",
    "https://travel-lush.com/dubai-bucket-list-activities/",
    "https://www.dubaitravelblog.com/best-tourist-attractions-in-dubai/",
    "https://www.dubaitravelplanner.com/places-to-visit-in-dubai/",
    "https://www.airalo.com/blog/must-see-tourist-places-in-dubai",
    "https://www.discoverwalks.com/blog/dubai/20-must-visit-places-in-dubai/",
    "https://traveltriangle.com/blog/adventure-sports-in-dubai/",
    "https://tusktravel.com/blog/popular-adventure-sports-in-dubai/",
    "https://www.dubaitravelplanner.com/adventure-activities-in-dubai/",
    "https://trip101.com/article/adventure-sports-in-dubai",
    "https://www.bucketlistly.blog/posts/things-to-do-in-dubai",
    "https://galaxiagroup.com/blog/adventures-in-dubai-from-desert-safaris-to-skydiving/",
    "https://www.uber.com/en-AE/blog/dubai-nightlife-spots/"
]
valid_urls = [url for url in blog_urls if is_url_valid(url)]


if __name__ == "__main__":
	ingest_multiple_blogs_to_vectorstore(valid_urls)

