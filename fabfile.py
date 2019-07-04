from fabric import Connection, Config, task

@task
def deploy(c):
    remote_user = "root"
    remote_password = "ae710077456d069d3f12454c0f"
    remote_host = "159.65.6.97"

    config = Config(overrides={'sudo': {'password': remote_password}})
    connect_kwarg = {'password': remote_password, 'allow_agent': False}
    conn = Connection(host=remote_host, user = remote_user, config = config, connect_kwargs=connect_kwarg)
    print("Success")

    conn.put("app.py")
    conn.put("config.json")

    conn.put("meal.json")
    conn.put("orders.json")
    conn.put("promo.json")
    conn.put("users.json")
    conn.put("promotions.json")

    print("Success!")

    print("Install requirements:")
    conn.sudo("pip3 install Flask Flask-CORS")
    conn.sudo("pip3 install twilio")

    print("Killdown")
    conn.sudo("pkill -F server.pid", warn = True)

    print("Start server")
    conn.sudo("nohup python3 app.py &> logs.txt & echo $! > server.pid")

    conn.close()
