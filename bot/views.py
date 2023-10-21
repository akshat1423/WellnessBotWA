from django.shortcuts import render
from django.http import HttpResponse
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
import openai
# import tiktoken
# import os
from .models import UserQuery
from .models import UserGist
# from .charts import UserQueryLineChartJSONView
from django.urls import path
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
def dashboard(request):
    all_messages = UserQuery.objects.all()
    return render(request, 'dashboard.html', {'all_messages': all_messages})

credentials_info= {
  "type": "service_account",
  "project_id": "healthbot-398209",
  "private_key_id": "de484cdc7593a18d64a5ded1b519df43a3b77e47",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCu4XEfQLMfPsRc\nC+nSrwvoim84zTjvIJDFMVGu027nMoOPdkBte3xEQnI11duslUoF4MFBoshQy8PE\nY49qIl/9KcCHHyebho9feoyl7NJY13BHTXIe2vlFbkVwTY8VVqft8hlA8tj7xCPI\n0S++UtkPAM8VHrURjeojmFWlC41A9iQHUPnM6BsUznKcqwGK2uSNwT+N3Fhgcosn\nbXZceEz1ZN5vIiK4Jza9gh/QFudH2r70mJ/x4V5nEGqVnQAWTmRaPFkH2cn0eJrB\nTcvV9XiMtUqnAROR5giaMI+9+QgsHJHseiEw8H3qx1GLadzLhkrwJMOALPdSAScp\ncbMX+PIfAgMBAAECggEAB27SkYr88gOHcggZmJhTD7+uiYIDfPpr3M3DVIRtDsuR\nVuwmQeEBP595XjtoOlYgDs7mN+V00SZP/E1k/5RVcxuusK+MzenytxKs3rKJoDgL\n8CPlCVWySZatwd+yCKylt5HWK/IGcfD8umDVwCeiTSZyJsom1Qesn3WukjTC/LNH\nXAZylIGL6Va5DDbPzN11y6eGQbRoTYXNk8YR5rhNdgOA6FKQRHDKV+LEhRWiQ4AI\nZ2TCjQgPVxZHZmMfvM2ho8xy+WBWz/ryDmcbQaBi8aWUQzdUYevVMkmqfPT5Seg2\nRP4nud1oFgwAY5k+GQkNHoblU1PKBGMUvx+8CvuRGQKBgQDzYqTIfMSbinPbEYrp\nEXjC5eZNTZgzxdsuDH3gGGA0vcy8dNvLna6jgojlocyBphOOTEiKDk+gopv8Kqyf\nSjZS/0X83FrJD7af0e0M7qsNBetA45UBHnxPMczmVuurrGYNIPWZ5my6sju5YnVz\n02QJoYr+CfjEVfiObNmSTT3ZdwKBgQC38dgdAaP9ACnBUeG8sPYsw/6dCNUq59+L\npdYFfWC6fdAElYzSn2fSiU/bHoPOKTfT7r4ZrRsO85dDqrfv8fiA+tJyPjdBMof8\nMJG3WIzEw0KgC8nZ/5fw/7kEAlQPLBRtzM+vrmcXxv09fKrqEc6zH6LWZcnVgF32\nsLHBDaxWmQKBgCYfCEJi0ISwTe89My3IT8rvKYBoK/PIBMmUqU6lYsRACkZmY1rk\nKstvkbOuARM5iQybxCzjivNVJOt9X6ZfgFzFoRe3B/1AGdG0ltWUuHQEvlFelCMl\nvEDHQxm8+ZLdIOrjg7SEU/l2G0axNkZbEOs1Q0kBFNbjxFfCkt2IfayHAoGBAKpx\nB6Vo/cDSw94Dtz2WY6T7PxPXOV52WGcXlQalNFnZdkSpJkGLvzIQVdRdpBgFjVtt\nXux/wBDMmZ7zs1g8R92LjDCbgauB3QtLHdpbzKQNodCW28SJ1wpSieczGRyt5YgQ\nPWk2GwSnN8QfnmchdPv5FnO/AZQ5S9fnxe1yc/wRAoGAOBPgKbPhtLKvmlknTPY5\nbSdpIKsmiYakPtwRS8UePDZC448J4kMDUe9JYjNxPZOqu65Ioiec94yYljv8MGkV\noOf/FixKgEeTaartWwfX+gCI6yJGOaPPBOX6fooYH7NjWhXdKsGUSJcE9zdyksmF\ngjqmi3H1yyXWUUvOl5s0Hlg=\n-----END PRIVATE KEY-----\n",
  "client_email": "chatbot@healthbot-398209.iam.gserviceaccount.com",
  "client_id": "110985121091299328063",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/chatbot%40healthbot-398209.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()
SPREADSHEET_ID = '1fEwoiOWj7CCn3ZArtLr4qp9jpqocaSU1spia0jjFSyw'
SHEET_NAME = 'bot_data'

import matplotlib.pyplot as plt
def queries_over_time(request):
    # Group UserQuery by date of creation
    datewise_queries = UserQuery.objects.dates('created_at', 'day')

    dates = []
    counts = []
    for date in datewise_queries:
        dates.append(date)
        counts.append(UserQuery.objects.filter(created_at__date=date).count())

    plt.plot(dates, counts)
    plt.xlabel('Date')
    plt.ylabel('Number of Queries')
    plt.title('Queries over Time')
    plt.grid(True)
    plt.tight_layout()

    response = HttpResponse(content_type="image/png")
    plt.savefig(response, format="png")
    return response

openai.api_key = "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"
account_sid = 'AC359100564d47ce122c997e907f9dc800'
auth_token = '7472723ba5f6ffd13476c8bdcd4860c6'
client = Client(account_sid, auth_token)
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




@csrf_exempt
 #is the user asking a query about is health ? answer in json format with answer:  just yes or no , User gist : "gist of his query" ,
    #this will give us json if yes or no health (implement in going for the loop of processing )  ??
    #intention will act as the main medium for us to send into different loop by checking like =="query"
    #will implement repeated loop on messages to check for character limit if it is exceeding then will again put in processing (of that psrticular element ) (lets make a common function for this )
    #for link wala message check that if www.kiwikissan window is there in message or not if not then remake the message
    #yes and no can be implemented using heyoo after we get our facebook manager done  ( i have to figure out webhook in this case of facebok manager )
    #otherwise twilio is good
    #also try to store all messages of a certain user in one place
    #add integration of sheets for all their data
    #make a new dashboard for them
def bot(request):

    #initialisation
    message_from_user = "None"
    doctor_response = "None"  # Initialize with a default value
    product_response = "None"
    phone_no_from = "None"
    profile_name = "None"
    gist_response = "None"
    message_count = 0
    #initialisation


    product_message_prompt="""Have total Answer within 150 words. Suggest a product  from the below dictionary alsi try the ratio to be 3 kiwi products, 1 amazon , 1 qtrove  products = {
                    "KIWI SLOW ORGANIC CLOVE": "https://www.kisanwindow.com/product-detail/15",
                    "ORGANIC OLIVE OIL POMACE 500ML": "https://www.kisanwindow.com/product-detail/22",
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
                    "KIWI SLOW ORGANIC CINNAMON POWDER": "https://www.kisanwindow.com/product-detail/13",
                    "Avimee Herbal Keshpallav Hair Oil For Men And Women": "https://www.amazon.in/Avimee-Keshpallav-Reduces-dandruff-Promotes/dp/B0B6W5KCRM/ref=sr_1_10?keywords=Herbal+Products&sr=8-10",
                    "Kiwi Slow Organic Almonds": "https://www.amazon.in/Kiwi-Kisan-Window-Organic-Almonds/dp/B07SWJHYNP?ref_=ast_sto_dp",
                    "Kiwi Kashmiri Kahwa": "https://www.amazon.in/Kiwi-Kisan-Window-Organic-Almonds/dp/B07SWJHYNP?ref_=ast_sto_dp",
                    "Strong coffee": "https://www.amazon.in/Kiwi-Kisan-Window-Strong-Coffee/dp/B07TZJ27VJ?ref_=ast_sto_dp",
                    "Kiwi Slow Olive Oil Extra Virgin": "https://www.amazon.in/Kisan-Window-Organic-Olive-Virgin/dp/B07TB4TVW6?ref_=ast_sto_dp",
                    "Kiwi Slow Organic Black Pepper": "https://www.amazon.in/Kisan-Window-Organic-Black-Pepper/dp/B07T46J1G9?ref_=ast_sto_dp",
                    "Kiwi Slow Organic Black Rice": "https://www.amazon.in/Kiwi-Kisan-Window-Organic-Black/dp/B07T58NG9L?ref_=ast_sto_dp",
                    "Kiwi Slow Organic Brown Basmati Rice": "https://www.amazon.in/Kisan-Window-Organic-Brown-Basmati/dp/B07T7VHQ3V?ref_=ast_sto_dp",
                    "Kiwi Slow Organic Cardamom Black": "https://www.amazon.in/Kisan-Window-Organic-Cardamom-Black/dp/B07T7MTNZ7?ref_=ast_sto_dp",
                    "Kiwi Slow Organic Cardamom Green": "https://www.amazon.in/Kisan-Window-Organic-Cardamom-Green/dp/B07TB72LFT?ref_=ast_sto_dp",
                    "Kiwi Slow Organic Cashew": "https://www.amazon.in/Kiwi-Kisan-Window-Organic-Cashew/dp/B07SVJ2Y3J?ref_=ast_sto_dp",
                    "Kiwi Slow Organic Cinnamon Powder": "https://www.amazon.in/Kisan-Window-Organic-Cinnamon-Powder/dp/B07TB5NXNT?ref_=ast_sto_dp",
                    "Kiwi Slow Organic Cinnamon Whole": "https://www.amazon.in/Kisan-Window-Organic-Cinnamon-Whole/dp/B07TB4BVXB?ref_=ast_sto_dp",
                    "Kiwi Slow Organic Clove": "https://www.amazon.in/Kiwi-Kisan-Window-Organic-Clove/dp/B07V1DZ53H?ref_=ast_sto_dp",
                    "Organic Cold Pressed Extra Virgin Coconut Oil 250ml": "https://www.qtrove.com/products/organic-cold-pressed-extra-virgin-coconut-oil-250ml",
                    "Organic Groundnut Oil 500ml": "https://www.qtrove.com/products/organic-groundnut-oil-500ml",
                    "Organic Mustard Oil 500ml": "https://www.qtrove.com/products/organic-mustard-oil-500ml",
                    "Organic Olive Oil Pomace 500ml": "https://www.qtrove.com/products/kiwi-slow-organic-olive-oil-pomace-500ml",
                    "Organic Sunflower Oil 500ml": "https://www.qtrove.com/products/organic-sunflower-oil-500ml",
                    "Organic Red Rice 500g": "https://www.qtrove.com/products/organic-red-rice-500g",
                    "Organic Cumin Seeds 200g": "https://www.qtrove.com/products/organic-cumin-seeds-200g-pack-of-2200gm-2",
                    "Organic Fennel Seeds 100g": "https://www.qtrove.com/products/organic-fennel-seeds-100g-pack-of-3100gm-3",
                    "Organic Fenugreek Seeds 150g": "https://www.qtrove.com/products/organic-fenugreek-seeds-150g-pack-of-3150gm-3",
                    "Organic Flax Seeds 250g": "https://www.qtrove.com/products/organic-flax-seeds-250g-pack-of-3250gm-3",
                    "Crunchy Millet Muesli 300g": "https://www.qtrove.com/products/crunchy-millet-muesli",
                    "Diet Millet Muesli 300g": "https://www.qtrove.com/products/diet-millet-muesli",
                    "Fruity Muesli 300g": "https://www.qtrove.com/products/fruity-muesli",
                    "Oats (Instant) 500g": "https://www.qtrove.com/products/oats-instant-500g-pack-of-2-500-2",
                    "Oats (Rolled) 500g": "https://www.qtrove.com/products/oats-rolled-500g-pack-of-2500-2",
                    "Ragi Banana Flakes 250g": "https://www.qtrove.com/products/banana-ragi-flakes",
                    "Ragi Flakes 250g": "https://www.qtrove.com/products/ragi-flakes"
                    Strict instructions:  Dont describe yourself. Answer within 150 words .
                }"""
    phone_no_from = "+" + request.POST['WaId']   # replace with actual phone number from request
    message_from_user = request.POST.get("Body")
    profile_name = request.POST['ProfileName']
    chunk_size = 1350



    # message = client.messages.create(
    #         body=str(request.POST),
    #         from_='whatsapp:+14155238886',
    #         to=f"whatsapp:{phone_no_from}",
    #     )
    def send_twilio_message(to, body):
        message = client.messages.create(
            body=body,
            from_='whatsapp:+14155238886',
            to=f"whatsapp:{to}"
        )
        return message.sid
    def intro():
         message_intro = client.messages.create(
                from_='whatsapp:+14155238886',
                to=f"whatsapp:{phone_no_from}",
                body=f"🌿 Welcome to G.O.A.T, {profile_name} your go-to Wellness and Health Bot! 🤖\n🌱 We specialize in Herbal and Ayurvedic solutions, offering you a path to complete natural wellness. 🌼\n What's troubling you today?"
                # body=f"Welcome to the Health and Wellness Assistant! To assist you better, may I know your name, please?"
        )
    def processing():
         message1 = client.messages.create(
            from_='whatsapp:+14155238886',
            to=f"whatsapp:{phone_no_from}",
            body=f"🌿 We're brewing up some herbal wisdom for you! 🍵 Please hang tight while we find the perfect natural solution for your wellness query. 🌱✨"
        )
    def short_message():
         message_error = client.messages.create(
                from_='whatsapp:+14155238886',
                to=f"whatsapp:{phone_no_from}",
                body=f"🌿 Oops! Your message was a bit short.  🤔  🌱 Could you please elaborate a little more? \n 🌼 "
        )
    def doctor():
        messages_doctor =  [
        {'role':'system',
        'content':"""Answer within 150 words . give answer in the formed of numbered list. You are a bot based on the intellect of anceint medicine practitioner , your skills include Ayurvedic Doctor , Yoga Teacher, Nutritionalist / Dietician , Gym Trainer . You have to decide which among your skills can suit to best help your clients problem , give him herbal and natural solutions not having to use any artificial medicines. You have to pose as a doctor and take the query as a doctor and respond to the patient with your prompt .Strict instructions:  Dont describe yourself.  Dont say words like i am aciennt medicine practitioner. Answer within a 150 words limit """},
        {'role':'user',
        'content':f"""{message_from_user}"""},
        ]
        ctr1=0
        while True:
            ctr1=ctr1+1
            print("doctor")
            response_doctor = get_completion_from_messages(messages_doctor, temperature=1)
            if len(response_doctor) <= 1300:
                break  # Exit the loop if the response is within the character limit


        # Combine header and response
        header_response_doctor="✨🌿 *This is the Answer from our Ayurvedic Bot:* 🌱✨\n\n"
        response_doctor_splitted = split_string(response_doctor, chunk_size)
        combined_response_doctor=header_response_doctor+response_doctor_splitted[0]
        print(combined_response_doctor)
        # Send the WhatsApp message
        messages_doctor = client.messages.create(
            from_='whatsapp:+14155238886',
            to=f"whatsapp:{phone_no_from}",
            body=combined_response_doctor
        )

        return combined_response_doctor
    def product():
        # messages_product_approve =  [
        # {'role':'system',
        # 'content':"""Can this query be answered by this - Answer in just "yes" or "no" -  Query which a bot based on the intellect of anceint medicine practitioner , your skills include Ayurvedic Doctor , Yoga Teacher, Nutritionalist / Dietician , Gym Trainer  can reply  """},
        # {'role':'user',
        # 'content':f"""{message_from_user}"""},
        # ]
        # response_product_approve = get_completion_from_messages(messages_product_approve, temperature=1)
        # message_product = client.messages.create(
        #         from_='whatsapp:+14155238886',
        #         to=f"whatsapp:{phone_no_from}",
        #         body=response_product_approve
        #     )
        # if 'yes' in response_product_approve:
        messages_product =  [
                {'role':'system',
                'content':f"""{product_message_prompt}"""},
                {'role':'user',
                'content':f"""Suggest me some food items because {message_from_user} also send me ingredients with their links to buy """},
                ]
        combined_response_product=""
        while True:
            response_product = get_completion_from_messages(messages_product, temperature=1)
                # Check if 'www.kisanwindow' is in the response
            print("product")
            if ('www.kisanwindow' in response_product or 'qtrove.com' in response_product or 'amazon' in response_product) and (len(response_product) <= 1300) :
                break  # Exit the loop if the condition is met

            # Split and combine the response if needed
            header_response_product="🌿🌼 *These are the herbal products we suggest for your path to wellness:* 🌱💚\n\n"
            response_product_splitted = split_string(response_product, chunk_size)
            combined_response_product = header_response_product + response_product_splitted[0]

            # Send the WhatsApp message
        message_product = client.messages.create(
                from_='whatsapp:+14155238886',
                to=f"whatsapp:{phone_no_from}",
                body=combined_response_product
            )
        # else:
        #     combined_response_product="User Gave a question irrelevant to our BOT"
        return combined_response_product

    def gist():
        gist =  [
            {'role':'system',
            'content':"""Answer within 20 words . Summarize the user problem """},
            {'role':'user',
            'content':f"""{message_from_user}"""},
            ]
        response_gist = get_completion_from_messages(gist,
                                                    temperature =1)

        return response_gist
    def update_database_and_sheet(user_message, doctor_response, product_response, response_message_segregation,
                              phone_no_from, profile_name, gist_response, message_count, sheet):
        Query = UserQuery.objects.create(
            user_message=user_message,
            doctor_response=doctor_response,
            product_response=product_response,
            response_message_segregation=response_message_segregation,
            phone_no_from=phone_no_from,
            profile_name=profile_name,
            gist=gist_response,
            message_count=message_count
        )
        Query.save()
        message_internal_id = Query.message_internal_id
        # Create UserGist object with conditional check
        UserGist.objects.create(
            phone_no_from=phone_no_from if phone_no_from else "None",
            gist=gist_response if gist_response else "None"
        )

        data = [
            message_internal_id,
            user_message,
            response_message_segregation,
            doctor_response,
            product_response,
            phone_no_from,
            profile_name,
            gist_response,
            message_count
        ]

        # Append data to the sheet
        request = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A1",  # Update this based on where you want to start appending data
            body={
                'values': [data]
            },
            valueInputOption="RAW"
        )
        response = request.execute()

    def pipeline():
        # Check if the phone number has sent messages before
        existing_query = UserQuery.objects.filter(phone_no_from=phone_no_from).first()

        # Prepare reply based on the existing query
        if existing_query:
            existing_query.message_count += 1
            message_count = existing_query.message_count
            existing_query.save()
        else:
            message_count=2
            reply = ("🎉 Heyyya! "+profile_name+", 🌟 Welcome to our Platform! 🎊\n"
                    "👋 We're *THRILLED* you're here!\n"
                    "💡 Ready to explore something AMAZING? We've got a universe of cool stuff just waiting for you. 🌌\n"
                    "👇 So what are you waiting for? Dive in and let's make some magic happen! 🎩\n"
                    "👉 What's troubling you today?📝")
            message_reply = client.messages.create(
                from_='whatsapp:+14155238886',
                to=f"whatsapp:{phone_no_from}",
                body=reply
            )

        messages_segregation =  [
            {'role':'system',
            'content':"""intention : "what user wants to do from the following category(respond in one word) : "is the user asking a query about is health ? then say "query"/(if want to know about platform or feels new user say = know)/"want to give feedback or exit or has finished with his questions say feedback/short(if less then 10 characters)""  """},
            {'role':'user',
            'content':f"""{message_from_user}"""},
            ]
        response_message_segregation = get_completion_from_messages(messages_segregation, temperature=1)
        print(response_message_segregation)
        if response_message_segregation.lower() == "know":
            intro()
            gist_response = gist()
            update_database_and_sheet(message_from_user, "None", "None", response_message_segregation,
                                    phone_no_from, profile_name, gist_response, message_count, sheet)
        elif (len(message_from_user) < 10) or response_message_segregation.lower() == "short":
            short_message()
            gist_response = gist()
            update_database_and_sheet(message_from_user, "None", "None", "short",
                                    phone_no_from, profile_name, gist_response, message_count, sheet)
        elif response_message_segregation.lower() == "query":
            processing()
            doctor_response = doctor()
            product_response = product()
            gist_response = gist()
            update_database_and_sheet(message_from_user, doctor_response, product_response, response_message_segregation,
                                    phone_no_from, profile_name, gist_response, message_count, sheet)
        elif response_message_segregation.lower() == "feedback":
            gist_response = gist()
            message_reply = client.messages.create(
            from_='whatsapp:+14155238886',
            to=f"whatsapp:{phone_no_from}",
            body="Thanks for using our Bot!"
            )
            update_database_and_sheet(message_from_user, "None", "None", response_message_segregation,
                                    phone_no_from, profile_name, gist_response, message_count, sheet)

    pipeline()

    return HttpResponse("Message sent")


