from youtubesearchpython import SearchVideos
import json
import telebot
from pytube import YouTube
from requests import get
from io import BytesIO

bot = telebot.TeleBot("5836671898:AAGK4FnQfeuZ7hBmGWNdPHG8nXsu3Aw8-qU")

@bot.message_handler(commands=["find_audio"])
def send_audio(message):
    command = message.text[:message.text.find(" ")]+message.text[-1]
    if message.text != command:
        try:
            sv = SearchVideos(message.text[11:], offset=1, mode="json", max_results=1)
            results = json.loads(sv.result())
            audio_url = results["search_result"][0]['link']
            audio_name = results["search_result"][0]['title']
            print(audio_url)
            yt = YouTube(audio_url)
            audio_url = yt.streams.filter(only_audio=True).first().url
            bot.send_message(chat_id=message.from_user.id, text=f"Sending '{audio_name}'. Wait a bit, please")
            response = get(audio_url)
            audio = BytesIO(response.content)
            bot.send_audio(chat_id=message.from_user.id, audio=audio, title=audio_name)
        except Exception as e:
            bot.send_message(chat_id=message.from_user.id, text=f"Sorry, got an error. Try to search for something else. "
                                                                f"Error text:\n{e}")
    else:
        bot.send_message(chat_id=message.from_user.id, text="Please, enter the valid message like this:\n"
                                                            f"{command} amazing phonk")

bot.polling()

