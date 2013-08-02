bhamari
=======

Asana-Beeminder integration

This repo began as a hackathon project towards integrating Asana and Beeminder. asana_reporter.py is a script that
fetches all completed Asana tasks with a given tag, removes the tag, and posts corresponding data points in a given
Beeminder goal. Currently, you'll have to hard-code in some values (marked with "#SET THIS") and figure out a way to
run the script periodically (e.g. cron).
