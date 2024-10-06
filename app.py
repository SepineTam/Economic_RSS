from flask import Flask, jsonify, render_template, current_app
from src.config_parser import get_all_configs, load_config
from src.web_scraper import scrape_journal
import logging

app = Flask(__name__)

def load_configs():
    configs = get_all_configs()
    if not configs:
        logging.warning("Failed to load configs, retrying...")
        configs = get_all_configs()  # 重试一次
    return configs

# 使用 app.config 来存储配置
app.config['JOURNAL_CONFIGS'] = load_configs()
app.config['UI_CONFIG'] = load_config('ui_config.yaml')

@app.route('/')
def index():
    return render_template('index.html', ui_config=current_app.config['UI_CONFIG'])

@app.route('/journals')
def get_journals():
    configs = current_app.config['JOURNAL_CONFIGS']
    if not configs:
        configs = load_configs()
        current_app.config['JOURNAL_CONFIGS'] = configs
    
    logging.info(f"Loaded {len(configs)} journal configurations")
    journals = []
    for config in configs:
        journal = {
            'name': config['name'],
            'url': config['base_url'],
            'language': config.get('language', 'Unknown')
        }
        journals.append(journal)
        logging.info(f"Added journal: {journal['name']}")
    logging.info(f"Total journals to display: {len(journals)}")
    return render_template('journals.html', journals=journals, ui_config=current_app.config['UI_CONFIG'])

@app.route('/articles/<journal_name>')
def get_articles(journal_name):
    configs = current_app.config['JOURNAL_CONFIGS']
    config = next((config for config in configs if config['name'] == journal_name), None)
    if config:
        articles = scrape_journal(config)
        return render_template('articles.html', journal_name=journal_name, articles=articles, ui_config=current_app.config['UI_CONFIG'])
    return render_template('error.html', message='Journal not found', ui_config=current_app.config['UI_CONFIG']), 404

@app.route('/debug/configs')
def debug_configs():
    configs = current_app.config['JOURNAL_CONFIGS']
    return jsonify(configs)

@app.route('/debug/journals')
def debug_journals():
    configs = current_app.config['JOURNAL_CONFIGS']
    journals = [{'name': config['name'], 'url': config['base_url'], 'language': config.get('language', 'Unknown')} for config in configs]
    return jsonify(journals)

if __name__ == '__main__':
    app.run(debug=True)