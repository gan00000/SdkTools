#coding=utf-8

import os
import time

sign_keystore_path = '/Users/ganyuanrong/AndroidProject/MWSDK/signkey/sdkv2_key.jks'
sign_keystore_alias = 'mwgamev2'
sign_keystore_password = 'mw888000'

# sign_keystore_path = '/Users/gan/Desktop/keystore/brmmd-keystore.jks'
# sign_keystore_alias = 'brmmd'
# sign_keystore_password = 'brmmd666888'


# sign_keystore_path = '/Users/gan/aspro/StarpyXMSdk/keystore/qqgame-keystore.jks'
# sign_keystore_alias = 'qqgame'
# sign_keystore_password = 'qq123456'


def get_current_time():
    # print time.time()
    t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    return t

def sign_apk(src_apk_path):

    sign_des_apk_path_dir = os.path.abspath(os.path.dirname(src_apk_path))

    sign_des_apk_path = os.path.join(sign_des_apk_path_dir,'sign-apk-' + get_current_time() + '.apk')


    sign_apk_cmd = 'jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore %s --storepass %s -signedjar %s  %s %s' % (
    sign_keystore_path, sign_keystore_password, sign_des_apk_path, src_apk_path, sign_keystore_alias)

    # sign_apk_cmd = "/Users/ganyuanrong/Library/Android/sdk/build-tools/32.0.0/apksigner sign --ks %s --ks-key-alias %s --ks-pass pass:%s --key-pass pass:%s --in  %s --out %s -v" % \
    #                (sign_keystore_path, sign_keystore_alias, sign_keystore_password,sign_keystore_password,src_apk_path, sign_des_apk_path)
    os.system(sign_apk_cmd)  # 签名

    return sign_des_apk_path


def zipalign_apk(src_apk_path):

    sign_des_apk_path_dir = os.path.abspath(os.path.dirname(src_apk_path))

    zipalign_apk_path = os.path.join(sign_des_apk_path_dir, 'sign-zipalign-apk-' + get_current_time() + '.apk')
    zipalign_apk_cmd = '/Users/ganyuanrong/Library/Android/sdk/build-tools/32.0.0/zipalign -f -v 4 %s %s' % (
        src_apk_path, zipalign_apk_path)
    os.system(zipalign_apk_cmd)  # 优化apk
    # os.remove(src_apk_path)


def rebuild_apk():

    decode_apk_dir = '/Users/ganyuanrong/Desktop/apkextrac'

    build_apk_dir = '/Users/ganyuanrong/Desktop/apks/'

    t_time = get_current_time()
    build_apk_file_name = t_time + '.apk'
    build_apk_path = os.path.join(build_apk_dir, build_apk_file_name)  # 反编译重新生成的包路径

    if os.path.exists(decode_apk_dir):
        apktool_build_cmd = 'apktool b  %s -o %s' % (decode_apk_dir, build_apk_path)
        os.system(apktool_build_cmd)

        return build_apk_path



def decodesignapk():

    apk_src = '/Users/ganyuanrong/Desktop/Calla_GAT_20220906195917.apk'
    decode_apk_dir = '/Users/ganyuanrong/Desktop/apkextrac/'
    # decode_apk_dir = ''
    build_apk_dir = '/Users/gan/apktooldir/apk/'

    # t_time = get_current_time()
    # build_apk_file_name = t_time + '.apk'
    # build_apk_path = os.path.join(build_apk_dir, build_apk_file_name)  # 反编译重新生成的包路径
    decode_apk_cmd = 'apktool d  %s -f -o %s' % (apk_src, decode_apk_dir)
    # sign_apk_name = t_time + '-sign.apk'
    # sign_apk_path = os.path.join(build_apk_dir, sign_apk_name)  # 签名包的路径\



    # sign_apk_cmd = 'jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore %s --storepass %s -signedjar %s  %s %s' % (
    # sign_keystore_path, sign_keystore_password, sign_apk_path, build_apk_path, sign_keystore_alias)
    # print decode_apk_cmd
    # print sign_apk_cmd

    # zipalign_apk_name = "宇州破壞神zipalign_" + t_time + '.apk'
    # zipalign_apk_path = os.path.join(build_apk_dir, zipalign_apk_name)  # 签名包的路径
    # zipalign_apk_cmd = '/Users/gan/Library/Android/sdk/build-tools/27.0.3/zipalign -f -v 4 %s %s' % (sign_apk_path, zipalign_apk_path)

    if os.path.exists(apk_src):
        os.system(decode_apk_cmd)
        pass

    if os.path.exists(decode_apk_dir):
        # apktool_build_cmd = 'apktool b  %s -o %s' % (decode_apk_dir, build_apk_path)
        # os.system(apktool_build_cmd)

        # os.system(sign_apk_cmd)  # 签名
        # os.system(zipalign_apk_cmd)  # 优化apk
        #
        # os.remove(build_apk_path)
        # os.remove(sign_apk_path)
        pass


if __name__ == '__main__':

    # decodesignapk()
    apk_path = rebuild_apk()

    signapkpath = sign_apk(apk_path)

    zipalign_apk(signapkpath)


