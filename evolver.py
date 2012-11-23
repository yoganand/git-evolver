

import os

from git import *

    
class CommandHandler(object):
    def __init__(self, repo, commits):
        self.repo = repo
        self.commits = commits
        self.git = repo.git
        self.previous_commit = None
        self.current_commit = None
        self.ndx = None
        self.first()
        
    def run(self, cmd="help"):
        try:
            command = getattr(self, cmd)
            return command()
        except AttributeError:
            return self.exit()

    def first(self):
        self.git.checkout(commits[-1])
        self.current_commit = commits[-1]
        self.ndx = 1
        return True

    def next(self):
        self.ndx += 1
        ndx = -1 * self.ndx 
        self.git.checkout(commits[ndx])
        self.previous_commit = self.current_commit
        self.current_commit = commits[ndx]
        return True

    def previous(self):
        if self.ndx == 1:
            return True
        self.ndx += -1
        ndx = -1 * self.ndx 
        self.git.checkout(commits[ndx])
        self.previous_commit = commits[ndx + 1]
        self.current_commit = commits[ndx]
        return True

    def current(self):
        print self.current_commit
        return True

    def number(self):
        print self.ndx
        return True

    def message(self):
        print repo.commit(self.current_commit).message
        return True

    def author(self):
        print repo.commit(self.current_commit).author
        return True

    def committer(self):
        print repo.commit(self.current_commit).committer
        return True

    def date(self):
        print repo.commit(self.current_commit).committed_date
        return True
 
    def files(self):
        files = self.git.diff('--name-only', 
				self.current_commit, 
				self.previous_commit)        
        print files
        return True

    def details(self):
        details = self.git.diff(self.current_commit, self.previous_commit) 
        print details
        return True 



    def help(self):
        print "help: list of commands"
        print "exit: exits the program"
        print "first: checkout the first commit"
        print "next: checkout the next commit"
        print "previous: checkout the previous commit"
        print "current: print the current commit"
        print "number: print the serial number for the commit"
        print "message: print the message from current commit"
        print "author: print the author of the repo"
        print "committer: print the committer of the current commit"
        print "date: print the committed date of current commit"
        print "files: print the files that were changed in the commit"
        print "details: print the diff of the current commit"
        return True
   
    def exit(self):
        return False
        


if __name__ == '__main__':
    repo_dir = os.path.dirname(os.path.realpath(__file__))
    repo = Repo(repo_dir)
    commits = []
    for commit in repo.iter_commits('master'):
        commits.append(commit.hexsha)

    command_handler = CommandHandler(repo, commits)
    exit = True
    while exit == True:
        cmd = raw_input("Command (type help for list of commands): ")
        exit = command_handler.run(cmd=cmd)
