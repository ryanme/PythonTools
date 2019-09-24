# coding: utf-8
# Author: ryan
# Time: 2019/08/13 0:01

"""
像java一样读取 *.properties配置
传递值支持a.b.c
"""


class PropertiesRead:

    def __init__(self, path):
        self.path = path
        self.property_dict = self.get_property()

    def property_dict_treat(self, key_name, value, property_dict):
        """
         递归
        :param key_name:
        :param value:
        :param property_dict:
        :return:
        """
        if key_name.find('.') > 0:
            key = key_name.split('.')[0]
            key_name_temp = key_name[len(key) + 1:]
            property_dict.setdefault(key, {})
            self.property_dict_treat(key_name_temp, value, property_dict[key])
        else:
            property_dict[key_name] = value

    def get_property(self):
        """
        组成字典
        :return:
        """
        property_dict = {}
        with open(self.path, 'r', encoding="UTF-8") as property_buffer:
            for line in property_buffer.readlines():
                line = line.strip().replace('\n', '')
                if line.find('=') and not line.startswith('#'):
                    sp = line.split('=')
                    key = sp[0].strip()
                    value = sp[1].strip()
                    self.property_dict_treat(key, value, property_dict)
        return property_dict

    def get(self, key, temp_property=None):
        """
         Give key name then return value.
        :param key:
        :param temp_property: 用来存储取多层字典值时中间过程的value
        :return:
        """
        if not temp_property:
            temp_property = self.property_dict
        if key.find('.') > 0:
            temp_key = key[len(key.split('.')[0])+1:]
            temp_property = temp_property[key.split('.')[0]]
            return self.get(temp_key, temp_property)   # 一定要return，否则递归return,最终值没有return,就会是None
        return temp_property.get(key)


if __name__ == "__main__":
    filepath = "sqlite3.properties"
    pr = PropertiesRead(filepath)
    print(pr.get('database.mysql.host_mysql'))
    print(pr.get('database_sqlite3'))

