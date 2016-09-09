# -*- coding: utf-8 -*-

import ast

class Factory:
    def create(self, eventtype):
        if eventtype == 'com.apama.fix.ExecutionReport':
            return FIXExecutionReport()
        elif eventtype == 'com.apama.oms.OrderUpdate':
            return (ApamaOrderUpdate())
        elif eventtype == 'com.apama.fix.NewOrderSingle':
            return FIXNewOrderSingleParser()
        elif eventtype == 'com.apama.oms.NewOrder':
            return (ApamaNewOrder())
        elif eventtype == 'com.apama.fix.OrderCancelReplaceRequest':
            return FIXOrderCancelReplaceRequest()
        elif eventtype == 'com.apama.oms.AmendOrder':
            return (ApamaAmendOrder())
        elif eventtype == 'com.apama.fix.OrderCancelRequest':
            return FIXOrderCancelRequest()
        elif eventtype == 'com.apama.oms.CancelOrder':
            return (ApamaCancelOrder())
        else:
            return None

class EventParser:
    # Receives a string list separated by comma, then returns the 1st element and the rest    
    def car(self, list):
        startpos = 0
        try:
            if list[0] == '[':
                try:
                    startpos = list.index(']')
                except ValueError:
                    return None,None
                    
            elif list[0] == '{':
                try:
                    startpos = list.index('}')
                except ValueError:
                    return None,None
                    
            i = list.index(',', startpos)
            first = list[0:i]
            rest = list[i+1:len(list)]
            return first, rest
        except ValueError:
            return list,None
        
    def parse(self, payload):
        pass
    
    # Parses any python data structure delimited by 'openchar' and
    # 'closerchar'. The data structure must start at position zero
    # of string 's' and the return will be the parsed structure, such
    # as a list or a dictionary, and the remaining of the string 's'.
    def parsestruct(self, s, openchar, closerchar):
        endsAT = self.findouterdelimiter(s, 0, 1, openchar, closerchar)
        
        # Unbalance delimiters
        if endsAT < 0:
            return None, s
        
        first = ast.literal_eval(s[0:endsAT+1])
        rest = s[endsAT+2:]
        return first, rest
    
    # Almost like parsestruct, but instead of return the parsed data
    # structure will simple discard it and will return just the
    # remaining.    
    def skipstruct(self, s, openchar, closerchar):
        endsAT = self.findouterdelimiter(s, 0, 1, openchar, closerchar)
        
        # Unbalance delimiters
        if endsAT < 0:
            return s
            
        return s[endsAT+2:]

    # Returns the position of the outer delimiter. Must be called
    #  as findouterdelimiter(string, 0, 1) and string must start
    # with the open delimiter.
    def findouterdelimiter(self, s, endpos, counter, openchar, closerchar):
        if counter == 0:
            return endpos   
        # Chegou ao final da string e não casou    
        if len(s) == 1:
            return -1    
        if s[1] == openchar:
            return self.findouterdelimiter(s[1:], endpos+1, counter+1, openchar, closerchar)    
        elif s[1] == closerchar:
            return self.findouterdelimiter(s[1:], endpos+1, counter-1, openchar, closerchar)     
        else:
            return self.findouterdelimiter(s[1:], endpos+1, counter, openchar, closerchar)


class ApamaAmendOrder(EventParser):
    def parse(self, payload):
        EventParser.parse(self, payload)
        d = {}
        
        f,l = self.car(payload)
        d['orderId'] = f
        
        f,l = self.car(l)
        d['serviceId'] = f
        
        f,l = self.car(l)
        d['symbol'] = f
        
        f,l = self.car(l)
        d['price'] = float(f)
        
        f,l = self.car(l)
        d['side'] = f
        
        f,l = self.car(l)
        d['type'] = f
        
        f,l = self.car(l)
        d['quantity'] = float(f)
        
        d['extra'], l = self.parsestruct(l, '{', '}')
        
        d['origin'] = 'Apama'
        
        return d
        
class ApamaCancelOrder(EventParser):
    def parse(self, payload):
        EventParser.parse(self, payload)
        d = {}
        
        f,l = self.car(payload)
        d['orderId'] = f
        
        f,l = self.car(l)
        d['serviceId'] = f
        
        d['extra'], l = self.parsestruct(l, '{', '}')
        
        d['origin'] = 'Apama'
        
        return d

class ApamaOrderUpdate(EventParser):
    def parse(self, payload):
        EventParser.parse(self, payload)
        d = {}
        
        f,l = self.car(payload)
        d['orderId'] = f
        
        f,l = self.car(l)
        d['symbol'] = f

        f,l = self.car(l)
        d['price'] = float(f)        
        
        f,l = self.car(l)
        d['side'] = f
        
        f,l = self.car(l)
        d['type'] = f        
        
        f,l = self.car(l)
        d['quantity'] = float(f)
        
        f,l = self.car(l)
        d['inMarket'] = bool(f)
        
        f,l = self.car(l)
        d['isVisible'] = bool(f)        
        
        f,l = self.car(l)
        d['modifiable'] = bool(f)        
        
        f,l = self.car(l)
        d['cancelled'] = bool(f)
        
        f,l = self.car(l)
        d['orderChangeRejected'] = bool(f)        
        
        f,l = self.car(l)
        d['externallyModified'] = bool(f)
        
        f,l = self.car(l)
        d['unknownState'] = bool(f)
        
        f,l = self.car(l)
        d['merketOrderId'] = f
        
        f,l = self.car(l)
        d['qtyExecuted'] = float(f)
        
        f,l = self.car(l)
        d['qtyRemaining'] = float(f)
        
        f,l = self.car(l)
        d['lastShares'] = float(f)
        
        f,l = self.car(l)
        d['lastPrice'] = float(f)
        
        f,l = self.car(l)
        d['avgPrice'] = float(f)

        f,l = self.car(l)
        d['status'] = f
        
        d['extra'], l = self.parsestruct(l, '{', '}')
        
        d['origin'] = 'Apama'
        
        return d

class ApamaNewOrder(EventParser):
    def parse(self, payload):
        EventParser.parse(self, payload)
        d = {}
        
        f,l = self.car(payload)
        d['orderId'] = f
        
        f,l = self.car(l)
        d['symbol'] = f
        
        f,l = self.car(l)
        d['price'] = float(f)
        
        f,l = self.car(l)
        d['side'] = f
        
        f,l = self.car(l)
        d['type'] = f
        
        f,l = self.car(l)
        d['quantity'] = float(f)
        
        f,l = self.car(l)
        d['serviceId'] = f
        
        f,l = self.car(l)
        d['brokerId'] = f
        
        f,l = self.car(l)
        d['bookId'] = f
        
        f,l = self.car(l)
        d['marketId'] = f
        
        f,l = self.car(l)
        d['exchange'] = f
        
        f,l = self.car(l)
        d['ownerId'] = f
        
        d['extra'], l = self.parsestruct(l, '{', '}')
        
        d['origin'] = 'Apama'
        
        return d

class FIXExecutionReport(EventParser):
    def parse(self, payload):
        EventParser.parse(self, payload)
        d = {}

        f,l = self.car(payload)
        d['TRANSPORT'] = f
    
        f,l = self.car(l)
        d['SESSION'] = f
        
        f,l = self.car(l)
        d['OrderID'] = f
        
        f,l = self.car(l)
        d['ClOrdID'] = f
        
        f,l = self.car(l)
        d['OrigClOrdID'] = f
        
        f,l = self.car(l)
        d['ExecID'] = f
        
        f,l = self.car(l)
        d['ExecTransType'] = f
        
        f,l = self.car(l)
        d['ExecType'] = f
        
        f,l = self.car(l)
        d['OrdStatus'] = f
        
        f,l = self.car(l)
        d['Account'] = f
        
        f,l = self.car(l)
        d['Symbol'] = f
        
        f,l = self.car(l)
        d['Side'] = f
        
        f,l = self.car(l)
        d['OrderQty'] = float(f)
        
        f,l = self.car(l)
        d['OrdType'] = f
        
        f,l = self.car(l)
        d['Price'] = float(f)
        
        f,l = self.car(l)
        d['LastShares'] = float(f)
        
        f,l = self.car(l)
        d['LastPx'] = float(f)
        
        f,l = self.car(l)
        d['LeaveQty'] = float(f)
        
        f,l = self.car(l)
        d['CumQty'] = float(f)
        
        f,l = self.car(l)
        d['AvgPx'] = float(f)
        
        # Skip NoPartyIDs
        l = self.skipstruct(l, '[', ']')
        
        d['ContraBroker'], l = self.parsestruct(l, '[', ']')
        
        d['Timestamps'], l = self.parsestruct(l, '{', '}')
        
        d['extra'], l = self.parsestruct(l, '{', '}')
        
        d['origin'] = 'FIX'
        
        d['orderId'] = None
        
        return d

class FIXNewOrderSingleParser(EventParser):
    def parse(self, payload):
        EventParser.parse(self, payload)
        d = {}
        
        f,l = self.car(payload)
        d['TRANSPORT'] = f
    
        f,l = self.car(l)
        d['SESSION'] = f

        f,l = self.car(l)
        d['ClOrdID'] = f

        f,l = self.car(l)
        d['Account'] = f

        f,l = self.car(l)
        d['HandlInst'] = f
        
        f,l = self.car(l)
        d['Symbol'] = f

        f,l = self.car(l)
        d['Side'] = f

        f,l = self.car(l)
        d['TransactTime'] = f

        f,l = self.car(l)
        d['OrderQty'] = float(f)

        f,l = self.car(l)
        d['OrdType'] = f

        f,l = self.car(l)
        d['Price'] = float(f)
        
        # Skip NoPartyIDs
        l = self.skipstruct(l, '[', ']')
        
        d['Timestamps'], l = self.parsestruct(l, '{', '}')
        
        d['extra'], l = self.parsestruct(l, '{', '}')
        
        d['origin'] = 'FIX'

        return d

class FIXOrderCancelReplaceRequest(EventParser):
    def parse(self, payload):
        EventParser.parse(self, payload)
        d = {}
        
        f,l = self.car(payload)
        d['TRANSPORT'] = f
    
        f,l = self.car(l)
        d['SESSION'] = f
        
        f,l = self.car(l)
        d['orderId'] = f
        
        f,l = self.car(l)
        d['OrigClOrdID'] = f
        
        f,l = self.car(l)
        d['ClOrdID'] = f
        
        f,l = self.car(l)
        d['Account'] = f
        
        f,l = self.car(l)
        d['HandInst'] = f
        
        f,l = self.car(l)
        d['Symbol'] = f
        
        f,l = self.car(l)
        d['Side'] = f
        
        f,l = self.car(l)
        d['TransactionTime'] = f
        
        f,l = self.car(l)
        d['OrderQty'] = float(f)
        
        f,l = self.car(l)
        d['OrderType'] = f
        
        f,l = self.car(l)
        d['Price'] = float(f)
        
        d['Timestamps'], l = self.parsestruct(l, '{', '}')
        
        d['extra'], l = self.parsestruct(l, '{', '}')
        
        d['origin'] = 'FIX'
        
        return d

class FIXOrderCancelRequest(EventParser):
    def parse(self, payload):
        EventParser.parse(self, payload)
        d = {}
        
        f,l = self.car(payload)
        d['TRANSPORT'] = f
    
        f,l = self.car(l)
        d['SESSION'] = f
        
        f,l = self.car(l)
        d['OrigClOrdID'] = f
        
        f,l = self.car(l)
        d['orderId'] = f
        
        f,l = self.car(l)
        d['ClOrdID'] = f
        
        f,l = self.car(l)
        d['Account'] = f
        
        f,l = self.car(l)
        d['Symbol'] = f
        
        f,l = self.car(l)
        d['Side'] = f
        
        f,l = self.car(l)
        d['TransactionTime'] = f
        
        f,l = self.car(l)
        d['OrderQty'] = float(f)
        
        d['Timestamps'], l = self.parsestruct(l, '{', '}')
        
        d['extra'], l = self.parsestruct(l, '{', '}')
        
        d['origin'] = 'FIX'
        
        return d

