from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import pandas as pd
import numpy as np



class Trader:
    lastAcceptablePrice = {'PEARLS': 10000, 'BANANAS': 4800, 'COCONUTS':7000, 'PINA_COLADAS':14000, 'DIVING_GEAR': 100000, 'BERRIES':3850 }
    bananas_max = 20
    pearls_max = 20
    pina_coladas_max = 300
    coconuts_max = 600
    diving_gear_max = 50
    berries_max = 250
    diff_from_mean = 0.000
    coconuts_data = []
    pina_coladas_data = []
    diving_gear_data = []
    dolphin_sightings_data = []
    berries_data = []
    berries_last_bought = 0

    def check_product(order: Order):
        return

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """


        # Initialize the method output dict as an empty dict
        result = {}
        # Initialize the list of Orders to be sent as an empty list
        orders: list[Order] = []
        # for trade_lst in state.own_trades.keys():
        #      print('\n')
        #      for trade in state.own_trades.get(trade_lst):
        #         if trade.price > self.lastAcceptablePrice[trade.symbol]:
        #             mode = ' SELL'
        #         else:
        #             mode = ' BUY'
        #         if trade.timestamp == state.timestamp-100:
        #             print(str(trade.quantity) + ' of ' + str(trade.symbol) + mode + ' for ' + str(int(trade.price)))
        # for product in state.order_depths.keys():
        #     print(product + str(state.position.get(product)))


        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():
            if product == 'PEARLS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

            
                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!
                filtered = dict()
                for(key, value) in order_depth.sell_orders.items():
                    if key > 0:
                        filtered[key] = value

                acceptable_price = (self.lastAcceptablePrice[product] + min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) /3
                self.lastAcceptablePrice[product] = acceptable_price
                try:
                    pearl_position = state.position[product]
                except:
                    pearl_position = 0

                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Check if the lowest ask (sell order) is lower than the above defined fair value

                    acceptable_ask = (acceptable_price-((self.diff_from_mean/100)*acceptable_price))
                    if (best_ask < acceptable_ask):
                        if ((pearl_position + 10) > self.pearls_max):
                            best_ask_volume = ( pearl_position + best_ask_volume)- self.pearls_max
                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        #print("BUY PEARLS", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))

                # The below code block is similar to the one above,
                # the difference is that it finds the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]

                    acceptable_bid = (acceptable_price+((self.diff_from_mean/100)*acceptable_price))
                    if (best_bid > acceptable_bid):
                        #if ((pearl_position - best_bid_volume) < 0):
                            #best_bid_volume = (best_bid_volume + (pearl_position - best_bid_volume))
                        #print("SELL PEARLS", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))

            if product == 'BANANAS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                
                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!

                acceptable_price = (self.lastAcceptablePrice['BANANAS'] + min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) /3
                self.lastAcceptablePrice['BANANAS'] = acceptable_price
                try:
                    banana_position = state.position[product]
                except:
                    banana_position = 0
                
                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                    acceptable_ask = (acceptable_price-((self.diff_from_mean/100)*acceptable_price))
                    if (best_ask < acceptable_ask):
                        
                        if ((banana_position + best_ask_volume) > self.bananas_max):
                            best_ask_volume = (banana_position + best_ask_volume)- self.bananas_max

                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        #print("BUY BANANAS", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))

                # The below code block is similar to the one above,
                # the difference is that it finds the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    acceptable_bid = (acceptable_price+((self.diff_from_mean/100)*acceptable_price))
                    if (best_bid > acceptable_bid):
                        #if ((banana_position - best_bid_volume) < 0):
                            #best_bid_volume = (best_bid_volume + (banana_position - best_bid_volume))
                        #print("SELL BANANAS", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))

            if product == "COCONUTS":
                order_depth_coconuts: OrderDepth = state.order_depths['COCONUTS']
                order_depth_pina_coladas: OrderDepth = state.order_depths['PINA_COLADAS']

                mid_price_coconuts = (min(order_depth_coconuts.sell_orders.keys()) + max(order_depth_coconuts.buy_orders.keys()))/2
                mid_price_pina_coladas = (min(order_depth_pina_coladas.sell_orders.keys()) + max(order_depth_pina_coladas.buy_orders.keys()))/2

                self.lastAcceptablePrice['COCONUTS'] = mid_price_coconuts*self.diff_from_mean
                self.lastAcceptablePrice['PINA_COLADAS'] = mid_price_pina_coladas*self.diff_from_mean

                self.coconuts_data.append(mid_price_coconuts)
                if len(self.coconuts_data) > 20:
                    self.coconuts_data.pop(0)
                
                self.pina_coladas_data.append(mid_price_pina_coladas)
                if len(self.pina_coladas_data) > 20:
                    self.pina_coladas_data.pop(0)

                d = {'coconuts':self.coconuts_data, 'pina_coladas':self.pina_coladas_data}
                df = pd.DataFrame(d)

                spread = df['coconuts'] - df['pina_coladas']

                spread_mean = spread.rolling(window=6).mean()
                spread_std = spread.rolling(window=6).std()
                zscore = (spread - spread_mean) / spread_std


                long_signal = zscore  < -1.0
                short_signal = zscore > 1.0
                exit_signal = abs(zscore) < .5


                avaliable_PINA_COLADAS = state.position.get('PINA_COLADAS')
                if avaliable_PINA_COLADAS == None:
                    avaliable_PINA_COLADAS = 0
                avaliable_COCONUTS = state.position.get('COCONUTS')
                if avaliable_COCONUTS == None:
                    avaliable_COCONUTS = 0


                # if avaliable_COCONUTS > (self.coconuts_max*80/100):
                #     orders.append(Order('COCONUTS', mid_price_coconuts, -100))
                # if avaliable_PINA_COLADAS > (self.pina_coladas_max*80/100):
                #     orders.append(Order('PINA_COLADAS', mid_price_pina_coladas, 100))

                if long_signal[long_signal.size-1]:
                    #long position
                    #buy pina_coladas
                    if len(order_depth.sell_orders) > 0:
                        best_ask = min(order_depth_pina_coladas.buy_orders.keys())
                        best_ask_volume = 100
                        #print("                           BUY PINA_COLADAS", str(best_ask_volume) + "x", best_ask)
                        orders.append(Order('PINA_COLADAS', best_ask, best_ask_volume))
                    #sell coconuts
                    if len(order_depth_coconuts.buy_orders) != 0:
                        best_bid = max(order_depth_coconuts.sell_orders.keys())
                        best_bid_volume = 100
                        #print("                           SELL COCONUTS", str(-best_bid_volume) + "x", best_bid)
                        orders.append(Order('COCONUTS', best_bid, -best_bid_volume))


                elif short_signal[short_signal.size-1]:
                    #short position
                    #buy coconuts
                    if len(order_depth.sell_orders) > 0:
                        best_ask = min(order_depth_coconuts.sell_orders.keys())
                        best_ask_volume = 100
                        #print("                           BUY COCONUTS", str(best_ask_volume) + "x", best_ask)
                        orders.append(Order('COCONUTS', best_ask, best_ask_volume))
                    #sell pina_coladas
                    if len(order_depth_pina_coladas.buy_orders) != 0:
                        best_bid = max(order_depth_pina_coladas.buy_orders.keys())
                        best_bid_volume = 100
                        #print("                           SELL PINA_COLADAS", str(-best_bid_volume) + "x", best_bid)
                        orders.append(Order('PINA_COLADAS', best_bid, -best_bid_volume))
                result['COCONUTS'] = (x for x in orders if x.symbol == 'COCONUTS')
                result['PINA_COLADAS'] = (x for x in orders if x.symbol == 'PINA_COALDAS')

            if product == "DIVING_GEAR":
                order_depth_diving_gear: OrderDepth = state.order_depths['DIVING_GEAR']

                mid_price_diving_gear = (min(order_depth_diving_gear.sell_orders.keys()) + max(order_depth_diving_gear.buy_orders.keys()))/2
                
                self.diving_gear_data.append(mid_price_diving_gear)
                if len(self.diving_gear_data) > 50:
                    self.diving_gear_data.pop(0)

                d = {'DIVING_GEAR': self.diving_gear_data}
                df = pd.DataFrame(d)

                df['sma'] = df['DIVING_GEAR'].rolling(window=6).mean()


                price = (df['DIVING_GEAR'].tail(1).to_list()[0])
                sma = df['sma'].tail(1).tolist()[0]

                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = order_depth.buy_orders[best_bid]
                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = order_depth.sell_orders[best_ask]
                avaliable_diving_gear = state.position.get(product)
                if avaliable_diving_gear == None:
                    avaliable_diving_gear = 0

                if (price < sma):
                    orders.append(Order(product, best_ask, -best_ask_volume))
                if (price > sma):
                    orders.append(Order(product, best_bid, -best_bid_volume))

                if avaliable_diving_gear < -self.diving_gear_max*70/100:
                    orders.append(Order(product, mid_price_diving_gear, -best_ask_volume))
                elif avaliable_diving_gear > self.diving_gear_max*70/100:
                    orders.append(Order(product, mid_price_diving_gear, -best_bid_volume))

            if product == "BERRIES":
                time = state.timestamp
                order_depth = state.order_depths[product]
                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = order_depth.buy_orders[best_bid]
                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = order_depth.sell_orders[best_ask]
                berries_avaliable = state.position.get(product)
                if berries_avaliable == None:
                    berries_avaliable =0

                mid_price = (best_bid + best_ask)/2

                if time < 45000:
                    if best_ask < self.berries_last_bought:
                        if berries_avaliable + best_ask_volume > self.berries_max:
                            best_ask_volume = self.berries_max - (berries_avaliable + best_ask_volume)
                        orders.append(Order(product, best_ask, -best_ask_volume))
                        orders.append(Order(product, best_bid, -self.lastAcceptablePrice['BERRIES']))
                    else:
                        orders.append(Order(product, best_ask, -best_ask_volume))
                elif time > 45000 and time < 55000:
                    if berries_avaliable - best_bid_volume < 0:
                        best_bid_volume = abs(berries_avaliable-best_bid_volume)
                    if mid_price <= self.lastAcceptablePrice[product]:
                        orders.append(Order(product, best_bid, -best_bid_volume))
                elif time >= 55000 and state.position.get(product) > 0:
                    if berries_avaliable - best_bid_volume < 0:
                        best_bid_volume = abs(berries_avaliable-best_bid_volume)
                    orders.append(Order(product, best_bid, -best_bid_volume))

                self.lastAcceptablePrice[product] = mid_price



        # Add all the above orders to the result dict
        for product in state.order_depths.keys():
            filtered = []
            for order in orders:
                if order.symbol == product:
                    filtered.append(order)
            result[product] = filtered
        # Return the dict of orders
        # These possibly contain buy or sell orders for PEARLS
        # Depending on the logic above
        return result
        