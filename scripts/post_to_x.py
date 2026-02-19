#!/usr/bin/env python3
"""
ALKINDUS Media Agent - X (Twitter) Poster
Posts health/pharma content automatically
"""

import os
import json
import random
import tweepy
from datetime import datetime

# X API Credentials
X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET = os.getenv('X_API_SECRET')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_SECRET = os.getenv('X_ACCESS_SECRET')

def get_client():
    """Initialize X API client"""
    return tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET
    )

# Health/Pharma content templates
CONTENT_TEMPLATES = [
    "💊 {topic}: {fact}\n\nYour health matters. Follow for more insights.",
    "🧬 Did you know? {fact}\n\n#{topic} #HealthTips",
    "⚕️ {topic} Update:\n{fact}\n\nStay informed, stay healthy.",
    "🔬 Research Spotlight:\n{fact}\n\n#{topic}",
    "💡 Health Tip: {fact}\n\n#{topic} #Wellness",
]

HEALTH_TOPICS = [
    {
        "topic": "Pharma Innovation",
        "facts": [
            "AI is accelerating drug discovery by 40% in 2025.",
            "Personalized medicine is becoming the new standard.",
            "mRNA technology is expanding beyond vaccines.",
        ]
    },
    {
        "topic": "Mental Health",
        "facts": [
            "Digital therapeutics are FDA-approved for anxiety treatment.",
            "Telehealth has increased mental health access by 300%.",
            "Mindfulness apps show measurable brain changes.",
        ]
    },
    {
        "topic": "Preventive Care",
        "facts": [
            "Early detection reduces treatment costs by 60%.",
            "Wearables now detect irregular heart rhythms accurately.",
            "Genetic screening is now accessible to everyone.",
        ]
    },
]

def generate_post():
    """Generate a health/pharma post"""
    topic_data = random.choice(HEALTH_TOPICS)
    fact = random.choice(topic_data["facts"])
    template = random.choice(CONTENT_TEMPLATES)
    
    content = template.format(
        topic=topic_data["topic"].replace(" ", ""),
        fact=fact
    )
    
    return content

def main():
    print(f"🚀 ALKINDUS Media Agent - {datetime.now()}")
    
    # Check credentials
    if not all([X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET]):
        print("❌ Missing X API credentials")
        return 1
    
    # Generate content
    post_content = generate_post()
    print(f"📝 Generated post:\n{post_content}\n")
    
    # Post to X
    try:
        client = get_client()
        response = client.create_tweet(text=post_content)
        print(f"✅ Posted successfully! Tweet ID: {response.data['id']}")
        return 0
    except Exception as e:
        print(f"❌ Error posting: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
