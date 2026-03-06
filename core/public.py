import os
import shutil
import stat
import sys
import logging
from pydantic import BaseModel
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(BASE_DIR)
from core import logging_conf
logging_conf.init_logging()

load_dotenv()   

class Config(BaseModel):
    """配置文件"""
    local_dir: str
    ydnote_dir: str
    smms_secret_token: str
    is_relative_path: bool = True
    del_spare_file: bool = True
    del_spare_dir: bool = True
    

class CookiesConfig(BaseModel):
    ynote_cstk: str
    ynote_login: str
    ynote_sess: str

def load_cookies() -> CookiesConfig:
    """加载 cookies"""
    cookies_config = CookiesConfig(
        ynote_cstk=os.getenv('YNOTE_CSTK'),
        ynote_login=os.getenv('YNOTE_LOGIN'),
        ynote_sess=os.getenv('YNOTE_SESS')
    )

    return cookies_config


def load_config() -> Config:
    config = Config(
        local_dir=os.getenv('LOCAL_DIR'),
        ydnote_dir=os.getenv('YDNOTE_DIR'),
        smms_secret_token=os.getenv('SMMS_SECRET_TOKEN'),
        is_relative_path=os.getenv('IS_RELATIVE_PATH'),
        del_spare_file=os.getenv('DEL_SPARE_FILE'),
        del_spare_dir=os.getenv('DEL_SPARE_DIR')
    )
    return config

def remove_readonly(func, path, _):
    """清除只读属性后重试删除"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def delete_folder(folder_path):
    """安全删除只读文件夹（包含子目录和文件）"""
    try:
        # 递归删除，遇到错误时调用remove_readonly处理
        shutil.rmtree(folder_path, onerror=remove_readonly)
    except Exception as e:
        logging.error(f"文件夹删除失败: {e}")

if __name__ == '__main__':
    print(load_config())
    print(load_cookies())