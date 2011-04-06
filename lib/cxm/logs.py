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


from twisted.python import log
import core
import syslog

def init(name):
	syslog.openlog(name, syslog.LOG_PID, syslog.LOG_DAEMON)

def info(message, **kw):
	log.msg(message, **kw)

def debug(message, **kw):
	if core.cfg['DEBUG']:
		log.msg("DEBUG: %s" % (message), **kw)
		
def warn(message, **kw):
	log.msg("Warning: %s" % (message), **kw)
	syslog.syslog(syslog.LOG_WARNING, str(message))

def err(message, **kw):
	log.err("Error: %s" % (message), **kw)
	syslog.syslog(syslog.LOG_ERR, str(message))

def emerg(message, **kw):
	log.err("CRITICAL ERROR: %s" % (message), **kw)
	syslog.syslog(syslog.LOG_EMERG, str(message))

# vim: ts=4:sw=4:ai