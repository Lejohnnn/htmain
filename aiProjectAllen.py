from io import BytesIO
from tkinter import Image
import google.generativeai as genai
from google.generativeai import types
import os
from fpdf import FPDF
import unicodedata

# gemini set up
api_key = 'AIzaSyCABHwlFwU8hzb3A8FsVuyh6rfgF1GYQDY'
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')




# function to create a PDF itinerary
# TO_DO: 
# ----- add pdf saving functionality
# ----- space out print statements
def checkCandidates(response):
    if not response.candidates:
        return "Error: No candidates found in the response."

    first_candidate = response.candidates[0]
    if not first_candidate.content:
        return "Error: No content found in the response candidate."

    parts = first_candidate.content.parts
    if not parts:
        return "Error: No text parts found in the response."

    filteredResponse = "".join([part.text for part in parts])
    filteredResponse = unicodedata.normalize('NFKD', filteredResponse).encode('ascii', 'ignore').decode('ascii')

    return filteredResponse


def saveItineraryToPDF(itinerary_text, destination, travel_dates):
    # create downloadable PDF
    itinerarypdf = FPDF()
    itinerarypdf.add_page()
    itinerarypdf.set_font("Arial", size=12)

    itinerarypdf.cell(200, 10, txt="Your Trip Itinerary", ln=True, align='C')
    itinerarypdf.cell(200, 10, txt=f"Destination: {destination}", ln=True)
    itinerarypdf.cell(200, 10, txt=f"Travel Dates: {travel_dates}", ln=True)
    itinerarypdf.multi_cell(0, 10, txt=itinerary_text)

    itinerarypdf.output("itinerary.pdf")
    print("Your itinerary has been saved as 'itinerary.pdf'.")

def createItinerary():
    print("Great! Let's start planning your trip.")
    destination = input("Where would you like to go? ")
    print(f"Awesome! You are going to {destination}.")

    travel_dates = input("What are your travel dates? ")
    activities = input("What activities are you interested in? (e.g., sightseeing, adventure, relaxation) ")
    
    # generate itinerary using Gemini
    prompt = f"Create a detailed itinerary for a trip to {destination} from {travel_dates} with activities like {activities}."
    try:
        response = model.generate_content(prompt)

        if not response.candidates:
            return "Error: No candidates found in the response."

        first_candidate = response.candidates[0]
        if not first_candidate.content:
            return "Error: No content found in the response candidate."

        parts = first_candidate.content.parts
        if not parts:
            return "Error: No text parts found in the response."

        itinerary_text = "".join([part.text for part in parts])
        itinerary_text = unicodedata.normalize('NFKD', itinerary_text).encode('ascii', 'ignore').decode('ascii')

        return itinerary_text, destination, travel_dates
    except Exception as e:
        return f"Error generating itinerary: {e}", None, None

def getTravelRecommendations():
    # TO_DO: Implement travel recommendations
    print("To get travel recommendations, please provide your ideal destination and interests.")
    destination = input("What is your ideal destination(if none put 'Any') ? ")
    interests = input("What are your interests? (e.g., culture, adventure, food) ")
    # generate recommendations using Gemini
    prompt = f"Provide travel recommendations for {destination} with interests in {interests}."
    try:
        response = model.generate_content(prompt)

        if not response.candidates:
            return "Error: No candidates found in the response."

        first_candidate = response.candidates[0]
        if not first_candidate.content:
            return "Error: No content found in the response candidate."

        parts = first_candidate.content.parts
        if not parts:
            return "Error: No text parts found in the response."

        recommendations_text = "".join([part.text for part in parts])
        recommendations_text = unicodedata.normalize('NFKD', recommendations_text).encode('ascii', 'ignore').decode('ascii')

        print(f"Here are your travel recommendations:\n{recommendations_text}")
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return None

def findLocalAttractions(): 
    # TO_DO: Implement local attractions
    print("To find local attractions, please provide your destination or Zip-Code.")
    destination = input("What is your destination/Zip? ")
    # generate local attractions using Gemini
    prompt = f"Find local attractions in {destination}."
    try:
        response = model.generate_content(prompt)

        if not response.candidates:
            return "Error: No candidates found in the response."

        first_candidate = response.candidates[0]
        if not first_candidate.content:
            return "Error: No content found in the response candidate."

        parts = first_candidate.content.parts
        if not parts:
            return "Error: No text parts found in the response."

        attractions_text = "".join([part.text for part in parts])
        attractions_text = unicodedata.normalize('NFKD', attractions_text).encode('ascii', 'ignore').decode('ascii')

        print(f"Here are some local attractions:\n{attractions_text}")
    except Exception as e:
        print(f"Error generating local attractions: {e}")
        return None

def chatbotMain():
    # TO_DO: Implement chatbot functionality
    print("Welcome to the travel assistant chatbot! How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        # generate response using Gemini
        prompt = f"User: {user_input}\nAssistant:"
        try:
            response = model.generate_content(prompt)

            chatbotResponse = checkCandidates(response)
            if not chatbotResponse:
                print("Error: No response generated.")
                continue

            print(f"Assistant: {chatbotResponse} \n Type 'quit' to exit the chat.")
        except Exception as e:
            print(f"Error generating response: {e}")




#chat intro
print("Welcome to your new favorite planning utility. My name is [blank] and I will be your travel assistant!")
username = input("Let's start by getting you name: ")
print(f"Hello {username}, I am excited to help you plan your next trip! \n")

# Ask user for input + menu

print("What would you like to do today? (e.g., plan a trip, get recommendations, etc.): ")
print("\n--- Menu ---")
print("1. Create Trip Itinerary")
print("2. Get Travel Recommendations")
print("3. Find Local Attractions")
print("4. General Q&A Bot")
print("0. Quit")

choice = int(input("Enter your choice: "))

if choice == 0:
    print("Thank you for using the travel assistant. Goodbye!")
    exit()
elif choice == 1:
    itinerary, destination, travel_dates = createItinerary()

    pdfChoice = input("Would you like to download your itinerary as a PDF? (yes(Y)/no): ").strip().lower()
    if pdfChoice == 'yes' or pdfChoice == 'Y':
        print("Saving your itinerary PDF...")
        saveItineraryToPDF(itinerary, destination, travel_dates)
    else:
        print(f"Here is your itinerary:\n{itinerary}")   
elif choice == 2:
    getTravelRecommendations()
elif choice == 3:   
    # TO_DO: Implement local attractions
    findLocalAttractions()
elif choice == 4:   
    chatbotMain()
# TO_DO:    

    


#user decision making






# MAKE LAYOUT FOR CODE
# COMEPLETE USRE INTER

# Push first ai response to the user

# Ask user for input
# Save user input

# Push user input to the ai

# possibly request export format (pics, pdf, etc)
# ----- utilize apis?

