from pyfedappwrap.engine.runtime import FedDBEngine

from app import BranchMergeApp

engine = FedDBEngine()
engine.register(BranchMergeApp())

if __name__ == '__main__':
    engine.start()
    engine.wait_until_stop()
