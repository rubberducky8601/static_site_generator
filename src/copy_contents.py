import os
import shutil


def copy_contents_r(src, dest):
    for file in os.listdir(src):
        src_file = os.path.join(src, file)
        dest_file = os.path.join(dest, file)

        if os.path.isdir(src_file):
            if not os.path.exists(dest_file):
                os.makedirs(dest_file)
                print(f"Created directory: {dest_file}")
            print(f"Entering recursive directory: {src_file}")
            copy_contents_r(src_file, dest_file)
        else:
            shutil.copy2(src_file, dest_file)
            print(f"Copied {src_file} to {dest_file}")


def copy_contents(src, dest):

    print(src)
    print(os.listdir(src))
    print(os.listdir(dest))
    # delete files in dest
    print("Deleting files in destination directory...")
    for file in os.listdir(dest):
        if os.path.isdir(os.path.join(dest, file)):
            print(f"Deleting directory: {file}")
            shutil.rmtree(os.path.join(dest, file))
        else:
            print(f"Deleting file: {file}")
            os.remove(os.path.join(dest, file))

    copy_contents_r(src, dest)
