# Import necessary modules
import json
import streamlit as st
from process_module import process
from output_module import output
from speak_module import speak
from remainder import set_reminder_with_alarm, note
import welcome
import webbrowser
import os
from web_jobs import games
import requests

# Initialize session state to store chat history and speaking status
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'is_speaking' not in st.session_state:
    st.session_state.is_speaking = True  # Default is speaking enabled

if 'speak_called' not in st.session_state:
    st.session_state.speak_called = False  # Initialize speak_called attribute

# Welcome message
welcome.greet()
os.system("cls")

# Display logo and title in the center
col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.title("LUFFY AI")

with col3:
    st.write(' ')

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image("pic of luffy logo.png", width=150)
with col3:
    st.write(' ')

# Load JSON file
try:
    file = json.load(open("luffy_dataset.json", encoding="utf-8"))
except FileNotFoundError:
    st.error("Unable to load JSON file.")
    st.stop()  # Stop further execution if file not found
except json.JSONDecodeError:
    st.error("Invalid JSON format.")
    st.stop()  # Stop further execution if JSON is invalid

# Function to process user input and manage speaking status
def process_user_input(user_input):
    # Add user input to chat history
    st.session_state.chat_history.append("You: " + user_input)

    # Display chat history
    for item in st.session_state.chat_history:
        st.write(item)

    for intent in file.get('intents', []):
        patterns = intent.get('patterns', [])
        responses = intent.get('responses', [])
        if user_input in patterns:
            for response in responses:
                st.session_state.chat_history.append("LUFFY AI: " + response)
                st.write("LUFFY AI: " + response)  # Display AI response
                if st.session_state.is_speaking:
                    speak(response)  # Speak AI response
            return True  # Exit the function once a match is found

    if user_input.lower() == "stop speaking":
        st.session_state.is_speaking = False
        st.write("You: " + user_input)  # Display user input
        # speak("Ok, I wont speak now")  # Speak confirmation message
        st.session_state.chat_history.append("LUFFY AI: Ok, I wont speak now")  # Add AI response to chat history
        st.write("LUFFY AI: Ok, I wont speak now")  # Display AI response
        return True

    if user_input.lower() == "start speaking":
        st.session_state.is_speaking = True
        st.session_state.chat_history.append("You: " + user_input)  # Add user input to chat history
        st.write("You: " + user_input)  # Display user input
        speak("Ok, I will speak now")  # Speak confirmation message
        st.session_state.chat_history.append("LUFFY AI: Ok, I will speak now")  # Add AI response to chat history
        st.write("LUFFY AI: Ok, I will speak now")  # Display AI response
        return True

    elif user_input.lower() == "cancel pizza":
        # Clear the pizza order details
        st.session_state.pop("order_details", None)
        st.info("Your pizza order has been cancelled.")
        return True

    elif user_input.lower() == "order a pizza":
        # Display pizza ordering form
        st.subheader("Pizza Ordering")
        pizza_type = st.radio("Select Pizza Type", ["Vegetarian", "Non-Vegetarian"])
        pizza_size = st.selectbox("Select Pizza Size", ["Small", "Medium", "Large"])
        toppings = st.text_input("Enter Toppings (comma-separated)")
        delivery_address = st.text_input("Enter Delivery Address")
        contact_number = st.text_input("Enter Contact Number")

        if st.button("Place Order"):
            # Validate inputs
            if not (pizza_type and pizza_size and delivery_address and contact_number):
                st.error("Please fill in all required fields.")
                return False

            # Simulate pizza ordering
            order_details = {
                "Pizza Type": pizza_type,
                "Pizza Size": pizza_size,
                "Toppings": toppings,
                "Delivery Address": delivery_address,
                "Contact Number": contact_number
            }
            st.session_state.order_details = order_details  # Store order details in session state
            st.success("Your pizza order has been successfully placed!")
            st.write("Order Details:")
            st.json(order_details)
            return True

    elif user_input.lower().startswith("remind me"):
        try:
            # Extract reminder text and time
            parts = user_input.split("at")
            if len(parts) == 2:
                reminder_text = parts[0].replace("Remind me", "").strip()
                reminder_time_str = parts[1].strip()
                # Set the reminder
                reminder = set_reminder_with_alarm(reminder_text, reminder_time_str)
                speak("OK, I was remained you ,Enjoy your task")
                if reminder:
                    st.session_state.chat_history.append(f"LUFFY AI: Reminder set: {reminder_text} at {reminder['time']}")
                    st.write("OK, I was remained you ,Enjoy your task")  # Display AI response
                else:
                    st.session_state.chat_history.append("LUFFY AI: Invalid reminder format. Please use format: 'Remind me [text] at [YYYY-MM-DD HH:MM:SS]'")
                    st.write("LUFFY AI: Invalid reminder format. Please use format: 'Remind me [text] at [YYYY-MM-DD HH:MM:SS]'")  # Display AI response
            else:
                raise ValueError
        except ValueError:
            st.session_state.chat_history.append("LUFFY AI: Invalid reminder format. Please use format: 'Remind me [text] at [YYYY-MM-DD HH:MM:SS]'")
            st.write("LUFFY AI: Invalid reminder format. Please use format: 'Remind me [text] at [YYYY-MM-DD HH:MM:SS]'")  # Display AI response
        return True

    elif "make a note" in user_input.lower():
        note_text = st.text_input("What would you like to write down?")
        if note_text:
            note(note_text)
            st.session_state.chat_history.append("LUFFY AI: Note saved successfully.")
            st.write("LUFFY AI: Note saved successfully.")  # Display AI response
            if st.session_state.is_speaking:
                speak("Note saved successfully.")  # Speak AI response
        else:
            st.session_state.chat_history.append("LUFFY AI: Note text is empty.")
            st.write("LUFFY AI: Note text is empty. PLease fill it")  # Display AI response
            if st.session_state.is_speaking:
                speak("Note text is empty. PLease fill it")  # Speak AI response
        return True

    elif user_input.startswith("where is"):
        # Extract the location from the user input
        location = user_input.split("where is")[1].strip()
        url = "https://www.google.com/maps/place/" + location.replace(" ", "+")
        webbrowser.open(url)
        st.write("Showing location on Google Maps...")
        speak("LUFFY AI: Showing location on Google Maps...")
        return True

    # elif user_input == "i want to play games" or "play games" or "play game" or "open game":
    #     games()
    #     return "enjoy your games"

    else:
        # Process user input using custom logic or external modules
        user_output = process(user_input)
        if user_output:
            st.session_state.chat_history.append("LUFFY AI: " + output(user_output))
            st.write("LUFFY AI: " + output(user_output))  # Display AI response
            if st.session_state.is_speaking:
                speak(output(user_output))  # Speak AI response
            return True

    return False

# Create a text input box for user input
user_input = st.text_input("Type your message here...")

# Process user input
if user_input and process_user_input(user_input):
    user_input = ""  # Clear the input field after processing
