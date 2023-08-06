import random


class RandomListOrDictGenerator() :
    """
        -   This object is used to automatically generate a list or a dictionary according to the size you specify.
        -   This size is defined at the instantiation of the object.
        -   By default, it generates a list or a dictionary of 5 elements.
        -   You can also specify the size of the list or dictionary when calling the method.
        -   You can also specify the size of keys/values when instantiating or calling the object
        
        examples : 
            #Instantiation with default parameters
            rd_ld = RandomListOrDictionnary(size=5, key_length=3, values_length=5)
            #We can specify the size
            my_list = rd_ld.createRandomDictionnary(3)
            my_dict = rd_ld.createRandomList(3)
    """
    
    def __init__(self, size=5, key_length=(random.randint(3,10)), values_length=(random.randint(3,10))):
        self.size = size
        self.key_length = key_length
        self.values_length = values_length
        
        
        
    def returnRandomString(self, size=10) :
        """Return random string with size that you have specified"""
        alpha_numeric = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = random.choices(alpha_numeric, k=(random.randint(3, size)))
        return "".join(key)
    
    
    def createRandomDictionnary(self, dict_size=None) :
        """Return random dictionary with size that you have specified"""
        dic = {}
        s = dict_size or self.size

        for i in range(s) :
            key = self.returnRandomString(self.key_length or 10)    
            value = self.returnRandomString(self.values_length or 10)
            dic[key] = value
        return dic
    
    
    def createRandomList(self, list_size=None) :
        """Return random list with size that you have specified"""
        list = []
        s = list_size or self.size

        for i in range(s) :   
            value = self.returnRandomString(self.values_length or 10)
            list.append(value)
        return list
    
# rld = RandomListOrDictionnary(10)

# print(rld.createRandomDictionnary())
# print(rld.createRandomList())
