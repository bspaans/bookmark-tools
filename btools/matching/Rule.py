class Rule:

    def __init__(self, bookmark = "", weight = 1.0, text = "", 
                 match_func = None, match_token = ""):
        self.bookmark = bookmark
        self.weight = weight
        self.text = text
        self.match_func = match_func
        self.match_token = match_token

    def weigh(self, file, variables):
        if self.match_func is not None and self.match_func(file, variables):
            return self.weight
        return 0.0

    def __str__(self):
        return "%s matches %s %s (weight = %f)" % (self.bookmark, 
                                                   self.match_token, 
                                                   self.text, 
                                                   self.weight)

    def __repr__(self):
        return self.__str__()   
