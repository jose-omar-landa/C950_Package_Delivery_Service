

class MyHashTable:

    # constructor that sets the array size and initializes the map array
    def __init__(self, initial_size=40):
        self.table = []
        for i in range(initial_size):
            self.table.append([])

    # function to add a value into the hash table.
    def insert(self, key, value):
        hash_bucket = hash(key) % len(self.table)
        hash_bucket_list = self.table[hash_bucket]

        # this will update the key if it already exists within the hash bucket list
        for key_value in hash_bucket_list:
            if key_value[0] == key:
                key_value[1] = value
                return True

        # if the key does not already exist within the hash bucket list, this will insert the
        # new value into the hash bucket list
        item = [key, value]
        hash_bucket_list.append(item)
        return True

    # this function will search for a value with the matching key within the hash table.
    # if the value is found, the function will return the value.
    # if the value is not found, the function will return None.
    def find(self, key):

        # this section will find the list where the given key is found
        hash_bucket = hash(key) % len(self.table)
        hash_bucket_list = self.table[hash_bucket]

        # this section will look for the key within the provided list.
        # will return either the corresponding value or None depending on if the key is found or not.
        for key_value_pair in hash_bucket_list:
            if key == key_value_pair[0]:
                return key_value_pair[1]
        return None

    # function to delete an item from the hash table for a given key
    # will only delete if the given key is found within the hash table
    def delete(self, key):

        # this section will find the list where the given key is found
        hash_bucket = hash(key) % len(self.table)
        hash_bucket_list = self.table[hash_bucket]

        # this section will delete the value from the list if the key is found
        # will not remove anything if the key is not found
        if key in hash_bucket_list:
            hash_bucket_list.remove(key)


