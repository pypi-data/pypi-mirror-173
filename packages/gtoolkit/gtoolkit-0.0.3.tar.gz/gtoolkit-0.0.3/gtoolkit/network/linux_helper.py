"""
    linux 文件的上传下载
    
    上传：需要含文件名的本地路径
    下载：需要含文件名的远程路径
"""
import time
import paramiko
from pathlib import Path
from loguru import logger


class LinuxSSH:
    def __init__(self, hostname: str, port: int, username: str, password: str):
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password

    # 普通连接
    def get_ssh_con(self):
        ssh = paramiko.SSHClient()
        policy = paramiko.AutoAddPolicy()
        ssh.set_missing_host_key_policy(policy)

        # 链接服务器
        ssh.connect(
            hostname=self._hostname,
            port=self._port,
            username=self._username,
            password=self._password
        )

        return ssh

    # 文件传输专用连接
    def get_ssh_file_con(self):
        ssh = paramiko.Transport((self._hostname, self._port))
        ssh.connect(username=self._username, password=self._password)
        transfer = paramiko.SFTPClient.from_transport(ssh)

        return ssh, transfer

    # 远程执行命令：多个命令用 ; 隔开
    def send_cmd(self, cmd):
        ssh = self.get_ssh_con()
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read().decode()
        stderr = stderr.read().decode()
        ssh.close()
        if stderr:
            return
        return result

    def upload(self, local_path: str, linux_path: str):
        """
        上传文件：都含有文件名
        
        :param local_path: 本地路径含文件名
        :param linux_path: linux 含文件名
        :return:
        """
        # 构造数据
        start_time = time.time()
        file_name = str(Path(linux_path).name) if str(Path(linux_path).suffix) else None
        if file_name is None:
            file_name = str(Path(local_path).name)
        linux_path = linux_path.replace('\\', '/')
        if Path(linux_path).suffix:
            linux_folder = str(Path(linux_path).parent).replace('\\', '/')
        else:
            raise Exception('linux 路径需含文件名！')

        # 先判断路径是否存在
        exists = self.send_cmd(f'cd {linux_folder};')
        if exists is None:
            self.send_cmd(f'mkdir -p {linux_folder};')

        # 再判断文件是否存在
        exists = self.send_cmd(f'cd {linux_folder};find {file_name}')
        if exists:
            self.send_cmd(f'cd {linux_folder};rm -rf {file_name}')
            time.sleep(1)

        # 上传
        ssh, transfer = self.get_ssh_file_con()
        try:
            transfer.put(localpath=local_path, remotepath=linux_path)
            transfer.close()
            logger.info(f'上传成功：{linux_path}\t耗时：{time.time() - start_time}')
            return True
        finally:
            ssh.close()

    # 下载：
    def download(self, linux_path: str, local_path: str, save_structure=False, remove_structure: str = ''):
        """

        :param linux_path: linux 路径含文件名
        :param local_path: 本地路径 含不含文件名都可以
        :param save_structure: 保存路径结构
        :param remove_structure: linux 路径结构需要去除的部分
        :return:
        """
        # 构造数据
        new_file_name = str(Path(local_path).name) if str(Path(local_path).suffix) else None
        if new_file_name is None:
            local_path = Path(local_path).absolute().parent
        else:
            local_path = Path(local_path).absolute()
        linux_path = str(Path(linux_path)).replace('\\', '/')
        linux_folder = str(Path(linux_path).parent).replace('\\', '/')
        remove_structure = str(Path(remove_structure)).replace('\\', '/')
        file_name = str(Path(linux_path).name)

        # 创建本地文件夹
        if save_structure:
            structure = linux_folder.replace(remove_structure, '').strip('/')
            local_path = str(Path(local_path).joinpath(structure))
        if new_file_name:
            local_file_path = str(Path(local_path).joinpath(new_file_name))
        else:
            local_file_path = str(Path(local_path).joinpath(file_name))
        Path(local_path).mkdir(parents=True, exist_ok=True)

        # 删除本地已存在文件
        if Path(local_file_path).exists():
            Path(local_file_path).unlink(missing_ok=True)

        # 下载到本地
        exists = self.send_cmd(f'cd {linux_folder};find {file_name}')
        if exists:
            ssh, transfer = self.get_ssh_file_con()
            transfer.get(remotepath=linux_path, localpath=local_file_path)
            transfer.close()
            logger.info(f'下载成功：{local_file_path}')
        else:
            logger.warning(f'文件不存在：{linux_path}')
