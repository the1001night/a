import platform

def usystem():
    uos = platform.system()
    uver = platform.release()
    uname = platform.node()
    result = f"ОПЕРАЦИОННАЯ СИСТЕМА:\n\tИмя системы: {uos}\n\tВерсия системы: {uver}\n\tПользователь: {uname}\n\n"
    return result, uos