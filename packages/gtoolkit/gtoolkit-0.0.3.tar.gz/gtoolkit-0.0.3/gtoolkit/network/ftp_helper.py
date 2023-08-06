"""
    包含 ftp 连接与下载器的方法
    这里下载文件有三个函数
        download_file：直接下载某个文件
        download_file_list：下载文件列表
        download_dir：下载某个目录（支持正则筛选文件）
    
    示例
        # 使用连接
        ftp_conn = FTPConn(host='', port=21, user='', pwd='')
        conn = ftp_conn.create_connection()

        # 下载文件
        ftp_down = FTPDownloader(ftp=ftp_conn, download_path='./test')
        ftp_down.download_file()
        ftp_down.download_file_list()
        ftp_down.download_dir(ftp_dir='', pattern=r'')
"""
import os
import re
import ftplib
import traceback
from ftplib import FTP
from pathlib import Path
from loguru import logger
from typing import Callable, List
from concurrent.futures import ThreadPoolExecutor


# 重写读取文件的方法
class MyFTP(FTP):
    def __init__(self):
        super().__init__()

    def show_dir(self, *args):
        """
        重写原来的 dir 方法

        :param args:
        :return:
        """
        cmd = 'LIST'
        line_list = []
        if args[-1:] and type(args[-1]) != type(''):
            args, func = args[:-1], args[-1]
        for arg in args:
            if arg:
                cmd = cmd + (' ' + arg)
        self.retrlines(cmd, line_list.append)

        out_list = []
        for line in line_list:
            result = re.findall(r'[a-z-]+ +\d+ +\w+ +\w+ +\d+ +\w+ +\d+ +[0-9:]+ +(.+)', line)[0]
            if result and result not in ['.', '..']:
                out_list.append(result.strip())
        return out_list


# ftp 连接
class FTPConn:
    def __init__(self, host: str, port: int, user: str, pwd: str, timeout: int = None, encoding: str = None):
        """

        :param host:
        :param port:
        :param user:
        :param pwd:
        :param timeout: 超时时间
        :param encoding: 编码
        """
        self.host = host
        self.port = port
        self.user = user
        self.passwd = pwd
        self.timeout = timeout or 30
        self.encoding = encoding or 'gbk'

        self.conn_list = []

    def create_connection(self) -> MyFTP:
        """
        创建连接

        :return:
        """
        ftp = MyFTP()
        ftp.set_pasv(True)
        ftp.encoding = self.encoding
        ftp.timeout = self.timeout
        ftp.connect(host=self.host, port=self.port)
        ftp.login(user=self.user, passwd=self.passwd)

        self.conn_list.append(ftp)

        return ftp

    def close(self, conn: MyFTP):
        """
        关闭连接

        :param conn:
        :return:
        """
        try:
            conn.close()
        except:
            pass
        finally:
            return self.conn_list.remove(conn)

    def close_all(self):
        """
        关闭所有 ftp 连接

        :return:
        """
        for conn in self.conn_list:
            self.close(conn)

    def __del__(self):
        self.close_all()


# 下载文件
class FTPDownloader:
    def __init__(self, ftp: FTPConn, download_path: str, thread: int = 1, max_retry: int = 3,
                 keep_structure: bool = True, failed_callback: Callable = None):
        """

        :param ftp: ftp 连接
        :param thread: 下载线程数
        :param max_retry: 最大下载重试次数
        :param failed_callback: 失败回调函数
        :param download_path: 下载文件夹
        :param keep_structure: 保留目录结构：在 download_path 基础上，后续目录结构与 ftp 一致（默认保留）
        """
        self.ftp = ftp
        self.thread = thread
        self.max_retry = max_retry
        self.failed_callback = failed_callback or self.default_callback
        self.download_path = download_path
        self.keep_structure = keep_structure

        self.file_list = []
        Path(download_path).mkdir(parents=True, exist_ok=True)

    def download_file(self, ftp_path: str, conn: MyFTP = None) -> bool:
        """
        下载指定文件

        :param ftp_path: 待下载文件路径
        :param conn: ftp 连接
        :return: 下载是否成功的布尔值
        """

        retry = 0
        while retry < self.max_retry:
            try:
                if conn is None:
                    conn = self.ftp.create_connection()
                return self._downloader(ftp_path=ftp_path, conn=conn)
            except Exception as e:
                retry += 1
                traceback.print_exc()

            if retry >= self.max_retry:
                self.failed_callback(ftp_path, False)

    def download_file_list(self, ftp_path_list: list, conn_list: List[MyFTP] = None):
        """
        循环下载文件列表

        :param conn_list: ftp 连接列表
        :param ftp_path_list: 待下载文件路径列表
        """
        if conn_list is None:
            conn_list = [self.ftp.create_connection() for _ in range(self.thread)]

        with ThreadPoolExecutor(self.thread) as t:
            index = 0
            for ftp_path in ftp_path_list:
                t.submit(self.download_file, ftp_path, conn_list[index])

                if index + 1 == len(conn_list):
                    index = 0
                else:
                    index += 1

    def download_dir(self, ftp_dir: str, pattern: str = None):
        """
        循环遍历文件夹，然后挨个下载文件，已下载的不会重复下载，但是会校验

        :param ftp_dir: 文件夹路径
        :param pattern: 通过正则进行筛选
        :return:
        """
        conn = self.ftp.create_connection()
        self.find_file(ftp_dir, conn, pattern)

        conn_list = [self.ftp.create_connection() for _ in range(self.thread - 1)]
        conn_list.append(conn)

        self.download_file_list(self.file_list, conn_list)

    def find_file(self, ftp_dir: str, conn: MyFTP = None, pattern: str = None):
        """
        循环遍历文件夹，寻找文件

        :param conn: ftp 连接
        :param ftp_dir: 文件夹路径
        :param pattern: 通过正则进行筛选
        :return:
        """
        if conn is None:
            conn = self.ftp.create_connection()

        # 切换目录并遍历当前目录的文件、文件夹
        conn.cwd(ftp_dir)
        file_list = conn.nlst()
        dir_list = conn.show_dir()
        dir_list = list(set(dir_list).difference(set(file_list)))

        # 文件夹则循环遍历
        for dir1 in dir_list:
            path = ftp_dir + '/' + dir1
            logger.info(path)
            self.find_file(path, conn, pattern)

        # 文件则加入待下载
        for file in file_list:
            ftp_path = ftp_dir + '/' + file

            # 文件筛选
            if pattern:
                if re.search(pattern, ftp_path):
                    self.file_list.append(ftp_path)
                continue

            self.file_list.append(ftp_path)

    def _downloader(self, ftp_path: str, conn: MyFTP) -> bool:
        """
        下载指定文件

        :param ftp_path: 待下载文件路径
        :return:
        """
        # 切换文件目录，并构造目录
        file_name = str(Path(ftp_path).name)  # 文件名
        file_remote_parent_path = str(Path(ftp_path).parent).replace('\\', '/')  # 远程文件父目录
        if self.keep_structure:
            file_download_path = str(Path(self.download_path).joinpath(ftp_path[1:]))  # 本地文件目录
            Path(file_download_path).parent.mkdir(parents=True, exist_ok=True)  # 创建本地保存目录
        else:
            file_download_path = str(Path(self.download_path).joinpath(file_name))  # 本地文件目录
        conn.cwd(file_remote_parent_path)

        # 检测是否需要断点续传
        if os.path.exists(file_download_path):
            f = open(file_download_path, 'ab')
            logger.info(f'本地文件存在将断点续传：{file_download_path}')
        else:
            f = open(file_download_path, 'wb')
            logger.info(f'正在下载：{file_download_path}')

        # 下载文件
        not_found = False
        try:
            file_download_size = os.path.getsize(file_download_path)
            conn.retrbinary(cmd='RETR ' + file_name, callback=f.write, rest=file_download_size)
            logger.info(f'下载完成：{ftp_path}')
            return True
        except ftplib.error_perm as e:
            if 'No such file or directory' not in str(e):
                raise e
            not_found = True
        finally:
            f.close()
            if not_found:
                os.unlink(file_download_path)

    @staticmethod
    def default_callback(ftp_path: str):
        logger.info(f'下载失败：{ftp_path}')
