import sys
import rpyc
import psutil
import dogtail.config
from dogtail import tree
from dogtail.utils import run
from rpyc.utils.server import ThreadPoolServer


class DogtailService(rpyc.Service):

    def __init__(self):
        self.driver = None

    def on_disconnect(self):
        if self.driver:
            for proc in psutil.process_iter():
                if proc.name() == self.driver.description.split('/')[-1]:
                    proc.kill()
                    break
            self.driver = None

    def exposed_remote(self, opts: dict, debug: bool = False):
        dogtail.config.config.logDebugToStdOut = debug
        dogtail.config.config.logDebugToFile = debug
        run(opts['app_path'], timeout=opts['timeout'], dumb=opts['dumb'])
        self.driver = tree.root.application(opts['app_name'])
        return self.driver


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server = ThreadPoolServer(DogtailService, port=port)
    server.start()