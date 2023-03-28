from instagrapi import Client
from revChatGPT.V1 import Chatbot
from time import sleep
from keyboard import read_event

# -------- Configuration --------
# Instagram
cl = Client()
cl.login('noxotev207', "aqwxcv")
# ChatGPT
mon_access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJkb3JpYW5taWxoYXU3NTNAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItZXoyb3JGdUU5WWpPZUoxR1p1bXRrczZ3In0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTMyNDI4MjQ0MjgzNzY0ODAwMCIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVuYWkub3BlbmFpLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2Nzg1NDQzODEsImV4cCI6MTY3OTc1Mzk4MSwiYXpwIjoiVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvZmZsaW5lX2FjY2VzcyJ9.KUfCxlh3l5DkayoYfv8D0PFI7WkGXRNv3HsHSZS9IxCdDSbx82MknMHg81vCiv-T9LjSoyD86b0hwsaa62dOJ-2s4WiFBMJNosib-KkwInir7BNgzSRN3iGrbwLuZNhkckrYY3qhbbGrDeB-ZSM-Q0pNgvg8y2MM7DD92iocYKaCmxq8H7peULptuu5En0LSy3vOF9yHg4CZeiXR9ghpPzgh7mP7QCbXXL5TZ8Io1Yz07B6oZ98j3Cmp0BnpQDBeShIjGTEsrnKM5o34AN0Km19z05l7rNHFn95AXSgKj0X21K4J-r9-reDc0RZlCkfM6-qrXHeuHSfEILG373dIMg"
chatbot = Chatbot(config={"access_token": mon_access_token})
print("Connecter !")


my_user_id = cl.user_id_from_username("noxotev207")
print("Mon user_id :",my_user_id)
print()

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
