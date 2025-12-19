#!/usr/bin/env python3
"""
Password Strength Tester
Requirements emphasized:
- 15+ characters
- Unpredictable keystrokes (avoid common patterns/sequences)
- Prefer passphrases (multiple words / spaced or separated)
"""

import re
import math
from dataclasses import dataclass
from typing import List, Tuple


COMMON_PATTERNS = [
    "qwerty", "asdf", "zxcv", "password", "letmein", "admin",
    "iloveyou", "welcome", "login", "abc123", "monkey"
]

KEYBOARD_SEQUENCES = [
    "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "1234567890"
]


@dataclass
class CheckResult:
    score: int
    rating: str
    issues: List[str]
    tips: List[str]


def has_mixed_charsets(pw: str) -> Tuple[bool, List[str]]:
    """Check for character variety; returns (good_enough, missing_descriptions)."""
    missing = []
    if not re.search(r"[a-z]", pw):
        missing.append("lowercase letter")
    if not re.search(r"[A-Z]", pw):
        missing.append("uppercase letter")
    if not re.search(r"\d", pw):
        missing.append("number")
    if not re.search(r"[^\w\s]", pw):  # symbols (not letters/digits/_ or whitespace)
        missing.append("symbol")
    # Not a hard requirement here, but improves strength.
    good = len(missing) <= 1  # allow one missing type
    return good, missing


def looks_like_passphrase(pw: str) -> bool:
    """
    Passphrase heuristic:
    - contains spaces, OR
    - contains 3+ "word-like" chunks separated by - _ . or space
    """
    if " " in pw.strip():
        # two+ words separated by spaces
        words = [w for w in pw.strip().split() if w]
        return len(words) >= 3

    chunks = re.split(r"[-_.]+", pw.strip())
    chunks = [c for c in chunks if c]
    # treat alphabetic chunks as "words"
    wordish = [c for c in chunks if re.fullmatch(r"[A-Za-z]{3,}", c)]
    return len(wordish) >= 3


def contains_common_or_predictable(pw: str) -> List[str]:
    """Return a list of predictability warnings."""
    p = pw.lower()
    warnings = []

    # Common passwords/words
    for pat in COMMON_PATTERNS:
        if pat in p:
            warnings.append(f"Contains common pattern/word: '{pat}'")

    # Keyboard sequences forward/backward (qwerty/asdf/12345)
    for seq in KEYBOARD_SEQUENCES:
        for i in range(len(seq) - 3):
            sub = seq[i:i+4]
            if sub in p:
                warnings.append(f"Contains keyboard/number sequence: '{sub}'")
            if sub[::-1] in p:
                warnings.append(f"Contains reversed keyboard/number sequence: '{sub[::-1]}'")

    # Simple ascending/descending runs like 1234 or abcd
    if re.search(r"(0123|1234|2345|3456|4567|5678|6789)", p):
        warnings.append("Contains ascending number run (e.g., 1234)")
    if re.search(r"(abcd|bcde|cdef|defg|efgh|fghi|ghij|hijk|ijkl|jklm|klmn|lmno|mnop|nopq|opqr|pqrs|qrst|rstu|stuv|tuvw|uvwx|vwxy|wxyz)", p):
        warnings.append("Contains alphabetical sequence (e.g., abcd)")

    # Repeated characters (aaaa, !!!!) or repeating groups (ababab)
    if re.search(r"(.)\1\1\1", pw):
        warnings.append("Contains 4+ repeated characters in a row")
    if re.search(r"(.{2,4})\1\1", p):
        warnings.append("Contains repeated patterns (e.g., abab, 1212, etc.)")

    return list(dict.fromkeys(warnings))  # de-duplicate, keep order


def estimate_entropy_bits(pw: str) -> float:
    """
    Very rough entropy estimate based on used character sets and length.
    This is a heuristic, not a guarantee.
    """
    pool = 0
    if re.search(r"[a-z]", pw):
        pool += 26
    if re.search(r"[A-Z]", pw):
        pool += 26
    if re.search(r"\d", pw):
        pool += 10
    if re.search(r"[^\w\s]", pw):
        pool += 32  # approximate symbol set
    if " " in pw:
        pool += 1  # space included
    pool = max(pool, 1)
    return len(pw) * math.log2(pool)


def rate_password(pw: str) -> CheckResult:
    issues = []
    tips = []
    score = 0

    # Length requirement (15+)
    if len(pw) >= 15:
        score += 35
    else:
        issues.append(f"Too short: {len(pw)} characters (need 15+).")
        tips.append("Use a 3–5 word passphrase to reach 15+ characters easily.")

    # Passphrase encouragement
    if looks_like_passphrase(pw):
        score += 20
    else:
        tips.append("Consider a passphrase (3+ words) using spaces or separators (e.g., hyphens).")

    # Character variety (not mandatory, but boosts strength)
    variety_good, missing = has_mixed_charsets(pw)
    if variety_good:
        score += 15
    else:
        # missing several types
        score += 5
        tips.append("Add more character variety (mix upper/lower, numbers, and symbols).")
        if missing:
            issues.append("Missing: " + ", ".join(missing) + ".")

    # Unpredictability / pattern checks
    warnings = contains_common_or_predictable(pw)
    if warnings:
        issues.extend(warnings)
        # penalize predictability
        score -= min(30, 10 * len(warnings))
        tips.append("Avoid keyboard patterns (qwerty/asdf), sequences (1234), and repeated chunks.")
    else:
        score += 20

    # Entropy heuristic bump
    entropy = estimate_entropy_bits(pw)
    if entropy >= 70:
        score += 10
    elif entropy >= 50:
        score += 5
    else:
        tips.append("Increase randomness: longer length + more varied characters helps.")

    # Clamp score
    score = max(0, min(100, score))

    if score >= 85:
        rating = "Strong"
    elif score >= 65:
        rating = "Moderate"
    else:
        rating = "Weak"

    return CheckResult(score=score, rating=rating, issues=issues, tips=tips)


def main() -> None:
    print("=== Password Strength Tester ===")
    pw = input("Enter a password/passphrase to test: ")

    result = rate_password(pw)

    print("\n--- Results ---")
    print(f"Rating: {result.rating}")
    print(f"Score:  {result.score}/100")

    if result.issues:
        print("\nIssues found:")
        for i, issue in enumerate(result.issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("\nIssues found: None ✅")

    if result.tips:
        print("\nTips to improve:")
        for i, tip in enumerate(result.tips, 1):
            print(f"  {i}. {tip}")

    print("\nNote: This tool uses heuristics and cannot guarantee real-world security.")


if __name__ == "__main__":
    main()
