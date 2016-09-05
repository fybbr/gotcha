# -*- coding: utf-8 -*-

##
## Provider base blass
##
class Provider(object): 
    connection_name = 'none'
    connection_port = 'none'    
    opmode = 'unknow'         

    def __init__(self, conn_name='', conn_port=''):
        self.connection_name = conn_name
        self.connection_port = conn_port

    def close(self):
        pass  
        
    def open(self):
        pass
    
    def parse(self, row):
        pass
    
    def read(self, From=''):
        pass

##
## FIX log provider
##      
class FIXLogProvider(Provider):
    fd = 0x00
    message_types = ['D','F','G','8']
    
    def __init__(self, conn_name='', conn_port=''):
        Provider.__init__(self, conn_name, conn_port)
        self.opmode = 'pull'

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
                    
    def read(self, From=''):
        Provider.read(self, From)        
        rows = []
        for row in self.fd:
            parsed = self.parse(row)
            if parsed != {}:
                rows.append(parsed)
        return(rows)

##
## Apama provider
##    
class ApamaProvider(Provider):

    def __init__(self, conn_name='', conn_port=''):
        Provider.__init__(self, conn_name, conn_port)
        self.opmode = 'push'
            
    def read(self, From=''):
        Provider.read(self, From)
        print('==> read(' + From + ') ' + self.opmode)