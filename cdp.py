#/usr/bin/env python3

from scapy.all import*
import struct

def mac_to_bytes(mac):
    mac_no_colon = mac.replace(":","")
    return bytes.fromhex(mac_no_colon)

class Eth_frame():
    def __init__(self,smac):
        self._dmac = "01:00:0C:CC:CC:CC"
        self._smac = smac
        self._payload = None
        
    def add_payload(self, payload):
        self._payload = payload

    
    def to_bytes(self):
        out =  mac_to_bytes(self._dmac)
        out += mac_to_bytes(self._smac)
        payload = self._payload.to_bytes()
        out += struct.pack("!H", len(payload) )
        out += payload
        return out
class LLC():
    def __init__(self):
        self._dsap = 0xAA
        self._ssap = 0xAA
        self._ctrl = 0x03
        self._oui = "00:00:0C"
        self._pid = 0x2000
        self._payload =  None

    def add_payload(self, payload):
            self._payload = payload

    
    def to_bytes(self):
        out = struct.pack("!3B", self._dsap, self._ssap, self._ctrl)
        out += mac_to_bytes(self._oui)  
        out += struct.pack("!H", self._pid)
        out += self._payload.to_bytes()
        return out

class CDP_hdr():
    def __init__(self):
        self._version = 1 
        self._ttl = 100
        self._checksum = 0 
        self._payload = list()
    
    def add_payload(self, payload):
        self._payload.append(payload)
    
    def to_bytes(self):
        out = struct.pack("!2BH", self._version, self._ttl, self._checksum)
        for tlv in self._payload:
            out += tlv.to_bytes()
        return out 

class TLV():
    def __init__(self, type):
        self._type = type
        self._lenght = 4
    def to_bytes(self):
        return struct.pack("!2H", self._type, self._lenght)
class TLV_device_id(TLV):
    
    def __init__(self, device_id):
        super().__init__(0x0001)        
        self._device_id = device_id
    def to_bytes(self):
        device_bytes = self._device_id.encode()
        self._lenght += len(device_bytes)
        out =  super().to_bytes()
        out += device_bytes
        return out 
class TLV_software(TLV):
    
    def __init__(self, version):
        super().__init__(0x0005)        
        self._version = version

    def to_bytes(self):
        device_bytes = self._version.encode()
        self._lenght += len(device_bytes)
        out =  super().to_bytes()
        out += device_bytes
        return out 

class TLV_platform(TLV_software):
    def __init__(self):
        super().__init__("PVSA_CDP")        
        self._type = 0x0006

    def to_bytes(self):
        return super().to_bytes()
    
class TLV_capabilities(TLV):
    def __init__(self, router =True, host=False, switch=False):
        super().__init__(0x0004)        
        self._isRouter = router
        self._isHost = host
        self._isSwitch = switch
    def to_bytes(self):
        capabilities = 0
        if self._isRouter:
            capabilities += 1
        if self._isHost:
            capabilities += 16
        if self._isSwitch:
            capabilities += 8
        self._lenght += 4
        return super().to_bytes() + struct.pack("!I", capabilities)


if __name__ ==  "__main__":
    IFACES.show()
    iface = IFACES.dev_from_index(12)
    sock = conf.L2socket(iface = iface)
    frame = Eth_frame("11:22:33:44:55:66")

    llc = LLC()
    cdp = CDP_hdr()
    tlv_device = TLV_device_id("pc-PVSA")
    cdp.add_payload(tlv_device)
    tlv_devices = TLV_capabilities(router=True)
    cdp.add_payload(tlv_devices)
    tlv_soft = TLV_software("20251124")
    cdp.add_payload(tlv_soft)
    tlv_platform = TLV_platform()
    cdp.add_payload(tlv_platform)
    llc.add_payload(cdp)
    frame.add_payload(llc)
    sock.send(frame.to_bytes())