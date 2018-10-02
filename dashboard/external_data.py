# Copyright 2013,2014 Music Technology Group - Universitat Pompeu Fabra
#
# This file is part of Dunya
#
# Dunya is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free Software
# Foundation (FSF), either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see http://www.gnu.org/licenses/

from __future__ import print_function
import os

from compmusic import image
from compmusic import kutcheris
from compmusic import wikipedia
from django.core.files.base import ContentFile

import data.models


def import_artist_kutcheris(a):
    artist = kutcheris.search_artist(a.name)
    if artist:
        print("Found data on kutcheris.com")
        aid = artist.values()[0]
        i, b, u = kutcheris.get_artist_details(aid)
        u = "http://kutcheris.com/artist.php?id=%s" % aid
        if b:
            sn = data.models.SourceName.objects.get(name="kutcheris.com")

    if b:
        source, created = data.models.Source.objects.get_or_create(source_name=sn, uri=u, defaults={"title": a.name})
        description = data.models.Description.objects.create(description=b, source=source)
        a.description = description
        a.save()


def import_artist_wikipedia(artist, source):
    print("Looking for data on wikipedia")

    wikipedia_url = source.uri
    name = os.path.basename(wikipedia_url)

    img, bio = wikipedia.get_artist_details(name)
    if bio:
        description = data.models.Description.objects.create(description=bio, source=source)
        # We call this with Composers too, which don't have `description_edited`
        # If d_edited is set, never overwrite it.
        if not getattr(artist, 'description_edited', False):
            artist.description = description
            artist.save()
    if img:
        if artist.image:
            if not os.path.exists(artist.image.image.path):
                artist.image.delete()
            elif artist.image.image.size != len(img):
                # If the imagesize has changed, remove the image
                os.unlink(existingimg.image.path)
                artist.image.delete()

        im = data.models.Image()
        im.image.save("artist-%s.jpg" % artist.mbid, ContentFile(img))
        artist.image = im


def import_release_image(release, directories=[]):
    if release.image:
        print("Image for release %s exists, skipping" % release.mbid)
        return

    i = image.get_coverart_from_caa(release.mbid)
    caa = True
    if not i:
        caa = False
        print("No image on CAA for %s, looking in directory" % release.mbid)
        i = image.get_coverart_from_directories(directories)
    if i:
        im = data.models.Image()
        if caa:
            uri = "http://archive.org/details/mbid-%s" % release.mbid
            sn = data.models.SourceName.objects.get(name="Cover Art Archive")
            source, created = data.models.Source.objects.get_or_create(source_name=sn, uri=uri, defaults={"title": release.title})
            im.source = source
        im.image.save("release-%s.jpg" % release.mbid, ContentFile(i))

        # If the image is a different size from one that already exists, then
        # replace it. Also remove if we have an item, but can't find the image
        # for it.
        if release.image:
            existingimg = release.image
            haveimage = True
            if not os.path.exists(existingimg.image.path):
                existingimg.delete()
            elif existingimg.image.size != len(i):
                # If the imagesize has changed, remove it
                os.unlink(existingimg.image.path)
                existingimg.delete()
        else:
            haveimage = False

        # If we have an image, don't add it
        if not haveimage:
            release.image = im
            release.save()
    else:
        print("Can't find an image for %s" % release.mbid)
