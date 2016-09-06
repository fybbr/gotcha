# -*- coding: utf-8 -*-

class Order:
    orderId = ''
    timestamp = ''
    exchange = ''
    route = ''    
    symbol = ''
    side = ''
    type = ''
    history = []    

    def __init__(self, orderID, timestamp, exchange, route, symbol, side, type):
        self.orderId = orderID
        self.timestamp = timestamp
        self.exchange = exchange
        self.route = route
        self.symbol = symbol
        self.side = side
        self.type = type
    
class OrderEvent:
    orderID = ''    
    timestamp = 0.0    
    evttype = 'umknow'
    body = {}
    
    def __init__(self, timestamp, evttype, body):
        self.timestamp = timestamp
        self.evttype = evttype
        self.body = body
    