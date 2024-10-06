import schedule
import time
from config_parser import get_all_configs
from web_scraper import scrape_journal
from content_comparator import compare_content
from rss_generator import generate_rss
from subscription_manager import SubscriptionManager
from email_sender import send_email
from utils import setup_logging, handle_error
import os
import json

@handle_error
def process_journal(config):
    articles = scrape_journal(config)
    
    # 加载上一次的数据
    data_file = os.path.join(config['storage']['data_dir'], 'latest_data.json')
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            old_articles = json.load(f)
    else:
        old_articles = []

    # 比较新旧数据
    diff = compare_content(old_articles, articles)

    if diff:
        # 更新 RSS
        rss_content = generate_rss(config, articles)
        with open(config['rss']['link'], 'w', encoding='utf-8') as f:
            f.write(rss_content)

        # 发送邮件通知
        sub_manager = SubscriptionManager('subscriptions.db')
        subscribers = sub_manager.get_subscribers(config['name'])
        for subscriber in subscribers:
            send_email(subscriber, config['email']['subject_template'].format(journal_name=config['name']),
                       config['email']['body_template'].format(journal_name=config['name'], article_list='\n'.join([a['title'] for a in articles[:config['email']['max_articles_per_email']]]))
                      )

    # 保存新数据
    os.makedirs(config['storage']['data_dir'], exist_ok=True)
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

def main():
    setup_logging()
    configs = get_all_configs()  # 不再需要传入 'config' 目录
    
    for config in configs:
        schedule.every(config['frequency']).do(process_journal, config)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()