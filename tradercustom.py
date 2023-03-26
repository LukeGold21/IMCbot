from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import pandas as pd
import numpy as np



class Trader:
    def __init__(self) -> None:
        self.lastAcceptablePrice = {'PEARLS': 10000, 'BANANAS': 4800, 'COCONUTS':7000, 'PINA_COLADAS':14000, 'BERRIES': 3850}
        self.last_mid_price={'BERRIES': 3850}
        self.coconuts_data = [8000 for i in range(30)]
        self.pina_coladas_data = [15000 for i in range(30)]

    
        self.bananas_max = 20
        self.pearls_max = 20
        self.pina_coladas_max = 300
        self.coconuts_max = 600
        self.diff_from_mean = 0.005


    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """


        # Initialize the method output dict as an empty dict
        result = {}
        # Initialize the list of Orders to be sent as an empty list
        
        orders: list[Order] = []
        orders.clear()
        result.clear()

        print(state.position.get('BANANAS'))

        # for trade_lst in state.own_trades.keys():
        #      print('\n')
        #      for trade in state.own_trades.get(trade_lst):
        #         if trade.price > self.lastAcceptablePrice[trade.symbol]:
        #             mode = ' SELL'
        #         else:
        #             mode = ' BUY'
        #         if trade.timestamp == state.timestamp-100:
        #             print(str(trade.quantity) + ' of ' + str(trade.symbol) + mode + ' for ' + str(int(trade.price)))







        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():
            # if product == 'PEARLS':
            #     # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
            #     order_depth: OrderDepth = state.order_depths[product]

            #     acceptable_price = (self.lastAcceptablePrice[product] + min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) /3
            #     best_ask = min(order_depth.sell_orders.keys())
            #     best_ask_volume = order_depth.sell_orders[best_ask]
            #     best_bid = max(order_depth.buy_orders.keys())
            #     best_bid_volume = order_depth.buy_orders[best_bid]

            #     avaliable_pearls = state.position.get(product)
            #     if avaliable_pearls ==None:
            #         avaliable_pearls = 0


                
            #     # If statement checks if there are any SELL orders in the PEARLS market
            #     if len(order_depth.sell_orders) > 0:           
            #         acceptable_ask = (acceptable_price-((self.diff_from_mean/100)*acceptable_price))
            #         if (best_ask < 10000)and avaliable_pearls < 1:
            #             #print("BUY PEARLS", str(best_ask_volume) + "x", best_ask)
            #             orders.append(Order(product, 9998, 1))

            #     if len(order_depth.buy_orders) != 0:
            #         acceptable_bid = (acceptable_price+((self.diff_from_mean/100)*acceptable_price))
            #         if (best_bid > 10000) and avaliable_pearls >-1:
            #             #print("SELL BANANAS", str(best_bid_volume) + "x", best_bid)
            #             orders.append(Order(product, 10002, -1))
            #     result[product] = orders




            # if product == 'BANANAS':
            #     # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
            #     order_depth: OrderDepth = state.order_depths[product]

            #     acceptable_price = (self.lastAcceptablePrice[product]+ min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) /3
            #     self.lastAcceptablePrice[product] = acceptable_price
            #     try:
            #         banana_position = state.position[product]
            #     except:
            #         banana_position = 0
                
            #     # If statement checks if there are any SELL orders in the PEARLS market
            #     if len(order_depth.sell_orders) > 0:
            #         if state.timestamp> 80000 and state.position[product] > 5:
            #             orders.append(Order(product, acceptable_price, -state.position[product]))

            #         # Sort all the available sell orders by their price,
            #         # and select only the sell order with the lowest price
            #         best_ask = min(order_depth.sell_orders.keys())
            #         best_ask_volume = order_depth.sell_orders[best_ask]

            #         # Check if the lowest ask (sell order) is lower than the above defined fair value
            #         acceptable_ask = (acceptable_price-((self.diff_from_mean/100)*acceptable_price))
            #         if (best_ask < acceptable_ask) and state.timestamp<80000:
            #             orders.append(Order(product, best_ask, int(best_ask_volume)))

            #     if len(order_depth.buy_orders) != 0:
            #         best_bid = max(order_depth.buy_orders.keys())
            #         best_bid_volume = order_depth.buy_orders[best_bid]
            #         acceptable_bid = (acceptable_price+((self.diff_from_mean/100)*acceptable_price))
            #         if (best_bid > acceptable_bid):
            #             #print("SELL BANANAS", str(best_bid_volume) + "x", best_bid)
            #             orders.append(Order(product, best_bid, best_bid_volume))
            #     result[product] = orders


            if product == "COCONUTS":
                order_depth_coconuts: OrderDepth = state.order_depths['COCONUTS']
                order_depth_pina_coladas: OrderDepth = state.order_depths['PINA_COLADAS']

                mid_price_coconuts = (min(order_depth_coconuts.sell_orders.keys()) + max(order_depth_coconuts.buy_orders.keys()))/2
                mid_price_pina_coladas = (min(order_depth_pina_coladas.sell_orders.keys()) + max(order_depth_pina_coladas.buy_orders.keys()))/2

                self.coconuts_data.append(mid_price_coconuts)
                self.pina_coladas_data.append(mid_price_pina_coladas)

                d = {'coconuts':self.coconuts_data, 'pina_coladas':self.pina_coladas_data}
                df = pd.DataFrame(d)

                spread = df['coconuts'] - df['pina_coladas']

                spread_mean = spread.rolling(window=6).mean()
                spread_std = spread.rolling(window=6).std()
                zscore = (spread - spread_mean) / spread_std

                long_signal = zscore  < -2.0
                short_signal = zscore > 2.0


                if long_signal[long_signal.size-1]:
                    #long position
                    #buy pina_coladas
                    if len(order_depth_pina_coladas.sell_orders) > 0:
                        best_ask = min(order_depth_pina_coladas.buy_orders.keys())
                        best_ask_volume = order_depth_pina_coladas.buy_orders[best_ask]
                        print("BUY PINA_COLADAS", str(-best_ask_volume), best_ask)
                        orders.append(Order('PINA_COLADAS', best_ask, -best_ask_volume))
                        result['PINA_COLADAS'] = orders
                    #sell coconuts
                    if len(order_depth_coconuts.buy_orders) != 0:
                        best_bid = max(order_depth_coconuts.sell_orders.keys())
                        best_bid_volume = order_depth_coconuts.sell_orders[best_bid]
                        print("SELL COCONUTS", str(best_bid_volume), best_bid)
                        orders.append(Order('COCONUTS', best_bid, -best_bid_volume))
                        result['COCONUTS'] = orders

                elif short_signal[short_signal.size-1]:
                    #short position
                    #buy coconuts
                    if len(order_depth_coconuts.sell_orders) > 0:
                        best_ask = min(order_depth_coconuts.sell_orders.keys())
                        best_ask_volume = order_depth_coconuts.sell_orders[best_ask]
                        print("BUY COCONUTS", str(-best_ask_volume), best_ask)
                        orders.append(Order('COCONUTS', best_ask, -best_ask_volume))
                        result['COCONUTS'] = orders
                    #sell pina_coladas
                    if len(order_depth_pina_coladas.buy_orders) != 0:
                        best_bid = max(order_depth_pina_coladas.buy_orders.keys())
                        best_bid_volume = order_depth_pina_coladas.buy_orders[best_bid]
                        print("SELL PINA_COLADAS", str(best_bid_volume), best_bid)
                        orders.append(Order('PINA_COLADAS', best_bid, -best_bid_volume))
                        result['PINA_COLADAS'] = orders



            # if product == "BERRIES":
            #     order_depth: OrderDepth = state.order_depths[product]
            #     best_bid = max(order_depth.buy_orders.keys())
            #     best_bid_volume = order_depth.buy_orders[best_bid]
            #     best_ask = min(order_depth.buy_orders.keys())
            #     best_ask_volume = order_depth.buy_orders[best_ask]
            #     mid_price = (best_ask + best_bid)/2
                
                
            #     if state.timestamp < 45000 or state.timestamp > 55000:
            #         #buy
            #         if len(order_depth.sell_orders) > 0:
            #             if best_ask < self.lastAcceptablePrice[product]:
            #                 #print("BUY BERREIS", str(best_ask_volume) + "x", best_ask)
            #                 orders.append(Order('BERRIES', best_ask, -best_ask_volume))
            #                 result['BERRIES'] = orders

            #     else:
            #         if self.last_mid_price.get('BERRIES') < mid_price:
            #             #sell
            #             if len(order_depth.buy_orders) != 0:
            #                 #print("SELL BERRIES", str(best_bid_volume) + "x", best_bid)
            #                 orders.append(Order('BERRIES', best_bid, -best_bid_volume))
            #                 result['BERRIES'] = orders

            #     self.last_mid_price['BERRIES'] = mid_price



        # Add all the above orders to the result dict
        
        # Return the dict of orders
        # These possibly contain buy or sell orders for PEARLS
        # Depending on the logic above
        return result
        