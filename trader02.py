from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import pandas as pd
import numpy as np



class Trader:
    def __init__(self) -> None:
        self.lastAcceptablePrice_pearls = 10000
        self.lastAcceptablePrice_bananas = 4800
        self.lastAcceptablePrice_coconuts = 7000
        self.lastAcceptablePrice_pina_coladas = 14000
        self.lastPrice_berries = 3850

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

        for trade in state.own_trades.keys():
            print(state.own_trades[trade])

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():

            if product == 'PEARLS':
                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                orders.append(Order(product,2, -2))
                result[product] = orders


            if product == 'BANANAS':
                pass

            if product == "COCONUTS":
                pass


            if product == "BERRIES":
                pass


        # Add all the above orders to the result dict
        
        # Return the dict of orders
        # These possibly contain buy or sell orders for PEARLS
        # Depending on the logic above
        return result
        