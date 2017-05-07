import os
import craftdl
import cactusgeneral
username=input("Your offline username:")
launcherProfiles = craftdl.launcherProfiles

name="pylaunch"
p = craftdl.Profile(launcherProfiles["profiles"][name])
os.system("cd minecraft && %s" % p.launchcmd(username))
