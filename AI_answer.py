import ollama

def ai_answer(transcript, question):
    if not transcript:
        return "I don't have a transcript to read yet!"
        
    prompt = f"""
    You are an expert assistant. Below is a transcript of a YouTube video. 
    Please answer the user's question based ONLY on the information provided in the transcript.
    
    TRANSCRIPT:
    {transcript}
    
    QUESTION:
    {question}
    """
    
    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': prompt}
    ])
    
    return response['message']['content']