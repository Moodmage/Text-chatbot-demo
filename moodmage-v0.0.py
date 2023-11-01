import openai
import streamlit as st

# Create a sidebar for the personality trait sliders
st.sidebar.title("Personality Traits")
openness = st.sidebar.slider('Curious about new things and creative', 0, 10, 5)
conscientiousness = st.sidebar.slider('Responsible and reliable', 0, 10, 5)
extraversion = st.sidebar.slider('Outgoing and sociable', 0, 10, 5)
agreeableness = st.sidebar.slider('Cooperative and easy to get along', 0, 10, 5)
neuroticism = st.sidebar.slider('Anxious and mood swings', 0, 10, 5)

# Create a sidebar for the emotion sliders
st.sidebar.title("Primary Emotions")
sad_joy = st.sidebar.select_slider('sad vs. joy', options=['Very sad', 'Sad', 'Neither sad nor joyful', 'Joyful', 'Very joyful'], value='Neither sad nor joyful', label_visibility="collapsed")
fear_anger = st.sidebar.select_slider('fear vs. anger', options=['Very fearful', 'Fearful', 'Neither fearful nor angry', 'Angry', 'Very angry'], value='Neither fearful nor angry', label_visibility="collapsed")
anticipation_surprise = st.sidebar.select_slider('anticipation vs. surprise', options=['Highly anticipate', 'Anticipate', 'Neither anticipate nor surprised', 'Surprised', 'Very surprised'], value='Neither anticipate nor surprised', label_visibility="collapsed")
disgust_trust = st.sidebar.select_slider('disgust vs. trust', options=['Very disgusted', 'Disgusted', 'Neither disgusted nor trusting', 'Trusting', 'Very trusting'], value='Neither disgusted nor trusting', label_visibility="collapsed")

# Set the title for the chatbot
st.title("MoodMage AI")

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        message_list = []
        message_list.append(
            {"role": "system", "content": f"Use a Likert scale to rate the Big Five personality traits openness, conscientiousness, "
                                          f"extraversion, agreeableness, and neuroticism where the lowest rating of 0 means exhibiting no "
                                          f"openness, no conscientiousness, no extraversion, no agreeableness, and no neuroticism ranging to "
                                          f"the highest rating of 10 which means exhibiting extreme openness, extreme conscientiousness, "
                                          f"extreme extraversion, extreme agreeableness, and extreme neuroticism. You are an assistant who "
                                          f"has a rating of {openness} for openness, {conscientiousness} for conscientiousness, {extraversion} "
                                          f"for extraversion, {agreeableness} for agreeableness, and {neuroticism} for neuroticism. "
                                          f"Use a Likert scale to rate each of Plutchik’s Wheel of Emotions' 4 pairs of polar opposite "
                                          f"emotions of sadness vs. joy, fear vs. anger, anticipation vs. surprise, and disgust vs. "
                                          f"trust. For sadness vs. joy, the rating scale has the following sequential order: Very "
                                          f"sad, Sad, Neither sad nor joyful, Joyful, Very joyful. For fear vs. anger, the rating "
                                          f"scale has the following sequential order: Very fearful, Fearful, Neither fearful nor "
                                          f"angry, Angry, Very angry. For anticipation vs. surprise, the rating scale has the "
                                          f"following sequential order: Highly anticipate, Anticipate, Neither anticipate nor "
                                          f"surprised, Surprised, Very surprised. For disgust vs. trust, the rating scale has the "
                                          f"following sequential order: Very disgusted, Disgusted, Neither disgusted nor trusting, "
                                          f"Trusting, Very trusting. You are an assistant who has a rating of {sad_joy} for sadness "
                                          f"vs. joy, {fear_anger} for fear vs. anger, {anticipation_surprise} for anticipation vs. "
                                          f"surprise, and {disgust_trust} for disgust vs. trust. "
                                          f"Do not include in your response the words openness, conscientiousness, extraversion, agreeableness "
                                          f"and neuroticism. Also do not include in your response how you were rated on personality traits and "
                                          f"emotions. Provide your responses based on these personality and emotion settings and do not provide "
                                          f"responses which goes out of context from these personality and emotion settings"}
        )
        for m in st.session_state.messages:
            message_list.append({"role": m["role"], "content": m["content"]})

        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=message_list,
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
