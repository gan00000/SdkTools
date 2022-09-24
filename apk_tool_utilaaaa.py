#coding=utf-8

import os
import time



def get_current_time():
    # print time.time()
    t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    return t

if __name__ == '__main__':

    apk_src = '/Users/gan/Downloads/欣欣十三水_killer.apk'

    decode_apk_dir = '/Users/gan/apktooldir/temp22/'
    # decode_apk_dir = ''
    build_apk_dir = '/Users/gan/apktooldir/apk/'

    t_time = get_current_time()
    build_apk_file_name = t_time + '.apk'
    build_apk_path = os.path.join(build_apk_dir, build_apk_file_name) #反编译重新生成的包路径

    decode_apk_cmd = 'apktool d  %s -f -o %s' % (apk_src, decode_apk_dir)

    sign_apk_name = t_time + '-sign.apk'
    sign_apk_path = os.path.join(build_apk_dir, sign_apk_name)#签名包的路径
    sign_keystore_path = '/Users/gan/Downloads/androidkiller.keystore'
    # sign_keystore_path = '/Users/gan/Desktop/keystore/ahdl.keystore'
    sign_keystore_alias = 'androidkiller'
    sign_keystore_password = 'killer'
    # sign_apk_cmd = 'jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore %s --storepass %s -signedjar %s  %s %s' %(sign_keystore_path, sign_keystore_password, sign_apk_path, build_apk_path,sign_keystore_alias)
    sign_apk_cmd = 'jarsigner -verbose -keystore %s --storepass %s -signedjar %s  %s %s' %(sign_keystore_path, sign_keystore_password, sign_apk_path, build_apk_path,sign_keystore_alias)
    # sign_apk_cmd = 'jarsigner -verbose -keystore %s -signedjar %s %s %s' %(sign_keystore_path, sign_keystore_password, sign_apk_path, build_apk_path,sign_keystore_alias)
    print decode_apk_cmd

    print sign_apk_cmd

    zipalign_apk_name = "zipalign_" + t_time + '.apk'
    zipalign_apk_path = os.path.join(build_apk_dir, zipalign_apk_name)  # 签名包的路径
    zipalign_apk_cmd = 'zipalign -f -v 4 %s %s'%(sign_apk_path,zipalign_apk_path)

    # if os.path.exists(apk_src):
    #     os.system(decode_apk_cmd)
    #     pass

    if os.path.exists(decode_apk_dir):

        apktool_build_cmd = 'apktool b  %s -o %s' % (decode_apk_dir, build_apk_path)
        os.system(apktool_build_cmd)

        os.system(sign_apk_cmd)  # 签名
        os.system(zipalign_apk_cmd)  # 优化apk

        os.remove(build_apk_path)
        os.remove(sign_apk_path)
        pass

