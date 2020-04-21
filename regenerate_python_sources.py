import json
import urllib.request
import zipfile
import io
import os
import subprocess
import sys
import distutils.dir_util

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(ROOT_DIR, os.path.join("build", "download"))
RUNTIME_DIR = os.path.join(ROOT_DIR, os.path.join("3rdparty", "runtime"))
SRC_DIR = os.path.join(ROOT_DIR, "src")
JAVA = "java" 

def main():
    downloadZserio()
    compileZserio()

def downloadZserio():
    print("Downloading the latest Zserio release JSON file...", end = "")
    latestZserioReleaseUrl = urllib.request.urlopen("https://api.github.com/repos/ndsev/zserio/releases/latest")
    latestZserioReleaseJson = json.loads(latestZserioReleaseUrl.read().decode('utf-8'))
    latestZserioVersion = latestZserioReleaseJson["tag_name"]
    latestZserioBinZipUrl = latestZserioReleaseJson["assets"][0]["browser_download_url"]
    latestZserioRuntimeLibsZipUrl = latestZserioReleaseJson["assets"][1]["browser_download_url"]
    print("OK (found version " + latestZserioVersion + ")")

    print("Downloading the latest Zserio binaries...", end = "")
    latestZserioBinZip = urllib.request.urlopen(latestZserioBinZipUrl)
    print("OK")
    print("Extracting the latest Zserio binaries...", end = "")
    latestZserioBinZipFile = zipfile.ZipFile(io.BytesIO(latestZserioBinZip.read()), 'r')
    latestZserioBinZipFile.extractall(DOWNLOAD_DIR)
    print("OK")

    print("Downloading the latest Zserio runtime...", end = "")
    latestZserioRuntimeLibsZip = urllib.request.urlopen(latestZserioRuntimeLibsZipUrl)
    print("OK")
    print("Extracting the latest Zserio runtime...", end = "")
    latestZserioRuntimeLibsZipFile = zipfile.ZipFile(io.BytesIO(latestZserioRuntimeLibsZip.read()), 'r')
    latestZserioRuntimeLibsZipFile.extractall(DOWNLOAD_DIR)
    print("OK")
    
    print("Copying python runtime...", end = "")  
    downloadedRuntimeDir = os.path.join(DOWNLOAD_DIR, os.path.join("runtime_libs", "python"))
    distutils.dir_util.copy_tree(downloadedRuntimeDir, RUNTIME_DIR)
    print("OK")

def compileZserio():
    print("Compiling tutorial schema...", end = "")
    zserioLibsDir = os.path.join(DOWNLOAD_DIR, "zserio_libs")
    zserioCore = os.path.join(zserioLibsDir, "zserio_core.jar")
    zserioPython = os.path.join(zserioLibsDir, "zserio_python.jar")
    zserioCmd = [JAVA,
                 "-cp", os.pathsep.join([zserioCore, zserioPython]),
                 "zserio.tools.ZserioTool",
                 "-python", SRC_DIR,
                 "-src", ROOT_DIR,
                 "tutorial.zs"]
    zserioResult = subprocess.call(zserioCmd, stdout=subprocess.DEVNULL)
    if zserioResult != 0:
        raise Exception("Zserio compilation failed!")
    print("OK")

if __name__ == "__main__":
    sys.exit(main())

