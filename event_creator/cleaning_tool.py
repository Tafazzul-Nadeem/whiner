import re
import spacy

def clean_component(text, entity_map, code_counters):
    # Helper functions to clean the text
    def redact_entities(text, entity_map, code_counters):
        nlp = spacy.load("en_core_web_trf")  # Transformer-based
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG"]:
                code_word = ""
                if ent.label_ == "PERSON":
                    code_word = f"Name{code_counters['PERSON']}"
                    code_counters["PERSON"] += 1
                    entity_map["person"][code_word] = ent.text

                elif ent.label_ == "ORG":
                    code_word = f"Company{code_counters['ORG']}"
                    code_counters["ORG"] += 1
                    entity_map["company"][code_word] = ent.text
                text = text.replace(ent.text, code_word)
        return text, entity_map, code_counters

    def extract_number_like_entities(text, entity_map, code_counters):
        pattern = r"(?:[+(\d])[\d\(\)\-\_\/\s]{4,}"  # At least 5 characters, starting with digit/(/+
        matches = re.findall(pattern, text)
        for m in matches:
            cleaned = m.strip()
            if not re.search(r"[a-zA-Z]", cleaned):
                digit_count = len(re.findall(r"\d", cleaned))
                if digit_count >= 5:
                    code_word = f"Secret{code_counters['SECRET']}"
                    code_counters["SECRET"] += 1
                    text = text.replace(cleaned, code_word)    
                    entity_map["secret"][code_word] = cleaned            
        return text, entity_map, code_counters
        
    def extract_username_password(text, entity_map, code_counters):
    #         SENSITIVE_TERMS = [
    # "username", "user_id", "email", "password", "pass", "pwd", "pin", "otp",
    # "secret", "key", "auth_token", "access_token", "refresh_token", "session_id",
    # "api_key", "security_code", "verification_code", "credit_card", "card_number",
    # "cvv", "iban", "ifsc", "account_number", "upi_id", "wallet_id", "transaction_id",
    # "phone", "mobile", "contact", "ssn", "aadhaar", "pan", "dob", "address",
    # "login", "signin", "credential", "security_answer", "security_question",
    # "reset_link", "recovery_code", "mfa_code", "2fa_token"
    # ]        
        SENSITIVE_TERMS = ["username", "password"]
        lines = text.splitlines()
        redacted_lines = []

        for line in lines:
            redacted = line
            # Match keyword (case-insensitive) and everything after it
            
            for keyword in SENSITIVE_TERMS:
                pattern = re.compile(rf"(?i)\b({re.escape(keyword)})\b\s*(.*)")
                match = pattern.search(redacted)
                if match:
                    sensitive_value = match.group(2).strip() if match.lastindex >= 2 else ""
                    code_word = f"Secret{code_counters['SECRET']}"
                    code_counters["SECRET"] += 1
                    redacted = redacted.replace(sensitive_value, f" {code_word}")
                    # redacted = pattern.sub(r"\1 " + code_word, redacted)
                    entity_map["secret"][code_word] = sensitive_value
            redacted_lines.append(redacted)

        return "\n".join(redacted_lines), entity_map, code_counters

    def remove_address(text, entity_map, code_counters):
        SENSITIVE_TERMS = ["address", "location", "residence"]

        lines = text.splitlines()
        redacted_lines = []
        skip_next = False

        for i in range(len(lines)):
            if skip_next:
                skip_next = False
                continue

            line = lines[i]
            redacted = line
            for keyword in SENSITIVE_TERMS:
                pattern = re.compile(rf"(?i)\b({re.escape(keyword)})\b(.*)")
                match = pattern.search(line)
                if match:
                    code_word = f"Secret{code_counters['SECRET']}"
                    code_counters["SECRET"] += 1

                    # Combine current and next line
                    next_line = lines[i + 1] if i + 1 < len(lines) else ""
                    secret_value = match.group(2) + "\n" + next_line
                    redacted = pattern.sub(r"\1 " + code_word, line)
                    entity_map["secret"][code_word] = secret_value.strip()

                    skip_next = True
                    break
            redacted_lines.append(redacted)
        return "\n".join(redacted_lines), entity_map, code_counters
    def clean_emailids(text, entity_map, code_counters):
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        matches = re.findall(email_pattern, text)
        for m in matches:
            code_word = f"Secret{code_counters['SECRET']}"
            code_counters["SECRET"] += 1
            text = text.replace(m, code_word)
            entity_map["secret"][code_word] = m
        return text, entity_map, code_counters
    
    def clean_weblinks(text, entity_map, code_counters):
        url_pattern = r"https?://[^\s]+"
        matches = re.findall(url_pattern, text)
        for m in matches:
            code_word = f"Secret{code_counters['SECRET']}"
            code_counters["SECRET"] += 1
            text = text.replace(m, code_word)
            entity_map["secret"][code_word] = m
        return text, entity_map, code_counters
    
    # Main cleaning process
    # Extract phone numbers
    text, entity_map, code_counters = extract_number_like_entities(text, entity_map, code_counters)
    # Redact entities like names and organizations
    text, entity_map, code_counters = redact_entities(text, entity_map, code_counters)
    # Extract usernames and passwords
    text, entity_map, code_counters = extract_username_password(text, entity_map, code_counters)
    # Remove addresses
    text, entity_map, code_counters = remove_address(text, entity_map, code_counters)
    # Clean email addresses
    text, entity_map, code_counters = clean_emailids(text, entity_map, code_counters)
    # Clean web links
    text, entity_map, code_counters = clean_weblinks(text, entity_map, code_counters)

    return text, entity_map, code_counters