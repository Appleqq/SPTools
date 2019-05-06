# This file contains the fastlane.tools configuration
# You can find the documentation at https://docs.fastlane.tools
#
# For a list of all available actions, check out
#
#     https://docs.fastlane.tools/actions
#
# For a list of all available plugins, check out
#
#     https://docs.fastlane.tools/plugins/available-plugins
#

# Uncomment the line if you want fastlane to automatically update itself
# update_fastlane

#plist路径
APP_INFO_PLIST_PATH = ‘./SPIntergrationIOS/Info.plist'
#打包的方式
ENV_PREFIX="Release"
#scheme 名称
SCHEME = "SPIntergrationIOS"

default_platform(:ios)

platform :ios do
  desc "Push a new beta build to TestFlight"
  lane :beta do
    build_app(workspace: "SPIntergrationIOS.xcworkspace", scheme: SCHEME)
    upload_to_testflight
  end
end

desc "打包上传到七牛"
lane :test do |options|
  #获取版本信息
  VERSION = get_version_number(xcodeproj: "SPIntergrationIOS.xcodeproj")
  #获取此版本对应的名称（需要在info.plist中加入自定义字段）
  PLIST_INFO_CUSTOMNAME = get_info_plist_value(path: "#{APP_INFO_PLIST_PATH}", key: 'CustomAppName')
  #打包出来IPA的名称
  IPA_NAME = "V" + "_" + "#{PLIST_INFO_CUSTOMNAME}" + "_" + "#{VERSION}" + "_" + "#{ENV_PREFIX}" + "_" + "#{SCHEME}" + ".ipa"

  gym(
  clean:true, #打包前clean项目
  export_method: "enterprise", #导出方式
  export_options: { compileBitcode: false},
  scheme:"SPIntergrationIOS", #scheme
  configuration: ENV_PREFIX,#环境
  output_directory:"./app",#ipa的存放目录
  export_xcargs: "allowProvisioningUpdates",
  include_bitcode: true,
  output_name: IPA_NAME 
  )
 #蒲公英的配置 替换为自己的api_key和user_key
  pgyer(api_key: "f33a17c189754ed0c1156b103dc167e6", user_key: "5e266d3f2c3e6206ca20c9c8bd166301",update_description: options[:desc])

end

desc "上传到qiniu"
lane :qiniu do |options|
sh

end