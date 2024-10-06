from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('subscription_form.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    # 处理订阅请求
    pass

@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    # 处理退订请求
    pass

if __name__ == '__main__':
    app.run(debug=True)