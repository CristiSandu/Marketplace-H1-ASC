"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """

        Thread.__init__(self, **kwargs)

        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):

        for cart in self.carts:
            cart_id = self.marketplace.new_cart() #create cart_id for every list of add and remove

            for ops in cart: #loop for every operations
                while ops["quantity"] != 0: #while quantity if not 0
                    if ops["type"] == "add": #verify if the operatio is to add or
                        ret = self.marketplace.add_to_cart(cart_id, ops["product"])
                        if ret:
                            ops["quantity"] -= 1
                        else:
                            time.sleep(self.retry_wait_time)
                    elif ops["type"] == "remove": #remove from cart
                        ret = self.marketplace.remove_from_cart(cart_id, ops["product"])
                        if ret is None: # if rezult is true substract from quantity else
                            ops["quantity"] -= 1
                        else:
                            time.sleep(self.retry_wait_time) #wait given times

            self.marketplace.place_order(cart_id) #at the end call place_order
