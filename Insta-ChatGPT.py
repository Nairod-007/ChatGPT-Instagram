from instagrapi import Client
from revChatGPT.V1 import Chatbot
from time import sleep
from keyboard import read_event

# -------- Configuration --------
# Instagram
cl = Client()
cl.login('id_account', "mdp_account")
# ChatGPT
mon_access_token = "access_token"
chatbot = Chatbot(config={"access_token": mon_access_token})
print("Connecter !")


# -------- (get) Message Insta (send) -> ChatGPT (get for send)-> Message Insta --------

def chatgpt(message, my_user_id, destinataire):
    if message.user_id != int(my_user_id):
        # Lis le dernier message de la conversation si le message ne m'appartient pas
        prompt = message.text
        user_id_message = "De " + destinataire + " : " + str(prompt)
        print(user_id_message)
        print()
        if "stop" not in prompt:
            # ChatGPT
            print("Je l'envoie à ChatGPT")
            response = ""
            for data in chatbot.ask(prompt):
                response = data["message"]
            print(response)
            cl.direct_send(response,[id_destinataire])
            print("Réponse envoyé !")
            conversation = chatbot.get_conversations()
            chatbot.delete_conversation(conversation[0]["id"])
            return True
        else:
            print("STOP")
            return False

z=True
while z:
    invitation = cl.direct_pending_inbox()
    if len(invitation) > 0:
        for conv in invitation:
            #Lis chaque conversation
            destinataires = conv.users
            destinataire = destinataires[0].username
            id_destinataire = cl.user_id_from_username(destinataire)

            messages = cl.direct_messages(conv.id)
            message = messages[0]
            z = chatgpt(message, my_user_id, destinataire)
            cl.direct_thread_hide(conv.id)
            print("conversation supprimer")

    # Récupère les messages :
    print("Je lis les messages")
    inbox_threads = cl.direct_threads()
    if len(inbox_threads) > 0:
        for last_thread in inbox_threads:
            #Lis chaque conversation
            destinataires = last_thread.users
            destinataire = destinataires[0].username
            id_destinataire = cl.user_id_from_username(destinataire)

            messages = cl.direct_messages(last_thread.id)
            message = messages[0]
            z = chatgpt(message, my_user_id, destinataire)
            cl.direct_thread_hide(last_thread.id)
            print("conversation supprimer")
    else:
        print("Il n'y a pas de message maitenant")
    
    sleep(10)

cl.logout()
