import re

def detectCommandInjection(inputString):
    cmd_injection_patterns = [
        r';\s*(?:ls|dir|pwd|rm|del|echo|cat|nc|netcat|wget|curl)\b',
        r'\|\s*(?:ls|dir|pwd|rm|del|echo|cat|nc|netcat|wget|curl)\b',
        r'&&\s*(?:ls|dir|pwd|rm|del|echo|cat|nc|netcat|wget|curl)\b',
        r'\$\(\s*(?:ls|dir|pwd|rm|del|echo|cat|nc|netcat|wget|curl)\s+(.*?)\s*\)',
        r'`(?:ls|dir|pwd|rm|del|echo|cat|nc|netcat|wget|curl)\s+([^`]*)`',
        r'\$\(\s*echo\s*(.*?)\s*\)\s*\|\s*(?:ls|dir|pwd|rm|del|echo|cat|nc|netcat|wget|curl)\b',
    ]

    for pattern in cmd_injection_patterns:
        if re.search(pattern, inputString, re.IGNORECASE):
            return True
    return False
