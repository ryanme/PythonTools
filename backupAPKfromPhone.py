#! python2.7
#encoding:utf-8

# tv.danmaku.bill 哔哩哔哩
# com.tencent.qqlive 腾讯视频
# com.netease.tx 天下
# com.tencent.tmgp.sgame 王者荣耀
# cn.soulapp.android Soul
# com.gmmohe.box gm魔盒
# com.tencent.karaoke 全民K歌
# com.ss.android.ugc.aweme 抖音
# com.kfc112.app.xcb0wi KFC
# com.taobao.idlefish 闲鱼
# com.tencent.mtt QQ浏览器
# com.tencent.mobileqq QQ
# com.snailgame.jysg.mian 九阳神功2
# com.sankuai.meituan 美团
# com.gamersky 游民时空
# com.aba.cctv rose直播
# com.weibo.internaltional 微博国际版
# com.pear.hot 梨视频
# com.smile.gifmake 快手
# com.babylivejuhe baby盒子
# com.taobao.mobile.dipei 口碑
# com.baidu.searchbox 百度
# com.netease.cloudmusic 网易云音乐
# cn.missevan 猫耳FM
# com.qiyi.video 爱奇艺
# com.zhihu.android 知乎
# com.alibaba.wireless 阿里巴巴
# com.MobileTicket 铁路12306
# air.tv.douyu.android 斗鱼
# com.same.android same
# com.taobao.taobao 淘宝
# com.kiwiwalks.witchsprings 魔女之泉3
# com.eonsun.myreader 老子搜书
# com.chbrs.live 小姐姐
# fm.xiami.main 虾米音乐
# com.eg.android.AlipayGphone 支付宝
# com.didapinche.booking 嘀嗒出行
# com.panda.videoliveplatform 熊猫直播
# com.heyhou.social 嘿吼
# com.jingdong.app.mail 京东
# cn.chdrs.live 优酱
# com.sohu.inputmethod.sogou 搜狗
# com.autonavi.minimap 高德地图
# com.sdu.didi.beatles 滴滴顺风车
# com.funny.cuite  cuite
# com.netease.newsreader.activity 网易新闻
# com.netease.yanxuan 网易严选
# com.sdu.didi.psnger 滴滴出行
# com.qq.ac.android 腾讯动漫
# com.ataaw.tianyi 天翼生活
# com.tencent.android.qqdownloader 应用宝
# com.clov4r.android.nil 么播mobo
# com.cib.cibmb 兴业银行
# com.chinamworld.main 建设银行
# cmb.pb 招商银行
# com.hoperun.intelligenceportal 我的南京
# org.zxq.teleri 斑马智行
# com.hpbr.bosszhipin boss直聘
# com.quark.browser 夸克浏览器
# com.taobao.trip 飞猪
# com.taptap  TapTap
# io.va.exposed VirtualXposed
# org.consenlabs.token imToken
# com.tmri.app.main 交管12123
# com.duapps.recorder 安卓录屏大师
# com.flyersoft.seekbooks 搜书大师
#
import os
out = os.popen('adb devices').read()
print(out)
#https://blog.csdn.net/signjing/article/details/51835017
#https://blog.csdn.net/henni_719/article/details/62223022