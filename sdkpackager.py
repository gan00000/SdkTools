import os
import shutil
import time
import zip_util

sdk_path = "/Users/gan/sdk/starpyandroidsdk/StarpySDK"
sdk_path_root = "/Users/gan/sdk/starpyandroidsdk/"


def get_current_time():
    return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))


def packager():

    current_time = get_current_time()
    sdk_path_temp_1 = os.path.join(sdk_path_root, current_time)

    if os.path.exists(sdk_path_temp_1):
        shutil.rmtree(sdk_path_temp_1)
    shutil.copytree(sdk_path, sdk_path_temp_1)
    list_dirs = os.walk(sdk_path_temp_1)

    for root, dirs, files in list_dirs:
        # for d in dirs:
        #     print os.path.join(root, d)
        for f in files:
            # delete git file
            if f == ".git" or f == ".gitignore":
                print ("delete " + os.path.join(root, f))
                # shutil.rmtree(os.path.join(root, f))
                os.remove(os.path.join(root, f))

            elif ".iml" in f:
                print f
                for d in dirs:
                    # delete build files
                    if d == ".git" or d == "build":
                        print "delete " + os.path.join(root, d)
                        shutil.rmtree(os.path.join(root, d))

    sdk_zip_name = os.path.join(sdk_path_root, "starpy-android-sdk-" + current_time + ".zip")
    zip_util.zip_dir(sdk_path_temp_1, sdk_zip_name)
    if os.path.exists(sdk_path_temp_1):
        shutil.rmtree(sdk_path_temp_1)

packager()