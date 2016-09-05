# -*- coding: utf-8 -*-

import providers

def main():

    LOGDIR = 'D:\\Users\\FabioTrader\\Documents\\Projects\\ApamaWork_5.1\\logs\\2016-09-02_Prod\\logs\\FIX_Log'    
    FIXUS = 'FIX.4.4-E2MUS-SGNUS.messages.current.log'      
      
    x = providers.FIXLogProvider(conn_name = LOGDIR + '\\' + FIXUS)    
    y = providers.ApamaProvider(conn_name='localhost', conn_port=15903)
    
    
    x.open()
    xx = x.read()
    x.close()
    
    c=0
    for i in xx:
        c = c + 1
        print c, i
        if c == 2:
            break

    y.open()
    y.read('345')
    y.close()

if __name__ == "__main__":
    main()