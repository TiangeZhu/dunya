# -*- coding: UTF-8 -*-

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

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import json

from hindustani import models

def get_filter_items():
    filter_items = [
            models.Artist.get_filter_criteria(),
            models.Release.get_filter_criteria(),
            models.Instrument.get_filter_criteria(),
            models.Raag.get_filter_criteria(),
            models.Taal.get_filter_criteria(),
            models.Laya.get_filter_criteria(),
            models.Form.get_filter_criteria()
    ]
    return filter_items

def searchcomplete(request):
    # TODO: Hindustani-specific search
    term = request.GET.get("term")
    ret = []
    error = False
    if term:
        try:
            suggestions = search.autocomplete(term)
            ret = [{"id": i, "label": l, "value": l} for i, l in enumerate(suggestions, 1)]
        except pysolr.SolrError:
            error = True
    return HttpResponse(json.dumps(ret), content_type="application/json")

def main(request):
    qartist = []
    qinstr = []
    qraag = []
    qtaal = []
    qrelease = []
    if "a" in request.GET:
        for i in request.GET.getlist("a"):
            qartist.append(int(i))
    if "i" in request.GET:
        for i in request.GET.getlist("i"):
            qinstr.append(int(i))
    if "c" in request.GET:
        for i in request.GET.getlist("c"):
            qrelease.append(int(i))
    if "r" in request.GET:
        for i in request.GET.getlist("r"):
            qraag.append(int(i))
    if "t" in request.GET:
        for i in request.GET.getlist("t"):
            qtaal.append(int(i))
    if "q" in request.GET:
        query = request.GET.get("q")
        # special case, we have this so we can put a ? in the arglist
        # but it's actually a browse
        if query == "1":
            query = None
    else:
        query = None

    numartists = models.Artist.objects.filter(dummy=False).count()
    numcomposers = models.Composer.objects.count()
    numraags = models.Raag.objects.count()
    numtaals = models.Taal.objects.count()
    numreleases = models.Release.objects.count()
    numinstruments = models.Instrument.objects.count()
    numworks = models.Work.objects.count()

    displayres = []
    querybrowse = False
    searcherror = False

    if qartist:
        # TODO: If instrument set, only show artists who perform this instrument
        querybrowse = True

        # If raag or taal is set, make a list to filter releases by
        rlist = []
        tlist = []
        if qraag:
            for rid in qraag:
                ra = models.Raag.objects.get(pk=rid)
                rlist.append(ra)
        if qtaal:
            for tid in qtaal:
                ta = models.Taal.objects.get(pk=tid)
                tlist.append(ta)

        if len(qartist) == 1:
            # If there is one artist selected, show their releases
            # (optionally filtered by raag or taal)
            aid = qartist[0]
            art = models.Artist.objects.get(pk=aid)
            displayres.append(("artist", art))
            if art.main_instrument:
                displayres.append(("instrument", art.main_instrument))
            for ra in rlist:
                displayres.append(("raag", ra))
            for ta in tlist:
                displayres.append(("taal", ta))
            for c in art.releases():
                displayres.append(("release", c))
        else:
            # Otherwise if more than one artist is selected,
            # show only releases that all artists perform in
            allreleases = []
            for aid in qartist:
                art = models.Artist.objects.get(pk=aid)
                displayres.append(("artist", art))
                if art.main_instrument:
                    displayres.append(("instrument", art.main_instrument))
                thisreleases = set(art.releases())
                allreleases.append(thisreleases)
            combinedreleases = reduce(lambda x, y: x & y, allreleases)

            for ra in rlist:
                displayres.append(("raag", ra))
            for ta in tlist:
                displayres.append(("taal", ta))

            for c in list(combinedreleases):
                displayres.append(("release", c))

    elif qinstr: # instrument query, but no artist
        querybrowse = True
        # instrument, people
        for iid in qinstr:
            instr = models.Instrument.objects.get(pk=iid)
            displayres.append(("instrument", instr))
            for p in instr.ordered_performers()[:5]:
                displayres.append(("artist", p.performer))

    elif qraag:
        querybrowse = True
        # raag, people
        for rid in qraag:
            ra = models.Raag.objects.get(pk=rid)
            displayres.append(("raag", ra))
            artists = ra.artists()
            if qinstr:
                # if instrument, only people who play that
                artists = artists.filter(main_instrument__in=qinstr)
            for a in artists[:5]:
                displayres.append(("artist", a))
    elif qtaal:
        querybrowse = True
        # taal, people
        for tid in qtaal[:5]:
            ta = models.Taal.objects.get(pk=tid)
            displayres.append(("taal", ta))
            percussionists = ta.percussion_artists()
            for a in ta.artists():
                if a not in percussionists:
                    percussionists.append(a)
            # TODO: We could order by percussionists, or by number of times they've
            # performed this taal, or by people with images
            artists = percussionists[:5]
            if qinstr:
                # if instrument, only people who play that
                artists = artists.filter(main_instrument__in=qinstr)
            for a in artists:
                displayres.append(("artist", a))
    elif qrelease:
        querybrowse = True
        # release, people
        for cid in qrelease:
            con = models.Release.objects.get(pk=cid)
            displayres.append(("release", con))
            artists = con.performers()
            for a in artists:
                displayres.append(("artist", a.performer))
                # if instrument, only people who play that?
    elif query:
        try:
            results = search.search(query)
        except pysolr.SolrError:
            searcherror = True
            results = {}
        artists = results.get("artist", [])
        instruments = results.get("instrument", [])
        releases = results.get("release", [])
        raags = results.get("raag", [])
        taals = results.get("taal", [])

        displayres = []
        for a in artists:
            displayres.append(("artist", a))
        for i in instruments:
            displayres.append(("instrument", i))
        for c in releases:
            displayres.append(("release", c))
        for r in raags:
            displayres.append(("raag", r))
        for t in taals:
            displayres.append(("taal", t))

        numartists = len(artists)
        numraags = len(raags)
        numtaals = len(taals)
        numreleases = len(releases)
        numinstruments = len(instruments)
        results = True
    else:
        results = None

        displayres = []

    if displayres:
        numartists = len([i for i in displayres if i[0] == "artist"])
        numraags = len([i for i in displayres if i[0] == "raag"])
        numtaals = len([i for i in displayres if i[0] == "taal"])
        numreleases = len([i for i in displayres if i[0] == "release"])
        numinstruments = len([i for i in displayres if i[0] == "instrument"])
    
    print displayres

    ret = {"numartists": numartists,
           "filter_items": json.dumps(get_filter_items()),
           "numcomposers": numcomposers,
           "numraags": numraags,
           "numtaals": numtaals,
           "numreleases": numreleases,
           "numworks": numworks,
           "numinstruments": numinstruments,

           "results": displayres,

           "querytext": query,
           "querybrowse": querybrowse,
           "qartist": json.dumps(qartist),
           "qinstr": json.dumps(qinstr),
           "qraag": json.dumps(qraag),
           "qtaal": json.dumps(qtaal),
           "qrelease": json.dumps(qrelease),
           "searcherror": searcherror
           }

    return render(request, "hindustani/index.html", ret)

def composer(request, uuid):
    composer = get_object_or_404(models.Composer, mbid=uuid)

    ret = {"composer": composer
          }
    return render(request, "hindustani/composer.html", ret)

def artistsearch(request):
    artists = models.Artist.objects.filter(dummy=False).order_by('name')
    ret = []
    for a in artists:
        ret.append({"id": a.id, "name": a.name})
    return HttpResponse(json.dumps(ret), content_type="application/json")

def artist(request, uuid):
    artist = get_object_or_404(models.Artist, mbid=uuid)

    ret = {"artist": artist
          }
    return render(request, "hindustani/artist.html", ret)

def releasesearch(request):
    releases = models.Release.objects.order_by('title')
    ret = []
    for r in releases:
        ret.append({"id": r.id, "title": r.title})
    return HttpResponse(json.dumps(ret), content_type="application/json")

def release(request, uuid):
    release = get_object_or_404(models.Release, mbid=uuid)

    ret = {"release": release
          }
    return render(request, "hindustani/release.html", ret)

def recording(request, uuid):
    recording = get_object_or_404(models.Recording, mbid=uuid)

    ret = {"recording": recording
          }
    return render(request, "hindustani/recording.html", ret)

def work(request, uuid):
    work = get_object_or_404(models.Work, mbid=uuid)

    ret = {"work": work
          }
    return render(request, "hindustani/work.html", ret)

def layasearch(request):
    layas = models.Laya.objects.all().order_by('name')
    ret = []
    for l in layas:
        ret.append({"id": l.id, "name": str(l)})
    return HttpResponse(json.dumps(ret), content_type="application/json")

def laya(request, layaid):
    laya = get_object_or_404(models.Laya, pk=layaid)

    ret = {"laya": laya
          }
    return render(request, "hindustani/laya.html", ret)

def raagsearch(request):
    raags = models.Raag.objects.all().order_by('name')
    ret = []
    for r in raags:
        ret.append({"id": r.id, "name": str(r)})
    return HttpResponse(json.dumps(ret), content_type="application/json")

def raag(request, raagid):
    raag = get_object_or_404(models.Raag, pk=raagid)

    ret = {"raag": raag
          }
    return render(request, "hindustani/raag.html", ret)

def taalsearch(request):
    taals = models.Taal.objects.all().order_by('name')
    ret = []
    for t in taals:
        ret.append({"id": t.id, "name": str(t)})
    return HttpResponse(json.dumps(ret), content_type="application/json")

def taal(request, taalid):
    taal = get_object_or_404(models.Taal, pk=taalid)

    """
    We display all the recordings of a taal and group them by 
    layas. Currently, the vilambit laya should be the last group
    shown. Recordings that are associated with more than one laya
    are only shown once in their first group
    """
    layas = models.Laya.objects.all().order_by('id') # To make sure the vilambit is the last
    recordings = taal.recording_set.all()
    tracks = []
    for laya in layas:
        tracks.append((laya, recordings.filter(layas=laya)))
        recordings = recordings.exclude(layas=laya)
    ret = { "taal": taal,
            "tracks": tracks,
          }
    return render(request, "hindustani/taal.html", ret)

def formsearch(request):
    forms = models.Form.objects.all().order_by('name')
    ret = []
    for l in forms:
        ret.append({"id": l.id, "name": str(l)})
    return HttpResponse(json.dumps(ret), content_type="application/json")

def form(request, formid):
    form = get_object_or_404(models.Form, pk=formid)

    ret = {"form": form
          }
    return render(request, "hindustani/form.html", ret)

def instrumentsearch(request):
    instruments = models.Instrument.objects.all().order_by('name')
    ret = []
    for l in instruments:
        ret.append({"id": l.id, "name": str(l)})
    return HttpResponse(json.dumps(ret), content_type="application/json")

def instrument(request, instrumentid):
    instrument = get_object_or_404(models.Instrument, pk=instrumentid)

    ret = {"instrument": instrument
          }
    return render(request, "hindustani/instrument.html", ret)

