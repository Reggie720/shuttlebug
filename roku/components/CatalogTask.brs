sub init()
    m.top.functionName = "loadCatalog"
end sub

sub loadCatalog()
    items = ParseJson(ReadAsciiFile("pkg:/data/catalog.json"))
    if Type(items) <> "roArray"
        m.top.result = {items: [], message: "Packaged catalog is invalid."}
        return
    end if
    request = CreateObject("roUrlTransfer")
    port = CreateObject("roMessagePort")
    request.SetMessagePort(port)
    request.SetCertificatesFile("common:/certs/ca-bundle.crt")
    request.SetUrl("https://shuttlebug.onrender.com/compliance/rights-register.json")
    request.AddHeader("Cache-Control", "no-cache")
    if not request.AsyncGetToString()
        m.top.result = {items: [], message: "Cannot check content rights. Try again with internet access."}
        return
    end if
    event = wait(30000, port)
    if Type(event) = "roUrlEvent"
        if event.GetResponseCode() = 200
            verified = ClearedItems(items, ParseJson(event.GetString()))
            m.top.result = {items: verified, message: verified.Count().ToStr() + " titles cleared for this session."}
            return
        end if
    end if
    request.AsyncCancel()
    m.top.result = {items: [], message: "Rights verification unavailable. Press OK on Browse to retry. Viewing is disabled until verified."}
end sub
