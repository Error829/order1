import redis

r = redis.Redis(host='localhost', port=6379)

r.execute_command("CONFIG", "SET", "requirepass", "359509tcw")
