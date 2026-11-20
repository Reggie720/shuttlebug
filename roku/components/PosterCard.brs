sub onContent()
    item = m.top.itemContent
    if item = invalid then return
    m.top.FindNode("art").uri = item.hdPosterUrl
    m.top.FindNode("title").text = item.title
    m.top.FindNode("meta").text = item.description
end sub

sub onFocus()
    m.top.FindNode("border").opacity = m.top.focusPercent
end sub
