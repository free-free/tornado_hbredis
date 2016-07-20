## tornado_hbredis 
 A tornado redis driver ,it's actually encapsulation  for [tornadis](https://github.com/thefab/tornadis)

## Example
```python3.5
    from tornado_hbredis import TornadoHBRedis
    
    client = TornadoHBRedis('localhost', 6379)
    
 
    client.set("name", "john")

    client.get("name")

    client.mset({"age": 21,"name": "xxx"})

    client.mget(["age", "name"])
 
    client.hkeys("test_keys")
    
    client.lpush("l1",["hello","marble"])
    
    client.lrange("l1",0,-1)
    
    #pipeline
    pipeline = client.pipeline()
    pipeline.set("address","foo")
    pipeline.hmset("hash",{"name": "john","age":21})
    pipeline.lpush("xx",[32,32,32,3244])
    yield pipeline.execute()
```

## Detail
  The detail api refer to [here][tornado_hbredis.py]
  

## LICENSE
  [MIT LICENSE](LICENSE)  
