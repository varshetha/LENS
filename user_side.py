import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests 
import json


# Load the pickled Crop classifier model
crop_clf = joblib.load('crop_classifier.pkl')

def predict_crop(Nitrogen,Phosphorous,Pottassium,Temp,humd,ph,rain):
      df = pd.DataFrame([[Nitrogen,Phosphorous,Pottassium,Temp,humd,ph,rain]],columns = ['N','P','K','temperature','humidity','ph','rainfall'])
      prediction = crop_clf.predict(df)
      #print(prediction)
      return prediction[0]
 
    
def get_details_put_crop():
       Temp,humd = get_loc_weather_details()
       Nitrogen = st.slider("Nitrogen (mineral ratio in the soil)",0,140,45)
       Pottassium = st.slider("Pottassium(mineral ratio in the soil)",5,205,60)
       Phosphorous = st.slider("Phosphorous(mineral ratio in the soil)",5,145,40)
       temperature = st.number_input("temperature",8,43,25)
       humidity = st.number_input("humidity",14,99,54)
       pH = st.number_input("pH(1-14) ",4.5,7.8,6.0)
       rain = st.number_input("Rainfall( in cm)",50.0,250.0,100.0)
       
       result =""      
       if st.button("Predict"):
             result = predict_crop(Nitrogen,Phosphorous,Pottassium,Temp,humd,pH,rain)
             result = result.upper()
             st.success('The suitable crop is {}'.format(result)) 
   
  
def get_loc_weather_details():
      dist = np.array(['ARIYALUR', 'COIMBATORE', 'CUDDALORE', 'DHARMAPURI', 'DINDIGUL','ERODE', 'KANCHIPURAM', 'KANNIYAKUMARI', 'KARUR', 'KRISHNAGIRI','MADURAI', 'NAGAPATTINAM', 'NAMAKKAL', 'PERAMBALUR', 'PUDUKKOTTAI','RAMANATHAPURAM', 'SALEM', 'SIVAGANGA', 'THANJAVUR','THE NILGIRIS','THENI', 'THIRUVALLUR', 'THIRUVARUR','TIRUCHIRAPPALLI', 'TIRUNELVELI', 'TIRUPPUR', 'TIRUVANNAMALAI','TUTICORIN', 'VELLORE', 'VILLUPURAM', 'VIRUDHUNAGAR'])
      
      district = st.selectbox('Enter your District ',dist)
      
      BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
      API_KEY = "59cbb5204c83b27201407a412adecc6f"
      URL = BASE_URL + "q=" + district + "&appid=" + API_KEY
  
      # Request for weather information
      response = requests.get(URL)
      
      if response.status_code == 200:
            report = response.json()
            main = report['main']
            main_df = pd.DataFrame.from_dict(pd.json_normalize(main), orient='columns')  
      else:
            print("cannot access weather api")
            return
          
      temper = main_df['temp'].values
      humd = main_df['humidity'].values
      
      return temper[0],humd[0] 
      

def main():
      
      # giving the webpage a title
      st.title("CROP CLASSIFICATION")
      get_details_put_crop()
   
    
if __name__=='__main__':
      main()

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://c4.wallpaperflare.com/wallpaper/805/538/482/sunset-4k-download-hd-wallpaper-preview.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 






