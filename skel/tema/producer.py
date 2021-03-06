"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

        # id producer from marketplace
        self.id_register_prod = self.marketplace.register_producer()

    def run(self):
        while 1: #in a infinit loop
            for (id_product, cant_prod, wait_time) in self.products:

                while cant_prod != 0: #while the cant needed is not 0
                    ret = self.marketplace.publish(str(self.id_register_prod), id_product)

                    if ret: #if return true
                        time.sleep(wait_time) #wait time and decrement cant_prod
                        cant_prod -= 1
                    else:#else wait number of seconds
                        time.sleep(self.republish_wait_time)
