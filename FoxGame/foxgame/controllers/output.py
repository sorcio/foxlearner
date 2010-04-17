from foxgame.controller import PostFilter
from foxgame.options import FoxgameOption

import os
import os.path
from glob import glob

import logging
log = logging.getLogger(__name__)

__extraopts__ = (FoxgameOption('logfile'),
                 FoxgameOption('append', type='bool'),
                 FoxgameOption('skiphead', type='bool'),
                 FoxgameOption('delimiter'),
                )

class CSV(PostFilter):
    """
    A simple postfilter which outputs sequential game data to CSV file.
    """

    logfile = 'game.csv'
    append = False
    skiphead = False
    delimiter = ','

    def set_up(self):
        self.file = None
        
        if self.append:
            self.open_append(self.logfile)
        else:
            self.open_new(self.logfile)
        
        if not self.skiphead:
            self.write_head()

    def open_new(self, basepath):
        base, ext = os.path.splitext(basepath)
        allfiles = glob(base + '-[0-9][0-9][0-9][0-9]' + ext)
        if allfiles:
            maxname = max(allfiles)
            nextn = int(maxname[len(base)+1:len(base)+5]) + 1
        else:
            nextn = 0
        path = '%s-%04d%s' % (base, nextn, ext)
        return self.lock_open(path)
        
    def open_append(self, basepath):
        return self.lock_open(basepath)
    
    def lock_open(self, path):
        self.lockfile = path + '.lock'
        if os.path.exists(self.lockfile):
            log.error('Output file is locked!')
            self.file = None
        else:
            log.info('Opening log file %s for <%s>',
                     path, self.pawn.__class__.__name__)
            open(self.lockfile, 'w+').close()
            self.file = open(path, 'a+')
    
    def tear_down(self):
        if self.file:
            log.debug('Closing log file')
            self.file.close()
            if self.lockfile:
                os.remove(self.lockfile)

    def write_head(self):
        if not self.file:
            return
        
        print >>self.file, '# starting logging'
        print >>self.file, '# nfoxes =', len(self.game.foxes)
        print >>self.file, '# game.size =', self.game.size.x, self.game.size.y
        print >>self.file, '# pawnclass =', self.pawn.__class__.__name__
        
        head = ['time']
        for i in range(len(self.game.foxes)):
            head.append('fox%d_x' % i)
            head.append('fox%d_y' % i)
            head.append('fox%d_speed_x' % i)
            head.append('fox%d_speed_y' % i)
        head += ['hare_x', 'hare_y',
                 'hare_speed_x', 'hare_speed_y',
                 'carrot_x', 'carrot_y',
                 'dir_h', 'dir_v']
        print >>self.file, self.delimiter.join(head)
    
    def update(self, direction, time):
        if not self.file:
            return
        
        line = [self.game.time_elapsed]
        for fox in self.game.foxes:
            line.append(fox.pos.x)
            line.append(fox.pos.y)
            line.append(fox.speed.x)
            line.append(fox.speed.y)
        line += [self.game.hare.pos.x, self.game.hare.pos.y,
                 self.game.hare.speed.x, self.game.hare.speed.y,
                 self.game.carrot.pos.x, self.game.carrot.pos.y,
                 direction.hor, direction.vert]
        
        print >>self.file, self.delimiter.join(map(str, line))
        
        return direction

import csv

def read_cvs(filename, delimiter=',', comment='#'):
    """
    A generator which parses CVS data.
    """
    csvfile = CommentedFile(open(filename), commentstring=comment)
    #dialect = csv.Sniffer().sniff(csvfile.read(1024))
    #csvfile.seek(0)
    reader = csv.DictReader(csvfile, delimiter=delimiter)
    
    for row in reader:
        for k in row:
            row[k] = float(row[k])
        yield row


class CommentedFile(object):
    """
    File object wrapper which skips lines
    starting with commentstring.
    """
    def __init__(self, f, commentstring="#"):
        self.f = f
        self.commentstring = commentstring

    def next(self):
        line = self.f.next()
        while line.startswith(self.commentstring):
            line = self.f.next()
        return line

    def __iter__(self):
        return self
