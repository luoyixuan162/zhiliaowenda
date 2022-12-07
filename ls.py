from exts import redis_store


email = "2857013039@qq.com"
redis_store.set("valid_code:{}".format(email), "8888", 120)
captcha_model = redis_store.get("valid_code:{}".format(email))
print(captcha_model)