import yaml
import os
import logging

def load_config(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"Config file not found: {config_file}")
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML in {config_file}: {e}")
    return None

def get_all_configs(global_config_file='./config.yaml'):
    logging.info(f"Attempting to load global config from: {os.path.abspath(global_config_file)}")
    global_config = load_config(global_config_file)
    if not global_config:
        logging.error("Failed to load global config")
        return []

    logging.info(f"Global config loaded: {global_config}")
    
    configs = []
    config_dir = os.path.dirname(global_config_file)
    
    for journal in global_config.get('journals', []):
        config_path = os.path.join(config_dir, 'config', journal['config_file'])
        if not os.path.exists(config_path):
            logging.error(f"Config file not found: {config_path}")
            continue
        logging.info(f"Attempting to load config for {journal['name']} from: {os.path.abspath(config_path)}")
        journal_config = load_config(config_path)
        if journal_config:
            journal_config['name'] = journal['name']
            configs.append(journal_config)
            logging.info(f"Loaded configuration for {journal['name']}")
        else:
            logging.error(f"Failed to load configuration for {journal['name']}")
    
    logging.info(f"Total configs loaded: {len(configs)}")
    return configs