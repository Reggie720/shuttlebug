Library "Roku_Ads.brs"

sub init()
    m.top.functionName = "showTestAd"
end sub

sub showTestAd()
    ' Supply one local, unpaid pod directly. Never request default/paid demand.
    framework = Roku_Ads()
    framework.SetLimitAdTracking(true)
    completed = framework.ShowAds(TestAdPod(m.top.sequence), invalid, m.top.view)
    if completed
        m.top.outcome = "complete"
    else
        m.top.outcome = "back"
    end if
end sub
