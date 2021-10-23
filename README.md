# dl.maxic.codes

A little test project I made to get to grips with Flask and writing REST APIs in Python... and to let me steal Twitter videos on my phone :^)

## Set up

I have this running on my VPS behind an Nginx reverse proxy so I didn't have to faff with making Flask use an SSL certificate. The Python file runs in a virtualenv as a systemd service so I can restart it easily.

On my phone, I have a simple iOS Shortcut that accepts a URL and makes a call to the API endpoint `dl.maxic.codes/v1/get_url` with `key` (the API key, this is a private instance 😘) and `url` (the URL of the video you want to download). The Python script downloads the video and sends it straight back out to the requester (aka me).

There's probably an easier way to do this, like just redirecting to the video URL itself, but some video services like YouTube limit access to the video files by IP which isn't ideal. For now, for me, this is probably enough 😇
