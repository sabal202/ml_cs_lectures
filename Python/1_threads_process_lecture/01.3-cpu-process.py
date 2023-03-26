from cpu_foobar import superfoo, ultrabar
import time
from multiprocessing import Process


if __name__ == '__main__':
    start = time.time()
    
    foo = Process(target=superfoo, args=(100, ))
    bar = Process(target=ultrabar, args=(100, ))
    foo.start()
    bar.start()
    foo.join()
    bar.join()
    print(f"Time: {time.time() - start:.4f}s")