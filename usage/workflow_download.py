从……起jmcomic进口 *
从……起jmcomic.cl进口JmcomicUI

# 下方填入你要下载的本子的id，一行一个，每行的首尾可以有空白字符
JM_albums='''
jm350788


'''

# 单独下载章节
JM_photos='''



'''


定义 env(名称，默认值，修剪=('[]','""',"''")):
    进口操作系统
值=os.getenv(姓名，没有一个)
    如果价值是 没有一个 或value=='':
        返回默认

    为一对在……内修剪：
        如果价值。startswith(一对[0]) 和价值。endswith(一对[1]):
value=value[1:-1]

    返回价值


定义 get_id_set(环境名称，给定):
aid_set=设置()
    为文本在……内 [
鉴于，
        (env(环境名称，'')).取代('-','\n'),
    ]:
aid_set。更新(str_to_set(文本))

    返回aid_set


定义 主要的():
album_id_set=get_id_set('JM_ALBUM_IDS'，jm_ablums)
photo_id_set=get_id_set('JM_PHOTO_IDS'，jm_photos)

helper=JmcomicUI()
助手。album_id_list=列表(album_id_set)
助手。photo_id_list=列表(photo_id_set)

option=get_option()
助手。跑(选项)
选项。call_all_plugin('下载后')


定义 get_option():
    #读取选项配置文件
option=create_option(操作系统。路径.abspath(操作系统。路径.参加(__file__，'。。/。。/assets/option/option_workflow_download.yml')))

    # 支持工作流覆盖配置文件的配置
    cover_option_config(选项)

    #把请求错误的html下载到文件，方便GitHub Actions下载查看日志
    log_before_raise()

    返回选项


定义 cover_option_config(选项：JmOption):
目录规则=env('DIR_rule',没有一个)
    如果目录规则(_R)是 不 没有一个:
_old=选项。目录规则(_R)
新的(_N)=DirRule(Dir_rule，base_dir=旧的。基底目录(_D))
选项。目录规则(_R)=新的(_N)

impl=env('CLIENT_IMPL',没有一个)
    如果impl是 不 没有一个:
选项。客户.impl=impl

后缀=env('Image_SUFFIX',没有一个)
    如果后缀是 不 没有一个:
选项。下载.图像.后缀=fix_suffix(后缀)


定义 log_before_raise():
JM_download_dir=env('JM_DOWNLOAD_DIR',工作空间())
    mkdir_if_not_exists(JM_download_dir)

    定义 决定文件路径(_F)(e):
RESP=e.语境.得到(ExceptionTool。context_KEY_RESP,没有一个)

        如果RESP是 没有一个:
后缀=str(time_stamp())
        其他:
后缀=resp.URL

name='-'.参加(
            fix_windir_name(它)
            为它在……内 [
e。描述,
                当前线程(_T)().姓名,
后缀
            ]
        )

路径=f'{JM_download_dir}/【出错了】{姓名}.log'
        返回路径

    定义 异常监听器(_L)(E:JmcomicException):
        """
        异常监听器，实现了在 GitHub Actions 下，把请求错误的信息下载到文件，方便调试和通知使用者
        """
        # 决定要写入的文件路径
        path = decide_filepath(e)

        # 准备内容
        content = [
            str(type(e)),
            e.msg,
        ]
        for k, v in e.context.items():
            content.append(f'{k}: {v}')

        # resp.text
        resp = e.context.get(ExceptionTool.CONTEXT_KEY_RESP, None)
        if resp:
            content.append(f'响应文本: {resp.text}')

        # 写文件
        write_text(path, '\n'.join(content))

    JmModuleConfig.register_exception_listener(JmcomicException, exception_listener)


if __name__ == '__main__':
    main()
