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
        self.id_producer_list = list() #list of producer id
        self.products_in_marketplace = list() #list of productis in marketplace
        # dict to count products for a producer key producer_id and value count_products
        self.prod_for_a_producer = dict()
        # dict to store links between key that is product name and value producer_id
        self.produc_producer_maping = dict()
        # dict that contain as key id_cart value a list with products in this cart
        self.carts_dic = dict()

        self.lock_reg_prod = Lock()
        self.lock_new_carts_count = Lock()
        self.lock_add_to_cart = Lock()
        self.lock_place_order = Lock()

        self.carts_count = 0 #count carts in market

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        producer_id = 0
        with self.lock_reg_prod:  # we need to make a order in distibut the id for producers
            if len(self.id_producer_list) == 0: # if len of list of id is 0
                self.id_producer_list.append(0) # start with 0 id for the firs producer
                producer_id = 0
            else:# else take last id known and increment with 1
                producer_id = self.id_producer_list[len(self.id_producer_list) - 1] + 1
                self.id_producer_list.append(producer_id) # and out in the list

        # return last producer_id
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
        if id_producer not in self.prod_for_a_producer.keys():
            self.prod_for_a_producer[id_producer] = 1 #add fisrt product
        #else if nr of products iis >= form max queue size for a producer
        elif self.prod_for_a_producer[id_producer] >= self.queue_size_per_producer:
            return False    # then return to wait
        else:    # else all is ok
            self.prod_for_a_producer[id_producer] += 1 #increment queue size

        self.products_in_marketplace.append(product) #add product in the list of product
        self.produc_producer_maping[product] = id_producer #and map product to producer
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.lock_new_carts_count: #we need to control order in making carts
            self.carts_count += 1 #increase count
            cart_id = self.carts_count #add id to new cart

        self.carts_dic[cart_id] = list() #put cart in cart_disc
        return cart_id #and return cart id


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
            if product not in self.products_in_marketplace:#verify if product is in market
                return False #if not return false

            self.prod_for_a_producer[self.produc_producer_maping[product]] -= 1
            #and remove product from list of productis in marketplace
            self.products_in_marketplace.remove(product)


        self.carts_dic[cart_id].append(product) #and put the prodact in cart
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        self.carts_dic[cart_id].remove(product) #remove from cart
        self.products_in_marketplace.append(product) #put back in marketplace
        #and increase nr of product from the producer of this product
        self.prod_for_a_producer[self.produc_producer_maping[product]] += 1


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """

        for product in self.carts_dic[cart_id]: #loop on list
            with self.lock_place_order: #and print on of at the time
                name = str(currentThread().getName())
                prod = str(product)
                print(name, "bought", prod)

        return self.carts_dic[cart_id] #return the list of products
