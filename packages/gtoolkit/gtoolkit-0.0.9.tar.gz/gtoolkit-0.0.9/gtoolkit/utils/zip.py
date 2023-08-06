"""
    压缩文件、文件夹
    解压压缩包

    注意：rar 需要额外配置，所以这里不提供
"""
import os
import zipfile
from pathlib import Path


class ZipHelper:
    def __init__(self, path: str):
        self.path = Path(path)

    def to_zip(self, save_path: str = None):
        """
        压缩目标

        :param save_path: 保存的地址，默认为压缩文件、文件夹的父目录
        :return:
        """
        if self.path.suffix.lower() == '.zip':
            return

        file_name = self._get_zip_name()
        save_path = Path(save_path) or self.path.parent
        save_path.mkdir(parents=True, exist_ok=True)
        file_path = save_path.joinpath(file_name)

        if self.path.is_dir():
            with zipfile.ZipFile(file_path, 'w') as z:
                for root, dirs, files in os.walk(self.path):
                    for file in files:
                        z.write(Path(root).joinpath(file), Path(root.replace(str(self.path), '')).joinpath(file))
        else:
            with zipfile.ZipFile(file_path, 'w') as z:
                z.write(self.path, self.path.name)

    def unpack_zip(self, unpack_path: str = None):
        """
        解压文件

        :param unpack_path:
        :return:
        """
        if self.path.suffix.lower() != '.zip':
            return

        unpack_path = Path(unpack_path) or self.path.parent
        unpack_path = unpack_path.joinpath(self.path.name.split('.')[0])
        unpack_path.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(self.path, 'r') as z:
            z.extractall(unpack_path)

    def _get_zip_name(self):
        """
        返回 zip 时的名字

        :return:
        """
        if self.path.is_dir():
            return self.path.name + '.zip'
        else:
            return self.path.name.split('.')[0] + '.zip'
