import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import ollama
import AI_answer

st.set_page_config(page_title="YouTube Summarizer", page_icon="📺")
st.title("📺 Local AI YouTube Summarizer")
st.write("Powered by Llama 3.2 running entirely on my Mac")

# Get the YouTube URL from the user
video_url = st.text_input("Paste a YouTube URL here:")


mode = st.selectbox(
                    "Choose Summary Style:",
                    [" ","5-Bullet Summary", "Explain Like I'm 5 (ELI5)", "Extract Action Items", "List Key Quotes"]
                )

if 'transcript' not in st.session_state:
    st.session_state['transcript'] = None
if 'summary' not in st.session_state:
    st.session_state['summary'] = None
if 'video' not in st.session_state:
    st.session_state['video'] = None

if st.button("Summarize Video"):
    
    if video_url:
        if(mode==" "):
            st.warning("Please choose a summary style")
        else:
            st.session_state['video'] = video_url
            try:
                # Extract the Video ID from the URL
                if "v=" in video_url:
                    video_id = video_url.split("v=")[1].split("&")[0]
                else:
                    video_id = video_url.split("/")[-1].split("?")[0]
                
                # Fetch the transcript
                with st.spinner("Downloading transcript..."):
                    _api= YouTubeTranscriptApi()
                    transcript_list= _api.list(video_id)
                    
                    try:
                        transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB', 'en-CA', 'en-AU'])
                    except:
                        for t in transcript_list:
                            transcript = t.translate('en')
                            break
                    
                    transcript_data = transcript.fetch()
                    texts= []
                    for d in transcript_data:
                        texts.append(d.text)
                    transcript_text = " ".join(texts)
                
                # Ask local Llama 3.2 to summarize it
                with st.spinner("Llama 3.2 is reading the video and writing a summary..."):
                    prompt = f"Please read this video transcript and give me a {mode} based on the main ideas:\n\n{transcript_text}"

                    response = ollama.chat(model='llama3.2', messages=[
                        {'role': 'user', 'content': prompt}
                    ])
                    #store the transcript_text
                    st.session_state['transcript'] = transcript_text
                    st.session_state['summary'] = response['message']['content']
                
                                    
            except Exception as e:
                st.error(f"Something went wrong: {e}\n(Make sure the video has captions enabled!)")
    else:
        st.warning("Please enter a URL first!")

if st.session_state['video']:
    st.video(st.session_state['video'])
if st.session_state['summary']:
    st.success("Summary Complete!")
    st.write(st.session_state['summary'])


st.divider()
st.subheader("💬 Chat with the Video")
user_query = st.text_input("Ask a specific question about the content of video:")

if st.button("Get Answer"):
    if not user_query:
        st.warning("Please type a question first!")
    elif not st.session_state['transcript']:
        st.warning("Please summarize a video first so I have something to read!")
    else:
        with st.spinner("Llama 3.2 is searching the transcript..."):
            answer = AI_answer.ai_answer(st.session_state['transcript'], user_query)
            st.info(answer)
    