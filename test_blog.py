# test_blog.py

from agents.blog_agent import ingest_multiple_blogs_to_vectorstore, search_blog, is_url_valid

blog_urls = [
    "https://lifewithbugo.com/travel-guide-to-dubai/",
    "https://wanderon.in/blogs/things-to-do-in-dubai",
    "https://myvintagemap.com/7-day-dubai-itinerary/",
    "https://trip101.com/article/adventure-sports-in-dubai",
    "https://www.bruisedpassports.com/wheres/offbeat-dubai",
]

valid_urls = [url for url in blog_urls if is_url_valid(url)]
print(f"🧪 Valid URLs: {len(valid_urls)}")

if valid_urls:
    ingest_multiple_blogs_to_vectorstore(valid_urls)
    search_blog("What are the best things to do in Dubai?")
else:
    print("❌ No valid URLs found.")

