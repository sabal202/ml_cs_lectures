from cpu_foobar import superfoo, ultrabar
import time
from threading import Thread

if __name__ == '__main__':
    start = time.time()
    
    foo = Thread(target=superfoo, args=(100, ))
    bar = Thread(target=ultrabar, args=(100, ))
    foo.start()
    bar.start()
    foo.join()
    bar.join()
    print(f"Time: {time.time() - start:.4f}s")
    