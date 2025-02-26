import streamlit as st
from PIL import Image
import io
import time

# Set page configuration
st.set_page_config(page_title="Chatbot with Image Support", layout="wide")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add custom CSS for better styling
st.markdown("""
<style>
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
}
.chat-message.user {
    background-color: #e6f7ff;
    border-left: 5px solid #1890ff;
}
.chat-message.bot {
    background-color: #f6f6f6;
    border-left: 5px solid #888888;
}
.chat-message img {
    max-width: 250px;
    border-radius: 0.3rem;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Display chat header
st.title("📱 Chatbot with Text & Image Support")
st.markdown("Type a message and/or upload an image to chat with the bot.")

# Display chat messages from history
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"<div class='chat-message user'><strong>You:</strong> {message['content']}</div>", unsafe_allow_html=True)
            if "image" in message:
                st.image(message["image"], width=250)
        else:
            st.markdown(f"<div class='chat-message bot'><strong>Bot:</strong> {message['content']}</div>", unsafe_allow_html=True)

# Chat input area
with st.container():
    col1, col2 = st.columns([5, 1])
    
    # Text input
    with col1:
        user_input = st.text_area("Your message:", key="input", height=100)
    
    # Image upload
    with col2:
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    
    # Send button
    if st.button("Send"):
        if user_input or uploaded_file:
            # Add user message to chat history
            user_message = {"role": "user", "content": user_input if user_input else ""}
            
            # Process uploaded image if any
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                # Convert to bytes for storage in session state
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format=image.format if image.format else 'PNG')
                user_message["image"] = img_byte_arr.getvalue()
            
            st.session_state.messages.append(user_message)
            
            # Simulate bot processing
            with st.spinner("Bot is thinking..."):
                time.sleep(1)  # Simulating processing time
            
            # Add bot response to chat history
            if uploaded_file and user_input:
                bot_response = f"I received your message and image. Your message was: '{user_input}'"
            elif uploaded_file:
                bot_response = "I received your image! What would you like to do with it?"
            else:
                bot_response = f"I received your message: '{user_input}'"
            
            st.session_state.messages.append({"role": "bot", "content": bot_response})
            
            # Rerun to update chat display
            st.experimental_rerun()

# Add a button to clear chat history
if st.button("Clear Conversation"):
    st.session_state.messages = []
    st.experimental_rerun()
