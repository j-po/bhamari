bhamari
=======

Asana-Beeminder integration

This repo began as a hackathon project towards integrating Asana and Beeminder. asana_reporter.py is a script that
fetches all completed Asana tasks with a given tag, removes the tag, and posts corresponding data points in a given
Beeminder goal. You'll need to set user-specific values in user_data.json and run the script periodically (e.g. with
cron) for full effect.
