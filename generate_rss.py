#!/usr/bin/env python3
"""
Automated RSS generator for Vimal & Sons
Reads posts from posts.txt and generates RSS feed
"""

import xml.etree.ElementTree as ET
import urllib.parse
from datetime import datetime, timedelta
import os

def read_posts_file():
    """Read posts from posts.txt file"""
    posts_data = []
    
    try:
        with open('posts.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
        for i, title in enumerate(lines):
            # Convert title to URL format
            url_title = urllib.parse.quote_plus(title.replace(' ', '+'))
            
            posts_data.append({
                'title': title,
                'description': f'Latest insights on {title.lower()}',
                'url': f'https://publish.obsidian.md/16061995/Publish/{url_title}',
                'date': datetime.now() - timedelta(days=i)  # Newest first
            })
            
    except FileNotFoundError:
        print("⚠️  posts.txt not found, using default posts")
        # Fallback to your current posts
        posts_data = [
            {
                'title': 'Time in the Market - Not Timing the Market',
                'description': 'Investment insights on the importance of staying invested rather than trying to time market movements.',
                'url': 'https://publish.obsidian.md/16061995/Publish/Time+in+the+Market+-+Not+Timing+the+Market',
                'date': datetime.now()
            },
            {
                'title': 'How to Time the Market',
                'description': 'Exploring market timing strategies and their effectiveness in investment planning.',
                'url': 'https://publish.obsidian.md/16061995/Publish/How+to+Time+the+Market',
                'date': datetime.now() - timedelta(days=1)
            },
            {
                'title': 'Book Highlights - Against the Gods',
                'description': 'Key insights and highlights from Peter L. Bernstein\'s book "Against the Gods" on risk and decision-making.',
                'url': 'https://publish.obsidian.md/16061995/Publish/Book+Highlights',
                'date': datetime.now() - timedelta(days=2)
            }
        ]
    
    return posts_data

def generate_rss_feed():
    """Generate RSS feed from posts data"""
    
    posts = read_posts_file()
    
    # Create RSS structure
    rss = ET.Element('rss', version='2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    
    channel = ET.SubElement(rss, 'channel')
    ET.SubElement(channel, 'title').text = 'Vimal & Sons'
    ET.SubElement(channel, 'description').text = 'Updates from Vimal & Sons Investment Garden'
    ET.SubElement(channel, 'link').text = 'https://publish.obsidian.md/16061995/Publish/Index'
    
    atom_link = ET.SubElement(channel, 'atom:link')
    atom_link.set('href', 'https://yashodhankhare.github.io/vimal-sons-rss/feed.xml')
    atom_link.set('rel', 'self') 
    atom_link.set('type', 'application/rss+xml')
    
    ET.SubElement(channel, 'language').text = 'en-us'
    ET.SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # Add items (newest first)
    for post in posts[:10]:  # Limit to 10 most recent posts
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = post['title']
        ET.SubElement(item, 'description').text = post['description']
        ET.SubElement(item, 'link').text = post['url']
        ET.SubElement(item, 'guid').text = post['url']
        ET.SubElement(item, 'pubDate').text = post['date'].strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # Write to file
    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ", level=0)
    tree.write('feed.xml', encoding='utf-8', xml_declaration=True)
    
    print("✅ RSS feed updated successfully!")
    print(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📝 Total posts: {len(posts)}")
    
    # List the posts
    print("\n📋 Current posts in feed:")
    for i, post in enumerate(posts[:10], 1):
        print(f"  {i}. {post['title']}")

if __name__ == "__main__":
    generate_rss_feed()