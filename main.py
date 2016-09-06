# -*- coding: utf-8 -*-

import providers
import sys

def main():

    orders = {}
    orderscrono = []    
    apama_helper = providers.ApamaProvider()
    
    # Read Apama input events from stdin
    # use engine_reveive -C GOTACH | main.py    
    try:
        while True:
            event = sys.stdin.readline()
            eventtype, body = apama_helper.process(event)
            
            if eventtype == 'com.apama.oms.NewOrder':
                order = apama_helper.produceOrder(body)
                orders[order.orderId] = order
                orderscrono.append(order.orderId)
                print '==>', order.timestamp, order.symbol, order.side
            elif eventtype:
                pass
                #orderevt = apama_helper.produceOrderEvent(eventtype, body)
                #orders[orderevt.orderID].history.add(orderevt)
    except KeyboardInterrupt:
        for o in orderscrono:
            print orders[o].symbol, orders[o].side, orders[o].type, orders[o].timestamp
            print '\n'
        

    '''
    LOGDIR = 'D:\\Users\\FabioTrader\\Documents\\Projects\\ApamaWork_5.1\\logs\\2016-09-02_Prod\\logs\\FIX_Log'    
    FIXUS = 'FIX.4.4-E2MUS-SGNUS.messages.current.log'      
    x = providers.FIXLogProvider(conn_name = LOGDIR + '\\' + FIXUS)    
    x.open()
    xx = x.read()
    x.close()
    
    c=0
    for i in xx:
        c = c + 1
        print c, i
        if c == 2:
            break
    '''

        
if __name__ == "__main__":
    main()