Library "Roku_Ads.brs"

sub Main(args = invalid as dynamic)
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
    scene.launch_args = args
    screen.Show()
    while true
        msg = wait(0, port)
        msgType = Type(msg)
        ' Direct event forwarding follows Roku's SGDEX deep-link reference sample.
        if msgType = "roInputEvent"
            scene.input_args = msg.GetInfo()
        else if msgType = "roSGScreenEvent"
            if msg.IsScreenClosed() then exit while
        else if msgType = "roSGNodeEvent"
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
        else if msgType = "roAppMemoryNotificationEvent"
            info = msg.GetInfo()
            if info.memoryUsagePercent >= 80 then scene.memoryPressure = true
        else if msgType = "roDeviceInfoEvent"
            info = msg.GetInfo()
            if info.generalMemoryLevel <> invalid then scene.memoryPressure = true
        end if
    end while
end sub
