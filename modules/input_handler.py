# Very preliminary user input sanitizer.
# This function only replaces whitespace with plus sign.
# The plus sign is used for Google location search.
def sanitize(input):
    return input.replace(' ','+')