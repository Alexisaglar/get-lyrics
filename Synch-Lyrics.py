# first : have python-dbus installed
# sudo apt-get install python-dbus

# run like this : python filename.py --notiftwenty --loop

import json
import sys
import os
import subprocess
from argparse import ArgumentParser

import dbus


session_bus = dbus.SessionBus()
#bus_data = ("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
spotify_bus = session_bus.get_object('org.mpris.MediaPlayer2.spotify',
                                     '/org/mpris/MediaPlayer2')
spotify_properties = dbus.Interface(spotify_bus,
                                    'org.freedesktop.DBus.Properties')
#print(spotify_properties)
#rhythmbox_bus = session_bus.get_object(*bus_data)
#interface = dbus.Interface(rhythmbox_bus, "org.freedesktop.DBus.Properties")
metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
#print(metadata)
position = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Position")
print(position)

parser = ArgumentParser()
parser.add_argument('--artist', action='store_true')
parser.add_argument('--song', action='store_true')
parser.add_argument('--album', action='store_true')
parser.add_argument('--position', action='store_true')
parser.add_argument('--duration', action='store_true')
parser.add_argument('--remaining', action='store_true')
parser.add_argument('--loop', action='store_true')
parser.add_argument('--notiftwenty', action='store_true')
parser.add_argument('--rating', action='store_true')
parser.add_argument('--format', default='json')

def main():
    args = parser.parse_args()
    data = dict()

    if args.position:
        data['position'] = str(position)

    if args.duration:
        data['duration'] = str(metadata['mpris:length'])

    if args.remaining:
        data['remaining'] = str(metadata['mpris:length'] - position)

    if args.rating:
        data['rating'] = str(metadata['xesam:userRating'] * 5)

    if args.notiftwenty:
        if metadata['xesam:userRating'] * 5 < 0.5:
            if metadata['mpris:length'] - position == 20000000:
                data['notiftwenty'] = str('true')
                subprocess.check_output(["notify-send",
                                         "Rhythmbox : notez cette piste !",
                                         "Ce morceau n'a actuellement pas de note...",
                                         "--icon=rhythmbox"])
        if args.loop:
            data['loop'] = str('true')
            subprocess.check_output("sleep 1 && python "+ os.path.realpath(__file__) +" --notiftwenty --loop", shell=True)


    if args.artist:
        data['artist'] = str(next(iter(metadata['xesam:albumArtist'])))

    if args.song:
        data['song'] = str(metadata['xesam:title'])

    if args.album:
        data['album'] = str(metadata['xesam:album'])

    sys.stdout.write(json.dumps(data))


if __name__ == '__main__':
    main()
