import re

expressions = \
    {
        'True':
            {
                r"\b(owo|uwu)\b",
                r"\b[oо0u🇴🇺]+[w🇼]+[oо0u🇴🇺]+\b",
                r"\b[oо0>u🇴🇺^]+[\s.,*_-`\\]*[w3🇼]+[\s,.*_-`\\]*[oо0^<u🇴🇺]\b"
            },
        'False':
            {
                r"(owo|uwu)",
                r"[oо0u🇴🇺]+[w🇼]+[oо0u🇴🇺]",
                r"[oо0>u🇴🇺^]+[\s.,*_-`\\]*[w3🇼]+[\s,.*_-`\\]*[oо0^<u🇴🇺]"
            }
    }

def __message_is_valid(message: str) -> bool:
    """Returns True if the message is valid.

    :param message: message to be evaluated
    :return: True if the message is valid
    """

    # Ignore empty messages
    if len(message) < 3 or message.isspace():
        return False

    return True

def fast_evaluate(message: str) -> bool:
    """Returns True if the message contains an OwO-like expression.

    Fast evaluate checks only if the message contains the exact
    characters 'owo' and 'uwu', and therefore is much less accurate
    than the normal evaluate function.

    :param message: message to be evaluated
    :return: True if the message contains an 'owo'-like expression
    """

    # Ignore empty messages
    if not __message_is_valid(message):
        return False

    if 'owo' in message.lower() or 'uwu' in message.lower():
        return True

    return False


def evaluate(message: str, word_boundaries: bool = False) -> bool:
    """Returns True if the message contains an OwO-like expression.

    :param word_boundaries: enable/disable boundary checks
    :param message: message to be evaluated
    :return: True if the message contains an 'owo'-like expression
    """

    # Ignore empty messages
    if not __message_is_valid:
        return False

    for expression in expressions[str(word_boundaries)]:
        if re.search(expression, message, re.IGNORECASE):
            return True

    return False
