def custom_left_alignment(content):
    fix_length = 30
    l = len(content)
    content += ' ' * (fix_length - l)
    return content
