from time import sleep

from yt.channel import *
from yt.helpers import *
from yt.user import *

ROOT_DIR = os.path.abspath(os.curdir)

if __name__ == '__main__':
    print("** Hola Hey, Azzrael_YT subs!!!\n")

    # Test main branch
    # r = get_channel_info("UCf6kozNejHoQuFhBDB8cfxA")
    r = get_current_user_info()
    print(json.dumps(r))