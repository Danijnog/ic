import tiktoken


def num_tokens_from_string(string, text_encoding) -> int:
    """
    Returns the number of tokens in a text string.
    """
    encoding = tiktoken.get_encoding(text_encoding)
    num_tokens = len(encoding.encode(string))

    return num_tokens


def truncate_text_tokens(text, text_encoding, max_tokens) -> list[int]:
    """
    Truncate a string to have `max_tokens` allowed by the embeddings API according to the given encoding.
    """
    encoding = tiktoken.get_encoding(text_encoding)

    return encoding.encode(text)[:max_tokens]


def truncate_text_tokens_decode(text, text_encoding, max_tokens) -> str:
    """
    Decode the string encoded.
    """
    encoding = tiktoken.get_encoding(text_encoding)

    return encoding.decode(encoding.encode(text)[:max_tokens])
