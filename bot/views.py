from django.shortcuts import render
from django.http import HttpResponse
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
import openai
import tiktoken
import os
from .models import UserQuery 

#important api keys and  Details

client = Client(account_sid, auth_token)

@csrf_exempt
def bot(request):
    message_from_user = request.POST.get("Body")
    chunk_size = 1300
    message_from_user_start1 = message_from_user.lower().startswith("hello")
    message_from_user_start2 = message_from_user.lower().startswith("hi")
    def get_completion(prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
        return response.choices[0].message["content"]
    def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=500):
        response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
        max_tokens=max_tokens, # the maximum number of tokens the model can ouptut 
    )
        return response.choices[0].message["content"]
    def split_string(text, chunk_size=1300):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    def intro():
         message_intro = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:+917990565567',
                body=f"🌿 Welcome to G.O.A.T, your go-to Wellness and Health Bot! 🤖\n🌱 We specialize in Herbal and Ayurvedic solutions, offering you a path to complete natural wellness. 🌼\n\n👉 What's troubling you today?\n📝 *Please start your query with the phrase \"Hello\"  or \"Hi\"* 👋"

        )
    def processing():
         message1 = client.messages.create(
            from_='whatsapp:+14155238886',
            to='whatsapp:+917990565567',
            body=f"🌿 We're brewing up some herbal wisdom for you! 🍵 Please hang tight while we find the perfect natural solution for your wellness query. 🌱✨"
        )
    def short_message():
         message_error = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:+917990565567',
                body=f"🌿 Oops! Your message was a bit short.  🤔  🌱 Could you please elaborate a little more? \n 🌼 *Start your message with \"Hello\" or \"Hi\"* so we can dig deeper into your herbal health and wellness journey. 🍃🌸"
        )
    def doctor():
            messages_doctor =  [  
            {'role':'system',
            'content':"""Answer within 150 words . give answer in the formed of numbered list. You are an anceint medicine practitioner , your skills include Ayurvedic Doctor , Yoga Teacher, Nutritionalist / Dietician , Gym Trainer . You have to decide which among your skills can suit to best help your clients problem , give him herbal and natural solutions not having to use any artificial medicines. """},    
            {'role':'user',
            'content':f"""{message_from_user}"""},
            ] 
            response_doctor = get_completion_from_messages(messages_doctor, 
                                                    temperature =1)
            header_response_doctor="✨🌿 *This is the Answer from our Ayurvedic Bot:* 🌱✨\n\n"
            response_doctor_splitted = split_string(response_doctor, chunk_size)
            combined_response_doctor=header_response_doctor+response_doctor_splitted[0]
            messages_doctor = client.messages.create(
            from_='whatsapp:+14155238886',
            to='whatsapp:+917990565567',
            body=combined_response_doctor
            )
            return combined_response_doctor
    def product():
        
            messages_product =  [  
            {'role':'system',
            'content':"""Have total Answer within 150 words. Suggest a product from the below dictionary products = {
                "KIWI SLOW ORGANIC CLOVE": "https://www.kisanwindow.com/product-detail/15",
                "ORGANIC OLIVE OIL POMACE 500ML": "https://www.kisanwindow.com/product-detail/22",
                "Avimee Herbal Keshpallav Hair Oil For Men And Women": "https://www.amazon.in/Avimee-Keshpallav-Reduces-dandruff-Promotes/dp/B0B6W5KCRM/ref=sr_1_10?keywords=Herbal+Products&sr=8-10",
                "KIWI KASHMIRI KAHWA": "https://www.kisanwindow.com/product-detail/2",
                "STRONG COFFEE": "https://www.kisanwindow.com/product-detail/3",
                "KIWI SAFFRON": "https://www.kisanwindow.com/product-detail/4",
                "KIWI SLOW OLIVE OIL EXTRA VIRGIN": "https://www.kisanwindow.com/product-detail/5",
                "KIWI SLOW ORGANIC TURMERIC POWDER": "https://www.kisanwindow.com/product-detail/6",
                "KIWI SLOW ORGANIC BLACK PEPPER": "https://www.kisanwindow.com/product-detail/7",
                "KIWI SLOW ORGANIC BLACK RICE": "https://www.kisanwindow.com/product-detail/8",
                "KIWI SLOW ORGANIC BROWN BASMATI RICE": "https://www.kisanwindow.com/product-detail/9",
                "KIWI SLOW ORGANIC CARDAMOM BLACK": "https://www.kisanwindow.com/product-detail/10",
                "KIWI SLOW ORGANIC CARDAMOM GREEN": "https://www.kisanwindow.com/product-detail/11",
                "KIWI SLOW ORGANIC CASHEW": "https://www.kisanwindow.com/product-detail/12",
                "KIWI SLOW ORGANIC CINNAMON POWDER": "https://www.kisanwindow.com/product-detail/13"
            }"""},
            {'role':'user',
            'content':f"""Suggest me some food items because {message_from_user} also send me ingredients with their links to buy """},
            ]
            response_product = get_completion_from_messages(messages_product, 
                                                    temperature =1)
            header_response_product="🌿🌼 *These are the herbal products we suggest for your path to wellness:* 🌱💚\n\n"
            response_product_splitted = split_string(response_product, chunk_size)
            combined_response_product=header_response_product+response_product_splitted[0]
            message_product = client.messages.create(
            from_='whatsapp:+14155238886',
            to='whatsapp:+917990565567',
            body=combined_response_product
            )
            return combined_response_product
    def pipeline():
        if not message_from_user_start1 and  not message_from_user_start2:
            intro()
        if len(message_from_user)<10:
            short_message()
        if message_from_user_start1 or message_from_user_start2:
            processing()
            doctor_response = doctor()  # Modify the doctor function to return the response
            product_response = product()  # Modify the product function to return the response

            UserQuery.objects.create(
            user_message=message_from_user,
            doctor_response=doctor_response,
            product_response=product_response
            )
    pipeline()  
    return HttpResponse("Message sent")
    


#Code With Intelligent OpenAI Analysis

#     messages = [
#         { "role": "system", "content": f"""You are a helpful assistant trained to analyze customer messages for a Wellness and Health Bot. Based on the content of the message, determine the appropriate response. The possible responses are:

# 1. If the message is from a new customer reply \"new customer\"
# 2. If the message is gibberish reply \"gibberish\"
# 2. If the message is too short to understand \"short message\"
# 3. If the message has enough context, \"enough context\"

# Analyze this customer message: "{message_from_user}"
# """},
#         {"role": "user", "content": message_from_user}
#     ]

#     # Get analysis from GPT-3.5
#     analysis = get_completion_from_messages(messages)
#     client.messages.create(
#         from_='whatsapp:+14155238886',
#         to='whatsapp:+917990565567',
#         body=f"{analysis[:1200]}"
#     )
#     # Decide which message to send based on the analysis
#     if "new customer" in analysis and "gibberish" in analysis:
#         send_welcome_message()
#     elif "short message" in analysis:
#         send_short_message_error()
#     elif "enough context" in analysis:
#         send_main_function_message()
#     else:
#         send_default_message()

#     return HttpResponse("Message processed")

# def send_welcome_message():
#     client.messages.create(
#         from_='whatsapp:+14155238886',
#         to='whatsapp:+917990565567',
#         body=f"🌿 Welcome to G.O.A.T, your go-to Wellness and Health Bot! 🤖\n🌱 We specialize in Herbal and Ayurvedic solutions, offering you a path to complete natural wellness. 🌼\n\n👉 What's troubling you today?\n📝 Please start your query with the phrase \"Hello\" or \"Hi\" 👋"
#     )

# def send_short_message_error():
#     client.messages.create(
#         from_='whatsapp:+14155238886',
#         to='whatsapp:+917990565567',
#         body=f"Your message is very short. Please describe your problem in more words, starting with 'Hello'."
#     )

# def send_main_function_message():
#     client.messages.create(
#         from_='whatsapp:+14155238886',
#         to='whatsapp:+917990565567',
#         body=f"We are working on your query. Please wait..."
#     )

# def send_default_message():
#     client.messages.create(
#         from_='whatsapp:+14155238886',
#         to='whatsapp:+917990565567',
#         body=f"Sorry, we couldn't understand your message. Could you please rephrase?"
#     )



###################
#If you want both doctor and product together then
# messages_doctor =  [  
        # {'role':'system',
        # 'content':"""Answer within 150 words . give answer in the formed of numbered list. You are an anceint medicine practitioner , your skills include Ayurvedic Doctor , Yoga Teacher, Nutritionalist / Dietician , Gym Trainer . You have to decide which among your skills can suit to best help your clients problem , give him herbal and natural solutions not having to use any artificial medicines. """},    
        # {'role':'user',
        # 'content':f"""{message_from_user}"""},
        # ] 
        # response_doctor = get_completion_from_messages(messages_doctor, 
        #                                         temperature =1)
        # response_product = get_completion_from_messages(messages_product, 
        #                                         temperature =1)

        # def split_string(text, chunk_size):
        #     return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        # chunk_size = 1300
        # header_response_doctor="✨🌿 *This is the Answer from our Ayurvedic Bot:* 🌱✨\n"
        # header_response_product="🌿🌼 *These are the herbal products we suggest for your path to wellness:* 🌱💚\n"
        # response_doctor_splitted = split_string(response_doctor, chunk_size)
        # response_product_splitted = split_string(response_product, chunk_size)
        
        # message = client.messages.create(
        # from_='whatsapp:+14155238886',
        # to='whatsapp:+917990565567',
        # body=header_response_product+response_product_splitted[0]
        # )