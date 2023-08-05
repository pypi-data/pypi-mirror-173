#用于筛选数据集当中的图片，按条件进行抽取
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config
from pycallgraph import GlobbingFilter

import numpy as np
import shutil
import threading
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
from PIL import Image
import tqdm
import json
from peewee import *
import os
import logging
import random
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level = logging.WARNING,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level = logging.ERROR,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

work_dir = r"\\10.10.1.39\d\FT190019_广汽本田_发动机外壳检测\已标注数据\模型1_加孔字v1\zftklwABCD"

database_proxy = DatabaseProxy()
#项目总表的ORM类
class General_Table(Model):

    class Meta:
        database = database_proxy

#数据基本类，实现增改删查的功能
class DataBaseTool():

    def __init__(self,database_obj,initalize_database = True):

        #数据库初始化状态
        self.initalize_database = initalize_database
        if self.initalize_database:
            if os.path.exists(os.path.join(work_dir, 'works.db')):
                os.remove(os.path.join(work_dir, 'works.db'))
            else:
                self.initalize_database = False

        #连接数据库，初始化数据库
        self.db = SqliteDatabase(os.path.join(work_dir, 'works.db'))
        database_proxy.initialize(self.db)
        self.db.connect()
        # 创建存储数据的表
        self.db.create_tables([database_obj])

        self.database_obj = database_obj

    def format_commend(self,kwargs = None, kwargs_advance = None, mode = "|"):
        if kwargs:
            commend = ""
            for attr , info in kwargs.items():
                single_commend = "(" + "self.database_obj" +"." + attr  + "==" +   "\"" +  info + "\""  + ")"
                commend += single_commend
                commend += mode
            return commend[:-1]
        if kwargs_advance:
            commend = ""
            for attr , info in kwargs_advance.items():
                if isinstance(info[1],str):
                    single_commend = "(" + "self.database_obj" +"." + attr + info[0] + "\"" +  info[1] + "\"" + ")"
                    commend += single_commend
                    commend += mode
                else:
                    single_commend = "(" + "self.database_obj" +"." + attr  + info[0]  + str(info[1])  + ")"
                    commend += single_commend
                    commend += mode

            return commend[:-1]

    def get_total_count(self):  # 获取数据总数

        logger.info("TOTAL_COUNT")
        results = (self.database_obj
                   .select()
                   .count()
                   )  # 调用query语句进行查询，返回调用结果
        return results

    def insert(self , **kwargs ): #新增条例
        logger.info("INSERT：{}".format(kwargs))
        return self.database_obj.create(**kwargs)

    def insertmany(self , kwargs ): #新增多个条例
        logger.info("INSERT：新增数据：{}".format(kwargs))
        with self.db.atomic():
            for batch in chunked(kwargs, 50):
                self.database_obj.insert_many(batch).execute()

    def update(self,id , kwargs): #更新条例
        # print(id, kwargs)
        logger.info("UPDATE：{}".format(kwargs))
        self.database_obj.update(kwargs).where(self.database_obj.id == id).execute()

    def delte(self,id): #删除条例
        self.database_obj.delete().where(self.database_obj.id == id).execute()
        logger.info("DELETE：{}".format(id))

    def search(self,attr,data): #单因素查询条例，返回二维列表
        logger.info("SEARCH：{}".format(attr + ":" + data ))
        result = []
        results =  (self.database_obj
        .select()
        .where( eval("self.database_obj." + attr) == data)) #调用query语句进行查询，返回调用结果
        for i in results:

            result.append(list(i.__dict__["__data__"].values())) #添加至数据类模型中
        return result

    def advance_search(self,kwargs = None, kwargs_advance = None, mode = "|"): #高级查询条例,多条件查询，返回二维列表
        if kwargs:
            result = []
            commend = self.format_commend(kwargs = kwargs, mode = mode)
            logger.info("ADVANCE_SEARCH：{}".format(commend))
            results =  (self.database_obj
            .select()
            .where( eval(commend))
            .order_by(self.database_obj.id)
            ) #调用query语句进行查询，返回调用结果
            for i in results:
                result.append(list(i.__dict__["__data__"].values()))
            # print(result)
            return result
        if kwargs_advance:
            result = []
            commend = self.format_commend(kwargs_advance = kwargs_advance,mode = mode)
            logger.info("ADVANCE_SEARCH：{}".format(commend))
            results =  (self.database_obj
            .select()
            .where( eval(commend))
            .order_by(self.database_obj.id)
            ) #调用query语句进行查询，返回调用结果
            for i in results:
                result.append(list(i.__dict__["__data__"].values()))
            return result

    def advance_search_count(self,kwargs): #高级查询条例,多条件查询，返回查询个数
        commend = self.format_commend(kwargs)
        logger.info("ADVANCE_SEARCH：{}".format(commend))
        results =  (self.database_obj
        .select()
        .where( eval(commend))
        .order_by(self.database_obj.id)
        .count()
        ) #调用query语句进行查询，返回调用结果
        return results

    def get_page_count(self, per_page = None):
        total_count = self.get_total_count()
        if total_count % per_page == 0:
            return (total_count % per_page)
        else:
            return (total_count % per_page + 1)

class DataFilter():

    def __init__(self, database_obj,initalize_database):

        self.dataworker = DataBaseTool( database_obj,initalize_database)
        self.worker_dir = work_dir
        self.image_size = self.get_image_size()
        self.GT_info = self.init_GT()

        self.categorys = {1:"1",2:"2",3:"3",4:"4",5:"5",6:"hp",7:"hs",8:"yw",9:"fh",
        10:"qk",11:"lg",12:"sx",13:"lxcl",14:"kp",15:"qr",16:"dr",17:"zw",18:"ljg",
        19:"dw",20:"mc",21:"ywcl",22:"tk",23:"lw",24:"ABCD",25:"*zf"}
        # self.category = ['1','2','3','4','5','hp','hs','yw','fh','qk','lg','sx','lxcl',
        #                   'kp', 'qr', 'dr', 'zw', 'ljg', 'dw', 'mc', 'ywcl', 'tk', 'lw',
        #                   'ABCD', '*zf']

    def init_GT(self):
        if not os.path.join(self.worker_dir,"GT_dict.json"):
            logger.error("加载GT：worker_dir下不存在GT文件，请确认")
        else:
            return json.load(open(os.path.join(self.worker_dir, "GT_dict.json"), 'rb'))

    def get_image_size(self):
        if not os.path.join(self.worker_dir,"image_size.json"):
            logger.error("获取图片大小：worker_dir下不存在image_size文件，将先开始获取...")
            return self.count()
        else:
            return json.load(open(os.path.join(self.worker_dir, "image_size.json"), 'rb'))

    def count(self):
        image_size = {}
        for filename in tqdm.tqdm(os.listdir(self.worker_dir)):
            if filename.endswith(".jpg"):
                file_path = os.path.join(self.worker_dir, filename)
                img = Image.open(file_path)
                imgSize = img.size  # 大小/尺寸
                w = img.width  # 图片的宽
                h = img.height  # 图片的高
                image_size[filename] = [h, w]
        print(image_size)
        with open(os.path.join(self.worker_dir, "image_size.json"), 'w') as f:
            json.dump(image_size, f, ensure_ascii=False)
        return json.load(open(os.path.join(self.worker_dir, "image_size.json"), 'rb'))

    def init_data(self): #初始化添加标签到数据库（执行一次即可）
        if self.dataworker.initalize_database :
            insert_format = []
            for each_image , image_info in self.GT_info.items():
                for each_GT in image_info:
                    data_format = {"imagename":None, "station":None,"camera":None,"camera_number":None,"category":None ,"ymin":None, "xmin":None, "ymax":None, "xmax":None,"w":None, "h":None, "area":None}
                    # image_np = cv2.imdecode(np.fromfile(os.path.join(self.worker_dir,each_image), dtype=np.uint8), 3)
                    # image_np = image_np.tolist()
                    # data_format["image_np"] = image_np
                    data_format["imagename"] = each_image
                    station_camera_number = each_image.split("_")[1:]
                    station = station_camera_number[0]
                    camera = station_camera_number[1][:2]+ station_camera_number[1][5]
                    camera_number = station_camera_number[2].split(".jpg")[0]
                    if "(" in camera_number:
                        camera_number = camera_number.split(" (")[0]
                    data_format["station"] = station
                    data_format["camera"] = camera
                    data_format["camera_number"] = camera_number
                    data_format["category"] = self.categorys[each_GT[0]]
                    data_format["ymin"]  = each_GT[1] * self.image_size[each_image][0]
                    data_format["xmin"] = each_GT[2] * self.image_size[each_image][1]
                    data_format["ymax"]  = each_GT[3] * self.image_size[each_image][0]
                    data_format["xmax"] = each_GT[4] * self.image_size[each_image][1]
                    data_format["w"] = each_GT[4] * self.image_size[each_image][1] - each_GT[2] * self.image_size[each_image][1]
                    data_format["h"] = each_GT[3] * self.image_size[each_image][0] - each_GT[1] * self.image_size[each_image][0]
                    data_format["area"] = data_format["w"] * data_format["h"]
                    insert_format.append(data_format)
            # print(insert_format)
            self.dataworker.insertmany(insert_format)
        else:
            logger.warning("INIT_DATA：数据库中已存在数据，初始化将前请先确认数据库状态")


    def insert_data(self): #初始化添加标签到数据库（执行一次即可）
        if not self.dataworker.initalize_database :
            insert_format = []
            for each_image , image_info in self.GT_info.items():
                for each_GT in image_info:
                    data_format = {"imagename":None, "station":None,"camera":None,"camera_number":None,"category":None ,"ymin":None, "xmin":None, "ymax":None, "xmax":None,"w":None, "h":None, "area":None}
                    # image_np = cv2.imdecode(np.fromfile(os.path.join(self.worker_dir,each_image), dtype=np.uint8), 3)
                    # image_np = image_np.tolist()
                    # data_format["image_np"] = image_np
                    data_format["imagename"] = each_image
                    station_camera_number = each_image.split("_")[1:]
                    station = station_camera_number[0]
                    camera = station_camera_number[1][:2]+ station_camera_number[1][5]
                    camera_number = station_camera_number[2].split(".jpg")[0]
                    if "(" in camera_number:
                        camera_number = camera_number.split(" (")[0]
                    data_format["station"] = station
                    data_format["camera"] = camera
                    data_format["camera_number"] = camera_number
                    data_format["category"] = self.categorys[each_GT[0]]
                    data_format["ymin"]  = each_GT[1] * self.image_size[each_image][0]
                    data_format["xmin"] = each_GT[2] * self.image_size[each_image][1]
                    data_format["ymax"]  = each_GT[3] * self.image_size[each_image][0]
                    data_format["xmax"] = each_GT[4] * self.image_size[each_image][1]
                    data_format["w"] = each_GT[4] * self.image_size[each_image][1] - each_GT[2] * self.image_size[each_image][1]
                    data_format["h"] = each_GT[3] * self.image_size[each_image][0] - each_GT[1] * self.image_size[each_image][0]
                    data_format["area"] = data_format["w"] * data_format["h"]
                    insert_format.append(data_format)
            # print(insert_format)
            self.dataworker.insertmany(insert_format)
        else:
            logger.warning("INSERT_DATA：数据库初始化状态为True，请确认数据库状态")

    def get_category_number(self , category): #获取单个索引标签数
        data_count = self.dataworker.advance_search_count({"category":category})
        logger.info("SEARCH：类别 {} 查询到 {} 个标签".format(category , data_count))

    def get_category_images(self , commend  ): #索引单个标签
        '''
        :param commend: 单个标签字符串
        :return: 图片名列表
        '''
        category = commend
        search_data = self.dataworker.advance_search(kwargs ={"category":category })
        image_list = []
        for each_data in search_data:
            image_list.append(each_data[0])
        image_list = set(image_list)
        logger.info("SEARCH：标签 {} 查询并返回 {} 张图片".format(commend , len(image_list)))
        return image_list

    def get_category_images_advance(self,category_list): #索引多个标签
        '''
        :param category_list: 要索引的标签列表
        :return: 图片名的列表
        '''
        total_image_list = []
        for each_category in category_list:
            image_list = self.get_category_images(each_category)
            total_image_list+= image_list
        total_image_list = set(total_image_list)
        logger.info("SEARCH：标签 {} 查询并返回 {} 张图片".format(category_list, len(total_image_list)))
        return total_image_list

    def get_cetegory_images_commend(self, commend,mode): #多条件查询标签
        search_data = self.dataworker.advance_search(kwargs_advance = commend,mode= mode)

        image_list = []
        for each_data in search_data:
            image_list.append(each_data[1])
        image_list = set(image_list)
        logger.info("SEARCH：条件 {} 查询并返回 {} 张图片".format(commend , len(image_list)))
        return image_list

    def copy_file(self , input_path_jpg , input_path_txt,output_path_jpg,output_path_txt): #执行数据拷贝
        shutil.copyfile(input_path_jpg, output_path_jpg)
        shutil.copyfile(input_path_txt,output_path_txt)

    def copy_threading_main(self,  input_path , output_dir): #多线程拷贝数据
        '''
        :param input_path: 图片名列表
        :param output_dir: 输出目录
        :return:
        '''
        logging.info("执行图片拷贝")
        logging.info("进程pid(%s)，即将开启%s个线程" % (os.getpid(), multiprocessing.cpu_count()))
        pool = ThreadPool(multiprocessing.cpu_count())  # 开启num个线程
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        for each_image in tqdm.tqdm(input_path):
            input_path_jpg = os.path.join(self.worker_dir , each_image)
            input_path_txt = os.path.join(self.worker_dir , each_image[:-4] + ".txt")
            output_path_jpg = os.path.join(output_dir , each_image)
            output_path_txt = os.path.join(output_dir , each_image[:-4] + ".txt")
            pool.apply_async(
                    func=self.copy_file,
                    args=(input_path_jpg , input_path_txt,output_path_jpg,output_path_txt)
                    )
        pool.close()
        pool.join()

    def data_count(self):

        pass

def main():
    import time
    worker = DataFilter(db, Custom_Table,"Custom_Table")
    # worker.count()
    worker.init_data()
    # image_list = worker.get_category_images_advance(["ABCD"])
    # random_image_list = random.sample(image_list,len(image_list)//2)
    # print(len(random_image_list))
    t1 = time.time()
    image_list = worker.get_cetegory_images_commend(commend = {"station":["==","OPM"], "camera":["==","B13"],"camera_number":["==","11"]},mode = "&")
    t2 = time.time()
    # worker.copy_threading_main(random_image_list, os.path.join(work_dir,"ABCD"))
    db.close()

if __name__ == "__main__":

    # graphviz = GraphvizOutput()
    # graphviz.output_file = 'graph.png'
    # with PyCallGraph(output=graphviz):
    #     main()
    #
    main()






