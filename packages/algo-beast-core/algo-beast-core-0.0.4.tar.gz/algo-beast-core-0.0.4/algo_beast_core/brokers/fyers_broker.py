from time import sleep

from algo_beast_protocols.broker import Broker


class FyersBroker(Broker):
  name = "AlgoBeastBroker"
  supported_modes = ["Live"]

  def __init__(self, broker_config) -> None:
    self.__broker_config = broker_config

  def fetch_data(self):
    print('fetching data')

  def subscribe(self, on_data):
    while True:
      sleep(1)
      on_data("test")
