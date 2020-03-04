from radix import Radix

class Prefixes(object):
    
    def __init__(self):
        
        # Patricia trie for reserved prefixes ipv4
        self.__reserved_tree_ipv4 = Radix()
        self.__reserved_tree_ipv4.add("0.0.0.0/8")
        self.__reserved_tree_ipv4.add("1.1.1.0/24")
        self.__reserved_tree_ipv4.add("10.0.0.0/8")
        self.__reserved_tree_ipv4.add("100.64.0.0/10")
        self.__reserved_tree_ipv4.add("127.0.0.0/8")
        self.__reserved_tree_ipv4.add("169.254.0.0/16")
        self.__reserved_tree_ipv4.add("172.16.0.0/12")
        self.__reserved_tree_ipv4.add("192.0.0.0/24")
        self.__reserved_tree_ipv4.add("192.0.2.0/24")
        self.__reserved_tree_ipv4.add("192.88.99.0/24")
        self.__reserved_tree_ipv4.add("192.168.0.0/16")
        self.__reserved_tree_ipv4.add("198.18.0.0/15")
        self.__reserved_tree_ipv4.add("198.51.100.0/24")
        self.__reserved_tree_ipv4.add("203.0.113.0/24")
        self.__reserved_tree_ipv4.add("224.0.0.0/4")
        self.__reserved_tree_ipv4.add("240.0.0.0/4")
        self.__reserved_tree_ipv4.add("255.255.255.255/32")
        
        # routable address space
        self.__routable_tree_ipv4 = Radix()
        
        
    def check_prefix_is_reserved(self, prefix):
        node = self.__reserved_tree_ipv4.search_best(prefix)
        if node:
            return True
        return False


    def check_prefix_is_routable(self, prefix):
        node = self.__routable_tree_ipv4.search_best(prefix)
        if node:
            return True
        return False
    
    
    def add_routable_prefix(self, prefix, mask):
        if len(prefix.split('.')) != 4:
            return
        
        self.__routable_tree_ipv4.add(prefix + '/' + mask)
        return

