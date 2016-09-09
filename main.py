# -*- coding: utf-8 -*-

import providers
import sys

def main():

    # All orders collection
    # key = orderId, value = Order
    orders = {}
    
    # Mapping from FIX OrderID (tag 37) to Apama orderId event field
    # key = FIX OrderID, value = Apama orderId
    fix_to_apama_orderid_map = {}
    
    # Apama orderId temporal sequence
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
                print '\n==>', order.orderId, order.timestamp, order.exchange, order.route, order.symbol, order.side, order.price, order.quantity
            elif eventtype:
                print '==>', eventtype
                
                orderevt = apama_helper.produceOrderEvent(eventtype, body)                
                
                # Use Apama OrderUpdate events to fill FIX to Apama id mapping
                if eventtype == 'com.apama.oms.OrderUpdate' and not fix_to_apama_orderid_map.has_key(orderevt.body['merketOrderId']):
                    fix_to_apama_orderid_map[orderevt.body['merketOrderId']] = orderevt.orderId
                elif eventtype == 'com.apama.fix.ExecutionReport' and fix_to_apama_orderid_map.has_key(orderevt.body['OrderID']):
                    orderevt.orderId = fix_to_apama_orderid_map[orderevt.body['OrderID']] 
                
                if orders.has_key(orderevt.orderId):
                    orders[orderevt.orderId].history.append(orderevt)
                else:
                    print '==> Key not found:', orderevt.orderId
                  
                        
    except KeyboardInterrupt:
        pass        

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