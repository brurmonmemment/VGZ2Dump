# VGZ2Dump
# small wrapper script around multidumper

import os, sys, gzip, shutil, subprocess, platform

vgm_path    = None
target_file = None

def check_path(path):
    if not os.path.exists(path):
        print("file doesn't exist!")
        
    return path

# vgm.gz -> vgm
def extract(vgmgz):
    new_name = os.path.splitext(os.path.abspath(vgmgz))[0] + ".vgm.gz"
    os.rename(vgmgz, new_name)
    local_copy = new_name
    
    global vgm_path
    vgm_path = os.path.splitext(local_copy)[0]

    print(f"Extracting {local_copy} to {vgm_path}...")
    with gzip.open(local_copy, "rb") as f_in:
        with open(vgm_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    global target_file
    target_file = os.path.abspath(vgm_path)
    
def run_md():
    # heres the multi of the dumper
    print(f"Dumping channels into {folder_name}...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    multidumper_path = os.path.join(script_dir, "dumputil", "multidumper.exe")

    try:
        if is_windows:
            subprocess.run([multidumper_path, target_file], check=True)
        else:
            subprocess.run(["wine", multidumper_path, target_file], check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 3221226505:
            print("The vgm's being used by another application so try closin' it.")
        else:
            print(f"Something happened. more specifically, {e.returncode} happened.")
        sys.exit(1)
        
    # clean up
    os.remove(target_file)
    print("Dump successful!")
    
    
# windos check
is_windows = os.name == "nt" or platform.system() == "Windows"

print("VGZ2Dump v1.0.3")
print("Powered by multidumper by maxim-zhao")
print("This script converts a .vgz or .vgm.gz file into a folder with dumps of the PSG/YM2612 channels.")
    
file_path = None
if len(sys.argv) == 2:
    file_path = check_path(sys.argv[1].strip())
elif len(sys.argv) == 1:
    file_path = check_path(input("Please put in the path of the file you would like to convert: ").strip())
else:
    print("usage:")
    print(" python VGZ2Dump.py <file path>")
    sys.exit(1)


file_path = os.path.abspath(file_path)

# Determine folder name
folder_name = os.path.splitext(os.path.basename(file_path))[0]
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
else:
    print(f"folder '{folder_name}' already exists! all extracted data in the folder will be overridden. ya have nobody to blame but yourself.")

# file the stuff
local_copy = os.path.join(folder_name, os.path.basename(file_path))
shutil.copy(file_path, local_copy)

if local_copy.endswith(".vgz"):
    print("Detected .vgz")
    extract(local_copy)
elif local_copy.endswith(".vgm.gz"):
    print("Detected .vgm.gz")
elif local_copy.endswith(".vgm"):
    print("Detected .vgm")
else:
    print("Invalid file extension. Must be .vgz, .vgm.gz or .vgm.")
    shutil.rmtree(folder_name)
    sys.exit(1)

run_md()
