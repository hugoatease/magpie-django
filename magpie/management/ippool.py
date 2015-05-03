# Copyright 2013-2015 Hugo Caille
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ipaddr

class Pool:
    def __init__(self, tun=True, subnets=None, exclude=None):
        if subnets is not None:
            self.subnets = subnets
        else:
            self.subnets = list()
        
        if exclude is not None:
            self.excludelist = exclude
        else:
            self.excludelist = list()
        
        self.tun = tun
    
    def addSubnet(self, address, cidr):
        subnet = {'subnet' : address, 'cidr' : cidr}
        if subnet not in self.subnets:
            self.subnets.append(subnet)
            
        
    def subnetPool(self, subnet):
        ippool = list()
        
        subnet = subnet['subnet'] + u'/' + unicode(subnet['cidr'])
        
        network = ipaddr.IPNetwork(subnet)
        
        if self.tun:
            subnets = network.iter_subnets(new_prefix=30)
        else:
            subnets = network.iter_subnets(new_prefix=32)
        
        for subnet in subnets:
            if self.tun:
                address = str(list(subnet)[1])
            else:
                address = str(list(subnet)[0])
            ippool.append(address)
        
        return ippool[2:-1]
    
    def exclude(self, address):
        if address not in self.excludelist:
            self.excludelist.append(address)
    
    def pool(self):
        results = list()
        
        for subnet in self.subnets:
            for address in self.subnetPool(subnet):
                if address not in self.excludelist:
                    result = subnet.copy()
                    result['address'] = address
                    results.append(result)
        
        return results
    
    def available(self):
        for subnet in self.subnets:
            for address in self.subnetPool(subnet):
                if address not in self.excludelist:
                    result = subnet.copy()
                    result['address'] = address
                    return result
        return None

if __name__ == "__main__":
    p = Pool()
    
    p.addSubnet("10.8.0.0", 24)
    p.addSubnet("10.8.1.0", 24)
    
    print p.pool()