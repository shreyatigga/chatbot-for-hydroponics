# from twilio.rest import Client
# import random
# account_sid = 'ACce8c67df3ad9eaad899e6f1ccaef264a'
# auth_token = 'c2a2968ee6c55f031069da476391f273'
# twilio_phone_number = '19033548083'
# user_phone_number = '+919059432169'

# # Generate random OTP
# otp = str(random.randint(1000, 9999))

# # Message content
# message_body = f'Your OTP is: {otp}'

# # Initialize Twilio client
# client = Client(account_sid, auth_token)

# # Send OTP via SMS
# message = client.messages.create(
#     body=message_body,
#     from_=twilio_phone_number,
#     to=user_phone_number
# )

# print("OTP sent successfully!")
import streamlit as st

number= st.text_input("enter your number")
if st.button("submit"):
    st.write(int(number))