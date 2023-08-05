from typing import Dict, List, Type

from algo_beast_protocols.broker import Broker
from algo_beast_protocols.broker_manager import BrokerManager

from algo_beast_core.brokers.algo_beast_broker import AlgoBeastBroker
from algo_beast_core.brokers.fyers_broker import FyersBroker


class BrokerManager(BrokerManager):
  __instance = None

  available_brokers: Dict[str, Type[Broker]] = {}

  def __init__(self):
    if BrokerManager.__instance:
      raise Exception("singleton can not be initiated more than one time")
    else:
      BrokerManager.__instance = self

  @staticmethod
  def get_singleton():
    if BrokerManager.__instance == None:
      BrokerManager.__instance = BrokerManager()

    return BrokerManager.__instance

  def get_broker(self, broker_name, broker_config) -> Broker:
    try:
      return self.available_brokers[broker_name](broker_config)
    except IndexError:
      raise Exception("Unknown broker")


  def register(self, brokers: List[Broker]):
    for broker in brokers:
      self.available_brokers[broker.name] = broker

broker_manager = BrokerManager.get_singleton()

# register brokers
broker_manager.register([
  AlgoBeastBroker,
  FyersBroker
])
