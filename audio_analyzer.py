from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Add it to your environment or .env file.")

client = OpenAI(api_key=api_key)


# -----------------------------
# 🔹 Generic LLM Caller
# -----------------------------
def call_llm(prompt, temperature=0.3):
    try:
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# -----------------------------
# 1. Transcription Agent
# -----------------------------
def transcription_agent(audio_file):
    try:
        with open(audio_file, "rb") as f:
            result = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=f
            )
        return result.text
    except Exception as e:
        return f"Transcription Error: {str(e)}"


# -----------------------------
# 2. Agents (Using Shared LLM)
# -----------------------------
def summarizer_agent(text):
    return call_llm(f"Summarize clearly:\n\n{text}")


def sentiment_agent(text):
    return call_llm(f"""
    Give sentiment:
    - Sentiment (Positive/Negative/Neutral)
    - Reason

    Text:
    {text}
    """, temperature=0)


def insights_agent(text):
    return call_llm(f"""
    Extract:
    - Key points
    - Trends
    - Actionable insights

    Text:
    {text}
    """)

def translation_agent(text, target_language):
    return call_llm(f"""
    Translate the following text into {target_language}.
    Only return translated text. No explanation.

    Text:
    {text}
    """)

def combined_report_agent(transcript, summary, sentiment, insights):
    prompt = f"""
    Create a comprehensive AI analysis report based on the following inputs.

    -------------------------
    TRANSCRIPT:
    {transcript}

    SUMMARY:
    {summary}

    SENTIMENT:
    {sentiment}

    INSIGHTS:
    {insights}

    -------------------------

    Generate a structured report with:

    1. Title
    2. Executive Summary
    3. Detailed Summary
    4. Key Insights & Trends
    5. Sentiment Analysis
    6. Key Decisions / Actions
    7. Risks / Concerns
    8. Final Conclusion

    Make it professional and concise.
    """

    return call_llm(prompt)

# -----------------------------
# 3. Supervisor
# -----------------------------
def run_pipeline(audio_path,target_language):

    print("🎧 Transcribing...")
    transcript = transcription_agent(audio_path)

    print("🧠 Running agents...")

    summary = summarizer_agent(transcript)
    sentiment = sentiment_agent(transcript)
    insights = insights_agent(transcript)
    translation = translation_agent(transcript,target_language)
   

    print("📊 Creating combined report...")
    combined_report = combined_report_agent(
        transcript,
        summary,
        sentiment,
        insights
    )

    # Save outputs
    outputs = {
        "transcript.txt": transcript,
        "translation.txt": translation,
        "sentiment.txt": sentiment,
        "insights.txt": insights,
        "summary.txt": summary,
        "final_report.txt": combined_report,
       
    }

    for file, content in outputs.items():
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

    print("✅ All outputs saved (including final report)!")
    return outputs

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    run_pipeline("output.mp3")