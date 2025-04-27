import google.generativeai as genai
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# gemini set up
api_key = 'AIzaSyCABHwlFwU8hzb3A8FsVuyh6rfgF1GYQDY'
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')




# function to create a PDF itinerary
# TO_DO: 
# ----- add pdf saving functionality
# ----- space out print statements

def createItinerary():
    print("Great! Let's start planning your trip.")
    destination = input("Where would you like to go? ")
    print(f"Awesome! You are going to {destination}.")

    travel_dates = input("What are your travel dates? ")
    activities = input("What activities are you interested in? (e.g., sightseeing, adventure, relaxation) ")
    
    # generate itinerary using Gemini
    prompt = f"Create a detailed itinerary for a trip to {destination} from {travel_dates} with activities like {activities}."
    response = model.generate_content(prompt)
    itinerary = response
    return itinerary



#chat intro
print("Welcome to your new favorite planning utility. My name is [blank] and I will be your travel assistant!")
username = input("Let's start by getting you name: ")
print(f"Hello {username}, I am excited to help you plan your next trip!")

# Ask user for input + menu

print("What would you like to do today? (e.g., plan a trip, get recommendations, etc.): ")
print("\n--- Menu ---")
print("1. Create Trip Itinerary")
print("2. Get Travel Recommendations")
print("3. Find Local Attractions")
print("4. Book Flights")
print("0. Quit")

choice = int(input("Enter your choice: "))

if choice == 0:
    print("Thank you for using the travel assistant. Goodbye!")
    exit()
elif choice == 1:
    itinerary = createItinerary()
    printout = create_pdf(itinerary)
    print (f"Here is your itinerary:\n {printout}")


#user decision making






# MAKE LAYOUT FOR CODE
# COMEPLETE USRE INTER

# Push first ai response to the user

# Ask user for input
# Save user input

# Push user input to the ai

# possibly request export format (pics, pdf, etc)
# ----- utilize apis?

