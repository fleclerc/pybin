import json

class LiquidationOrder:

    def __init__(self):
        self.symbol = ""
        self.side = ""
        self.type = ""
        self.timeInForce = ""
        self.origQty = 0.0
        self.price = 0.0
        self.averagePrice = 0.0
        self.orderStatus = ""
        self.lastFilledQty = 0.0
        self.lastFilledAccumulatedQty = 0.0
        self.time = 0
    def toJSON(self):
        return self.__dict__

class LiquidationOrderEvent:

    def __init__(self):
        self.eventType = ""
        self.eventTime = 0
        self.data = None

    @staticmethod
    def json_parse(json_wrapper):
        result = LiquidationOrderEvent()
        result.eventType = json_wrapper.get_string("e")
        result.eventTime = json_wrapper.get_int("E")
        data = json_wrapper.get_object("o")
        element = LiquidationOrder()
        element.symbol = data.get_string("s")
        element.side = data.get_string("S")
        element.type = data.get_string("o")
        element.timeInForce = data.get_string("f")
        element.origQty = data.get_float("q")
        element.price = data.get_float("p")
        element.averagePrice = data.get_float("ap")
        element.orderStatus = data.get_string("X")
        element.lastFilledQty = data.get_float("l")
        element.lastFilledAccumulatedQty = data.get_float("z")
        element.time = data.get_int("T")
        result.data = element
        return result

    def toJSON(self):
        d = self.__dict__.copy()
        d['data'] = d['data'].toJSON()
        return d
        #return json.dumps(self, default=lambda o: o.__dict__, 
        #    sort_keys=True, indent=4)        