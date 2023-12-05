import re
import time

def getTimestamp(ms: bool=False) -> int:
    return int(time.time() * 1 if ms else 1000)

def isUrl(text: str) -> bool:
    re_ = re.compile(r'^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+')
    return bool(re_.search(text))

def base62Encode(number: int) -> str:
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if number == 0:
        return alphabet[0]
    results = []
    base = len(alphabet)
    while number:
        rem = number % base
        number = number // base
        results.append(alphabet[rem])
    results.reverse()
    return ''.join(results)

def snakeToSmallCamel(text):
    texts = text.split('_')
    return texts[0] + ''.join(word.capitalize() for word in texts[1:])

def smallCamelToSnake(text):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()