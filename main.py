from PIL import Image
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类

"""
收到消息，输出jmcomic的漫画pdf文件
"""

# 注册插件
@register(name="jmcomic", description="收到消息，输出jmcomic的漫画pdf文件", version="0.1",
          author="idk")
class RemoveTagsPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        super().__init__(host)  # 必须调用父类的初始化方法

    # 异步初始化
    async def initialize(self):
        pass

    def all2PDF(input_folder, pdfpath, pdfname):
        paht = input_folder
        zimulu = []  # 子目录（里面为image）
        image = []  # 子目录图集
        sources = []  # pdf格式的图

        with os.scandir(paht) as entries:
            for entry in entries:
                if entry.is_dir():
                    zimulu.append(int(entry.name))
        # 对数字进行排序
        zimulu.sort()

        for i in zimulu:
            with os.scandir(paht + "/" + str(i)) as entries:
                for entry in entries:
                    if entry.is_dir():
                        print("这一级不应该有自录")
                    if entry.is_file():
                        image.append(paht + "/" + str(i) + "/" + entry.name)

        if "jpg" in image[0]:
            output = Image.open(image[0])
            image.pop(0)

        for file in image:
            if "jpg" in file:
                img_file = Image.open(file)
                if img_file.mode == "RGB":
                    img_file = img_file.convert("RGB")
                sources.append(img_file)

        pdf_file_path = pdfpath + "/" + pdfname
        if pdf_file_path.endswith(".pdf") == False:
            pdf_file_path = pdf_file_path + ".pdf"
        output.save(pdf_file_path, "pdf", save_all=True, append_images=sources)


    def jm(cm_id):
        # 自定义设置：
        config = "./config.yml"
        loadConfig = jmcomic.JmOption.from_file(config)
        #如果需要下载，则取消以下注释
        manhua = cm_id
        for id in manhua:
            jmcomic.download_album(id,loadConfig)

        with open(config, "r", encoding="utf8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            path = data["dir_rule"]["base_dir"]

        i = 0
        
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir():
                    if os.path.exists(os.path.join(path +'/' +entry.name + ".pdf")):
                        print("文件：《%s》 已存在，跳过" % entry.name)
                        return 
                    else:
                        print("开始转换：%s " % entry.name)
                        RemoveTagsPlugin.all2PDF(path + "/" + entry.name, path, manhua[i])
            i = i + 1

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 GroupNormalMessageReceived 的对象
        if "@jm" in msg:  # 如果消息含有Jm查询
            
            txt = msg.strip("@jm").strip(" ").strip("\n")
            txt.split(",")
            self.jm(txt)
            
            # 输出调试信息
            self.ap.logger.debug("jm_get: {}".format(ctx.event.sender_id))

            # 添加文件目录
            for id in txt:
                ctx.add_return("reply",url='./img/'+ txt +'.pdf')

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass