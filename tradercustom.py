from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import statistics


class Trader:
    lastAcceptablePrice0 = 10000
    lastAcceptablePrice1 = 4800
    bananas_max = 20
    pearls_max = 20
    diff_from_mean = 0.005

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}
        # Initialize the list of Orders to be sent as an empty list
        orders: list[Order] = []

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'PEARLS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                

                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!
                filtered = dict()
                for(key, value) in order_depth.sell_orders.items():
                    if key > 0:
                        filtered[key] = value

                acceptable_price = (self.lastAcceptablePrice0 + min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) /3
                self.lastAcceptablePrice0 = acceptable_price
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
                        if ((pearl_position + best_ask_volume) > self.pearls_max):
                            best_ask_volume = ( pearl_position + best_ask_volume)- self.pearls_max
                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
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
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))



            #FOR BANANAS
            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'BANANAS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                
                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!

                acceptable_price = (self.lastAcceptablePrice1 + min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) /3
                self.lastAcceptablePrice1 = acceptable_price
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
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
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
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))

        # Add all the above orders to the result dict
        result[product] = orders
        # Return the dict of orders
        # These possibly contain buy or sell orders for PEARLS
        # Depending on the logic above
        return result
        