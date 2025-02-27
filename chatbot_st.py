import streamlit as st
import time
import openai

# (Optional) If using OpenAI, set your API key:
# openai.api_key = "YOUR_API_KEY"

# 1) Set page config (optional), e.g. wide layout
st.set_page_config(layout="wide")

# 2) Create a container at the top to display chat messages
chat_container = st.container()

# 3) Inject custom CSS to pin an input bar at the bottom
st.markdown(
    """
    <style>
    /* A container fixed at bottom, spanning full width */
    #fixed-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 10px 0px 10px 0px;
        margin: 0;
        background-color: white;
        border-top: 1px solid #ccc;
        z-index: 9999;  /* ensure it's on top */
    }
    /* Make Streamlit main content area avoid overlapping the fixed container */
    /* This "padding-bottom" should match or exceed the container's height */
    .main .block-container {
        padding-bottom: 120px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 4) We’ll keep track of conversation in session_state if you like
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5) Define a function to simulate or call an actual LLM in streaming mode
def generate_llm_response_stream(prompt):
    """
    Example: yields partial output chunks for streaming.
    Replace with your real LLM streaming logic (OpenAI, etc.).
    """
    # Fake streaming: just break prompt into chunks
    # In a real scenario, you'd do something like:
    #   response = openai.Completion.create(..., stream=True)
    #   for chunk in response:
    #       yield chunk.choices[0].text
    for i in range(len(prompt)):
        time.sleep(0.02)  # simulate delay
        yield prompt[i]

# 6) Display all messages so far (above the fixed input)
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")

# 7) Create a placeholder for the LLM's *streaming* response
#    We'll fill this as we receive partial text
stream_placeholder = chat_container.empty()

# 8) Now define the fixed input UI via custom HTML container
st.markdown("<div id='fixed-input-container'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([6, 1, 1])  # Adjust ratio as needed

with col1:
    user_input = st.text_input("Enter your prompt", "", label_visibility="collapsed")
with col2:
    send_clicked = st.button("Send", type="primary")
with col3:
    clear_clicked = st.button("Clear")

st.markdown("</div>", unsafe_allow_html=True)

# 9) Handle button logic
if send_clicked and user_input.strip():
    # a) Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # b) "Stream" LLM response
    partial_response = ""
    for token in generate_llm_response_stream(f"Echo: {user_input}"):
        partial_response += token
        # Update the placeholder *live*
        stream_placeholder.markdown(f"**Assistant:** {partial_response}")

    # c) Append final LLM response to the chat
    st.session_state.messages.append({"role": "assistant", "content": partial_response})

    # d) Re-run the app so that messages appear in the normal chat layout
    st.experimental_rerun()

if clear_clicked:
    st.session_state.messages = []
    st.experimental_rerun()

st.markdown(
    """
    <div style="height: 200px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;" id="fixed-container">
    """,
    unsafe_allow_html=True
)

# Now place the empty placeholder inside that container
placeholder = st.empty()

# Close the fixed container div
st.markdown("</div>", unsafe_allow_html=True)
import streamlit as st
from html import escape

st.set_page_config(layout="wide")

st.title("Professional Chatbot UI Demo")

# ------------------------------------------------------------------------------
# 1) Inject custom CSS for chat container & message bubbles
# ------------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* The overall chat container: fixed height, scrollable, nice background */
    #chat-container {
        height: 400px;
        overflow-y: auto;
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 10px;
        margin-bottom: 20px; 
    }

    /* Common bubble styling: margin, padding, border-radius, etc. */
    .chat-bubble {
        max-width: 60%;
        padding: 10px 15px;
        margin-bottom: 10px;
        border-radius: 15px;
        font-family: sans-serif;
        line-height: 1.4;
    }

    /* User message bubble: align right, different color */
    .chat-bubble-user {
        background-color: #0084ff;
        color: white;
        margin-left: auto;  /* push it to the right */
    }

    /* Assistant message bubble: align left, different color */
    .chat-bubble-assistant {
        background-color: #e4e6eb;
        color: black;
        margin-right: auto; /* push it to the left */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------------------
# 2) Use session_state to store the conversation
# ------------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of dicts: {"role": "user"/"assistant", "content": "..."}

# ------------------------------------------------------------------------------
# 3) Show the chat container with current messages
#    We'll use st.markdown with HTML to display each message as a bubble.
# ------------------------------------------------------------------------------
# Opening the container div
st.markdown('<div id="chat-container">', unsafe_allow_html=True)

# Render each message in a bubble
for msg in st.session_state.messages:
    # Decide which bubble class to use
    if msg["role"] == "user":
        bubble_class = "chat-bubble chat-bubble-user"
    else:
        bubble_class = "chat-bubble chat-bubble-assistant"

    # Escape HTML special chars in content to avoid injection
    content = escape(msg["content"])

    # Build the bubble HTML
    bubble_html = f"""
    <div class="{bubble_class}">
        {content}
    </div>
    """
    st.markdown(bubble_html, unsafe_allow_html=True)

# Close the container div
st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 4) Input area for new user messages (like a chat input)
# ------------------------------------------------------------------------------
user_text = st.text_input("Your message", label_visibility="collapsed")

# A button to send the new message
if st.button("Send", type="primary"):
    if user_text.strip():
        # Append the new user message
        st.session_state.messages.append({"role": "user", "content": user_text.strip()})

        # Here you'd call your LLM. For demo, we just echo a placeholder.
        # LLM response:
        assistant_reply = f"I see you said: {user_text}"
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        
        # Rerun to refresh the chat display
        st.experimental_rerun()

