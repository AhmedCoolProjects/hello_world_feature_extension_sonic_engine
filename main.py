from scapy.all import *
from yapsy.IMultiprocessPlugin import IMultiprocessPlugin
from sonic_engine.util.functions import loadConfig, relative
from sonic_engine.core.database import __db__
from sonic_engine.model.extension import FeatureConfig


class HelloWorldFeatureExtension(IMultiprocessPlugin):
    def __init__(self, p):
        IMultiprocessPlugin.__init__(self, p)

        # TODO: to be added as a simple function in the sonic engine
        self.config = loadConfig(FeatureConfig, relative(
            __file__, './config.yaml'))

        print("--> Hello World Feature Extension Loaded")

    def run(self):
        for inpt in self.config.channels.input.files or []:
            print("Start")
            self.extract_ip_addresses(inpt)

    def extract_ip_addresses(self, pcap_file_path):

        packets = rdpcap(pcap_file_path)

        for packet in packets:
            if IP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                print(f"Source IP: {src_ip}, Destination IP: {dst_ip}")


if __name__ == '__main__':
    obj = HelloWorldFeatureExtension(None)
    obj.run()