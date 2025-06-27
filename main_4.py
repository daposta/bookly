def decipher(ciphertext, knownWord):
    # Preserve original case information
    original_case = []
    for char in ciphertext:
        original_case.append(char.isupper())
    
    # Work with lowercase versions for comparison
    ciphertext_lower = ciphertext.lower()
    knownWord_lower = knownWord.lower()
    
    # Try all possible Caesar cipher shifts
    for shift in range(26):
        decrypted = ""
        for char in ciphertext_lower:
            if char.isalpha():
                decoded = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                decrypted += decoded
            else:
                decrypted += char
        
        if knownWord_lower in decrypted:
            # Restore original case
            result = ""
            for i, char in enumerate(decrypted):
                if i < len(original_case) and char.isalpha() and original_case[i]:
                    result += char.upper()
                else:
                    result += char
            return result
    
    # Fallback: try pattern matching with words of same length
    cipher_words = ciphertext_lower.split()
    for cipher_word in cipher_words:
        if len(cipher_word) == len(knownWord_lower):
            shift = (ord(cipher_word[0]) - ord(knownWord_lower[0])) % 26
            valid_shift = True
            
            for i in range(len(knownWord_lower)):
                expected_cipher = chr((ord(knownWord_lower[i]) - ord('a') + shift) % 26 + ord('a'))
                if expected_cipher != cipher_word[i]:
                    valid_shift = False
                    break
            
            if valid_shift:
                result = ""
                for i, char in enumerate(ciphertext_lower):
                    if char.isalpha():
                        decoded_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                        # Restore original case
                        if i < len(original_case) and original_case[i]:
                            decoded_char = decoded_char.upper()
                        result += decoded_char
                    else:
                        result += char
                return result
    
    return ciphertext



# Test the function
ciphertext =  "Eqfkpi vguvu ctg hwp!" #"cdeb nqxg" #input().strip()
knownWord = "tests" #input().strip()
result = decipher(ciphertext, knownWord)
print(result)