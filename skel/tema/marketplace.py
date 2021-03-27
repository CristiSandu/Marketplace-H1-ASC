"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock, currentThread

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """

        self.queue_size_per_producer = queue_size_per_producer
        self.id_producer_list = list()
        self.max_prod_for_a_producer = dict()
        self.products_in_marketplace = list()
        self.produc_producer_maping = dict()
        self.carts_dic = dict()

        self.carts_count = 0


        self.lock_reg_prod = Lock()
        self.lock_new_carts_count = Lock()
        self.lock_add_to_cart = Lock()
        self.lock_print = Lock()





    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        producer_id = 0
        with self.lock_reg_prod:
            if len(self.id_producer_list) == 0:
                self.id_producer_list.append(0)
                producer_id = 0
            else:
                producer_id = self.id_producer_list[len(self.id_producer_list) - 1] + 1
                self.id_producer_list.append(producer_id)

        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        id_producer = int(producer_id)
        if id_producer not in self.max_prod_for_a_producer.keys():
            self.max_prod_for_a_producer[id_producer] = 1
        else:
            if self.max_prod_for_a_producer[id_producer] >= self.queue_size_per_producer:
                return False
            self.max_prod_for_a_producer[id_producer] += 1

        self.products_in_marketplace.append(product)
        self.produc_producer_maping[product] = id_producer
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.lock_new_carts_count:
            self.carts_count += 1
            cart_id = self.carts_count

        self.carts_dic[cart_id] = []

        return cart_id


    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.lock_add_to_cart:
            if product not in self.products_in_marketplace:
                return False
            self.max_prod_for_a_producer[self.produc_producer_maping[product]] -= 1
            self.products_in_marketplace.remove(product)
        self.carts_dic[cart_id].append(product)
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        self.carts_dic[cart_id].remove(product)
        self.products_in_marketplace.append(product)

        self.max_prod_for_a_producer[self.produc_producer_maping[product]] += 1


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        list_prod = self.carts_dic.pop(cart_id, None)

        for product in list_prod:
            with self.lock_print:
                print("{} bought {}".format(currentThread().getName(), product))


        return list_prod
