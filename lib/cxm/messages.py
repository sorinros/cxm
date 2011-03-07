# -*- coding:Utf-8 -*-

# cxm - Clustered Xen Management API and tools
# Copyleft 2011 - Nicolas AGIUS <nagius@astek.fr>
# $Id:$

###########################################################################
#
# This file is part of cxm.
#
# cxm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###########################################################################


from pprint import pprint
import time
from dnscache import DNSCache

# TODO a passer en cfg
CLUSTER_NAME="cltest"




class Message(object):
	def __init__(self, host=None):
		if host is None:
			self.node=DNSCache.getInstance().name
		else:
			self.node=DNSCache.getInstance().get_by_ip(host)

	def type(self):
		for (key, value) in MessageHelper.map.iteritems():
			if type(self) == value:
				return key
		raise MessageError("Wrong type !")

	def parse(self, data):
		self.cluster=data['cluster']

		# Discard message from others clusters 
		if self.cluster != CLUSTER_NAME:
			raise IDontCareException("Message from other cluster %s ignored." % (self.cluster))

	def forge(self):
		self.cluster=CLUSTER_NAME

	def value(self, data):
		data['cluster']=self.cluster
		return {"type": self.type(), "data": data}

class MessageSlaveHB(Message):
	def __init__(self, host=None):
		super(MessageSlaveHB,self).__init__(host)

	def parse(self, data):
		super(MessageSlaveHB,self).parse(data)
		self.ts=data['ts']
		self.vms=data['vms']

		# Check variable type
		if type(self.vms) != list:
			raise MessageError("vms must be a list")

		return self
	
	def forge(self, node):
		super(MessageSlaveHB,self).forge()
		self.ts=int(time.time())
		self.vms=map(lambda x: x.name, node.get_vms())
		return self

	def value(self):
		msg = {'ts': self.ts, 'vms': self.vms}
		return super(MessageSlaveHB,self).value(msg)

	def __repr__(self):
		return str("<MessageSlaveHB from "+ self.node +" : "+str(self.ts)+">")

class MessageMasterHB(Message):
	
	def __init__(self, host=None):
		super(MessageMasterHB,self).__init__(host)

	def parse(self, data):
		super(MessageMasterHB,self).parse(data)
		self.status=data['status']

		# Check variable type
		if type(self.status) != dict:
			raise MessageError("Status must be a dict")

		return self
		
	def forge(self, status):
		super(MessageMasterHB,self).forge()

		self.status=status
		return self

	def value(self):
		msg = {'status': self.status}
		return super(MessageMasterHB,self).value(msg)

	def __repr__(self):
		return str("<MessageMasterHB from "+ self.node +" : "+str(self.status)+">")


class MessageHelper(object):

	map = {
		"slavehb" : MessageSlaveHB,
		"masterhb" : MessageMasterHB,
	}

	@staticmethod
	def get(msg, host):
		try:
			# Throw KeyError if the message is bad
			return MessageHelper.map[msg['type']](host).parse(msg['data'])
		except KeyError, e:
			raise MessageError("KeyError: "+str(e))

	@staticmethod
	def type(msg):
		if msg['type'] in Messages.map:
			return msg['type']
		else:
			raise MessageError("bad type")


class MessageError(Exception):
	pass

class IDontCareException(Exception):
	pass


# vim: ts=4:sw=4:ai