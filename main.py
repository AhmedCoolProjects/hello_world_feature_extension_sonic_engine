import uuid
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

        print("--> Hello World Feature Extension DUPLICATION BRANCH Loaded")


    def run(self):
        for inpt in self.config.channels.input.files or []:
            self.extract_ip_addresses(inpt)

    def extract_ip_addresses(self, pcap_file_path):

        packets = rdpcap(relative(__file__, pcap_file_path))
        for packet in packets:
            if IP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                self.store_in_db(src_ip, dst_ip)

    def store_in_db(self, src_ip, dst_ip):

        ip_data_id = uuid.uuid4().hex
        __db__.store('ip_data', ip_data_id, {
            'src_ip': src_ip,
            'dst_ip': dst_ip
        })
        for ch in self.config.channels.publish:
            __db__.publish(ch, ip_data_id)

