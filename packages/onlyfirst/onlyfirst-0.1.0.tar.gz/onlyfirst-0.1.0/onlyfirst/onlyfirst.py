
from unittest import expectedFailure


def handle_file():
    pass


def process_single(text: str) -> str:
    # remove space.
    inx = text.find('=')
    if inx == -1:
        raise Exception(f'{text} contains no `=`')
    if text.count('\n') > 2:
        raise Exception('too many \\n')
    return text[:inx+1]


def process_paragraph(text: str) -> str:
    res = []
    for short in text.split('\n'):
        short = short.strip()
        # skip empty
        if short:
            res.append(process_single(short))
    return "\n".join(res) + "\n"
