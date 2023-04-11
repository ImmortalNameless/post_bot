from aiogram import executor, types
from flask import Flask, request
from handlers.all import dp

app = Flask(__name__)

@app.route('/botttt', methods=['POST'])
def handle_webhook():
    update = types.Update(**request.json)
    dp.process_update(update)
    return 'OK'

executor.start_webhook(
    dp,
    "/botttt"
)
