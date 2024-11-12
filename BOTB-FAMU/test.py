# Create an API AI Connection and prompt
import google.generativeai as genai
import streamlit as st
import csv
from PIL import Image

genai.configure(api_key='AIzaSyAHCPq-zDiT4bTRKBxCzhyFUbASoaCDixU')
model = genai.GenerativeModel('gemini-pro')

# st.dataframe = open('BOTB-FAMU/data/ftn_charting_2022.csv', 'r')
# file_data = file.read()
# type(file)
# csvreader = csv.reader(file)

# def dataAnaly():
#     file = open("qbr_season_level.csv, "r") as stats:
            
pic = st.file_uploader("Enter Image")
img = Image.open(pic)
outP = model.generate_content(["Analyze this dataset and make a choice of 4 plays to run next:", img])
outP.resolve()
st.write(outP.text)
