import os, sys, platform, time
import SCons.Builder
from subprocess import call

# ======================================= Sciezki i ustawienia ======================================= 

PROJECT_PATH_WINDOWS = 'D:/Uczelnia/PracaMagisterska/GenomeBrowser/trunk/implementation'
PROJECT_PATH_LINUX = '/home/mhaponiu/Pobrane/webomics'

# PYTHON INCLUDE
PYTHON_INCLUDE_WINDOWS = 'E:/Python27/include'
PYTHON_INCLUDE_LINUX = '/usr/include/python2.7'

# PYTHON LIB
PYTHON_LIB_WINDOWS = 'E:/Python27/libs'
PYTHON_LIB_LINUX = '/usr/lib/python2.7'

# BOOST
BOOST_INCLUDE_WINDOWS = 'E:/boost/boost_1_51'
BOOST_INCLUDE_LINUX = '/usr/local/include/boost'
BOOST_LIB_WINDOWS = 'E:/boost/boost_1_51/lib'
LIBBOOST_PYTHON = '/usr/local/lib/libboost_python.so'

# FLEX
FLEX_PATH_WINDOWS = 'E:/flex_sdk'
FLEX_PATH_LINUX = '/home/mhaponiu/flex_sdk_4.6'

FLEX_CONFIG_LINUX = 'config_linux.xml'
FLEX_CONFIG_WINDOWS = 'config_windows.xml'

# NAZWA BIBLIOTEKI WSPOLDZIELONEJ
LIB_NAME = 'calc'

# SCIEZKA PRZEGLADARKI INTERNETOWEJ
WEB_LINUX = '/usr/bin/google-chrome'
WEB_WINDOWS = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

# NCBI BLAST
NCBI_BLAST_WINDOWS = 'E:\NCBI\blast-2.2.27+\bin'
NCBI_BLAST_LINUX = ''

# ====================================================================================================

# Wyeksportowanie wszystkich zmiennych ze sciezkami
Export('PROJECT_PATH_WINDOWS')
Export('PROJECT_PATH_LINUX')

# PYTHON
Export('PYTHON_INCLUDE_WINDOWS PYTHON_INCLUDE_LINUX PYTHON_LIB_WINDOWS PYTHON_LIB_LINUX')

# BOOST
Export('BOOST_INCLUDE_WINDOWS BOOST_INCLUDE_LINUX BOOST_LIB_WINDOWS LIBBOOST_PYTHON')

# FLEX
Export('FLEX_PATH_WINDOWS')
Export('FLEX_PATH_LINUX')
Export('FLEX_CONFIG_LINUX')
Export('FLEX_CONFIG_WINDOWS')

Export('WEB_WINDOWS')
Export('WEB_LINUX')

# ====================================================================================================

# Mozliwosci uruchomienia
vars = Variables('custom.py')
vars.Add(BoolVariable('calc','Ustaw na 1, aby zbudowac biblioteke obliczeniowa.', 0) )
vars.Add(BoolVariable('client','Ustaw na 1, aby zbudowac interfejs uzytkownika.', 0) )
vars.Add(BoolVariable('run','Ustaw na 1, aby uruchomic aplikacje serwera.', 0) )
vars.Add(BoolVariable('runclient','Ustaw na 1, aby uruchomic aplikacje klienta.', 0) )
vars.Add(BoolVariable('debug','Ustaw na 1, aby uruchomic wersje debug aplikacji serwera.', 0) )
vars.Add(BoolVariable('test','Ustaw na 1, aby uruchomic testy jednostkowe.', 0) )
vars.Add(BoolVariable('testapp','Ustaw na 1, aby uruchomic testy jednostkowe serwera aplikacji.', 0) )
vars.Add(BoolVariable('shell','Ustaw na 1, aby uruchomic powloke serwera aplikacji.', 0) )
vars.Add(BoolVariable('createdb','Ustaw na 1, aby utworzyc tabele bazy danych.', 0) )
vars.Add(BoolVariable('syncdb','Ustaw na 1, aby zaladowac poczatkowe dane genomu ogorka.', 0) )

# Srodowisko
env = Environment(variables=vars)

# Pomoc
Help(vars.GenerateHelpText(env))

# Sciezki
env.Append( ENV = {'PATH' : os.environ['PATH'] })
env.Append( LIBPATH = [ Dir('./') ] )

os.putenv('DJANGO_SETTINGS_MODULE','server.config.settings')

if(platform.system() == "Linux"):
    WEB_BROWSER = WEB_LINUX
elif(platform.system() == "Windows"):
    WEB_BROWSER = WEB_WINDOWS
else:
    print platform.system() + " nie obslugiwany!"
    sys.exit(1)
	
if env['debug'] == 1:
	DEBUG = True
else:
	DEBUG = False
	
Export('DEBUG')
	
if env['calc'] == 1:
    SConscript(['calculation/SConscript'], exports=['env'])
elif env['client'] == 1:
    SConscript(['client/SConscript'], exports=['env'])
    #os.system('"' + WEB_BROWSER + '" ' + os.getcwd() + '/client/build/CucumberBrowser.html')
elif env['run'] == 1:
    os.system('python server/config/manage.py runserver &')
elif env['runclient'] == 1:
	os.system('"' + WEB_BROWSER + '" ' + os.getcwd() + '/client/build/WebOmicsViewer.html')
elif env['testapp'] == 1:
    os.system('python server/config/manage.py test')
elif env['test'] == 1:
    if(platform.system() == "Linux"):
        print "\n---------------------------------------------"
        print "Testy algorytmu BLAST\n"
        call('calculation/build/tests/calcBlastTests')
        print "\n---------------------------------------------"
        print "Testy algorytmu SW\n"
        call('calculation/build/tests/calcSWTests')
        print "\n---------------------------------------------"
        print "Testy algorytmu KMP\n"
        call('calculation/build/tests/calcKMPTests')
        print "\n---------------------------------------------"
        print "Testy algorytmu BM\n"
        call('calculation/build/tests/calcBMTests')
    elif(platform.system() == "Windows"):
        print "\n---------------------------------------------"
        print "Testy algorytmu BLAST\n"
        call('calculation/build/tests/calcBlastTests.exe')
        print "\n---------------------------------------------"
        print "Testy algorytmu SW\n"
        call('calculation/build/tests/calcSWTests.exe')
        print "\n---------------------------------------------"
        print "Testy algorytmu KMP\n"
        call('calculation/build/tests/calcKMPTests.exe')
        print "\n---------------------------------------------"
        print "Testy algorytmu BM\n"
        call('calculation/build/tests/calcBMTests.exe')
elif env['shell'] == 1:
    os.system('python server/config/manage.py shell')
elif env['createdb'] == 1:
    os.system('python server/config/manage.py syncdb')
elif env['syncdb'] == 1:
    dirList = os.listdir(os.path.join('server', 'fixtures'))
    for fname in dirList:
        print "Loading application data:", fname.replace('_data.json', '')
        os.system('python server/config/manage.py loaddata server/fixtures/' + str(fname))
