# Password Strength Tester (Python)

## Project Overview
This project is a Python-based password strength tester designed to evaluate whether a password meets modern security best practices. The script checks password length, unpredictability, and the use of passphrases to encourage stronger and more secure authentication.

## Password Requirements
A strong password in this project must:
- Be at least **15 characters long**
- Avoid predictable keystrokes and common patterns (e.g., `qwerty`, `1234`, repeated characters)
- Prefer **passphrases** using multiple words separated by spaces or symbols
- Use a mix of characters when possible (uppercase, lowercase, numbers, symbols)

## Features
- Length validation (15+ characters)
- Detection of common keyboard patterns and sequences
- Repeated character and pattern detection
- Passphrase recognition
- Password scoring system with feedback
- Clear strength rating: Weak, Moderate, or Strong

## How to Run the Script
1. Ensure Python 3 is installed on your system
2. Open the project folder in Visual Studio Code
3. Open a terminal in VS Code
4. Run the script using:
   ```bash
   python password_strength_tester.py
# Password-strength-tester
