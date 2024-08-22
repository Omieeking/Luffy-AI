from database import get_name
import platform

name = get_name()

def os():
    if "Windows" in str(platform.uname()):
        return True
    else:
        return False
print(os())



# system_info = platform.uname()
#
# print(system_info)

