from . import pypiruntime as __runtime


def run():
    rt = __runtime.init_runtime()
    __runtime.execute(rt)
    __runtime.postprocess(rt)


if __name__ == "__main__":
    run()
