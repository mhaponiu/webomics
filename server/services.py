## @package server
#  Modul informacyjny serwera - test komunikacji, logi serwera, czas serwera
#  @author: Piotr Roz

import datetime
import sys
import os

from server.utils import log as LOG

request = 0
log_path = os.path.join('server', 'log', 'cgb_server.log')

def echo():
	LOG.INFO("Rozpoczynam test komunikacji")
	global request
	request += 1
	LOG.INFO("Test komunikacji zakonczony powodzeniem.")
	return "Echo: " + str(request)

def startClient():
	#if os.path.exists(log_path):
	#	open(log_path, "w")
	LOG.INFO("\n\n=========================== START KLIENTA APLIKACJI ==============================\n")

def getServerTime():
	LOG.INFO("Pobieram czas serwerowy.")
	return datetime.datetime.now().isoformat()

## Funkcja zwracajaca ostatnich num_lines linii logow
#  @param num_lines: liczba linii, ktora zostanie zwrocona
#  @return: zwrocone linie logow
def getLogFile(num_lines):
	LOG.INFO("Rozpoczynam pobieranie " + str(num_lines) + " ostatnich linii z loggera.")
	log = open(log_path, 'r')
	lines = log.readlines()[-int(num_lines):]
	new_lines = []
	for line in lines:
		new_lines.append(line.replace("\n", "<br/>"))
	LOG.INFO("Zakonczylem pobieranie linii z loggera.")
	return new_lines