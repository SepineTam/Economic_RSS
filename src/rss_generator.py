from feedgen.feed import FeedGenerator

def generate_rss(config, articles):
    fg = FeedGenerator()
    fg.title(config['rss']['title'])
    fg.description(config['rss']['description'])
    fg.link(href=config['rss']['link'])
    
    for article in articles:
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=article['link'])
        fe.description(article['abstract'])
    
    return fg.rss_str(pretty=True)