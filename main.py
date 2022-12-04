from flask import Flask, request
import chatgpt

app = Flask('chatgpt-server')


@app.route('/')
def index():
    return 'server is running'


@app.route('/chat', methods=['POST'])
def chat():
    question = request.form['question']
    answer = chatgpt.ask(question)
    return answer


if __name__ == '__main__':
    chatgpt.start_browser()
    app.run()
