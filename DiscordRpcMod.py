import inspect
import time

from . import rpc


CLIENT_ID = "1028309753035759757"


def get_RiftWizard():
    # Returns the RiftWizard.py module object 
    for f in inspect.stack()[::-1]:
        if "RiftWizard.py" in str(f):
            return inspect.getmodule(f[0])

    return inspect.getmodule(f[0])

RiftWizard = get_RiftWizard()
steam = RiftWizard.SteamAdapter

start_time = time.mktime(time.localtime())

rpc_obj = None


def init():
    global rpc_obj

    print("DiscordRpcMod by github.com/akintos")

    rpc_obj = rpc.DiscordIpcClient.for_platform(CLIENT_ID)
    print("Discord RPC connection successful.")

    # Hook orig_set_presence_menu
    orig_set_presence_menu = steam.set_presence_menu

    def set_presence_menu():
        orig_set_presence_menu()
        set_state("Main menu")

    steam.set_presence_menu = set_presence_menu
    
    # Hook set_presence_level
    orig_set_presence_level = steam.set_presence_level

    def set_presence_level(level):
        orig_set_presence_level(level)
        trial_name = RiftWizard.main_view.game.trial_name or "Normal game"
        set_state(f"Realm {level}", trial_name)

    steam.set_presence_level = set_presence_level
    
    # set_state("Main menu") # not required


def set_state(state, details=None):
    activity = {
            "state": state,
            # "details": "Flamefest",
            "timestamps": {
                "start": start_time
            },
            "assets": {
                "large_image": "default"
            }
    }
    if details:
        activity["details"] = details

    rpc_obj.set_activity(activity)

try:
    init()

except Exception as e:
    print(e)
    print("Failed to init Discord RPC")
