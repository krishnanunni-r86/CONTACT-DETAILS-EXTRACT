
# Import required libraries
import whisper  # Speech-to-text
import spacy    # NLP
import re       # Regex for pattern matching
import phonenumbers  # Phone number parsing


# Transcribe audio file to text using Whisper
def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]



# Extract entities (name, address, email, phone, etc.) from text
def extract_entities(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = {"NAME": [], "GPE": [], "ADDRESS": [], "EMAIL": [], "PHONE": []}

    # Use spaCy NER for names, locations, and addresses
    for ent in doc.ents:
        # spaCy does not provide per-entity confidence, so we use a default value
        if ent.label_ == "PERSON":
            entities["NAME"].append({"value": ent.text, "confidence": 0.95})
        elif ent.label_ == "GPE":
            entities["GPE"].append({"value": ent.text, "confidence": 0.93})
        elif ent.label_ == "LOC":
            entities["ADDRESS"].append({"value": ent.text, "confidence": 0.90})

    # Regex for US street addresses (e.g., 327, Oak Meadow Drive, Austin, Texas, 78745)
    # Stop address extraction at email or phone number patterns
    address_pattern = r"\d{1,6}[,]? [\w .'-]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Trace|Way|Place|Pl|Terrace|Ter|Circle|Cir|Loop|Parkway|Pkwy|Highway|Hwy|Trail|Trl)?[\w .,'-]*?(?=,? [A-Za-z .'-]+,? [A-Za-z]{2,},? \d{5}(?:-\d{4})?)(?:,? [A-Za-z .'-]+,? [A-Za-z]{2,},? \d{5}(?:-\d{4})?)?"
    address_matches = re.findall(address_pattern, text, re.IGNORECASE)
    # Remove any address match that contains an email or phone number
    address_matches = [a for a in address_matches if not re.search(r"@|\bat\b|\d{3}[-.\s]\d{3}[-.\s]\d{4}|\(\d{3}\)\s*\d{3}[-.\s]\d{4}", a)]
    if not address_matches:
        # fallback: try to match up to city, state, zip, but stop at email/phone
        fallback_pattern = r"\d{1,6}[,]? [\w .'-]+,? [A-Za-z .'-]+,? [A-Za-z]{2,}(?:,? \d{5}(?:-\d{4})?)?"
        address_matches = re.findall(fallback_pattern, text, re.IGNORECASE)
        address_matches = [a for a in address_matches if not re.search(r"@|\bat\b|\d{3}[-.\s]\d{3}[-.\s]\d{4}|\(\d{3}\)\s*\d{3}[-.\s]\d{4}", a)]
    # Assign a default confidence for regex-matched addresses
    entities["ADDRESS"].extend([{"value": a.strip(" ,."), "confidence": 0.88} for a in address_matches])

    # Email regex: match username@domain.com or username at domain.com
    # Improved email regex: only match valid email patterns, not phrases like 'me at ...'
    # Match: username@domain.com or username at domain.com (with optional spaces), but only if username and domain are not common English words
    # Preprocess text: replace common spoken email patterns
    # Preprocess text: replace spoken email patterns
    # Robust spoken email normalization
    # Replace ' dot ' with '.' in likely email phrases
    email_text = re.sub(r"([a-zA-Z0-9_.+-]+)\s+at\s+([a-zA-Z0-9_.+-]+)\s+dot\s+([a-zA-Z]{2,})", r"\1@\2.\3", text)
    # Replace ' at ' with '@' only if followed by something that looks like a domain
    email_text = re.sub(r"([a-zA-Z0-9_.+-]+)\s+at\s+([a-zA-Z0-9_.+-]+\.[a-zA-Z]{2,})", r"\1@\2", email_text)
    # Remove trailing punctuation from email phrases
    email_text = re.sub(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z]{2,})[.,]", r"\1", email_text)
    # Attempt to reconstruct emails missing '@' (e.g., robinchavariyat-ahoo.com -> robinchavariyat@yahoo.com)
    email_text = re.sub(r"([a-zA-Z0-9_.+-]+)[- ]ahoo\.com", r"\1@yahoo.com", email_text)
    email_text = re.sub(r"([a-zA-Z0-9_.+-]+)[- ]gmail\.com", r"\1@gmail.com", email_text)
    email_text = re.sub(r"([a-zA-Z0-9_.+-]+)[- ]outlook\.com", r"\1@outlook.com", email_text)
    # Email regex: match username@domain.com
    email_matches = re.findall(r"\b([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9_.+-]+\.[a-zA-Z]{2,})\b", email_text)
    # Only keep emails where username is not 'me' and domain is a valid domain (contains at least one dot and is not just a name)
    normalized_emails = [f"{user}@{domain}" for user, domain in email_matches if user.lower() != "me" and domain.count('.') > 0]
    # Assign high confidence for regex-matched emails
    entities["EMAIL"].extend([{"value": e, "confidence": 0.99} for e in normalized_emails])

    # Normalize phone numbers: add country code if missing, remove extra spaces
    phone_text = re.sub(r"(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})", r"+1 \1-\2-\3", text)
    phone_numbers = set()
    for match in phonenumbers.PhoneNumberMatcher(phone_text, "US"):
        phone_number = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        phone_numbers.add(phone_number)
    # Only add phone numbers once, after deduplication
    entities["PHONE"] = [{"value": num, "confidence": 0.99} for num in sorted(phone_numbers)]

    return entities


# Example usage for testing the extract_entities function
if __name__ == "__main__":
    # Sample text containing a name, location, email, and phone number
    sample_text = "John Doe lives in New York. Contact him at john.doe@email.com or +1 555-123-4567."
    # Extract entities from the sample text
    result = extract_entities(sample_text)
    # Print the extracted entities
    print(result)
