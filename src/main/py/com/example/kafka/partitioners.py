from random import random
import hashlib
from kafka.partitioner import murmur2

def sticky_key_partitioner(key, all_partitions, available):
    """
    Customer Kafka partitioner to get the partition corresponding to key
    :param key: partitioning key
    :param all_partitions: list of all partitions sorted by partition ID
    :param available: list of available partitions in no particular order
    :return: one of the values from all_partitions or available
    """
    numPartitions = len(all_partitions)
    sp = int(abs(numPartitions*0.3))
    p = 0
    if key is None:
        raise Exception("All messages must have sensor name as key")

    m = murmur2(key)
    if key == b"TESS":
        p = int(abs(m) % sp)
    else:
        p = int(abs(m) % (numPartitions - sp) + sp)
    return all_partitions.index(p)


def hash_partitioner(key, all_partitions, available):
    """
    Customer Kafka partitioner to get the partition corresponding to key
    :param key: partitioning key
    :param all_partitions: list of all partitions sorted by partition ID
    :param available: list of available partitions in no particular order
    :return: one of the values from all_partitions or available
    """

    if key is None:
        if available:
            return random.choice(available)
        return random.choice(all_partitions)

    idx = int(hashlib.sha1(key).hexdigest(), 16) % (10 ** 8)
    idx &= 0x7fffffff
    idx %= len(all_partitions)
    return all_partitions[idx]


#
#
#
if __name__ == '__main__':

    all_partitions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    key_abc = "ABC"
    key_xyz = "XYZ"
    key_TESS = "TESS"

    print("============ sticky_key_partitioner =============")
    print("Key = {} - Partition = {}".format(key_abc, sticky_key_partitioner(key_abc.encode(), all_partitions, all_partitions)))
    print("Key = {} - Partition = {}".format(key_abc, sticky_key_partitioner(key_abc.encode(), all_partitions, all_partitions)))
    print("Key = {} - Partition = {}".format(key_abc, sticky_key_partitioner(key_abc.encode(), all_partitions, all_partitions)))

    print("Key = {} - Partition = {}".format(key_xyz, sticky_key_partitioner(key_xyz.encode(), all_partitions, all_partitions)))
    print("Key = {} - Partition = {}".format(key_xyz, sticky_key_partitioner(key_xyz.encode(), all_partitions, all_partitions)))
    print("Key = {} - Partition = {}".format(key_xyz, sticky_key_partitioner(key_xyz.encode(), all_partitions, all_partitions)))

    print("Key = {} - Partition = {}".format(key_TESS, sticky_key_partitioner(key_TESS.encode(), all_partitions, all_partitions)))
    print("Key = {} - Partition = {}".format(key_TESS, sticky_key_partitioner(key_TESS.encode(), all_partitions, all_partitions)))
    print("Key = {} - Partition = {}".format(key_TESS, sticky_key_partitioner(key_TESS.encode(), all_partitions, all_partitions)))

    print("============ hash_partitioner =============")

    print("Key = {} - Partition = {}".format(key_abc, hash_partitioner(key_abc.encode(), all_partitions, all_partitions)))
    print("Key = {} - Partition = {}".format(key_abc, hash_partitioner(key_abc.encode(), all_partitions, all_partitions)))
    print("Key = {} - Partition = {}".format(key_abc, hash_partitioner(key_abc.encode(), all_partitions, all_partitions)))

    print("Key = {} - Partition = {}".format(key_xyz, hash_partitioner(key_xyz.encode(), all_partitions, all_partitions)))
    print("Key = {} - Partition = {}".format(key_xyz, hash_partitioner(key_xyz.encode(), all_partitions, all_partitions)))
    print("Key = {} - Partition = {}".format(key_xyz, hash_partitioner(key_xyz.encode(), all_partitions, all_partitions)))

    print("Key = {} - Partition = {}".format(key_TESS, hash_partitioner(key_TESS.encode(), all_partitions, all_partitions)))
    print("Key = {} - Partition = {}".format(key_TESS, hash_partitioner(key_TESS.encode(), all_partitions, all_partitions)))
    print("Key = {} - Partition = {}".format(key_TESS, hash_partitioner(key_TESS.encode(), all_partitions, all_partitions)))


