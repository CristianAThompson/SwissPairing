# Swiss Pairing With PostGreSQL
*In this we'll cover how and what to install in order
to correctly open and run the Swiss Pairing tournament_test.py file*

## Applications you'll need:
1. [Oracle VM Virtual Box](https://www.virtualbox.org/wiki/Download_Old_Builds_4_3): We use version 4.3.40 and only the hosts are required, not the SDK.
2. [Vagrant](https://www.vagrantup.com/downloads.html) The most recent verion of Vagrant must also be installed.
3. [Git Bash](https://git-scm.com/downloads) Will be the command line we will use to navigate to and run the files.

## The Files
Click [here](https://github.com/CristianAThompson/SwissPairing/archive/master.zip) to download the folder containing the needed files, or if you know how to use git you can clone `https://github.com/CristianAThompson/SwissPairing.git`

## Steps to initial run:

1. First open your git bash.
2. Using command-line navigation `cd` followed by the location from where your prompt starts for instance windows command prompt opens at `c/Users/<Your Username>` to navigate to the desktop it would be `cd Dekstop` Note: the directory is case specific. If you need to see what files are within the current directory you can use `ls`.
3. Once you've navigated inside the folder `SwissPairing` inside your command line interface you will run `vagrant up` which will start the initial install of all the necessary dependencies to run the tournament files.
4. After the command finishes you will follow it with `vagrant ssh` which will log you in to the virtual environment where we will run the files.
5. After it is installed the command line will say `vagrant@vagrant-ubuntu-trusty-32:~$` once this appears we will have to navigate to the tournament folder so we can run the files to do this we will have to run `cd ..` two times to move to the parent folders.
6. After having run `cd ..` two times we should have the line `vagrant@vagrant-ubuntu-trusty-32:/$` instead, once here we will type in `cd vagrant/tournament` to navigate to the folder with the tournament files.
7. Once we've run that command it should say `vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$` once here we need to run the sql file to create the database and tables for the tournament.
8. To create the database we will type `psql`
9. You'll know you're inside psql when it says `vagrant=>` we will then type `\i tournamentdb.sql` which will create the database after which we will type `\c tournament` and run `\i tournamenttables.sql` again and it will create all the tables needed. After it runs type `\q` to leave psql
10. Finally to run the tournament_test file we will type `python tournament_test.py`
11. To exit Vagrant after the test simply type `logout`
12. To stop Vagrant running in the background when done type `vagrant halt`
