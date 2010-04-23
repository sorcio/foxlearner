from pygame.colordict import THECOLORS

class ColorsDict(object):
    def __init__(self, dic):
        self.dic = dic
        
    def __getitem__(self, name):
        return self.dic[name.lower()]

colors = ColorsDict(THECOLORS)
