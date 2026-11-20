sub init()
    m.top.backgroundColor = "0x101010FF"
    for each id in ["navigation", "movies", "preview", "poster", "movieTitle", "description", "status", "details", "detailTitle", "detailDescription", "detailButtons", "detailCredit", "searchPanel", "keyboard", "searchButtons", "video", "adView", "adLabel", "adWatchdog", "metadata", "detailPoster", "detailMetadata", "breadcrumb"]
        m[id] = m.top.FindNode(id)
    end for
    m.items = []
    m.filtered = []
    m.favorites = {}
    m.progress = {}
    m.history = []
    m.rows = []
    m.query = ""
    m.category = ""
    m.series = ""
    m.season = ""
    m.section = "Browse"
    m.mode = "browse"
    m.testAds = false
    m.current = invalid
    m.pendingPlay = ""
    m.checking = false
    m.sourceIndex = 0
    m.resumeAt = 0
    m.midDone = false
    m.adPending = ""
    m.lastSaved = 0
    m.lastPosition = 0
    m.queuedLaunch = ""
    m.registry = CreateObject("roRegistrySection", "Shuttlebug")
    stored = ParseJson(m.registry.Read("favorites"))
    if Type(stored) = "roAssociativeArray" then m.favorites = stored
    stored = ParseJson(m.registry.Read("progress"))
    if Type(stored) = "roAssociativeArray" then m.progress = CleanPositions(stored, ParseJson(ReadAsciiFile("pkg:/data/catalog.json")))
    stored = ParseJson(m.registry.Read("history"))
    m.history = CleanHistory(stored)
    m.top.ObserveField("launchId", "onLaunchId")
    updateNavigation()
    m.navigation.ObserveField("itemSelected", "onNavigation")
    m.movies.ObserveField("rowItemFocused", "onMovieFocus")
    m.movies.ObserveField("rowItemSelected", "onMovieSelected")
    m.detailButtons.ObserveField("buttonSelected", "onDetailButton")
    m.searchButtons.ObserveField("buttonSelected", "onSearchButton")
    m.video.ObserveField("state", "onVideoState")
    m.video.ObserveField("position", "onPosition")
    m.adWatchdog.ObserveField("fire", "onAdTimeout")
    m.adVideo = m.top.FindNode("adVideo")
    m.adVideo.ObserveField("state", "onLocalAdState")
    m.catalogTask = CreateObject("roSGNode", "CatalogTask")
    m.catalogTask.ObserveField("result", "onCatalog")
    m.adTask = CreateObject("roSGNode", "AdTask")
    m.adTask.ObserveField("outcome", "onAdOutcome")
    m.navigation.SetFocus(true)
    checkRights()
end sub

sub updateNavigation()
    root = CreateObject("roSGNode", "ContentNode")
    label = "Test ads: OFF"
    if m.testAds then label = "Test ads: ON (unpaid)"
    for each title in ["Home", "Search", "Favorites", label, "About & privacy"]
        node = root.CreateChild("ContentNode")
        node.title = title
    end for
    m.navigation.content = root
end sub

sub checkRights()
    if m.checking then return
    m.checking = true
    m.status.text = "Checking live content permissions..."
    m.catalogTask.control = "RUN"
end sub

sub onCatalog()
    result = m.catalogTask.result
    m.checking = false
    m.items = result.items
    m.status.text = result.message
    renderMovies()
    if m.pendingPlay <> ""
        id = m.pendingPlay
        m.pendingPlay = ""
        found = invalid
        for each item in m.items
            if item.id = id then found = item
        end for
        if found = invalid
            showMessage("Unavailable", "This title is no longer cleared, or the rights check could not finish. Playback has not started.")
        else
            m.current = found
            beginSession()
        end if
    end if
end sub

sub renderMovies()
    m.filtered = []
    if m.section = "Browse" and m.category = ""
        m.rows = HomeShelves(m.items, m.favorites, m.progress, m.history)
        m.breadcrumb.text = "HOME  /  Discover something worth watching"
    else
        entries = FilterTitles(m.items, m.query, m.favorites, m.section = "Favorites")
        label = m.section
        if m.section = "Browse"
            entries = BrowseEntries(m.items, m.category, m.series, m.season)
            label = m.category
            if m.series <> "" then label = m.series
            if m.season <> "" then label = label + " / " + m.season
        end if
        m.rows = []
        AddShelf(m.rows,label,entries)
        m.breadcrumb.text = "HOME  /  " + label
    end if
    content = CreateObject("roSGNode", "ContentNode")
    for each row in m.rows
        rowNode = content.CreateChild("ContentNode")
        rowNode.title = row.title
        for each item in row.items
            m.filtered.Push(item)
            child = rowNode.CreateChild("ContentNode")
            child.title = item.title
            child.description = TitleMetadata(item)
            child.hdPosterUrl = "pkg:/images/splash.jpg"
            if item.image <> invalid and item.image <> "" then child.hdPosterUrl = item.image
            if item.folder = true
                for each episode in m.items
                    if episode.kind = "TV" and episode.series = item.series
                        item.image = episode.image
                        child.hdPosterUrl = episode.image
                        exit for
                    end if
                end for
            end if
            if item.episode <> invalid then child.title = "E" + item.episode.ToStr() + " - " + item.title
        end for
    end for
    m.movies.content = content
    if m.filtered.Count() = 0
        m.movieTitle.text = "Your next discovery is coming"
        m.metadata.text = ""
        m.description.text = "No cleared titles in this section. Choose Home, search again or check your connection."
        m.poster.uri = "pkg:/images/splash.jpg"
    else
        m.movies.jumpToRowItem = [0,0]
        showPreview(0)
    end if
end sub

function focusedIndex(selected as boolean) as integer
    pair = m.movies.rowItemFocused
    if selected then pair = m.movies.rowItemSelected
    if pair = invalid or pair.Count() <> 2 then return -1
    if pair[0] < 0 or pair[0] >= m.rows.Count() then return -1
    if pair[1] < 0 or pair[1] >= m.rows[pair[0]].items.Count() then return -1
    index = pair[1]
    for i = 0 to pair[0] - 1
        index = index + m.rows[i].items.Count()
    end for
    return index
end function

sub onNavigation()
    selected = m.navigation.itemSelected
    if selected = 0
        m.category = ""
        m.series = ""
        m.season = ""
        m.section = "Browse"
        m.query = ""
        renderMovies()
        checkRights()
    else if selected = 1
        openSearch()
        return
    else if selected = 2
        m.section = "Favorites"
        m.query = ""
        renderMovies()
    else if selected = 3
        m.testAds = not m.testAds
        updateNavigation()
        m.navigation.jumpToItem = 3
        m.status.text = "Test commercials are unpaid. No ad-server or paid-demand requests are made."
        m.navigation.SetFocus(true)
        return
    else
        showMessage("Shuttlebug - A Hog Entertainment", "Developer preview. Not published or monetized. Favorites and progress stay in this Roku device's registry. Rights verification contacts Shuttlebug; video hosts receive normal connection information. Test ads are optional unpaid house commercials. No account or payment required. Privacy: https://shuttlebug.onrender.com/privacy.html  Support: ahogentertainment@gmail.com")
        return
    end if
    if m.filtered.Count() > 0 then m.movies.SetFocus(true)
end sub

sub onMovieFocus()
    showPreview(focusedIndex(false))
end sub

sub showPreview(index as integer)
    if index < 0 or index >= m.filtered.Count() then return
    item = m.filtered[index]
    m.movieTitle.text = item.title
    m.metadata.text = TitleMetadata(item)
    if item.folder = true
        m.description.text = "Press OK to open. Back returns to the previous section. Only available, rights-cleared episodes appear."
        m.poster.uri = "pkg:/images/splash.jpg"
        return
    end if
    m.description.text = item.description
    m.poster.uri = item.image
end sub

sub onMovieSelected()
    index = focusedIndex(true)
    if index < 0 or index >= m.filtered.Count() then return
    item = m.filtered[index]
    if item.folder = true
        m.category = item.category
        m.series = item.series
        m.season = item.season
        renderMovies()
        m.movies.SetFocus(true)
        return
    end if
    m.current = item
    showDetails()
end sub

sub showDetails()
    if m.current = invalid then return
    m.mode = "details"
    m.details.visible = true
    m.detailTitle.text = m.current.title
    m.detailMetadata.text = TitleMetadata(m.current)
    m.detailPoster.uri = m.current.image
    m.detailDescription.text = m.current.description
    saved = 0
    if m.progress.DoesExist(m.current.id) then saved = m.progress[m.current.id]
    label = "Play"
    if saved > 0 then label = "Resume at " + Int(saved).ToStr() + " seconds"
    favoriteLabel = "Add to Favorites"
    if m.favorites.DoesExist(m.current.id) then favoriteLabel = "Remove from Favorites"
    m.detailButtons.buttons = [label, "Play from beginning", favoriteLabel, "Credits & license"]
    m.detailCredit.text = m.current.credit + Chr(10) + m.current.license + " | Full original credits retained."
    m.detailButtons.SetFocus(true)
end sub

sub onDetailButton()
    choice = m.detailButtons.buttonSelected
    if choice = 0 or choice = 1
        if m.checking
            m.status.text = "Wait for the rights check, then try Play again."
            return
        end if
        m.resumeAt = 0
        if choice = 0 and m.progress.DoesExist(m.current.id) then m.resumeAt = m.progress[m.current.id]
        m.pendingPlay = m.current.id
        m.detailDescription.text = "Checking current permissions before playback..."
        checkRights()
    else if choice = 2
        m.favorites = ToggleFavorite(m.favorites, m.current.id)
        savePreferences()
        renderMovies()
        showDetails()
    else
        item = m.current
        attribution = item.credit
        if item.captionCredit <> "" then attribution = attribution + Chr(10) + item.captionCredit
        showMessage("Credits - " + item.title, attribution + Chr(10) + item.license + Chr(10) + item.licenseUrl + Chr(10) + "Permission: " + item.rights + Chr(10) + "Source: " + item.source + Chr(10) + item.changes + Chr(10) + "Creators do not endorse Shuttlebug.")
    end if
end sub

sub savePreferences()
    m.registry.Write("favorites", FormatJson(m.favorites))
    m.registry.Write("progress", FormatJson(m.progress))
    m.registry.Write("history", FormatJson(m.history))
    m.registry.Flush()
end sub

sub openSearch()
    m.mode = "search"
    m.searchPanel.visible = true
    m.keyboard.text = m.query
    m.keyboard.SetFocus(true)
end sub

sub onSearchButton()
    if m.searchButtons.buttonSelected = 0
        m.query = m.keyboard.text.Trim()
        m.section = "Search"
        renderMovies()
    end if
    closeSearch()
end sub

sub closeSearch()
    m.mode = "browse"
    m.searchPanel.visible = false
    if m.filtered.Count() > 0
        m.movies.SetFocus(true)
    else
        m.navigation.SetFocus(true)
    end if
end sub

sub showMessage(title as string, message as string)
    dialog = CreateObject("roSGNode", "Dialog")
    dialog.title = title
    dialog.message = message
    dialog.buttons = ["OK"]
    dialog.ObserveField("buttonSelected", "closeMessage")
    m.top.dialog = dialog
end sub

sub closeMessage()
    m.top.dialog.close = true
    if m.mode = "details"
        m.detailButtons.SetFocus(true)
    else
        m.navigation.SetFocus(true)
    end if
end sub

sub beginSession()
    m.details.visible = false
    m.mode = "video"
    m.sourceIndex = 0
    m.midDone = false
    m.lastPosition = m.resumeAt
    m.lastSaved = m.resumeAt
    if m.testAds
        requestTestAd("preroll")
    else
        startFilm()
    end if
end sub

sub startFilm()
    if m.current = invalid then return
    m.mode = "video"
    content = CreateObject("roSGNode", "ContentNode")
    stream = m.current.sources[m.sourceIndex]
    content.title = m.current.title
    content.url = stream.url
    content.streamFormat = stream.format
    content.length = m.current.duration
    content.playStart = m.resumeAt
    content.subtitleTracks = m.current.subtitleTracks
    m.video.content = content
    m.video.visible = true
    m.video.SetFocus(true)
    m.video.control = "play"
end sub

sub onPosition()
    if m.mode <> "video" or m.current = invalid then return
    if m.video.state <> "playing" and m.video.state <> "paused" then return
    m.lastPosition = m.video.position
    if Abs(m.lastPosition - m.lastSaved) >= 15
        m.progress[m.current.id] = m.lastPosition
        m.lastSaved = m.lastPosition
        savePreferences()
    end if
    ' Accelerated developer-only test; never use this schedule for paid ads.
    if m.testAds and not m.midDone and m.lastPosition >= 30
        m.midDone = true
        m.resumeAt = m.lastPosition
        requestTestAd("midroll")
    end if
end sub

sub requestTestAd(sequence as string)
    m.adPending = sequence
    m.adWatchdog.control = "start"
    if m.video.state = "playing" or m.video.state = "paused" or m.video.state = "buffering"
        m.mode = "stoppingForAd"
        m.video.control = "stop"
    else
        showTestAd()
    end if
end sub

sub showTestAd()
    ' Local developer preview: use the native Video node rather than RAF.
    ' Unpaid preview only. Production RAF integration is not invoked here.
    m.mode = "ad"
    m.localAdStarted = false
    m.video.visible = false
    m.adView.visible = true
    m.adLabel.visible = true
    m.adVideo.visible = true
    clip = CreateObject("roSGNode", "ContentNode")
    clip.url = "pkg:/media/test-commercial.mp4"
    clip.streamFormat = "mp4"
    m.adVideo.content = clip
    m.top.SetFocus(true)
    m.adWatchdog.control = "start"
    m.adVideo.control = "play"
end sub

sub finishLocalAd()
    if m.mode <> "ad" then return
    m.mode = "resumingAfterAd"
    m.adWatchdog.control = "stop"
    m.adVideo.control = "stop"
    m.adVideo.visible = false
    m.adView.visible = false
    m.adLabel.visible = false
    m.mode = "video"
    if m.queuedLaunch <> ""
        id = m.queuedLaunch
        m.queuedLaunch = ""
        m.mode = "browse"
        m.pendingPlay = id
        m.resumeAt = 0
        checkRights()
    else
        startFilm()
    end if
end sub

sub onLocalAdState()
    if m.mode <> "ad" then return
    state = m.adVideo.state
    if state = "playing"
        m.localAdStarted = true
    else if state = "finished" or state = "error"
        finishLocalAd()
    else if state = "stopped" and m.localAdStarted
        finishLocalAd()
    end if
end sub

sub onAdOutcome()
    ' Legacy task callback; native local ad playback is used instead.
end sub

sub onAdTimeout()
    if m.mode = "ad"
        ' Never leave the viewer trapped behind an unavailable test ad.
        finishLocalAd()
    else if m.mode = "stoppingForAd"
        m.queuedLaunch = ""
        endPlayback(false)
        m.detailDescription.text = "Test commercial skipped because the film player did not stop in time. Your position is saved. Turn test ads OFF and try Play again."
    end if
end sub

sub onVideoState()
    state = m.video.state
    if m.mode = "stoppingForAd" and state = "stopped"
        showTestAd()
        return
    end if
    if m.mode <> "video" then return
    if state = "playing"
        recordViewing()
    else if state = "paused"
        m.lastPosition = m.video.position
        m.progress[m.current.id] = m.lastPosition
        m.lastSaved = m.lastPosition
        savePreferences()
    else if state = "stopped"
        endPlayback(false)
    else if state = "finished"
        endPlayback(true)
    else if state = "error"
        m.sourceIndex++
        if m.sourceIndex < m.current.sources.Count()
            m.resumeAt = m.lastPosition
            startFilm()
        else
            endPlayback(false)
            showMessage("Playback unavailable", "This provider stream could not play. Check your connection or try another cleared title. Device codec compatibility still requires hardware testing.")
        end if
    end if
end sub

sub endPlayback(completed as boolean)
    m.mode = "details"
    m.adWatchdog.control = "stop"
    m.adVideo.control = "stop"
    m.adVideo.visible = false
    m.adView.visible = false
    m.adLabel.visible = false
    m.queuedLaunch = ""
    m.adPending = ""
    m.video.control = "stop"
    m.video.visible = false
    if m.current <> invalid
        position = m.lastPosition
        if completed then position = 0
        m.progress[m.current.id] = position
        savePreferences()
        showDetails()
    end if
end sub

function onKeyEvent(key as string, press as boolean) as boolean
    if not press then return false
    if m.mode = "ad"
        if key = "back"
            finishLocalAd()
            return true
        end if
        return true
    end if
    if m.mode = "video"
        if key = "back"
            endPlayback(false)
            return true
        else if key = "play" or key = "OK"
            if m.video.state = "paused"
                m.video.control = "resume"
            else
                m.video.control = "pause"
            end if
            return true
        end if
        return false
    else if m.mode = "stoppingForAd"
        if key = "back"
            m.adPending = ""
            endPlayback(false)
            return true
        end if
        return true
    else if m.mode = "search"
        if key = "back"
            closeSearch()
            return true
        else if key = "down" and m.keyboard.IsInFocusChain()
            m.searchButtons.SetFocus(true)
            return true
        else if key = "up" and m.searchButtons.IsInFocusChain()
            m.keyboard.SetFocus(true)
            return true
        end if
    else if m.mode = "details"
        if key = "back"
            m.pendingPlay = ""
            m.details.visible = false
            m.mode = "browse"
            if m.items <> invalid then renderMovies()
            if m.filtered.Count() > 0
                m.movies.SetFocus(true)
            else
                m.navigation.SetFocus(true)
            end if
            return true
        end if
    else
        if key = "right" and m.navigation.IsInFocusChain() and m.filtered.Count() > 0
            m.movies.SetFocus(true)
            return true
        else if key = "left" and m.movies.IsInFocusChain()
            m.navigation.SetFocus(true)
            return true
        else if key = "options" and m.movies.IsInFocusChain() and m.filtered.Count() > 0
            index = focusedIndex(false)
            if index >= 0 and index < m.filtered.Count()
                if m.filtered[index].folder = true then return true
                m.favorites = ToggleFavorite(m.favorites, m.filtered[index].id)
                savePreferences()
                renderMovies()
            end if
            return true
        else if key = "back"
            if m.section = "Browse" and m.category <> "" and m.category <> invalid
                if m.season <> ""
                    m.season = ""
                else if m.series <> ""
                    m.series = ""
                else
                    m.category = ""
                end if
                renderMovies()
                m.movies.SetFocus(true)
                return true
            end if
            if not m.navigation.IsInFocusChain()
                m.navigation.SetFocus(true)
                return true
            end if
            m.top.exitRequested = true
            return true
        end if
    end if
    return false
end function

sub onLaunchId()
    id = m.top.launchId
    if id = "" then return
    if m.mode = "ad" or m.mode = "stoppingForAd"
        m.queuedLaunch = id
        return
    end if
    if m.mode = "video" then endPlayback(false)
    m.searchPanel.visible = false
    m.pendingPlay = id
    m.resumeAt = 0
    if not m.checking then checkRights()
end sub

sub recordViewing()
    if m.current = invalid then return
    if m.history = invalid then m.history = []
    if m.history.Count() > 0
        if m.history[0] = m.current.id then return
    end if
    nextHistory = [m.current.id]
    for each id in m.history
        if id <> m.current.id and nextHistory.Count() < 50 then nextHistory.Push(id)
    end for
    m.history = nextHistory
    savePreferences()
end sub
