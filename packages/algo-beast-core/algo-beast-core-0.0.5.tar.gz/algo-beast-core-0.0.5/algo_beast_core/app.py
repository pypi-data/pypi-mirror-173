from algo_beast_core.broker_manager import broker_manager
from algo_beast_core.brokers.algo_beast_broker import AlgoBeastBroker
from algo_beast_core.brokers.fyers_broker import FyersBroker
from algo_beast_core.helpers.validate_session import validate_session
from algo_beast_core.session import Session
from algo_beast_core.store import store


class App:
  def __init__(self) -> None:
    self.__session = None
    self.__store = store
    self.__broker_manager = broker_manager
    self.__broker = None

    # register brokers
    self.__broker_manager.register([
      AlgoBeastBroker,
      FyersBroker
    ])

  def add_session(self, args):
    try:
      validate_session(args)
      self.__session = Session(args)
    except Exception as e:
      raise e

  def run(self):
    try:
      self.__broker = self.__broker_manager.get_broker(self.__session.broker_name, self.__session.broker_config)

      self.__store.setup(self.__broker)
      self.__store.run()
    except Exception as e:
      raise e
