import re

# def extract_number_like_entities(text):
#     pattern = r"[+]?[\d\(\)\-\_\/\s]{5,}"  # Match sequences of digits and allowed symbols
#     matches = re.findall(pattern, text)
#     # Clean and filter matches: must contain at least 5 digits, and no letters
#     result = []
#     for m in matches:
#         print(m)
#         cleaned = m.strip()
#         if not re.search(r"[a-zA-Z]", cleaned):
#             digit_count = len(re.findall(r"\d", cleaned))
#             if digit_count >= 5:
#                 result.append(cleaned)
#     return result

# # Example
# text = "Contact us at +91 (512) 234/a754-2554 or (123) 456-7890. Avoid ABC123."
# print(extract_number_like_entities(text))

def extract_number_like_entities(text):
    pattern = r"(?:[+(\d])[\d\(\)\-\_\/\s]{4,}"  # At least 5 characters, starting with digit/(/+
    matches = re.findall(pattern, text)
    result = []
    for m in matches:
        print(m)
        cleaned = m.strip()
        if not re.search(r"[a-zA-Z]", cleaned):
            digit_count = len(re.findall(r"\d", cleaned))
            if digit_count >= 5:
                result.append(cleaned)
    return result

# Example
text = "Call +91 (512) 234/754-2554 or (123) 456-7890, not at  ABC123 or  hello."
print(extract_number_like_entities(text))
