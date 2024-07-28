import re
import unicodedata
from typing import Dict, Any


def error_response(message: str, status_code: int) -> Dict[str, Any]:
    return {'message': message}, status_code


def sanitize_username(username: str) -> str:
    username = username.strip()
    username = username.replace(' ', '_')
    username = re.sub(r'[^\w\s-]', '', username)
    username = ''.join(c for c in unicodedata.normalize('NFD', username)
                       if unicodedata.category(c) != 'Mn')
    return username.lower()
