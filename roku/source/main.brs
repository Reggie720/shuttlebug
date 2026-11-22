Library "Roku_Ads.brs"

sub Main(args as dynamic)
    screen = CreateObject("roSGScreen")
    port = CreateObject("roMessagePort")
    screen.SetMessagePort(port)
    input = CreateObject("roInput")
    input.SetMessagePort(port)
    memory = CreateObject("roAppMemoryMonitor")
    device = CreateObject("roDeviceInfo")
    device.SetMessagePort(port)
    if memory <> invalid
        memory.SetMessagePort(port)
        if not memory.EnableMemoryWarningEvent(true) then device.EnableLowGeneralMemoryEvent(true)
        print "Memory usage percent: "; memory.GetMemoryLimitPercent()
        print "Memory available KB: "; memory.GetChannelAvailableMemory()
        print "Memory limits: "; FormatJson(memory.GetChannelMemoryLimit())
    else
        device.EnableLowGeneralMemoryEvent(true)
    end if
    ' Enable required measurement metadata. No ad requests or paid demand.
    raf = Roku_Ads()
    raf.SetLimitAdTracking(true)
    raf.enableAdMeasurements(true)
    scene = screen.CreateScene("ShuttlebugScene")
    scene.ObserveField("exitRequested", port)
    scene.ObserveField("playbackMetadata", port)
    if Type(args) = "roAssociativeArray"
        if args.contentId <> invalid then scene.launchId = args.contentId
    end if
    screen.Show()
    while true
        msg = wait(0, port)
        ' Keep the roInput branch explicit for certification analysis.
        if type(msg) = "roInputEvent"
            if msg.IsInput()
                info = msg.GetInfo()
                if Type(info) = "roAssociativeArray"
                    if info.contentId <> invalid then scene.launchId = info.contentId
                end if
            end if
        else if type(msg) = "roSGScreenEvent"
            if msg.IsScreenClosed() then exit while
        else if type(msg) = "roSGNodeEvent"
            if msg.GetField() = "exitRequested"
                if msg.GetData()
                    screen.Close()
                    exit while
                end if
            else if msg.GetField() = "playbackMetadata"
                metadata = msg.GetData()
                raf.setContentGenre(metadata.genre, false)
                raf.setContentId(metadata.id)
                raf.setContentLength(metadata.duration)
            end if
        else if type(msg) = "roAppMemoryNotificationEvent"
            info = msg.GetInfo()
            if info.memoryUsagePercent >= 80 then scene.memoryPressure = true
        else if type(msg) = "roDeviceInfoEvent"
            info = msg.GetInfo()
            if info.generalMemoryLevel <> invalid then scene.memoryPressure = true
        end if
    end while
end sub
