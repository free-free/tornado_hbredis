#-*- coding:utf-8 -*-
from collections import deque
import functools
import copy

from tornado import gen
import tornadis

def decode(func):
    @functools.wraps(func)
    @gen.coroutine
    def wrapper(self, *args, **kwargs):
        data = None
        result = yield func(self, *args, **kwargs)
        if self._bytes_decode == True:
            if isinstance(result, list):
                data = list(map(lambda item: item.decode() if \
                    isinstance(item,bytes) else item, result))
            elif isinstance(result, dict):
                data = {}
                for k, v in result.items():
                    data[k] = v.decode()
            else:
                try:
                    data = result.decode()
                except Exception:
                    data = result
        else: 
            data = result
        return data
    return wrapper


class StringCommandsMixin:

    @decode
    @gen.coroutine
    def set(self, key, value):
        if isinstance(value, float):
            value = str(value)
        result = yield self._client.call('set', key, value)
        return result

    @decode
    @gen.coroutine
    def sget(self, key):
        result = yield self._client.call('get', key)
        return result

    @decode
    @gen.coroutine
    def incrby(self, key, inc):
        result = yield self._client.call('incrby', key, inc)
        return result

    @decode
    @gen.coroutine
    def incr(self, key):
        result = yield self._client.call('incr', key)
        return result

    @decode
    @gen.coroutine
    def decrby(self, key, dec):
        result = yield self._client.call('decrby', key, dec)
        return result
 
    @decode
    @gen.coroutine
    def decr(self, key):
        result = yield self._client.call('decr', key)
        return result

    @decode
    @gen.coroutine
    def incrbyfloat(self, key, floatinc):
        result = yield self._client.call('incrbyfloat', key, str(floatinc))
        return result

    @decode
    @gen.coroutine
    def append(self, key, appendstr):
        result = yield self._client.call('append', key, appendstr)
        return result

    @decode
    @gen.coroutine
    def strlen(self, key):
        result = yield self._client.call("strlen", key)
        return result

    @decode
    @gen.coroutine
    def mset(self, pairs):
        pairs_to_list = deque()
        for k, v in pairs.items():
            pairs_to_list.extend([k, v])
        result = yield self._client.call("mset", *list(pairs_to_list))
        return result

    @decode
    @gen.coroutine
    def mget(self, *keys):
        if isinstance(keys[0], (list, tuple)):
            keys = keys[0]
        result = yield self._client.call("mget", *list(keys))
        return result

    @decode
    @gen.coroutine
    def getbit(self, key, offset):
        result = yield self._client.call("getbit", key, offset)
        return int(result)

    @decode
    @gen.coroutine
    def setbit(self, key, offset, value):
        if int(value) > 0 or int(value) < 0:
            value = 1
        result = yield self._client.call("setbit", key, offset, value)
        return result

    @decode
    @gen.coroutine
    def bitcount(self, key, startbyte, endbyte):
        result = yield self._client.call("bitcount", key, int(startbyte), int(endbyte))
        return int(result)

    @decode
    @gen.coroutine
    def bit_or(self, key1, key2, resultkey=None):
        result = None
        if resultkey:
            yield self._client.call("bitop", "or", resultkey, key1, key2)
            result = yield self._client.call("get", resultkey)
        else:
            yield self._client.call("bitop", "or", key1 + '_' + key2, key1, key2)
            result = yield self._client.call('get', key1 + '_' + key2)
            yield self._client.call("del", key1 + '_' + key2)
        return result

    @decode
    @gen.coroutine
    def bit_and(self, key1, key2, resultkey=None):
        result = None
        if resultkey:
            yield self._client.call("bitop", "and", resultkey, key1, key2)
            result = yield self._client.call("get", resultkey)
        else:
            yield self._client.call("bitop", "and", key1 + '_' + key2, key1, key2)
            result = yield self._client.call("get", key1 + '_' + key2)
            yield self._client.call("del", key1 + '_' + key2)
        return result

    @decode
    @gen.coroutine
    def bit_xor(self, key1, key2, resultkey=None):
        result = None
        if resultkey:
            yield self._client.call("bitop", "xor", resultkey, key1, key2)
            result = yield self._client.call("get", resultkey)
        else:
            yield self._client.call("bitop", "xor", key1 + '_' + key2, key1, key2)
            result = yield self._client.call("get", key1 + '_' + key2)
            yield self._client.call("del", key1 + '_' + key2)
        return result

    @decode
    @gen.coroutine
    def bit_not(self, key, resultkey=None):
        result = None
        if resultkey:
            yield self._client.call("bitop", "not", resultkey, key)
            result = yield self._client.call("get", resultkey)
        else:
            yield self._client.call("bitop", "not", key + '_' + key[::-1], key)
            result = yield self._client.call("get", key + '_' + key[::-1])
            yield self._client.call('del', key + '_' + key[::-1])
        return result


class HashCommandsMixin:

    @decode
    @gen.coroutine
    def hget(self, key, field):
        result = yield self._client.call('hget', key, field)
        return result

    @decode
    @gen.coroutine
    def hmget(self, key, *fields):
        if isinstance(fields[0], (list, tuple)):
            fields = fields[0]
        result = yield self._client.call("hmget", key, *list(fields))
        data = {}
        for i, value in enumerate(result):
            data[fields[i]] = value
        return data

    @decode
    @gen.coroutine
    def hset(self, key, field, value):
        result = yield self._client.call('hset', key, field, value)
        return result

    @decode
    @gen.coroutine
    def hmset(self, key, pairs):
        pairs_to_list = deque()
        for k, v in pairs.items():
            pairs_to_list.extend([k, v])
        result = yield self._client.call('hmset', key, *list(pairs_to_list))
        return result

    @decode
    @gen.coroutine
    def hexists(self, key, field):
        result = yield self._client.call('hexists', key, field)
        return result

    @decode
    @gen.coroutine
    def hgetall(self, key):
        result = yield self._client.call('hgetall', key)
        data = {}
        length = len(result)
        for kvi in range(0, length, 2):
            k = result[kvi].decode()
            data[k] = result[kvi+1]
        return data

    @decode
    @gen.coroutine
    def hincrby(self, key, field, inc):
        result = yield self._client.call('hincrby', key, field, inc)
        return result

    @decode
    @gen.coroutine
    def hdel(self, key, *fields):
        result = None
        if isinstance(fields[0], (list, tuple)):
            fields = fields[0]
            result = yield self._client.call('hdel', key, *list(fields))
        else:
            result = yield self._client.call("hdel", key, *list(fields))
        return result

    @decode
    @gen.coroutine
    def hkeys(self, key):
        result = yield self._client.call('hkeys', key)
        return result

    @decode
    @gen.coroutine
    def hlen(self, key):
        result = yield self._client.call('hlen', key)
        return result

    @decode
    @gen.coroutine
    def hvals(self, key):
        result = yield self._client.call('hvals', key)
        return result


class ListCommandsMixin:

    @decode
    @gen.coroutine
    def lpush(self, key, *val_l):
        if isinstance(val_l[0], (list, tuple)):
            val_l = val_l[0]
        result = yield self._client.call("lpush", key, *list(val_l))
        return result

    @decode
    @gen.coroutine
    def rpush(self, key, *val_l):
        if isinstance(val_l[0], (tuple, list)):
            val_l = val_l[0]
        result = yield self._client.call("rpush", key, *list(val_l))
        return result

    @decode
    @gen.coroutine
    def lpop(self, key):
        result = yield self._client.call("lpop", key)
        return result

    @decode
    @gen.coroutine
    def rpop(self, key):
        result = yield self._client.call("rpop", key)
        return result

    @decode
    @gen.coroutine
    def llen(self, key):
        result = yield self._client.call("llen", key)
        return result

    @decode
    @gen.coroutine
    def lrange(self, key, start, end):
        result = yield self._client.call("lrange", key, start, end)
        return result

    @decode
    @gen.coroutine
    def lrem(self, key, count, value):
        result = yield self._client.call("lrem", key, count, value)
        return result

    @decode
    @gen.coroutine
    def lindex(self, key, index):
        result = yield self._client.call("lindex", key, index)
        return result

    @decode
    @gen.coroutine
    def lset(self, key, index, value):
        result = yield self._client.call("lset", key, index, value)
        return result

    @decode
    @gen.coroutine
    def ltrim(self, key, start, end):
        result = yield self._client.call("ltrim", key, start, end)
        return result

    @decode
    @gen.coroutine
    def linsert(self, key, pivot, value, direc="after"):
        result = yield self._client.call("linsert", key, direc, pivot, value)
        return result

    @decode
    @gen.coroutine
    def linsertafter(self, key, pivot, value):
        result = yield self.linsert(key, pivot, value, 'after')
        return result

    @decode
    @gen.coroutine
    def linsertbefore(self, key, pivot, value):
        result = yield self.linsert(key, pivot, value, 'before')
        return result

    @decode
    @gen.coroutine
    def rpoplpush(self, src, dest):
        result = yield self._client.call("rpoplpush", src, dest)
        return result


class SetCommandsMixin:

    @decode
    @gen.coroutine
    def sadd(self, key, *vals):
        result = None
        if isinstance(vals[0], (tuple, list)):
            vals = vals[0]
            result = yield self._client.call('sadd', key, *list(vals))
        else:
            result = yield self._client.call("sadd", key, *list(vals))
        return result

    @decode
    @gen.coroutine
    def srem(self, key, *vals):
        if isinstance(vals[0], (tuple, list)):
            vals = vals[0]
            result = yield self._client.call("srem", key, *list(vals))
        else:
            result = yield self._client.call("srem", key, *list(vals))
        return result

    @decode
    @gen.coroutine
    def smembers(self, key):
        result = yield self._client.call("smembers", key)
        return result

    @decode
    @gen.coroutine
    def sismember(self, key, val):
        result = yield self._client.call("sismember", key, val)
        return result

    @decode
    @gen.coroutine
    def sdiff(self, *args):
        if len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                result = yield self._client.call("sdiff", *list(args[0]))
                return result
        else:
            result = yield self._client.call("sdiff", *args)
            return result

    @decode
    @gen.coroutine
    def sinter(self, *args):
        if len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                result = yield self._client.call("sinter", *list(args[0]))
                return result
        else:
            result = yield self._client.call("sinter", *args)
            return result

    @decode
    @gen.coroutine
    def sunion(self, *args):
        if len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                result = yield self._client.call("sunion", *list(args[0]))
                return result
        else:
            result = yield self._client.call("sunion", *args)
            return result

    @decode
    @gen.coroutine
    def scard(self, key):
        result = yield self._client.call("scard", key)
        return result

    @decode
    @gen.coroutine
    def sdiffstore(self, dest, *args):
        if len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                result = yield self._client.call("sdiffstore", dest, *list(args[0]))
                return result
        else:
            result = yield self._client.call("sdiffstore", dest, *args)
            return result

    @decode
    @gen.coroutine
    def sunionstore(self, dest, *args):
        if len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                result = yield self._client.call("sunionstore", dest, *list(args[0]))
                return result
        else:
            result = yield self._client.call("sunionstore", dest, *args)
            return result

    @decode
    @gen.coroutine
    def srandmember(self, key, count):
        result = yield self._client.call("srandmember", key, count)
        return result

    @decode
    @gen.coroutine
    def spop(self, key):
        result = yield self._client.call("spop", key)
        return result


class GenericCommandsMixin:

    @decode
    @gen.coroutine
    def delete(self, key):
        result = yield self._client.call("del", key)
        return result

    @decode
    @gen.coroutine
    def exists(self, key):
        result = yield self._client.call("exists", key)
        return result

    @decode
    @gen.coroutine
    def expire(self, key, expires):
        result = yield self._client.call("expire", key, int(expires))
        return result

    @decode
    @gen.coroutine
    def expireat(self, key, expire_ts):
        result = yield self._client.call("expireat", key, int(expire_ts))
        return result

    @decode
    @gen.coroutine
    def allkeys(self, pattern):
        result = yield self._client.call("keys", pattern)
        return result

    @decode
    @gen.coroutine
    def keytype(self, key):
        result = yield self._client.call("type", key)
        return result

    @decode
    @gen.coroutine
    def ttl(self, key):
        result = yield self._client.call("ttl", key)
        return result

    @decode
    @gen.coroutine
    def rename(self, key, newkey):
        result = yield self._client.call("rename", key, newkey)
        return result

    @decode
    @gen.coroutine
    def renamenx(self, key, newkey):
        result = yield self._client.call("renamenx", key, newkey)
        return result

    @decode
    @gen.coroutine
    def randomkey(self):
        result = yield self._client.call("randomkey")
        return result

    @decode
    @gen.coroutine
    def move(self, key, db):
        result = yield self._client.call("move", key, db)
        return result

    @decode
    @gen.coroutine
    def persist(self, key):
        result = yield self._client.call("persist", key)
        return result

    @decode
    @gen.coroutine
    def pexpire(self, key, milis):
        result = yield self._client.call("pexpire", key, milis)
        return result

    @decode
    @gen.coroutine
    def pexpireat(self, key, milis_st):
        result = yield self._client.call("pexpireat", key, milis_st)
        return result

    @decode
    @gen.coroutine
    def pttl(self, key):
        result = yield self._client.call("pttl", key)
        return result


class ServerCommandsMixin:

    @decode
    @gen.coroutine
    def dbsize(self):
        result = yield self._client.call("dbsize")
        return result

    @decode
    @gen.coroutine
    def flushall(self):
        result = yield self._client.call("flushall")
        return result

    @decode
    @gen.coroutine
    def flushdb(self):
        result = yield self._client.call("flushdb")
        return result


class _PipelineWrapper(object):
    _commands_convert_pairs = {
        "delete": "del"
    }

    def __init__(self, hbredis, pipeline, client):
        self._pipeline = pipeline
        self._client = client
        self._bytes_decode = hbredis._bytes_decode

    def _dict_to_list(self, val_dict):
        val_l = deque()
        for k, v in val_dict.items():
            val_l.extend([k, v])
        return list(val_l)

    def _command_convert(self, command):
        return self._commands_convert_pairs.get(command, command)

    def _pipeline_commands(self, *args, **kw):
        commands = self._commands.split('_')
        if len(args) > 1:
            parsed_args = deque()
            parsed_args.appendleft(args[0])
            if isinstance(args[1], dict):
                parsed_args.extend(self._dict_to_list(args[1]))
            elif isinstance(args[1], (list, tuple)):
                parsed_args.extend(list(args[1]))
            else:
                parsed_args.extend(list(args[1:]))
        else:
            parsed_args = args
        if len(commands) == 1:
            commands[0] = self._command_convert(commands[0])
            self._pipeline.stack_call(commands[0], *list(parsed_args))
        elif len(commands) == 2:
            self._pipeline.stack_call(commands[0], commands[1],\
                *list(parsed_args))
        else:
            pass

    def __getattr__(self, attr):
        self._commands = attr
        return self._pipeline_commands

    @decode
    @gen.coroutine
    def execute(self):
        result = yield self._client.call(self._pipeline)
        return result


class TornadoHBRedis(
    dict,
    HashCommandsMixin,
    StringCommandsMixin,
    ListCommandsMixin,
    SetCommandsMixin,
    GenericCommandsMixin,
    ServerCommandsMixin
):

    def __init__(self, host, port, autoconnect=True, bytes_decode=False):
        assert isinstance(host, str)
        assert isinstance(port, int)
        assert isinstance(autoconnect, bool)
        self._host = host
        self._port = port
        self._autoconnect = autoconnect
        self._bytes_decode = bytes_decode
        self._client = tornadis.Client(
            host=self._host, port=self._port, autoconnect=self._autoconnect)

    def pipeline(self):
        self.__pipeline_wrapper = _PipelineWrapper(self,
            tornadis.Pipeline(), self._client)
        return self.__pipeline_wrapper
