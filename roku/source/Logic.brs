function FilterTitles(items as object, query as string, favorites as object, onlyFavorites as boolean) as object
    result = []
    for each item in items
        allowed = true
        if onlyFavorites then allowed = favorites.DoesExist(item.id)
        text = LCase(item.title + " " + item.genre + " " + item.description)
        if item.series <> invalid then text = text + " " + LCase(item.series)
        if query <> "" and Instr(1, text, LCase(query)) = 0 then allowed = false
        if allowed then result.Push(item)
    end for
    return result
end function

function ClearedItems(items as object, rights as object) as object
    result = []
    if Type(rights) <> "roArray" then return result
    for each item in items
        count = 0
        approved = false
        for each record in rights
            if Type(record) = "roAssociativeArray"
                if record.id = item.id
                    count++
                    matches = record.rightsStatus = "reviewed"
                    for each field in ["license", "licenseUrl", "rights", "source", "credit", "changes"]
                        if record[field] <> item[field] then matches = false
                    end for
                    approved = matches
                end if
            end if
        end for
        if count = 1 and approved then result.Push(item)
    end for
    return result
end function

function ToggleFavorite(favorites as object, id as string) as object
    if favorites.DoesExist(id)
        favorites.Delete(id)
    else
        favorites[id] = true
    end if
    return favorites
end function

function TestAdPod(sequence as string) as object
    return {
        viewed: false
        renderSequence: sequence
        renderTime: 0
        duration: 5.0
        tracking: []
        ads: [{
            duration: 5.0
            streamFormat: "mp4"
            adServer: "Shuttlebug unpaid local test"
            adId: "shuttlebug-house-test"
            adTitle: "TEST ADVERTISEMENT - NO PAID REVENUE"
            advertiser: "A Hog Entertainment (unpaid demonstration)"
            streams: [{url: "pkg:/media/test-commercial.mp4", tracking: []}]
        }]
    }
end function

function CleanPositions(raw as dynamic, items as object) as object
    clean = {}
    if Type(raw) <> "roAssociativeArray" then return clean
    for each item in items
        value = raw[item.id]
        valueType = Type(value)
        if valueType = "Integer" or valueType = "roInt" or valueType = "Float" or valueType = "roFloat" or valueType = "Double" or valueType = "roDouble" or valueType = "LongInteger" or valueType = "roLongInteger"
            if value >= 0 and value < item.duration then clean[item.id] = value
        end if
    end for
    return clean
end function

' Folder records never enter the playback or rights catalog.
function BrowseEntries(items as object, category as string, series as string, season as string) as object
    result = []
    seen = {}
    if category = ""
        return [{folder:true,title:"Movies",category:"Movies",series:"",season:""}, {folder:true,title:"TV Shows",category:"TV",series:"",season:""}]
    end if
    for each item in items
        if item.kind = category
            if category = "Movies"
                result.Push(item)
            else
                show = item.series
                if show = invalid or show = "" then show = item.title
                group = "Episodes (season unspecified)"
                if item.season <> invalid then group = "Season " + item.season.ToStr()
                if series = ""
                    if not seen.DoesExist(show)
                        seen[show] = true
                        result.Push({folder:true,title:show,category:"TV",series:show,season:""})
                    end if
                else if show = series
                    if season = ""
                        if not seen.DoesExist(group)
                            seen[group] = true
                            result.Push({folder:true,title:group,category:"TV",series:show,season:group})
                        end if
                    else if season = group
                        result.Push(item)
                    end if
                end if
            end if
        end if
    end for
    return result
end function

function TitleMetadata(item as object) as string
    result = ""
    if item.year <> invalid then result = item.year.ToStr()
    if item.genre <> invalid and item.genre <> "" then result = result + "  |  " + item.genre
    if item.duration <> invalid then result = result + "  |  " + Int(item.duration / 60).ToStr() + " min"
    if item.contentRating <> invalid and item.contentRating <> "" then result = result + "  |  " + item.contentRating
    if item.episode <> invalid then result = result + "  |  Episode " + item.episode.ToStr()
    return result
end function

sub AddShelf(rows as object, title as string, items as object)
    if items.Count() > 0 then rows.Push({title:title,items:items})
end sub

function HomeShelves(items as object, favorites as object, progress as object, history as object) as object
    rows = []
    continuing = []
    saved = []
    movies = []
    recent = []
    for each item in items
        if progress.DoesExist(item.id)
            if progress[item.id] > 0 and progress[item.id] < item.duration then continuing.Push(item)
        end if
        if favorites.DoesExist(item.id) then saved.Push(item)
        if item.kind = "Movies" then movies.Push(item)
    end for
    for each id in history
        for each item in items
            if item.id = id then recent.Push(item)
        end for
    end for
    AddShelf(rows,"Continue Watching",continuing)
    AddShelf(rows,"Featured Movies",movies)
    newly = []
    ' ISO catalog-added dates sort lexically; unknown dates do not imply newness.
    for each item in movies
        if item.added <> invalid and item.added <> ""
            newly.Push(item)
            position = newly.Count() - 1
            while position > 0
                if newly[position].added <= newly[position-1].added then exit while
                previous = newly[position-1]
                newly[position-1] = newly[position]
                newly[position] = previous
                position--
            end while
        end if
    end for
    AddShelf(rows,"Newly Added Movies",newly)
    for each genre in ["Action","Comedy","Drama","Documentary","Family","Animation","Adventure","Fantasy","Sci-fi"]
        titles = []
        for each item in movies
            if LCase(item.genre) = LCase(genre) then titles.Push(item)
        end for
        label = genre + " Movies"
        if genre = "Documentary" then label = "Documentaries"
        AddShelf(rows,label,titles)
    end for
    shows = BrowseEntries(items,"TV","","")
    for each show in shows
        for each item in items
            if item.kind = "TV" and item.series = show.series
                show.image = item.image
                show.description = item.description
                exit for
            end if
        end for
    end for
    AddShelf(rows,"TV Shows",shows)
    docs = []
    for each item in items
        if item.kind = "TV" and item.genre = "Documentary" then docs.Push(item)
    end for
    AddShelf(rows,"Documentary Episodes",docs)
    AddShelf(rows,"My Favorites",saved)
    AddShelf(rows,"Recently Watched",recent)
    return rows
end function

function CleanHistory(raw as dynamic) as object
    clean = []
    if Type(raw) <> "roArray" then return clean
    seen = {}
    for each id in raw
        if Type(id) = "String" or Type(id) = "roString"
            if not seen.DoesExist(id) and clean.Count() < 50
                clean.Push(id)
                seen[id] = true
            end if
        end if
    end for
    return clean
end function
