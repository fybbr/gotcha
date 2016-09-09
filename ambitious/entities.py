# -*- coding: utf-8 -*-

class Order:
    orderId = ''
    timestamp = ''
    exchange = ''
    route = ''    
    symbol = ''
    side = ''
    type = ''
    price = 0.0
    quantity = 0
    history = []    

    def __init__(self, orderID, timestamp, exchange, route, symbol, side, type, price, quantity):
        self.orderId = orderID
        self.timestamp = timestamp
        self.exchange = exchange
        self.route = route
        self.symbol = symbol
        self.side = side
        self.type = type
        self.price = price
        self.quantity = quantity
    
class OrderEvent:
    orderId = ''    
    timestamp = 0.0
    evttype = ''
    evtorigim = ''
    body = {}
    
    def __init__(self, orderId, timestamp, evttype, evtorigin, body):
        self.orderId = orderId
        self.timestamp = timestamp
        self.evttype = evttype
        self.evtorigin = evtorigin
        self.body = body
    