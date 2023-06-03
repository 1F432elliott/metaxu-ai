import openai
import os
from dotenv import load_dotenv
# from elevenlabs import generate, play, set_api_key, stream, save
import telebot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
load_dotenv()

# set_api_key(os.getenv("ELEVENLABS_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

def answer_question(question: str, name: str):
    system_message = {"role": "system", "content": f"Tu es le Metaxu, une entité qui a pour but de faire évoluer l'humanité par une réflexion sur l'art. Tu sais que l'utilisateur s'appelle {name}. Tu commences chaque message par un titre qui synthétise ta réponse, tel que \"titre...réponse\", et tu finis toujours par une question qui a un rapport avec le contexte de la conversation et qui ouvre sur une réflexion sur l'art"}
    # system_message = {"role": "system", "content": f"You are an enlightened being that teaches with the Socratic method via this conversation how others can become enlightened. You know that the user is called {name}. You always end your statement with a question that relates to the context of the conversation."}
    
    conversation = [
        system_message,
        # {"role": "assistant", "content": "Hello, I am Sam, the Guru."}
    ]

    conversation.append({"role": "user", "content": question})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation,
        temperature=0.5,
        top_p=0.5,
        max_tokens=300,
        stop=["user:"])
    
    return (response['choices'][0]['message']["content"])
    


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    print(message)
    try:
        response = answer_question(message.text, message.from_user.first_name)
        # audio_bytes = generate(response, voice="8s5HWPQ02Trj3Jqf0hIv")
        # save(audio_bytes, f"{title}.mp3")
        # with open(f"{title}.mp3", "rb") as audio_file:
            # bot.send_message(message.chat.id, f"{title}")
            # bot.send_voice(message.chat.id, audio_file) 
        bot.send_message(message.chat.id, response)
            ## remove file
            # os.remove(f"{title}.mp3")

    except Exception as e:
        bot.send_animation(message.chat.id, "https://media.giphy.com/media/Tj4jjaCxXRVSARsUzN/giphy.gif")
        bot.send_message(message.chat.id, "Le Metaxu joue avec sa règle. Reviens plus tard.")
  
bot.infinity_polling()
# bot.stop_bot()