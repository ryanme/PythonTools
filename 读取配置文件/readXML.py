# coding:utf8
import os
import xml.etree.cElementTree as cET


def get_value(filename, key):
    xmlFilePath = os.path.abspath(filename)
    if not os.path.exists(xmlFilePath):
        raise "Has no such file: %s" % xmlFilePath
    try:
        tree = cET.parse(xmlFilePath)
        root = tree.getroot()
    except Exception as e:
        raise "Errors:  %s"  % e
    dict1 = {}
    for child in root:
        tag = child.tag
        value = child.text
        value = value.replace("\\", "/")
        dict1[tag] = value
    try:
        value = dict1[key]
        return value
    except:
        raise "Has no key: %s" % key

if __name__ == "__main__":
    filename = input("文件名:")
    key = input("属性:")
    value = get_value(filename, key)
    print('The value of %s is %s' % (key, value))