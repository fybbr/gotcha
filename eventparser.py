# -*- coding: utf-8 -*-

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
    
    def parsesequence(self, seq):
        try:
            seq.index('[')
            seq.index(']')
            s = seq[1:len(seq)-1]
            return(s.split(','))
        except ValueError:
            return None
            
    def parsedict(self, dic):
        try:
            dic.index('{')
            dic.index('}')
            d = dic[1:len(dic)-1]
            retdic = {}
            try:
                for e in d.split(','):
                    try:
                        tag, value = e.split(':')
                        retdic[tag.strip('"')] = value.strip('"')
                    except:
                        pass
            except:
                pass
            return retdic
        except ValueError:
            return None


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
        
        f,l = self.car(l)
        d['extra'] = self.parsedict(f)
        
        return d
        
class ApamaCancelOrder(EventParser):
    def parse(self, payload):
        EventParser.parse(self, payload)
        d = {}
        
        f,l = self.car(payload)
        d['Id'] = f
        
        f,l = self.car(l)
        d['serviceId'] = f
        
        f,l = self.car(l)
        d['extra'] = self.parsedict(f)
        
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
        
        f,l = self.car(l)
        d['extra'] = self.parsedict(f)
        
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
        
        f,l = self.car(l)
        d['extra'] = self.parsedict(f)
        
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
        
        f,l = self.car(l)
        d['NoPartyIDs'] = self.parsesequence(f)
        
        f,l = self.car(l)
        d['ContraBroker'] = self.parsesequence(f)
        
        f,l = self.car(l)
        d['Timestamps'] = self.parsedict(f)
        
        f,l = self.car(l)
        d['Extra'] = self.parsedict(f)

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
        
        f,l = self.car(l)
        d['NoPartyIDs'] = self.parsesequence(f)
        
        f,l = self.car(l)
        d['Timestamps'] = self.parsedict(f)
        
        f,l = self.car(l)
        d['Extra'] = self.parsedict(f)

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
        d['OrderID'] = f
        
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
        
        f,l = self.car(l)
        d['Timestamps'] = self.parsedict(f)
        
        f,l = self.car(l)
        d['Extra'] = self.parsedict(f)
        
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
        d['OrderID'] = f
        
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
        
        f,l = self.car(l)
        d['Timestamps'] = self.parsedict(f)
        
        f,l = self.car(l)
        d['Extra'] = self.parsedict(f)
        
        return d

