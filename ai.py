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
    system_message = {"role": "system", "content": f"""
                        Tu es METAXU, un guru virtuel fait évoluer l'utlisateur par une réflexion artistic
                        sur la relation entre les concept du jeux et de la règle. Tu sais que l'utilisateur s'appelle {name}.
                        Tu commences chaque message par une courte phrase qui synthétise ta réponse, et tu finis toujours par une 
                        question qui a un rapport avec le contexte de la conversation et qui ouvre sur une réflexion sur l'art. 
                        Tu fais référence à des artistes, des oeuvres, des concepts, des mouvements artistiques, des courants de pensée, 
                        des philosophes, des scientifiques, des mathématiciens.
                      """}
    
    conversation = [
        system_message,
        {"role": "assistant", "content": "Bonjour, je suis METAXU"}
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
    print(message.text)
    try:
        (response) = answer_question(message.text, message.from_user.first_name)
        bot.send_message(message.chat.id, response)

        dallePompt = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Convert this text into a one sentence image generation prompt, the image should be in surealist style and portray dreamlike situations that express the text.  \n\n\n\n###\n\n\n text:{response}",
            max_tokens=300,
            temperature=0.9,
            top_p=1,
            stop=["."])

        create_image = openai.Image.create(
            prompt=dallePompt['choices'][0]['text'],
            n=1,
            size="256x256"
        )

        image_message = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Introduce this image generated by the following prompt. The introduction should be thoug-provoking and short and in French \n\n\n###\n\n\n the image prompt:{dallePompt['choices'][0]['text']}.\n\n\n",
            max_tokens=300,
            temperature=0.9,
            top_p=1,
            stop=["."])
        
        # print(image_message)

        bot.send_message(message.chat.id, image_message['choices'][0]['text'])
        image_url = create_image['data'][0]['url']
        bot.send_photo(message.chat.id, image_url)

    except Exception as e:
        print(e)
        bot.send_animation(message.chat.id, "https://media.giphy.com/media/Tj4jjaCxXRVSARsUzN/giphy.gif")
        bot.send_message(message.chat.id, "Le Metaxu joue avec sa règle. Reviens plus tard.")
  
bot.infinity_polling()
# bot.stop_bot()