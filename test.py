import time

timp_app = []

time_start = int(round(time.time() * 1000))
time.sleep(2)
t_dupa = int(round(time.time() * 1000))

timp_app.append((t_dupa - time_start))

time_start = int(round(time.time() * 1000))
time.sleep(2)
t_dupa = int(round(time.time() * 1000))

timp_app.append((t_dupa - time_start))

time_start = int(round(time.time() * 1000))
time.sleep(2)
t_dupa = int(round(time.time() * 1000))

timp_app.append((t_dupa - time_start))

time_start = int(round(time.time() * 1000))
time.sleep(2)
t_dupa = int(round(time.time() * 1000))

timp_app.append((t_dupa - time_start))

print(timp_app)
