import re

def detectSQLi(inputString):
    sqli_patterns = [
        r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|TRUNCATE|OR|AND|UNION|JOIN)\b',
        r'\b(OR\s+\d+\s*\=\s*\d+)\b',
        r'\b(AND\s+\d+\s*\=\s*\d+)\b',
        r'\b(UNION\s+SELECT\s+\d+)\b',
        r'\b(SELECT\s+.*?\s+FROM\s+.*?WHERE\s+.*?=.*?\b)',
        
    ]
    for pattern in sqli_patterns:
        if re.search(pattern, inputString, re.IGNORECASE):
            return True
    return False
