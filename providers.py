# -*- coding: utf-8 -*-

import eventparser
import entities

##
## Provider base blass
##
class Provider(object): 
    connection_name = 'none'
    connection_port = 'none'    

    def __init__(self, conn_name='', conn_port=''):
        self.connection_name = conn_name
        self.connection_port = conn_port

    def close(self):
        pass  
        
    def open(self):
        pass
    
    def parse(self, row):
        pass
    
    def read(self):
        pass

##
## FIX log provider
##      
class FIXLogProvider(Provider):
    fd = 0x00
    message_types = ['D','F','G','8']
    
    def __init__(self, conn_name='', conn_port=''):
        Provider.__init__(self, conn_name, conn_port)

    def close(self):
        Provider.close(self)
        self.fd.close()
    
    def open(self):
        Provider.open(self)
        self.fd = open(self.connection_name, 'r')
        
    def parse(self, row):
        rowdict = {}
        
        timestamp, body = row.split(' : ')        
        try:
            for element in body.split('\x01'):
                try:
                    tag, val = element.split('=')
                    rowdict[tag] = val
                except:
                    pass
        except:
            pass
            
        # Filtro por tipo de mensagem    
        if  rowdict.has_key('35') and rowdict['35'] in self.message_types:
            rowdict['timestamp'] = timestamp            
            return(rowdict)
        else:
            return({})
                    
    def read(self):
        Provider.read(self)        
        rows = []
        for row in self.fd:
            parsed = self.parse(row)
            if parsed != {}:
                rows.append(parsed)
        return rows

##
## Apama provider
##    
class ApamaProvider(Provider):
    
    def parse(self, event):
        # Extract event type and payload from event        
        try:
            i = event.index('(')
            eventtype = event[0:i]
            payload = event[i+1:len(event)-2]
        except:
            eventtype = None
            payload = None

        # Creates a parser for the event type        
        parser = eventparser.Factory().create(eventtype)
        elements = parser.parse(payload)
        
        return eventtype, elements
    
    # Process Apama events        
    def process(self, event):
        
        # Black list
        # Strings to be discarded
        try:
            event.index('BATCH')
            return None,None
        except ValueError:
            pass
        
        eventtype, body = self.parse(event)
        return eventtype, body
    
    def produceOrder(self, body):
        order = entities.Order(body['orderId'], 
                               body['extra']['timestamp'],
                               '',
                               '', 
                               body['symbol'], 
                               body['side'],
                               body['type'])
        return order
    
    def prodiceOrderEvent(self, eventtype, body):
        pass
    