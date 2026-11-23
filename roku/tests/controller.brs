sub Main()
    m.launchComplete = true
    m.startupDialog = false
    m.history = []
    m.adVideo = {visible:false,control:"",state:"none"}
    m.adView = {visible:false}
    m.adLabel = {visible:false}
    m.queuedLaunch = ""
    m.top = {exitRequested:false,SetFocus:sub(value):end sub}
    m.video = {state:"playing",control:"",visible:true,position:30}
    m.adWatchdog = {control:""}
    m.mode = "video"
    require(onKeyEvent("play",true),"media key handled")
    require(m.video.control = "pause","pause command")
    m.video.state = "paused"
    require(onKeyEvent("play",true),"resume handled")
    require(m.video.control = "resume","resume command")
    require(not onKeyEvent("back",false),"key-up ignored")
    m.current = invalid
    require(onKeyEvent("back",true),"video Back")
    require(m.video.control = "stop" and not m.video.visible,"Back stops and hides video")
    m.mode = "browse"
    m.navigation = {SetFocus:sub(value):end sub,active:true,IsInFocusChain:function():return m.active:end function}
    m.movies = {focused:false,SetFocus:sub(value):m.focused=value:end sub}
    m.filtered = [{id:"one"}]
    require(onKeyEvent("right",true),"nav to movies")
    require(m.movies.focused,"movie list focus")
    m.top = {exitRequested:false,SetFocus:sub(value):end sub}
    require(onKeyEvent("back",true),"root Back handled")
    require(m.top.exitRequested,"root exit signal")
    m.mode = "video"
    m.current = {id:"one"}
    m.progress = {}
    m.favorites = {}
    m.registry = {Write:sub(k,v):end sub,Flush:sub():end sub}
    m.lastSaved = 30
    m.testAds = true
    m.midDone = false
    m.video.state = "playing"
    onPosition()
    require(m.mode = "stoppingForAd","midroll waits for decoder release")
    require(m.resumeAt = 30 and m.midDone,"midroll bookmark and one-shot latch")
    m.adView = {visible:false}
    m.adLabel = {visible:false}
    m.adTask = {view:invalid,sequence:"",control:""}
    m.adWatchdog = {control:""}
    m.video.state = "stopped"
    onVideoState()
    require(m.mode = "ad" and m.adVideo.control = "play","native test ad launched after stop")
    require(m.adPending = "midroll" and m.adLabel.visible,"test midroll label")
    m.current = invalid
    require(onKeyEvent("back",true),"scene handles ad Back")
    require(m.mode = "video" and not m.adVideo.visible and not m.adLabel.visible,"Back clears ad overlay")
    for outcome = 0 to 2
        m.mode = "ad"
        m.adVideo.visible = true
        m.adLabel.visible = true
        m.localAdStarted = false
        m.adVideo.state = "stopped"
        onLocalAdState()
        require(m.mode = "ad","initial stopped event ignored")
        if outcome = 0
            m.adVideo.state = "error"
            onLocalAdState()
        else if outcome = 1
            m.adVideo.state = "finished"
            onLocalAdState()
        else
            onAdTimeout()
        end if
        require(m.mode = "video" and not m.adVideo.visible and not m.adLabel.visible,"ad failure/completion/timeout clears player")
        onLocalAdState()
        require(m.mode = "video","late ad event cannot restart recovery")
    end for
    m.current = {id:"one",title:"Cleared test",sources:[{url:"https://example.com/movie.mp4",format:"mp4"}],duration:120,subtitleTracks:[]}
    m.sourceIndex = 0
    m.resumeAt = 43
    m.video.SetFocus = sub(value):end sub
    m.mode = "ad"
    finishLocalAd()
    require(m.video.control = "play" and m.video.visible,"film restarts after ad")
    require(m.video.content.playStart = 43,"film resumes at saved bookmark")
    m.rows = [{items:[{id:"a"},{id:"b"}]},{items:[{id:"c"}]}]
    m.movies.rowItemFocused = [1,0]
    m.movies.rowItemSelected = [0,1]
    require(focusedIndex(false) = 2,"row focus maps to correct title")
    require(focusedIndex(true) = 1,"row selection maps to correct title")
    m.movies.rowItemSelected = [4,0]
    require(focusedIndex(true) = -1,"stale row selection rejected")
    m.items = []
    m.query = ""
    m.section = "Browse"
    m.category = ""
    m.series = ""
    m.season = ""
    m.metadata = {text:""}
    m.breadcrumb = {text:""}
    m.movieTitle = {text:""}
    m.description = {text:""}
    m.poster = {uri:""}
    m.pendingPlay = "one"
    m.mode = "details"
    m.details = {visible:true}
    require(onKeyEvent("back",true),"Back cancels pending play")
    require(m.pendingPlay = "" and m.mode = "browse","no delayed autoplay after Back")
    m.mode = "stoppingForAd"
    m.current = invalid
    m.adView = {visible:true,GetChildCount:function():return 0:end function,RemoveChildrenIndex:sub(n,i):end sub}
    m.detailDescription = {text:""}
    m.queuedLaunch = "one"
    onAdTimeout()
    require(m.mode = "details" and m.video.control = "stop","ad handoff timeout returns safely")
    require(m.queuedLaunch = "" and m.adVideo.control = "stop","timeout cancels pending ad and queued launch")
    m.mode = "video"
    m.current = {id:"one"}
    m.video.state = "paused"
    m.video.position = 43
    onVideoState()
    require(m.progress.one = 43,"pause saves latest position")
    m.video.state = "buffering"
    m.video.position = 0
    onPosition()
    require(m.progress.one = 43,"buffering does not reset resume bookmark")
    m.video.state = "stopped"
    m.current = invalid
    onVideoState()
    require(m.mode = "details" and not m.video.visible,"native stop returns from player")
    m.launchComplete = false
    m.top = {beacons:[], signalBeacon:sub(name):m.beacons.Push(name):end sub}
    markLaunchComplete()
    markLaunchComplete()
    require(m.top.beacons.Count() = 1 and m.top.beacons[0] = "AppLaunchComplete", "launch beacon fires once")
    m.top.launchId = "new-title"
    m.mode = "ad"
    onLaunchId()
    require(m.queuedLaunch = "new-title", "warm deep link queues safely during ad")
    m.mode = "browse"
    m.checking = true
    m.searchPanel = {visible:true}
    onLaunchId()
    require(m.pendingPlay = "new-title" and m.resumeAt = 0, "warm deep link reaches rights-gated playback")
    require(not m.searchPanel.visible, "deep link closes search overlay")
    m.video = {visible:false,content:{title:"old"}}
    m.adVideo = {visible:false,content:{title:"test"}}
    m.details = {visible:false}
    m.preview = {visible:false}
    m.detailPoster = {uri:"old"}
    m.poster = {uri:"old"}
    onMemoryPressure()
    require(m.video.content = invalid and m.adVideo.content = invalid, "low memory releases inactive players")
    require(m.poster.uri = "" and m.detailPoster.uri = "", "low memory releases hidden artwork")
    require(DeepLinkContentId(invalid) = "", "absent launch arguments ignored")
    require(DeepLinkContentId({contentId:42}) = "", "non-string content ID ignored")
    require(DeepLinkContentId({contentId:"   "}) = "", "blank content ID ignored")
    require(DeepLinkContentId({command:"pause"}) = "", "unrelated input does not select a film")
    m.top = {launch_args:{contentId:" bbb ",mediaType:"movie"},input_args:{contentId:"bbs1",mediaType:"episode"},launchId:""}
    onLaunchArguments()
    require(m.top.launchId = "bbb", "cold movie launch enters common playback path")
    onInputArguments()
    require(m.top.launchId = "bbs1", "warm episode input enters common playback path")
    m.top.input_args = {contentId:123}
    onInputArguments()
    require(m.top.launchId = "bbs1", "malformed input preserves current selection")
    print "PASS controller media keys, Back, focus, resume, ad recovery, launch beacon, memory cleanup and cold/warm deep-link argument validation"
end sub

sub require(condition as boolean, label as string)
    if not condition
        print "FAIL " + label
        stop
    end if
end sub
