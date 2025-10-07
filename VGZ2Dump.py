import os
import gzip
import shutil
import platform
is_windows = os.name == "nt" or platform.system() == "Windows"
custom_folder_name = False
predetermined_folder_name = ""
file = ""
folder_name = ""

print("VGZ2Dump v1.0.1")
print("Powered by multidumper by maxim-zhao")
print("This script is designed to turn a .vgz or .vgm.gz file (more specifically a Sega Genesis soundtrack) into a folder with dumps of the PSG/YM2612.")

while True:
    file = input("Please put in the path of the file you would like to convert: ").strip()

    if not os.path.exists(file):
        print("File doesn't exist")
        continue

    file = os.path.abspath(file)

    if custom_folder_name and predetermined_folder_name == "":
        while True:
            folder_name = input("Please provide the name of the folder you would like the dumped channels to be in (you can disable this in the script): ").strip()

            if folder_name == "":
                print("Invalid folder name")
                continue

            break

    else:
        folder_name = os.path.splitext(os.path.basename(file))[0]

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    local_copy = os.path.join(folder_name, os.path.basename(file))
    shutil.copy(file, local_copy)

    if local_copy.endswith(".vgz"):
        print("Detected .vgz")
        print("Changing file extension to .vgm.gz...")
        new_name = local_copy.replace(".vgz", ".vgm.gz")
        os.rename(local_copy, new_name)
        local_copy = new_name
    elif local_copy.endswith(".vgm.gz"):
        print("Detected .vgm.gz")
    else:
        print("Invalid file extension")
        shutil.rmtree(folder_name)
        continue

    vgm_path = local_copy.replace(".vgm.gz", ".vgm")
    print(f"Extracting {local_copy} to {vgm_path}...")
    with gzip.open(local_copy, "rb") as f_in:
        with open(vgm_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    os.remove(local_copy)
    break

print(f"Dumping channels into {folder_name}")
os.chdir(folder_name)

multidumper_path = os.path.abspath("../dumputil/multidumper.exe")
target_file = os.path.basename(vgm_path)

if is_windows:
    os.system(f"\"{multidumper_path}\" \"{target_file}\"")
else:
    os.system(f"wine \"{multidumper_path}\" \"{target_file}\"")

os.remove(target_file)

os.chdir("..")
print("Dump successful!")
