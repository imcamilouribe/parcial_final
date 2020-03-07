import redis



if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379, db=0)
    #r.set("msg:helloz", "Hello Redis!!!")

    print(r.get('msh:hello'))
    r.lrange