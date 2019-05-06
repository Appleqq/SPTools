from biplist import InvalidPlistException
from qiniu import Auth, put_file,etag
import qiniu.config
import os
import plistlib
from bs4 import BeautifulSoup

#需要填写你的 Access Key 和 Secret Key
access_key = 'pydoM4TkAUnY_nrmVIypZX8RWCKMTciS9lO0Tf-z'
secret_key = 'NSjEs3Eiwii5p3HAQEd_AGjrKxwmqCnGt4mzR6If'

# 上传文件到七牛云服务器
def upload_qiniu(name):
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'ios-ipa'

    # 上传后保存的文件名
    key = name

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    localfile = 'app/' + name

    ret, info = put_file(token, key, localfile)

    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)

def upload_file_qiniu(name, localfile):
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'ios-ipa'

    # 上传后保存的文件名
    key = name

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_file(token, key, localfile)

    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)

#获取文件名称
def file_name(file_dir):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.ipa':
                L.append(file)
    return L

#上传完成ipa之后，修改manifest.plist 文件内容
def change_manifest(download_url):
    localfile = 'iosUpdate/' + 'manifest.plist'
    try:
        manifest = plistlib.readPlist(localfile)
        print(manifest)
        assets = manifest['items'][0]['assets']
        metadata = manifest['items'][0]['metadata']
        '''替换下载的url'''
        download_info = assets[0]
        download_info['url'] = download_url

        """截取下载的url"""
        info = download_url.split('/')

        '''获取ipa的名字'''
        ipa_name = info[-1]

        '''取出版本信息'''
        version = ipa_name.split('_')[2]

        '''替换版本信息'''
        metadata['bundle-version'] = version

        '''获取上传到七牛的名字'''
        manifest_name = ipa_name.replace('SPIntergrationIOS.ipa', 'manifest.plist')
        plistlib.writePlist(manifest, localfile)

        return manifest_name


    except(InvalidPlistException) as e:
        print("Not a plist:", e)

def change_index_html(manifest_name):
    manifest_url = 'itms-services://?action=download-manifest' + '&' + 'url+' + manifest_name
    file = 'iosUpdate/' + 'index.html'
    soup = BeautifulSoup(open(file))
    for a1 in soup.findAll('a1'):
        a1['href'] = manifest_url

    print(soup)


if __name__ == '__main__':
    #os.system('fastlane test desc:测试打包')
    # 获取当前文件路径
    current_path = os.path.abspath(__file__)
    # 获取父级文件路径
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    path = file_name(father_path)
    #print(path[0])
    #upload_qiniu(path[0])
    manifest_name = change_manifest("https://iosipa.xspinfo.com/V_SP_3.1.18_test_SPIntergrationIOS.ipa")
    #upload_file_qiniu(manifest_name, 'iosUpdate/manifest.plist')
    #change_index_html('V_SP_3.1.17_manifest.plist')

