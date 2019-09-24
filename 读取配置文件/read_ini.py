# coding: utf8
import configparser
import os

"""
读取ini配置文件
"""


class GetConfig:
    def __init__(self, ini_path):
        self.conf = self.createconf(ini_path)

    def createconf(self, ini_path):
        if 'ini' not in ini_path:
            raise 'The file of %s ini!!!' % ini_path
        curpath = os.path.dirname(os.path.realpath(__file__))
        cfgpath = os.path.join(curpath, r"..\config\\"+ini_path)
        if not os.path.exists(cfgpath):
            raise 'The file of %s it not exists!!!' % cfgpath
        # conf = configparser.ConfigParser()
        conf = configparser.RawConfigParser()
        try:
            conf.read(cfgpath, encoding='utf-8')
        except Exception as e:
            raise e
        return conf

    """
    返回确切的某个key的value
    """
    def getconf(self, section, key):
        try:
            value = self.conf.get(section, key)
            return value
        except Exception as e:
            raise '[ERROR]: %s' % e

    """
    适合较多的参数的场合，例如读取的是数据库配置，返回值类似元祖
    """
    def getsection(self, section):
        try:
            sectioninfo = self.conf[section]
            return sectioninfo
        except Exception as e:
            raise '[ERROR]: %s' % e
