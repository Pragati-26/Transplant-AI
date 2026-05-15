import json
from groq import Groq
from ..config import get_settings
from ..utils.errors import AIServiceError

settings = get_settings()

def _local_explanation(data: dict, ml_score: float) -> dict:
    """Fallback: generate explanation locally without any API."""
    pct = round(ml_score * 100, 1)

    if ml_score >= 0.75:   recommendation = "Excellent"
    elif ml_score >= 0.55: recommendation = "Good"
    elif ml_score >= 0.35: recommendation = "Moderate"
    else:                  recommendation = "Poor"

    def clean(b): return str(b).upper().replace('+','').replace('-','')
    abo_map = {
        ('O','O'):1,('O','A'):0,('O','B'):0,('O','AB'):0,
        ('A','A'):1,('A','AB'):1,('A','O'):0,('A','B'):0,
        ('B','B'):1,('B','AB'):1,('B','O'):0,('B','A'):0,
        ('AB','AB'):1,('AB','A'):0,('AB','B'):0,('AB','O'):0,
    }
    abo_ok  = abo_map.get((clean(data['donor_blood_type']), clean(data['patient_blood_type'])), 0)
    age_gap = abs(data['patient_age'] - data['donor_age'])

    blood_text  = f"Blood type compatibility is {'confirmed' if abo_ok else 'not confirmed'} ({data['donor_blood_type']} donor to {data['patient_blood_type']} patient)."
    age_text    = f"Age gap of {age_gap} years is {'acceptable' if age_gap <= 15 else 'a concern'}."
    health_text = f"Organ health score {data['health_score']}/10 with {data['survival_chance']}% predicted survival {'indicates strong viability' if data['health_score'] >= 7 else 'suggests moderate condition'}."

    return {
        "recommendation": recommendation,
        "explanation":    f"{blood_text} {age_text} {health_text}"
    }


def get_explanation(data: dict, ml_score: float) -> dict:
    pct = round(ml_score * 100, 1)

    prompt = f"""A kidney transplant ML model scored this donor-patient pair: {pct}% compatibility.

Patient: age {data['patient_age']}, weight {data['patient_weight']}kg, blood type {data['patient_blood_type']}
Donor:   age {data['donor_age']}, weight {data['donor_weight']}kg, blood type {data['donor_blood_type']}
Organ health score: {data['health_score']}/10
Biological markers: {data['biological_markers']}/10
Predicted survival chance: {data['survival_chance']}%

Respond ONLY with this JSON, no markdown, no extra text:
{{
  "recommendation": "<Excellent|Good|Moderate|Poor>",
  "explanation": "<3 sentence clinical explanation of key factors>"
}}"""

    # Try Groq first
    try:
        if not settings.groq_api_key:
            raise ValueError("No Groq API key set")

        print("Calling Groq API...")
        client   = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a clinical AI for kidney transplantation. Respond only with valid JSON, no markdown."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        raw    = response.choices[0].message.content.strip()
        raw    = raw.replace("```json","").replace("```","").strip()
        print(f"Groq response: {raw}")
        parsed = json.loads(raw)

        if "recommendation" not in parsed or "explanation" not in parsed:
            raise ValueError("Missing keys")

        return parsed

    except Exception as e:
        print(f"Groq failed ({type(e).__name__}: {e}) — using local fallback")
        return _local_explanation(data, ml_score)