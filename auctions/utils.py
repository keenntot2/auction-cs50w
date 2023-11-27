
# username string to asterisk (for privacy)
def secure_username(username):
    strlen = len(username)
    mid_chars = username[1:strlen-1]
    return username.replace(mid_chars, '*' * (strlen-2))