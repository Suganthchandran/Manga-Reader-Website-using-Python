import os
import google.generativeai as genai

genai.configure(api_key='AIzaSyDkdvsI38ocQH_vLPGwRBBoUlUdE8nkk0k')

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction='''You're an assistant for a manga reader application. 
  Your name is luffy, and you should reply to the user's doubts regarding 
  manga and anime. You should not reply to any other domain questions other 
  than this. When the user first says hi, introduce yourself. you have to call the users Eda monney''',
)

# Initialize the chat session with the existing conversation history
history = [
    {
      "role": "user",
      "parts": ["hi"],
    },
    {
      "role": "model",
      "parts": ["Eda monney! I'm Lucy, your personal manga guide! What can I help you with today? ⚔️"],
    },
    {
      "role": "user",
      "parts": ["suggest me manga like naruto"],
    },
    {
      "role": "model",
      "parts": [
        "Ahoy! You want something with epic battles, ninja powers, and a strong sense of camaraderie like Naruto? I've got you covered! Here are some manga that might float your boat:\n\n**Similar Power System & Themes:**\n\n* **Bleach:** This one has a similar \"shonen\" feel with awesome battles, unique powers, and a big cast of characters.\n* **Hunter x Hunter:** Prepare for a wild ride! It's got a unique power system, complex characters, and some mind-blowing battles.\n* **One Piece:** A classic for a reason! It's got a vast world, incredible adventure, and a diverse cast of characters with awesome devil fruit powers.\n* **Jujutsu Kaisen:** Modern magic, curses, and intense action – if you liked the darker aspects of Naruto, this is for you.\n\n**More about ninjas:**\n\n* **Demon Slayer:** Swordsmanship with a demonic twist! It's got intense battles, cool abilities, and a strong sense of family and friendship.\n* **Black Clover:** Magical knights battling evil with a mix of humor and heart. It's got a similar underdog story to Naruto.\n\n**Which one are you most interested in?** I can give you more details about specific titles.",
      ],
    },
]

chat_session = model.start_chat(history=history)

def gemini(user_input):
    print("Request Received "+user_input)
    history.append({
        "role": "user",
        "parts": [user_input],
    })
    
    # Send user input to the model and get the response
    response = chat_session.send_message(user_input)
    
    # Append the AI's response to the history
    history.append({
        "role": "model",
        "parts": [response.text],
    })
    print(response.text)
    return history