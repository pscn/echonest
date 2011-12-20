# -*- coding: utf-8 -*-

# Copyright 2011 Peter Schnebel <pschnebel@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

# This plugin is copied from the lastfm plugin by Lukáš Lalinský

import sys
from PyQt4 import QtCore, QtGui

class Ui_EchoNestOptionsPage(object):
    def setupUi(self, EchoNestOptionsPage):
        EchoNestOptionsPage.setObjectName("EchoNestOptionsPage")
        EchoNestOptionsPage.resize(QtCore.QSize(QtCore.QRect(0,0,305,317).size()).expandedTo(EchoNestOptionsPage.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(EchoNestOptionsPage)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.rename_files = QtGui.QGroupBox(EchoNestOptionsPage)
        self.rename_files.setObjectName("rename_files")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.rename_files)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(2)
        self.vboxlayout1.setObjectName("vboxlayout1")

        # FIXME:  how to upload files?  how to get the filenames?
        # self.echonest_upload = QtGui.QCheckBox(self.rename_files)
        # self.echonest_upload.setObjectName("echonest_upload")
        # self.vboxlayout1.addWidget(self.echonest_upload)

        self.echonest_artist_title_lookup = QtGui.QCheckBox(self.rename_files)
        self.echonest_artist_title_lookup.setObjectName("echonest_artist_title_lookup")
        self.vboxlayout1.addWidget(self.echonest_artist_title_lookup)

        self.vboxlayout.addWidget(self.rename_files)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(263,21,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.retranslateUi(EchoNestOptionsPage)
        QtCore.QMetaObject.connectSlotsByName(EchoNestOptionsPage)
        #EchoNestOptionsPage.setTabOrder(self.echonest_upload,self.echonest_artist_title_lookup)

    def retranslateUi(self, EchoNestOptionsPage):
        self.rename_files.setTitle(_("echonest"))
        #self.echonest_upload.setText(_("Upload files"))
        self.echonest_artist_title_lookup.setText(_("Use artist title lookup"))

