function FilterTitles(items as object, query as string, favorites as object, onlyFavorites as boolean) as object
    result = []
    for each item in items
        allowed = true
        if onlyFavorites then allowed = favorites.DoesExist(item.id)
        text = LCase(item.title + " " + item.genre + " " + item.description)
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
