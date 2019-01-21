from Serialize.bean import Bean

from Serialize.clas import Clas

try:
    import cPickle as pickle
except ImportError:
    import pickle


def serialize(obj):
    """
    持久化对象
    """
    f = open('dump.txt', 'wb')
    pickle.dump(obj, f)
    f.close()


def deserialize():
    """
    解析持久化对象
    """
    f = open('dump.txt', 'rb')
    obj = pickle.load(f)
    return obj


def serializeClass(c):
    """
    持久化类
    """
    f = open('dump2.txt', 'wb')
    pickle.dump(c, f)
    f.close()


def deserializeClass():
    """
    解析持久化类
    """
    f = open('dump2.txt', 'rb')
    c = pickle.load(f)
    return c


if __name__ == '__main__':
    # 持久化对象
    obj = Bean(x=2, y=4)
    serialize(obj)
    # 解析持久化对象
    obj2 = deserialize()
    print(obj2.getX())
    print(obj2.getY())

    # 持久化类
    serializeClass(Clas)
    # 解析持久化类
    clas = deserializeClass()
    print(clas.klassmeth('test1'))
    print(clas.statmeth('test2'))
