sub Main()
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
    m.navigation = {active:true,IsInFocusChain:function():return m.active:end function}
    m.movies = {focused:false,SetFocus:sub(value):m.focused=value:end sub}
    m.filtered = [{id:"one"}]
    require(onKeyEvent("right",true),"nav to movies")
    require(m.movies.focused,"movie list focus")
    m.top = {exitRequested:false}
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
    require(m.mode = "ad" and m.adTask.control = "RUN","RAF task launched after stop")
    require(m.adTask.sequence = "midroll" and m.adLabel.visible,"test midroll label")
    require(not onKeyEvent("back",true),"RAF receives Back")
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
    require(m.queuedLaunch = "" and m.adTask.control = "STOP","timeout cancels pending ad and queued launch")
    m.mode = "ad"
    m.adTask.outcome = "back"
    m.queuedLaunch = "one"
    onAdOutcome()
    require(m.mode = "details" and m.queuedLaunch = "","Back during ad wins over queued deep link")
    m.mode = "video"
    m.current = {id:"one"}
    m.video.state = "paused"
    m.video.position = 43
    onVideoState()
    require(m.progress.one = 43,"pause saves latest position")
    print "PASS controller media keys, Back, remote focus, midroll latch, resume bookmark and decoder-release sequencing"
end sub

sub require(condition as boolean, label as string)
    if not condition
        print "FAIL " + label
        stop
    end if
end sub
