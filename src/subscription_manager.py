import sqlite3

class SubscriptionManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_table()
    
    def create_table(self):
        # 创建用户订阅表
        pass
    
    def add_subscription(self, email, journal):
        # 添加订阅
        pass
    
    def remove_subscription(self, email, journal):
        # 移除订阅
        pass
    
    def get_subscribers(self, journal):
        # 获取特定期刊的所有订阅者
        pass