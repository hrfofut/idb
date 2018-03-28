def unbinary(s):
    """Removes the first two characters and the last character of a string, then adds necessary info for browser to see b64 image.
    Useful because encoding a binary to b64 adds "b'" to the front and "'" to the back.
    """
    return 'data:image/jpeg;base64,' + s[2:-1]
