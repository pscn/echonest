# -*- coding: utf-8 -*-

# Copyright 2011 Peter Schnebel <pschnebel@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

# This plugin is copied from the lastfm plugin by Lukáš Lalinský

PLUGIN_NAME = u'echonest'
PLUGIN_AUTHOR = u'Peter Schnebel'
PLUGIN_DESCRIPTION = u'Lookup bpm, energy and danceability in echo nest.'
PLUGIN_VERSION = "0.1"
PLUGIN_API_VERSIONS = ["0.15"] # FIXME:  unsure

from PyQt4 import QtCore
from picard.metadata import register_track_metadata_processor
from picard.ui.options import register_options_page, OptionsPage
from picard.config import BoolOption, FloatOption
from picard.plugins.echonest.ui_options_echonest import Ui_EchoNestOptionsPage
from picard.util import partial
from pyechonest import song as echosong
from pyechonest import track as echotrack
from pyechonest import config as echoconfig
from pyechonest.util import EchoNestAPIError
import traceback

# please get your own api key @ http://developer.echonest.com/ if you change
# any of this code
echoconfig.ECHO_NEST_API_KEY = "UUTWEXSUI5PN95PID"

# FIXME:  only for hijacking add_task of xmlws
from picard.webservice import REQUEST_DELAY
ECHONEST_HOST = "developer.echonest.com"
ECHONEST_PORT = 80
REQUEST_DELAY[(ECHONEST_HOST, ECHONEST_PORT)] = 200

def req_plus(album):
    album._requests += 1

def req_minus(album):
    album._requests -= 1
    album._finalize_loading(None)

def lookup_track(album, metadata, release, track):
    tagger = album.tagger
    upload = tagger.config.setting["echonest_upload"]
    artist_title_lookup = tagger.config.setting["echonest_artist_title_lookup"]
    songs = []
    try:
      songs = echosong.profile([u"musicbrainz:song:%s" % metadata['musicbrainz_trackid']],
          buckets="audio_summary")
    except EchoNestAPIError:
      if artist_title_lookup:
        songs = echosong.search(title=metadata['title'], artist=metadata['artist'])
    min_diff = tagger.config.setting["echonest_duration_diff"]
    match = None
    for song in songs:
        # try to match based on duration / length
        len_diff = abs(metadata.length / 1000.0 - song.audio_summary['duration'])
        if min_diff < 0.0 or len_diff < min_diff:
            min_diff = len_diff
            match = song
    if match:
        metadata['bpm'] = str(match.audio_summary['tempo'])
        metadata['comment:Songs-DB_Energy'] = str(match.audio_summary['energy'])
        metadata['comment:Songs-DB_Danceability'] = str(match.audio_summary['danceability'])
    elif upload:
        # FIXME:  how do i get the filename for this track?
        pass
    req_minus(album)

def process_track(album, metadata, release, track):
    # FIXME: do not hijack add_task
    req_plus(album)
    album.tagger.xmlws.add_task(partial(lookup_track, album, metadata, release, track)
        , ECHONEST_HOST, ECHONEST_PORT, priority=True, important=True)

class EchoNestOptionsPage(OptionsPage):
    NAME = "echonest"
    TITLE = "echonest"
    PARENT = "plugins"

    options = [
        BoolOption("setting", "echonest_upload", False),
        BoolOption("setting", "echonest_artist_title_lookup", True),
        FloatOption("setting", "echonest_duration_diff", 5.0),
    ]

    def __init__(self, parent=None):
        super(EchoNestOptionsPage, self).__init__(parent)
        self.ui = Ui_EchoNestOptionsPage()
        self.ui.setupUi(self)

    def load(self):
        #self.ui.echonest_upload.setChecked(self.config.setting["echonest_upload"])
        self.ui.echonest_artist_title_lookup.setChecked(self.config.setting["echonest_artist_title_lookup"])
        #self.ui.echonest_duration_diff.setChecked(self.config.setting["echonest_duration_diff"])

    def save(self):
        #self.config.setting["echonest_upload"] = self.ui.echonest_upload.isChecked()
        self.config.setting["echonest_artist_title_lookup"] = self.ui.echonest_artist_title_lookup.isChecked()
        #self.config.setting["echonest_duration_diff"] = self.ui.echonest_duration_diff.value()

register_track_metadata_processor(process_track)
register_options_page(EchoNestOptionsPage)

# eof
