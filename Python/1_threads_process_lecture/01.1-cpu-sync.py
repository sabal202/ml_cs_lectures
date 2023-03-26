from cpu_foobar import superfoo, ultrabar
import time


if __name__ == '__main__':
    start = time.time()
    foo = superfoo(100)
    bar = ultrabar(100)
    print(f"Time: {time.time() - start:.4f}s")
