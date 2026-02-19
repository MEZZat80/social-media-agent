#!/usr/bin/env python3
"""
ALKINDUS Media Agent - Content Reader
Reads articles from X, LinkedIn, Instagram and organizes to Obsidian
"""

import os
import json
import re
from datetime import datetime
from urllib.parse import urlparse

# X API Credentials
X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')

class ContentReader:
    def __init__(self):
        self.obsidian_path = "/root/.openclaw/workspace/obsidian"
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create Obsidian structure if not exists"""
        dirs = [
            f"{self.obsidian_path}/01-Inbox",
            f"{self.obsidian_path}/02-Articles/X",
            f"{self.obsidian_path}/02-Articles/LinkedIn", 
            f"{self.obsidian_path}/02-Articles/Instagram",
            f"{self.obsidian_path}/03-Insights",
            f"{self.obsidian_path}/04-Outputs"
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
    
    def extract_x_article(self, url):
        """Extract X/Twitter article content"""
        # TODO: Implement X API v2 read
        return {
            "platform": "X",
            "url": url,
            "author": "",
            "content": "",
            "date": datetime.now().isoformat(),
            "tags": []
        }
    
    def process_shared_link(self, url):
        """Process shared social media link"""
        domain = urlparse(url).netloc.lower()
        
        if "twitter.com" in domain or "x.com" in domain:
            return self.extract_x_article(url)
        elif "linkedin.com" in domain:
            return {"platform": "LinkedIn", "url": url, "date": datetime.now().isoformat()}
        elif "instagram.com" in domain:
            return {"platform": "Instagram", "url": url, "date": datetime.now().isoformat()}
        else:
            return {"platform": "Other", "url": url, "date": datetime.now().isoformat()}
    
    def save_to_obsidian(self, article):
        """Save article to Obsidian vault"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{self.obsidian_path}/01-Inbox/{date_str}-{article['platform']}-article.md"
        
        content = f"""---
platform: {article['platform']}
url: {article['url']}
date: {article['date']}
tags: {article.get('tags', [])}
status: unread
---

# Article from {article['platform']}

Source: {article['url']}

## Content

{article.get('content', 'Content to be extracted...')}

## Notes

- 

## Insights

- 
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename
    
    def generate_insights(self, articles):
        """Generate insights from collected articles"""
        insights_file = f"{self.obsidian_path}/03-Insights/{datetime.now().strftime('%Y-%m-%d')}-insights.md"
        
        content = f"""---
date: {datetime.now().isoformat()}
article_count: {len(articles)}
---

# Daily Insights

## Articles Collected

"""
        for article in articles:
            content += f"- [{article['platform']}] {article['url']}\n"
        
        content += """
## Key Themes

- 

## Content Opportunities

- 

## Action Items

- [ ] 
"""
        
        with open(insights_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return insights_file

def main():
    reader = ContentReader()
    print(f"🚀 ALKINDUS Content Reader - {datetime.now()}")
    print("Ready to process shared links...")
    print(f"Obsidian vault: {reader.obsidian_path}")

if __name__ == "__main__":
    main()
