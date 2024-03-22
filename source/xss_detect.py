import re

def detectXSS(inputString):
    xss_patterns = [
        r'<script\b[^>]*>(.*?)</script>',
        r'<.*?on\w+=.*?>',
        r'<img\b[^>]*\s+src\s*=\s*(["\'])(.*?)\1',
        r'<a\b[^>]*\s+href\s*=\s*(["\'])(.*?)\1',
        r'\b(document\.cookie)\b',
    ]
    for pattern in xss_patterns:
        if re.search(pattern, inputString, re.IGNORECASE):
            return True
    return False
