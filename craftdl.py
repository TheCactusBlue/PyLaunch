import os
import json
import urllib
import urllib.request
import cactusgeneral
from zipfile import ZipFile, BadZipfile

class Profile:
    def __init__(self, data):
        self.data = data
        self.name = data["name"]
        self.version = data["lastVersionId"]
        self.libs = []
        self.fileIndex = [("minecraft/versions/%s/%s.json" % (self.version, self.version),
                           "http://s3.amazonaws.com/Minecraft.Download/versions/%s/%s.json" % (
                           self.version, self.version)),
                          ("minecraft/versions/%s/%s.jar" % (self.version, self.version),
                           "http://s3.amazonaws.com/Minecraft.Download/versions/%s/%s.jar" % (
                           self.version, self.version))
                          ]
        f = None
        try:
            f = open("minecraft/versions/%s/%s.json" % (self.version, self.version), "r")
        except IOError or FileNotFoundError:
            cactusgeneral.makeDir("minecraft/versions/%s" % self.version)
            self.downloadFile("minecraft/versions/%s/%s.json" % (self.version, self.version),
                              "http://s3.amazonaws.com/Minecraft.Download/versions/%s/%s.json" % (
                              self.version, self.version)
                              )
            f = open("minecraft/versions/%s/%s.json" % (self.version, self.version), "r")
        sdata = f.read()
        f.close()

        self.versionInfo = json.loads(sdata)
        self.mainClass = self.versionInfo["mainClass"]
        self.mcargs = self.versionInfo["minecraftArguments"]
        self.jar = "versions/%s/%s.jar" % (self.version, self.version)

        for libinfo in self.versionInfo["libraries"]:
            librep = libinfo.get("url", "https://libraries.minecraft.net/")
            name = libinfo["name"]
            package, name, version = name.split(":")
            relpath = package.replace(".", "/") + "/" + name + "/" + version + "/" + name + "-" + version + ".jar"
            self.fileIndex.append(("minecraft/libraries/" + relpath, librep + relpath))
            self.libs.append("libraries/" + relpath)

            if "natives" in libinfo and cactusgeneral.currentOS in libinfo["natives"]:
                cactusgeneral.makeDir("minecraft/natives")
                natstr = libinfo["natives"][cactusgeneral.currentOS].replace("${arch}", cactusgeneral.bits)
                relpath = package.replace(".", "/") + "/" + name + "/" + version + "/" + name + "-" + version + "-" + natstr + ".jar"
                libpath = "minecraft/libraries/" + relpath
                liburl = librep + relpath
                if not os.path.exists(libpath):
                    self.downloadFile(libpath, liburl)
                    print
                    ">Extract " + libpath
                    try:
                        zipfile = ZipFile(libpath, "r")
                        for name in zipfile.namelist():
                            if not (name.startswith("META-INF") or name.startswith(".")):
                                zipfile.extract(name, "minecraft/natives")
                        zipfile.close()
                    except BadZipfile:
                        print
                        "!!! BAD JAR/ZIP FILE !!!"
                        try:
                            os.remove(libpath)
                        except:
                            pass
        # Getting assets index
        assetsName = self.versionInfo.get("assets", "legacy")
        assetsIndexFile = "minecraft/assets/indexes/%s.json" % assetsName
        assetsIndexLink = "https://s3.amazonaws.com/Minecraft.Download/indexes/%s.json" % assetsName
        self.downloadFile(assetsIndexFile, assetsIndexLink)

        f = open(assetsIndexFile, "r")
        assetsData = json.loads(f.read())
        f.close()

        for key, value in assetsData["objects"].items():
            hash = value["hash"]
            pref = hash[:2]
            self.fileIndex.append((
                "minecraft/assets/objects/%s/%s" % (pref, hash),
                "http://resources.download.minecraft.net/%s/%s" % (pref, hash)
            ))

    # Downloading some stuff here :)
    def downloadMissingFiles(self):
        for filename, url in self.fileIndex:
            if not os.path.exists(filename):
                try:
                    self.downloadFile(filename, url)
                except:
                    pass

    def downloadFile(self, filename, url):
        print(">Downloading " + filename)
        dirname = filename.rsplit("/", 1)[0]
        cactusgeneral.makeDir(dirname)

        inf = urllib.request.urlopen(url)
        outf = open(filename, "wb")
        while 1:
            b = inf.read(1)
            if len(b) == 0:
                break
            else:
                outf.write(b)
        inf.close()
        outf.close()


launcherProfiles = {
    "selectedProfile": "N/A",
    "profiles": {}
}
# Reads launcherProfiles
try:
    f = open("minecraft/launcher_profiles.json", "r")
    launcherProfiles = json.loads(f.read())
    f.close()
except:
    pass
name = "pylaunch"
p = Profile(launcherProfiles["profiles"][name])  # Change PyLaunch
p.downloadMissingFiles()
