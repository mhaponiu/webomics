from threading import Thread
import time

import logging
logger = logging.getLogger('cgb')  # logger z settings.py

## Klasa przetrzymujaca wszystkie informacje o dzialaniu watkow dlugotrwalych
# Wzorzec Singleton
class RemoteManager(object):
    ## Obiekt singletona
    instance = None
    
    ## Slownik ze wszystkimi watkami {id : (percent, result)}
    remotes = {}
    
    ## Aktualnie przypisany numer ID
    current_id = 0
    
    ## Konstruktor
    def __init__(self):
        if not (RemoteManager.instance):
            RemoteManager.instance = self
        return
    
    ## Funkcja tworzaca watek w ktorym uruchamia podana funkcje
    #  @param function: Uruchamiana funkcja
    #  @param parameters: Lista parametrow uruchamianej funkcji
    #  @return: ID uruchomionego watku
    def run(self, function, params):
        # Inicjacja funkcji w tablicy watkow
        self.instance.remotes[self.instance.current_id] = (0, "", None)
        thread_id = self.instance.current_id
        self.instance.current_id += 1

        # Uruchomienie funkcji w oddzielnym watku
        FunctionThread(thread_id, self.update, function, params).start()
        
        return thread_id

    ## Funkcja aktualizujaca tablice watkow
    #  @param thread_id: ID uruchamianego watku
    #  @param percent: Procent wykonania funkcji
    #  @param result: Rezultat wykonania funkcji
    #  @return: 
    def update(self, thread_id, percent, comment = "", inc = False, result = None):
        try:
            if inc == True:
                old_percent = self.instance.remotes[thread_id][0]
                comment = self.instance.remotes[thread_id][1]
                print "OLD", old_percent
                self.instance.remotes[thread_id] = (old_percent + percent, comment, result)
                print "Po uaktualnieniu:", self.instance.remotes[thread_id]
            else:
                self.instance.remotes[thread_id] = (percent, comment, result)
        except KeyError:
            return None
        
    ## Funkcja zwracajaca wynik dzialania (progres) funkcji o zadanym ID
    #  @param thread_id: ID watku
    #  @return: 
    def get(self, thread_id):
        try:
            return self.instance.remotes[thread_id]
        except KeyError:
            return None
        
    def size(self):
        return len(self.instance.remotes);

RM = RemoteManager()

class FunctionThread(Thread):
    def __init__(self, thread_id, update, function, parameters):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.function = function
        self.parameters = parameters
        self.update = update

    def callback(self, percent, comment, inc = False):
        self.update(self.thread_id, percent, comment, inc)
        time.sleep(0.1)

    def run(self):
        result = self.function(self.callback, **(self.parameters))
        self.update(self.thread_id, 100, "Finished", False, result)

if __name__ == '__main__':
    m = RemoteManager()