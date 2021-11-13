import rediscluster
import certifi


startup_nodes = [{"host": "clustercfg.xxxxx.xxxxx.memorydb.us-east-1.amazonaws.com", "port": "6379"}]

print("begin")

# Note: decode_responses must be set to True when used with python3
rc = rediscluster.RedisCluster(startup_nodes=startup_nodes, username='default', password='on ~* &* +@all',skip_full_coverage_check=True, decode_responses=True, ssl=True, ssl_ca_certs=certifi.where())
rc.set("foo", "bar")
print(rc.get("foo"))

for i in range(1,2):
    rc.set("foo" + str(i), "bar" + str(i))
    print(rc.get("foo" + str(i)))
    

# Alternate simple mode of pointing to one startup node
# rc = rediscluster.RedisCluster(
#     host="clustercfg.shard2-replica2.zzia5k.memorydb.us-east-1.amazonaws.com",
#     port=6379,
#     decode_responses=True,
# )
#rc.set("foo", "bar")

print("==================")

# Retrieve the slow mapping (equivalent of "CLUSTER SLOTS")
print("This is the cluster slows information")
print(rc.cluster('slots'))
