import whisper
import spacy
import re
import phonenumbers

def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]


def extract_entities(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = {"NAME": [], "GPE": [], "ADDRESS": [], "EMAIL": [], "PHONE": []}

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["NAME"].append(ent.text)
        elif ent.label_ == "GPE":
            entities["GPE"].append(ent.text)
        elif ent.label_ == "LOC":
            entities["ADDRESS"].append(ent.text)

    # Regex for US street addresses (e.g., 327, Elk Meadow Drive Austin, Texas, 78745)
    address_pattern = r"\d{1,6}[,]? [\w .'-]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Trace|Way|Place|Pl|Terrace|Ter|Circle|Cir|Loop|Parkway|Pkwy|Highway|Hwy|Trail|Trl)?[\w .,'-]*?\d{5}(?:-\d{4})?"
    address_matches = re.findall(address_pattern, text, re.IGNORECASE)
    if not address_matches:
        # fallback: try to match up to city, state, zip
        fallback_pattern = r"\d{1,6}[,]? [\w .'-]+,? [A-Za-z .'-]+,? [A-Za-z]{2,}(?:,? \d{5}(?:-\d{4})?)?"
        address_matches = re.findall(fallback_pattern, text, re.IGNORECASE)
    entities["ADDRESS"].extend([a.strip(" ,.") for a in address_matches])

    # Improved email regex: only match valid email patterns, including obfuscated ' at '
    # Match: username@domain.com or username at domain.com (with optional spaces)
    email_matches = re.findall(r"[\w\.-]+\s*(?:@|\s+at\s+)\s*[\w\.-]+\.[a-zA-Z]{2,}", text, re.IGNORECASE)
    # Normalize obfuscated emails (replace ' at ' with '@' and remove spaces)
    normalized_emails = [re.sub(r"\s*(?:@|\s+at\s+)\s*", "@", e.replace(" ", "")) for e in email_matches]
    entities["EMAIL"].extend(normalized_emails)

    for match in phonenumbers.PhoneNumberMatcher(text, "US"):
        phone_number = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        entities["PHONE"].append(phone_number)

    return entities

# Example usage for testing the extract_entities function
if __name__ == "__main__":
    # Sample text containing a name, location, email, and phone number
    sample_text = "John Doe lives in New York. Contact him at john.doe@email.com or +1 555-123-4567."
    # Extract entities from the sample text
    result = extract_entities(sample_text)
    # Print the extracted entities
    print(result)
