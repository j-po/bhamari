bhamari
=======

Asana-Beeminder integration

This repo began as a hackathon project towards integrating Asana and Beeminder. asana_reporter.py is a script that
fetches all completed Asana tasks with a given tag, removes the tag, and posts corresponding data points in a given
Beeminder goal. You'll need to set user-specific values in user_info.json and run the script periodically (e.g. with
cron) for full effect.

The Beeminder API calls here stopped working recently, making the script pretty useless. After spending a few hours trying to fix it, I've contacted Beeminder about it maybe being something on their end. (See Issue #12)
