import textwrap, re, itertools, string, datetime
from src.comms.models import Channel
from . CommAddon.models import ChanCommConf
from django.utils.timezone import utc

STAFFREP = "Staff Reports"

def utcnow():
    return datetime.datetime.utcnow().replace(tzinfo=utc)

def stringsecs(ststring):
    if not ststring:
        return False
    datestring = ststring.split(" ")
    rsecs = 0
    for interval in datestring:
        if re.match('^[\d]+s$', interval.lower()):
            rsecs =+ int(interval.lower().rstrip("s"))
        elif re.match('^[\d]+m$', interval):
            rsecs =+ int(interval.lower().rstrip("m")) * 60
        elif re.match('^[\d]+h$', interval):
            rsecs =+ int(interval.lower().rstrip("h")) * (60 * 60)
        elif re.match('^[\d]+d$', interval):
            rsecs =+ int(interval.lower().rstrip("d")) * (60 * 60 * 24)
        elif re.match('^[\d]+w$', interval):
            rsecs =+ int(interval.lower().rstrip("w")) * (60 * 60 * 24 * 7)
        elif re.match('^[\d]+y$', interval):
            rsecs =+ int(interval.lower().rstrip("y")) * (60 * 60 * 24 * 7 * 365)
    return rsecs

def cemit(target,msg):
    if not target:
        return
    if not msg:
        return
    channel = Channel.objects.get_channel(target)
    if not channel:
        return
    chanconf,created = ChanCommConf.objects.get_or_create(chankey=channel)
    header = "<{%s%s{n>" % (chanconf.color,channel.key)
    channel.msg("%s %s" % (header,msg))

def msghead(ststring,error=False):
    if not ststring:
        ststring = "SYSTEM"
    if error:
        return "{m-=<{w%s{m>=- {rERROR:{n " % ststring.upper()
    else:
        return "{m-=<{w%s{m>=-{n " % ststring.upper()
        

def table(ststring, fwidth, llength):
    """
    This function returns a tabulated string composed of a basic list of words.
    """
    rstring = ""
    newlineat = llength / fwidth
    curfield = 0
    for element in ststring:
        if curfield < newlineat:
            rstring = rstring + string.ljust(element[:fwidth],fwidth)
            curfield = curfield + 1
        else:
            rstring = rstring + "\n" + string.ljust(element[:fwidth],fwidth)
            curfield = 0
    return rstring

def center(ststring,width=None,fill=None,rfill=None,color=None,markup=None):
    """
    This centers a string within another string composed of given fill.
    """
    rstring = ""
    if fill == None:
        fill = " "
    if rfill == None:
        rfill = fill
    if width == None:
        width = 78
    if color == None:
        color = "{n"
    if markup == None:
        markup = 0
    if ststring == None:
        ststring = ""
    strlen = len(ststring) - markup
    sidelen = (width - strlen) / 2
    siderem = (width - strlen) % 2
    prelstring = fill * 999
    prelstring = color + prelstring[0:sidelen]
    prerstring = rfill * 999
    prerstring = color + prerstring[0:(sidelen + siderem)] + "{n"
    rstring = prelstring + ststring + prerstring
    return rstring

def header(ststring=None,hmarkup=None):
    """
    This is a default setup for center() that prints nice headers.
    """
    hfill = "-=-"
    hcolor = "{M"
    if hmarkup == None:
        hmarkup = 0
    if ststring:
        hstring = "{n{M<{m* {n{w" + ststring + "{n {m*{M>{n"
        return center(ststring=hstring,width=78,fill=hfill,rfill=hfill,color=hcolor,markup=hmarkup + 18)
    else:
        return center(ststring=None,width=78,fill=hfill,rfill=hfill,color=hcolor,markup=hmarkup)

def align(cols,widths=None,strings=None):
    """
    I don't know HOW to explain this one...
    """
    if cols is None:
        cols = 1
    if widths is None:
        widths = [78]

def speak(speaker,input,fancy=False):
    """
    This formats strings based on input to resemble say, pose, etc, style messages in all kinds of odd places.
    """
    
    if input[:1] == ":":
        rstring= " ".join([speaker,input[1:]])
    elif input[:1] == ";":
        rstring = speaker + input[1:]
    elif fancy and input[-1] == "?":
        rstring = '%s asks, "%s"' % (speaker,input)
    elif fancy and input[-1] == "!":
        rstring = '%s exclaims, "%s"' % (speaker,input)
    else:
        rstring = '%s says, "%s"' % (speaker,input)
    return rstring