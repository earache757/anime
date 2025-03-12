I have this running on a crontab every Sunday morning.

It opens a firefox window...
  checks if an ics exists on downloads and checks the date
  downloads the ICS file from https://work-nu-tawny.vercel.app/anime.html
  moves to a folder and renames (this is since I use it in Thunderbird so need the same filename)
  closes the browser
  sends notifications to gotify

Of course, this is VERY rough and the website may go down at any time, but this was a fun personal project I figured I'd share.

Note, check the code and adjust to your pathing and you can remove gotify if needed (naturally!)
