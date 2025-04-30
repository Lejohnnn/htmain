import streamlit as st
import google.generativeai as genai
from google.generativeai import types
from fpdf import FPDF
import unicodedata
from PIL import Image
from io import BytesIO
import os

# gemini set up
api_key = 'AIzaSyCABHwlFwU8hzb3A8FsVuyh6rfgF1GYQDY'
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to check and filter AI response
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

# Function to save itinerary to PDF
def saveItineraryToPDF(itinerary_text, destination, travel_dates):
    itinerarypdf = FPDF()
    itinerarypdf.add_page()
    itinerarypdf.set_font("Arial", size=12)

    itinerarypdf.cell(200, 10, txt="Your Trip Itinerary", ln=True, align='C')
    itinerarypdf.cell(200, 10, txt=f"Destination: {destination}", ln=True)
    itinerarypdf.cell(200, 10, txt=f"Travel Dates: {travel_dates}", ln=True)
    itinerarypdf.multi_cell(0, 10, txt=itinerary_text)

    pdf_path = "itinerary.pdf"
    itinerarypdf.output(pdf_path)
    return pdf_path

# Function to create trip itinerary
def createItinerary(destination, travel_dates, activities):
    prompt = f"Create a detailed itinerary for a trip to {destination} from {travel_dates} with activities like {activities}."
    try:
        response = model.generate_content(prompt)
        itinerary_text = checkCandidates(response)
        if not itinerary_text:
            return "Error: No response generated.", None

        return itinerary_text, None
    except Exception as e:
        return f"Error generating itinerary: {e}", None

# Function to get travel recommendations
def getTravelRecommendations(destination, interests):
    prompt = f"Provide travel recommendations for {destination} with interests in {interests}."
    try:
        response = model.generate_content(prompt)
        recommendations_text = checkCandidates(response)
        if not recommendations_text:
            return "Error: No response generated."

        return recommendations_text
    except Exception as e:
        return f"Error generating recommendations: {e}"

# Function to find local attractions
def findLocalAttractions(destination):
    prompt = f"Find local attractions in {destination}."
    try:
        response = model.generate_content(prompt)
        attractions_text = checkCandidates(response)
        if not attractions_text:
            return "Error: No response generated."

        return attractions_text
    except Exception as e:
        return f"Error generating local attractions: {e}"

# Streamlit UI
def main():
    st.title("AI Travel Assistant")
    st.sidebar.title("Menu")
    menu = st.sidebar.selectbox("Choose an option", ["Home", "Create Trip Itinerary", "Get Travel Recommendations", "Find Local Attractions", "Upload Image"])

    if menu == "Home":
        st.write("Welcome to the AI Travel Assistant! Use the menu to navigate through the options.")

    elif menu == "Create Trip Itinerary":
        st.header("Create Trip Itinerary")
        destination = st.text_input("Enter your destination:")
        travel_dates = st.text_input("Enter your travel dates:")
        activities = st.text_input("Enter activities you're interested in (e.g., sightseeing, adventure):")
        if st.button("Generate Itinerary"):
            if destination and travel_dates and activities:
                itinerary, error = createItinerary(destination, travel_dates, activities)
                if error:
                    st.error(error)
                else:
                    st.success("Itinerary generated successfully!")
                    st.text(itinerary)
                    if st.button("Download as PDF"):
                        pdf_path = saveItineraryToPDF(itinerary, destination, travel_dates)
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button(label="Download PDF", data=pdf_file, file_name="itinerary.pdf", mime="application/pdf")
            else:
                st.error("Please fill in all fields.")

    elif menu == "Get Travel Recommendations":
        st.header("Get Travel Recommendations")
        destination = st.text_input("Enter your ideal destination (or 'Any'):")
        interests = st.text_input("Enter your interests (e.g., culture, adventure, food):")
        if st.button("Get Recommendations"):
            if destination and interests:
                recommendations = getTravelRecommendations(destination, interests)
                st.text(recommendations)
            else:
                st.error("Please fill in all fields.")

    elif menu == "Find Local Attractions":
        st.header("Find Local Attractions")
        destination = st.text_input("Enter your destination or Zip-Code:")
        if st.button("Find Attractions"):
            if destination:
                attractions = findLocalAttractions(destination)
                st.text(attractions)
            else:
                st.error("Please enter a destination or Zip-Code.")

    elif menu == "Upload Image":
        st.header("Upload Image")
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                img = Image.open(uploaded_file)
                st.image(img, caption="Uploaded Image", use_column_width=True)
                st.success("Image uploaded successfully!")
                # Add functionality to analyze the image if needed
            except Exception as e:
                st.error(f"Error uploading image: {e}")


main()

