import hashlib
import logging
import os
import stat
from os import path
import json
import requests
import psutil
import sys


class AutoUpdate(object):
    VERSION_FILE_NAME = "version.json"
    local_version_info = {}
    MODE = "no_check"
    URL = ""
    FORCE = False
    CWD = ""
    UPDATE_MODE = "silent"
    LOCAL_VERSION_INFO_JSON_PATH = ""
    LOGGER = logging.getLogger(__name__)
    CALLBACK = None
    NEED_RESTART = True
    DIRECT_URL = None

    def __init__(self, SETTINGS={}, callback=None, direct_url=None) -> None:
        # 获取项目工作路径
        self.CWD = os.getcwd()
        self.CALLBACK = callback
        self.MODE = SETTINGS.get("mode", "no_check")
        self.URL = SETTINGS.get("url", "")
        self.UPDATE_MODE = SETTINGS.get("update_mode", "silent")
        self.NEED_RESTART = SETTINGS.get("restart", True)
        self.DIRECT_URL = direct_url

        # 读取版本文件
        self.LOCAL_VERSION_INFO_JSON_PATH = path.join(
            self.CWD, self.VERSION_FILE_NAME)

    def get_web_file_md5(self, url):
        m = hashlib.md5()
        resp = requests.get(url, stream=True)
        for i in resp.iter_content(chunk_size=1024):
            if i:
                m.update(i)
        return m.hexdigest()
    
    def get_local_file_md5(self, p):
        m = hashlib.md5()
        with open(p, "rb") as f:
            data = f.read(1024)
            if len(data) > 0:
                m.update(data)
        return m.hexdigest()


    def direct_update(self):
        if path.exists(path.join(self.CWD, psutil.Process().name()+".bak")):
            os.remove(path.join(self.CWD, psutil.Process().name()+".bak"))
        if self.get_web_file_md5(self.DIRECT_URL) == self.get_local_file_md5(path.join(self.CWD, psutil.Process().name())):
            return
        os.rename(path.join(self.CWD, psutil.Process().name()), path.join(self.CWD, psutil.Process().name()+".bak"))
        self.download(self.DIRECT_URL, path.join(self.CWD, psutil.Process().name()))
        os.chmod(path.join(self.CWD, psutil.Process().name()),
                 stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        self.restart()

    def check_update(self):
        # 如果直接给出直链下载
        if self.DIRECT_URL:
            self.direct_update()
            return
        if path.exists(self.LOCAL_VERSION_INFO_JSON_PATH):
            f = open(self.LOCAL_VERSION_INFO_JSON_PATH, "rb")
            file_content = f.read()
            f.close()
            self.local_version_info = json.loads(file_content)
        else:
            f = open(self.LOCAL_VERSION_INFO_JSON_PATH, "w")
            f.write(json.dumps(self.local_version_info))
            f.close()

        if self.MODE == "check_on_start":
            self.check_on_start()
        elif self.MODE == "check_on_time":
            self.check_on_time()
        elif self.MODE == "no_check":
            self.LOGGER.debug("no check for update")
        else:
            raise Exception("mode参数错误")

    def check_on_start(self):
        # 如果当前的local_version_info.version是NONE,则必须更新
        if self.local_version_info.get("version", None) is None:
            self.FORCE = True
        resp = requests.get(self.URL)
        cloud_version_info = json.loads(resp.content)
        cloud_version = cloud_version_info.get("version")
        self.FORCE = cloud_version_info.get("force", False)
        self.LOGGER.info(cloud_version_info)

        if self.need_update(cloud_version):
            self.LOGGER.info("need")
            self.update(cloud_version_info)

    def check_on_time(self):
        pass

    def need_update(self, cloud_version) -> bool:
        if self.local_version_info.get("version", None) is None:
            return True
        local_version: str = self.local_version_info.get("version")
        return cloud_version > local_version and self.FORCE

    def update(self, cloud_version_info):
        if self.UPDATE_MODE == "silent":
            self.silent_update(cloud_version_info)
        elif self.UPDATE_MODE == "graphic":
            self.graphic_update(cloud_version_info)
        else:
            raise Exception("update_mode参数错误")

    def restart(self):
        exe = sys.executable
        os.execl(exe, *sys.argv)

    def silent_update(self, cloud_version_info):
        filename = cloud_version_info.get("filename", None)
        md5_text = cloud_version_info.get("md5", None)
        assert filename != None
        # 重命名，由于windows不支持运行的时候删除自己
        self.LOGGER.info("重命名源文件")
        if path.exists(path.join(self.CWD, filename+".bak")):
            os.remove(path.join(self.CWD, filename+".bak"))
        os.rename(path.join(self.CWD, filename),
                  path.join(self.CWD, filename+".bak"))
        assert cloud_version_info.get("download_url") != None
        self.download(cloud_version_info.get("download_url"), path.join(self.CWD, filename), md5_text)
        self.local_version_info = cloud_version_info
        os.chmod(path.join(self.CWD, filename),
                 stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        f = open(self.LOCAL_VERSION_INFO_JSON_PATH, "w")
        f.write(json.dumps(self.local_version_info))
        f.close()
        self.LOGGER.info(psutil.Process().cmdline())
        self.LOGGER.info(psutil.Process().name())
        self.LOGGER.info("更新完成,重启程序")
        if self.NEED_RESTART:
            self.restart()

    def graphic_update(self, cloud_version_info):
        pass

    def download(self, url, f, md5_text=None):
        check_md5 = md5_text is not None
        m = hashlib.md5()
        with open(f, "wb") as f:
            resp = requests.get(url, stream=True)
            content_length = resp.headers["Content-Length"]
            content_length = int(content_length)
            count = 0
            for i in resp.iter_content(chunk_size=1024):
                if i:
                    count += len(i)
                    f.write(i)
                    m.update(i)
                    if self.CALLBACK is not None:
                        self.CALLBACK(content_length, count)
            if m.hexdigest() != md5_text and check_md5:
                raise Exception("文件损坏，重新下载")
