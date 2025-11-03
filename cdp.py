#!/usr/bin/env python3

from scapy.all import *
import struct

def mac_to_bytes(mac):
    return bytes.fromhex(mac.replace(":", ""))

class Eth_frame():
    def __init__(self, smac):
        self._dmac = "01:00:0C:CC:CC:CC"
        self._smac = smac
        self._payload = None

    def add_payload(self, payload):
        self._payload = payload

    def to_bytes(self):
        out = mac_to_bytes(self._dmac)
        out += mac_to_bytes(self._smac)
        out += struct.pack("!H", len(self._payload.to_bytes()))
        out += self._payload.to_bytes()
        return out

class LLC():
    def __init__(self):
        self._dsap = 0xAA
        self._ssap = 0xAA
        self._ctrl = 0x03
        self._oui = "00:00:0C"
        self._pid = 0x2000
        self._payload = None

    def add_payload(self, payload):
        self._payload = payload

    def to_bytes(self):
        out = struct.pack("!3B", self._dsap, self._ssap, self._ctrl)
        out += mac_to_bytes(self._oui)
        out += struct.pack("!H", self._pid)
        if self._payload:
            out += self._payload.to_bytes()
        return out

class CDP_hdr():
    def __init__(self):
        self._version = 2
        self._ttl = 180
        self._checksum = 0
        self._payload = []  # ✅ fixed

    def add_payload(self, payload):
        self._payload.append(payload)

    def to_bytes(self):
        out = struct.pack("!2BH", self._version, self._ttl, self._checksum)
        for tlv in self._payload:
            out += tlv.to_bytes()
        return out

class CDP_TLV():
    def __init__(self, tlv_type, value_bytes):
        self._type = tlv_type
        self._length = 4
        self._value_bytes = value_bytes

    def to_bytes(self):
        return struct.pack("!HH", self._type, self._length) + self._value_bytes

class TLV_device_ID(CDP_TLV):
    def __init__(self, device_id):
        device_bytes = device_id.encode()
        super().__init__(0x0001, device_bytes)
        self._device_id = device_id

    def to_bytes(self):
        device_bytes = self._device_id.encode()
        self._length = 4 + len(device_bytes)
        out = super().to_bytes()
        return out

if __name__ == "__main__":
    IFACES.show()
    iface = IFACES.dev_from_index(12)
    sock = conf.L2socket(iface=iface)

    frame = Eth_frame("11:22:33:44:55:66")
    llc = LLC()
    cdp = CDP_hdr()
    tlv_device = TLV_device_ID("Device1")
    cdp.add_payload(tlv_device)
    llc.add_payload(cdp)
    frame.add_payload(llc)
    sock.send(frame.to_bytes())