sub Main(args as dynamic)
    screen = CreateObject("roSGScreen")
    port = CreateObject("roMessagePort")
    screen.SetMessagePort(port)
    input = CreateObject("roInput")
    input.SetMessagePort(port)
    scene = screen.CreateScene("ShuttlebugScene")
    scene.ObserveField("exitRequested", port)
    if Type(args) = "roAssociativeArray"
        if args.contentId <> invalid then scene.launchId = args.contentId
    end if
    screen.Show()
    while true
        event = wait(0, port)
        if Type(event) = "roSGScreenEvent"
            if event.IsScreenClosed() then exit while
        else if Type(event) = "roSGNodeEvent"
            if event.GetField() = "exitRequested" and event.GetData()
                screen.Close()
                exit while
            end if
        else if Type(event) = "roInputEvent"
            if event.IsInput()
                info = event.GetInfo()
                if info.contentId <> invalid then scene.launchId = info.contentId
            end if
        end if
    end while
end sub
