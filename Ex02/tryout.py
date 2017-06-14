import win32evtlog
import wmi

def try7():
    c = wmi.WMI()
    tmp = c.query(
        "Select SourceName, Message from Win32_NTLogEvent where Logfile = \"Application\"")
    print c

#taking too long
#cant read specific log
def main():
    server = 'localhost'  # name of the target computer to get event logs
    logtype = 'System'
    hand = win32evtlog.OpenEventLog(server, logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)

    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if events:
            for event in events:
                if event.EventID == "92":
                    print 'Event Category:', event.EventCategory
                    print 'Time Generated:', event.TimeGenerated
                    print 'Source Name:', event.SourceName
                    print 'Event ID:', event.EventID
                    print 'Event Type:', event.EventType
                    data = event.StringInserts
                    if data:
                        print 'Event Data:'
                        for msg in data:
                            print msg
                    break

# getting nothing...
def try0():
    server = 'localhost'  # name of the target computer to get event logs
    logtype = 'System'
    hand = win32evtlog.OpenEventLog(server, logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(hand)

    events = win32evtlog.ReadEventLog(hand, flags, 0)
    events_list = [event for event in events if event.EventID == "92"]
    if events_list:
        print 'Event Category:', events_list[0].EventCategory

# not working
def try1():
    c = wmi.WMI(privileges=["Security"])
    watcher = c.Win32_NTLogEvent.watch_for("creation", 2, Type="error")
    while 1:
        error = watcher()
        print "Error in %s log: %s" % (error.Logfile, error.Message)
        # send mail to sysadmin etc.

# dont know what the connection between this and log files
def try3():
    c = wmi.WMI()
    for i in c.Win32_NTLogEvent(EventType=2, Logfile="Application"):
        print i
        # break

# tring by query, but dont get much info
def try2():
    rval = 0  # Default: Check passes.

    # Initialize WMI objects and query.
    wmi_o = wmi.WMI('.')
    wql = ("SELECT * FROM Win32_NTLogEvent WHERE Logfile="
           "'Application' AND EventCode='1003'")

    # Query WMI object.
    wql_r = wmi_o.query(wql)

    print wql_r

    if len(wql_r):
        rval = -1  # Check fails.

    return rval



if __name__ == '__main__':
    main()