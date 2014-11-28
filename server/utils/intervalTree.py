import sys
import operator

import logging
logger = logging.getLogger('cgb')  # logger z settings.py

## Klasa drzewa przedzialowego
class IntervalTree(object):
    ## Konstruktor
    #  @param intervals: Lista przedzialow zawierajaca atrybuty start oraz stop
    #  @param depth: Glebokosc drzewa 
    #  @param minbucket: Jezeli kazdy wezel w drzewie ma mniejsza wartosc od tego parametru - elementy staja sie lisciem
    #  @param _extent: 
    #  @param maxbucket: Jezeli ilosc przedzialow jest wieksza od tego parametru, wezel jest dzielone powodujac zwiekszenie glebokosci drzewa (niezaleznie od parametru depth)
    def __init__(self, intervals, depth = 16, minbucket = 96, _extent = None, maxbucket = 4096, counter = 0):
        depth -= 1
        counter += 1
        # Konczymy budowanie drzewa?
        if (depth == 0 or len(intervals) < minbucket) and len(intervals) > maxbucket:
            self.intervals = intervals
            self.left = self.right = None
            return
        
        # Za duzo rekurencji?
        if counter >= 1200:
            self.intervals = intervals
            self.left = self.right = None
            return

        if _extent is None:
            # Posortowanie dla zwiekszenia wydajnosci dzialania drzewa
            intervals.sort(key = operator.attrgetter('start'))

        left, right = _extent or (min(i.start for i in intervals), max(i.stop for i in intervals))
        #center = intervals[len(intervals)/ 2].stop
        center = (left + right) / 2.0

        self.intervals = []
        lefts, rights = [], []

        for interval in intervals:
            if interval.stop < center:
                lefts.append(interval)
            elif interval.start > center:
                rights.append(interval)
            else:
                self.intervals.append(interval)

        self.left = lefts and IntervalTree(lefts, depth, minbucket, (left, center), maxbucket, counter) or None
        self.right = rights and IntervalTree(rights, depth, minbucket, (center, right), maxbucket, counter) or None
        self.center = center

    ## Funkcja szukajaca do ktorych przedzialow nalezy zadany przedzial
    #  @param start: Poczatek przedzialu 
    #  @param stop: Koniec przedzialu
    #  @return: Lista przedzialow odpowiadajaca zadanemu przedzialowi
    def find(self, start, stop):
        if self.intervals and not stop < self.intervals[0].start:
            overlapping = [i for i in self.intervals if i.stop >= start and i.start <= stop]
        else:
            overlapping = []

        if self.left and start <= self.center:
            overlapping += self.left.find(start, stop)

        if self.right and stop >= self.center:
            overlapping += self.right.find(start, stop)

        return overlapping

## Klasa reprezentujaca pojedynczy przedzial
class Interval(object):
    ## Konstruktor
    #  @param start: Poczatek przedzialu
    #  @param stop: Koniec przedzialu
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __unicode__(self):
        return str(self.start) + "; " + str(self.stop)


## Glowna funkcja uruchamiajaca skrypt, jezeli nie jest on importowany jako modul
def main(argv):
    interval_tree = IntervalTree([Interval(4.029, 30.726), Interval(33.043, 37.951), Interval(37.951, 38.761), Interval(39.452, 39.452)])
    for interval in interval_tree.find(8.0, 34.1):
        print "(", interval.start, ";", interval.stop, ")"

if __name__ == '__main__':
    main(sys.argv[1:])
