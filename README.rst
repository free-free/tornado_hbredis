tornado_hbredis 
==================

 A tornado redis driver ,it's actually encapsulation  for `tornadis <https://github.com/thefab/tornadis>`_


Quickstarted
------------------

string operation
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from tornado_hbredis import TornadoHBRedis
    
    client = TornadoHBRedis('localhost', 6379, autoconnect=True, bytes_decode=False)
    # params: 'autoconnect' default value is True
    #         'bytes_decode' default value is False,which means the data from db will be bytes
    #                if 'bytes_decode' equal to True, which means the data from db will decoded
    
    yield client.set("name", "john")
    yield client.sget("name")
    # return opertaon result
    yield client.incrby("age", 2)
    yield client.incr("age")
    yield client.decrby("age", 2)
    yield client.decr("age")
    yield client.incrbyfloat("key", 0.1)
    # return str result length
    yield client.append("name", "xxxx")
    yield client.strlen("name")
    
    yield client.mset({"key1":"val1", "key2":"val2"})
    yield client.mget("key1", "key2")
    # or yield client.mget(["key1", "key2"])
   
    yield client.getbit("key", offset=1)
    yield client.setbit("key", offset=1, 1)
    yield client.bitcount("key", 0, 1)
    yield client.bit_or("key1", "key2", resultkey=None)
    yield client.bit_and("key1", "key2", resultkey=None)
    yield client.bit_xor("key1", "key2", resultkey=None)
    yield client.bit_not("key", resultkey=None)
 

hash operation
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from tornado_hbredis import TornadoHBRedis

    client = TornadoHBRedis("localhost", 6379)
    
    yield client.hmset("key", {"field1":"xxxx" ,"field2":21})
    yield client.hmget("key", "field1", "field2")
    # or yield client.hmget("key", ["field1", "field2"])
    yield client.hgetall("key")
    yield client.hget("key", "field")
    yield client.hdel("key", "field1", "field2")
    # or yield client.hdel("key", ["field1", "field2"])
    yield client.hkeys("key")
    yield client.hlen("key")
    yield client.hvals("key")
    yield client.hexists("key","field")
    yield client.hincrby("key","field", 20)


list operation
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    from tornado_hbredis import TornadoHBRedis 
    
    client = TornadoHBRedis("localhost", 6379)
  
    yield client.lpush("list1", 12, 32 ,32)
    # or yield client.lpush("list1",[12, 32, 32])
    yield client.rpush("list1", "21", "43")
    # or yield client.rpush("list1",["21", "43"])
    yield client.lrange("list1", 0, -1)
    yield client.lpop("list1")
    yield client.rpop("list1")
    yield client.llen("list1")
    yield client.lrem("list1", count=3 ,"marble")
    yield client.lindex("list1", 2)
    yield client.lset("list1", 2, "hello")
    yield client.ltrim("list1", 1, 4)
    yield client.linsert("list1", "pivot", "value", direc="after")
    yield client.linsertafter("list1", "pivot", "value")
    yield client.linsertbefore("list1", "pivot", "value")
    yield client.rpoplpush("src_list", "dest_list") 


set operation
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from tornado_hbredis import TornadoHBRedis 
    
    client = TornadoHBRedis("localhost", 6379)

    yield client.sadd("set1", "yyy")
    # or yield client.sadd("set1", ["xxx","zzz"])
    yield client.srem("set1", "yyy")
    #or  yield client.srem("set1", ["xxx","zzz"])
    yield client.smembers("set1")
    yield client.sismember("set1","xx")
    yield client.sdiff("set1","set2")
    yield client.sinter("set1", "set2")
    yield client.sunion("set1", "set2")
    yield client.scard("set1")
    yield client.sdiffstore("set3","set1","set2")
    yield client.sunionstore("set4","set1","set2")
    yield client.srandmember("set1", 2)
    yield client.smembers("set4")
    yield client.spop("set1")


general commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from tornado_hbredis import TornadoHBRedis 
    
    client = TornadoHBRedis("localhost", 6379)

    yield client.delete("set4")
    yield client.exists("set4")
    yield client.expire("key", 40)
    yield cleint.expireat("key",123832190)
    yield client.allkeys("*")
    yield client.keytype("set1")
    yield client.ttl("set1")
    yield client.rename("old_kname", "newkeyname")
    yield client.renamenx("old_kname", "newkeyname")
    yield client.move("key", "db_number")
    yield client.persist("key")
    yield client.pexpire("key", "millisecond")
    yield client.pexipreat("key","milisecond timestamp")
    yield cleint.pttl("key")


server commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from tornado_hbredis import TornadoHBRedis 
    
    client = TornadoHBRedis("localhost", 6379)
    
    yield client.dbsize()
    yield client.flushall()
    yield client.flushdb()


pipeline 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
      
    from tornado_hbredis import TornadoHBRedis 
    
    client = TornadoHBRedis("localhost", 6379)

    pipeline = client.pipeline()
    pipeline.set("address","foo")
    pipeline.hmset("hash",{"name": "john", "age": 21})
    pipeline.lpush("xxx", [21,43,43,43,54])
    yield pipeline.execute()


    
Detail
------------

  The detail api refer to `here <tornado_hbredis.py>`_


LICENSE
------------

  `MIT LICENSE <LICENSE>`_
