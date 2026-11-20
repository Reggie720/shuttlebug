sub Main()
    item = {id:"one", title:"Big Buck Bunny",genre:"Animation",description:"A gentle rabbit",license:"CC BY 3.0",licenseUrl:"https://license",rights:"https://rights",source:"https://source",credit:"Creator",changes:"Unchanged"}
    rights = [{id:"one",rightsStatus:"reviewed",license:item.license,licenseUrl:item.licenseUrl,rights:item.rights,source:item.source,credit:item.credit,changes:item.changes}]
    require(ClearedItems([item],rights).Count() = 1,"cleared title")
    duplicate = [rights[0], rights[0]]
    require(ClearedItems([item],duplicate).Count() = 0,"duplicate rights rejected")
    require(ClearedItems([item],[invalid,"bad",42]).Count() = 0,"malformed records rejected")
    rights[0].rightsStatus = "hold"
    require(ClearedItems([item],rights).Count() = 0,"revoked title")
    rights[0].rightsStatus = "reviewed"
    rights[0].license = "different"
    require(ClearedItems([item],rights).Count() = 0,"changed license")
    require(ClearedItems([item],invalid).Count() = 0,"offline fail closed")
    require(FilterTitles([item],"bUnNy",{},false).Count() = 1,"case insensitive search")
    require(FilterTitles([item],"rabbit",{},false).Count() = 1,"description search")
    require(FilterTitles([item],"missing",{},false).Count() = 0,"empty search result")
    require(FilterTitles([item],"",{},true).Count() = 0,"empty favorites")
    favorites = ToggleFavorite({},"one")
    require(FilterTitles([item],"",favorites,true).Count() = 1,"saved favorite")
    favorites = ToggleFavorite(favorites,"one")
    require(FilterTitles([item],"",favorites,true).Count() = 0,"removed favorite")
    for each sequence in ["preroll","midroll"]
        pod = TestAdPod(sequence)
        require(pod.renderSequence = sequence,"ad sequence")
        require(pod.ads[0].streams[0].url = "pkg:/media/test-commercial.mp4","local creative only")
        require(pod.tracking.Count() = 0,"no pod beacons")
        require(pod.ads[0].streams[0].tracking.Count() = 0,"no impression beacons")
        require(pod.duration = 5,"five second test")
    end for
    item.duration = 600
    require(CleanPositions({one:42},[item]).one = 42,"valid bookmark")
    require(CleanPositions({one:"bad"},[item]).Count() = 0,"corrupt bookmark")
    require(CleanPositions({one:9999},[item]).Count() = 0,"out of range bookmark")
    require(CleanPositions({one:-1},[item]).Count() = 0,"negative bookmark")
    require(CleanPositions({unknown:42},[item]).Count() = 0,"removed title bookmark")
    print "PASS BrightScript rights gate, revocation, search, favorites and unpaid ad pod logic"
end sub

sub require(condition as boolean, label as string)
    if not condition
        print "FAIL " + label
        stop
    end if
end sub
