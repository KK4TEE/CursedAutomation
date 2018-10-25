import curses 
import random
import time

import pyHS100  # Download and install from GitHub
import nmap     # pip3 install python-nmap

VERSION         = "0.1.2"
DESKLAMPURL     = "10.42.40.22"
FRIDGELAMPURL   = "10.42.40.21"
MOVEABLELAMPURL = "10.42.40.20"
STRINGLIGHTSURL = "10.42.40.144"
LIVINGFANURL    = "10.42.40.136"

SPHONE          = "10.42.42.42"
KPHONE          = "10.42.42.43"
#KPHONE          = "192.168.1.67"
PHONELIST       = [ SPHONE, KPHONE]

REFRESHTIME     = 15.0 	       #Seconds
screen = curses.initscr() 
#curses.noecho() 
screen.nodelay(True)
#screen.halfdelay(1)
curses.curs_set(0) 
screen.keypad(1) 
curses.mousemask(1)
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_WHITE)
curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

screen.addstr("Home Automation Interface Attempt\n\n")
screen.addstr("Searching for devices...")
candleMode = False


def DrawColorButton( label, y, x):
    screen.addstr( y    , x, label,      curses.color_pair(0))
    screen.addstr( y + 1, x, "  WARM  ", curses.color_pair(4))
    screen.addstr( y + 2, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 3, x, "  RED   ", curses.color_pair(1))
    screen.addstr( y + 4, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 5, x, "  BLUE  ", curses.color_pair(3))
    screen.addstr( y + 6, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 7, x, "  GREEN ", curses.color_pair(2))
    screen.addstr( y + 8, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 9, x, " CANDLE ", curses.color_pair(4))
    screen.addstr( y + 10, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 11, x, "  WHITE ", curses.color_pair(5))


def DrawOnOffButton( label, y, x):
    screen.addstr( y    , x, label,      curses.color_pair(0))
    screen.addstr( y + 1, x, "   ON   ", curses.color_pair(2))
    screen.addstr( y + 2, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 3, x, "   MOD  ", curses.color_pair(5))
    screen.addstr( y + 4, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 5, x, "   OFF  ", curses.color_pair(1))


def DrawBrightnessButton( label, y, x):
    screen.addstr( y    , x, label,      curses.color_pair(0))
    screen.addstr( y + 1, x, "  FULL  ", curses.color_pair(2))
    screen.addstr( y + 2, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 3, x, "   75%  ", curses.color_pair(5))
    screen.addstr( y + 4, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 5, x, "   50%  ", curses.color_pair(5))
    screen.addstr( y + 6, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 7, x, "   25%  ", curses.color_pair(5))
    screen.addstr( y + 8, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 9, x, "   MIN  ", curses.color_pair(1))


def DrawMoodButton( label, y, x):
    screen.addstr( y    , x, label,      curses.color_pair(0))
    screen.addstr( y + 1, x, "BUSINESS", curses.color_pair(2))
    screen.addstr( y + 2, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 3, x, "  MOVIE ", curses.color_pair(5))
    screen.addstr( y + 4, x, " ------ ", curses.color_pair(0))
    screen.addstr( y + 5, x, "   OFF  ", curses.color_pair(1))


#TODO: Fix spelling of panel
def DrawButtonPannel():
    DrawOnOffButton( "  DESK   ", 1, 0)
    DrawOnOffButton( " FRIDGE  ", 1, 10)
    DrawOnOffButton( "MOVEABLE ", 1, 20)
    DrawOnOffButton( " STRING  ", 1, 30)
    DrawOnOffButton( "  FAN    ", 1, 40)
    DrawColorButton( "  DESK   ", 1, 50)

def DrawPhonePanel(phones, y, x):
    #
    label = " PORTABLE PHONES "
    screen.addstr( y    , x, label,      curses.color_pair(0))
    if SPHONE in phones:
        s = "SPHONE : ONLINE "
        screen.addstr( y + 1, x, s, curses.color_pair(2))
    else: 
        s = "SPHONE : OFFLINE"
        screen.addstr( y + 1, x, s, curses.color_pair(1))
    screen.addstr( y + 2, x, "  -- ------ --    ", curses.color_pair(0))
    if KPHONE in phones:
        s = "KPHONE : ONLINE "
        screen.addstr( y + 3, x, s, curses.color_pair(2))
    else: 
        s = "KPHONE : OFFLINE"
        screen.addstr( y + 3, x, s, curses.color_pair(1))
    #TODO: ADD CHECKS FOR ADDITIONAL PHONE
    screen.addstr( y + 4, x, "  -- ------ --  ", curses.color_pair(0))


def FindListDevices():
    tp = pyHS100.Discover.discover()
    #tpKeyList = [*tp]
    yL = 1
    xStart = 12
    '''
    for deviceURL in tpKeyList:
        screen.addstr( yL, xStart, deviceURL)
        yL += 1
    ''' 
    return tp


def CheckPhones(listAddr):
    phoneStatus = {}
    stringAddr = ""
    for s in listAddr:
        stringAddr += s + ' '
    nm = nmap.PortScanner()
    nm.scan(hosts=stringAddr, arguments='-n -sP -PE -PA21,23,80,3389, -w 1')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:
        #print('{0}:{1}'.format(host, status))
        #if host in ['10.42.42.2']:
        if status in ['up']:
            if host in PHONELIST:
                phoneStatus[host] = [True, time.time()]
                #print('STATUS IS SO GOOD RIGHT NOW FOR ' + host)
    return phoneStatus


cColor    = [30, 85, 34]
maxcColor = [ 35, 95, 45]
mincColor = [25, 75, 24]
def CandleColor():
    cColor    = [30, 85, 34]
    maxcColor = [ 35, 95, 45]
    mincColor = [25, 75, 24]
    rRange = 60

    cColor = cColor + [random.randint(-rRange, rRange),
                       random.randint(-rRange, rRange),
                       random.randint(-rRange,rRange)] 
    return cColor
'''
    if cColor[0] > maxcColor[0]:
        cColor = maxcColor[0]
    elif cColor[0] < mincColor[0]:
        cColor[0] = mincColor[0]
    if cColor[1] > maxcColor[1]:
        cColor = maxcColor[1]
    elif cColor[1] < mincColor[1]:
        cColor[1] = mincColor[1]
    if cColor[2] > maxcColor[2]:
        cColor = maxcColor[2]
    elif cColor[2] < mincColor[2]:
        cColor[2] = mincColor[2]
    #tp[ModBulbURL].hsv = ( 30, 1, 34)
'''
  #  return cColor

def main(stdscr):
    print('phones...')
    phones = (CheckPhones(PHONELIST))
    print(phones)
    time.sleep(1)
    print('SmartDevices...')
    tp = FindListDevices()
    screen.clear()
    screen.addstr( 0,0, "kkAutomation, Version " + VERSION)
    DrawButtonPannel()
    DrawPhonePanel(phones, 7, 0) #TODO: MOVE TO UPDATE LOOP
    DrawBrightnessButton( "  VIS  ", 1, 60 ) 
    DrawMoodButton( " MOOD  ", 13, 60)
    candleMode = False
    ModBulbURL      = DESKLAMPURL
    lastRefreshTime = time.time()
    lastLoopTime = time.time()
    
    while True:
        if lastRefreshTime + REFRESHTIME < time.time():
            screen.addstr( 7, 0, "  --REFRESH--    ", curses.color_pair(1))
            #curses.doupdate()
            screen.refresh()
            #time.sleep(0.21)
            phones = (CheckPhones(PHONELIST))
            lastRefreshTime = time.time()
            DrawPhonePanel(phones, 7, 0)
            
        event = screen.getch() 
        if event == ord("q"): break
        #if event == ord("a"): screen.addstr( 5, 5, "LIGHT ON! ")
        #if event == ord("z"): screen.addstr( 5, 5, "LIGHT OFF!") 
        if event == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            y, x = screen.getyx()
            screen.addstr(y, x, screen.instr(my, mx, 5))
            screen.addstr(12, 5, "Screen resolution is:   " + str(screen.getmaxyx()))
            screen.addstr(13, 5, "Screen location is   Y: " + str(y) + " X: " + str(x))
            screen.addstr(14, 5, "Y: " + str(my) + " X: " + str(mx) + str("     "))

            if my in range (0, 3):
                # An ON button was pressed
                if mx in range(0, 9):
                    if DESKLAMPURL in tp:
                        tp[DESKLAMPURL].turn_on()
                elif mx in range ( 10, 19):
                    if FRIDGELAMPURL in tp:
                        tp[FRIDGELAMPURL].turn_on()
                elif mx in range (20, 29):
                    if MOVEABLELAMPURL in tp:
                        tp[MOVEABLELAMPURL].turn_on()
                elif mx in range (30, 39):
                    if STRINGLIGHTSURL in tp:
                        tp[STRINGLIGHTSURL].turn_on()
                elif mx in range (40, 49):
                    if LIVINGFANURL in tp:
                        tp[LIVINGFANURL].turn_on()

            elif my is 4:
                # A MOD button was pressed
                if mx in range(0, 9):
                    if DESKLAMPURL in tp:
                        ModBulbURL = DESKLAMPURL
                        DrawColorButton( "  DESK  ", 1, 50)
                elif mx in range ( 10, 19):
                    if FRIDGELAMPURL in tp:
                        ModBulbURL = FRIDGELAMPURL
                        DrawColorButton( " FRIDG  ", 1, 50)
                elif mx in range (20, 29):
                    if MOVEABLELAMPURL in tp:
                        ModBulbURL = MOVEABLELAMPURL
                        DrawColorButton( "  MOVE  ", 1, 50)
                elif mx in range (30, 39):
                    if STRINGLIGHTSURL in tp:
                        pass
                        #ModBulbURL = STRINGLIGHTSURL
                        #DrawColorButton( " STRING ", 1, 50)
                elif mx in range (40, 49):
                    if LIVINGFANURL in tp:
                        pass
                        #ModBulbURL = LIVINGFANURL
                        #DrawColorButton( "  FAN   ", 1, 50)
            
            elif my in range (6,8):
                # An OFF button was pressed
                if mx in range(0, 9):
                    if DESKLAMPURL in tp:
                        tp[DESKLAMPURL].turn_off()
                elif mx in range ( 10, 19):
                    if FRIDGELAMPURL in tp:
                        tp[FRIDGELAMPURL].turn_off()
                elif mx in range (20, 29):
                    if MOVEABLELAMPURL in tp:
                        tp[MOVEABLELAMPURL].turn_off()
                elif mx in range (30, 39):
                    if STRINGLIGHTSURL in tp:
                        tp[STRINGLIGHTSURL].turn_off()
                elif mx in range (40, 49):
                    if LIVINGFANURL in tp:
                        tp[LIVINGFANURL].turn_off()

            # Color Selection Buttons

            if mx in range (50, 59):
                modBulbBrightness = tp[ModBulbURL].brightness 
            if my is 2:
                if mx in range (50, 59):
                    #print("WARM SELECTED!")
                    tp[ModBulbURL].hsv = ( 30, 85, modBulbBrightness)
                    #print("HSV: " + str(tp[DESKLAMPURL].hsv) + "   ]")
                    #print("COL: " + str(tp[DESKLAMPURL].color_temp)+ "   ]")
            elif my is 4:
                if mx in range (50, 59):
                    tp[ModBulbURL].hsv = ( 1, 100, modBulbBrightness)
                    #print("RED SELECTED!")
                    
            elif my is 6:
                if mx in range (50, 59):
                    tp[ModBulbURL].hsv = ( 246, 100, modBulbBrightness)
                    #print("BLUE SELECTED!")
            elif my is 8:
                if mx in range (50, 59):
                    tp[ModBulbURL].hsv = ( 125, 100, modBulbBrightness)
                    #print("GREEN SELECTED!")
            elif my is 10:
                if mx in range (50, 59):
                    candleMode = True
                    #tp[ModBulbURL].hsv = CandleColor()
                    #print("CANDLE SELECTED!")
            elif my is 12:
                if mx in range (50, 59):
                    tp[ModBulbURL].hsv = ( 30, 0, modBulbBrightness)
                    #print("WHITE SELECTED!")

            # Brightness buttons
            if my is 2:
                if mx in range (60, 69):
                    tp[ModBulbURL].brightness = 100
            elif my is 4:
                if mx in range (60, 69):
                    tp[ModBulbURL].brightness = 75
            elif my is 6:
                if mx in range (60, 69):
                    tp[ModBulbURL].brightness = 50
            elif my is 8:
                if mx in range (60, 69):
                    tp[ModBulbURL].brightness = 25
            elif my is 10:
                if mx in range (60, 69):
                    tp[ModBulbURL].brightness = 1

            if my is 14:
                if mx in range (60, 69):
                    # Business
                    tp[DESKLAMPURL].turn_on()
                    tp[DESKLAMPURL].hsv = ( 30, 0, 90)
                    tp[FRIDGELAMPURL].turn_on()
                    tp[FRIDGELAMPURL].hsv = ( 30, 0, 90)
                    tp[MOVEABLELAMPURL].turn_on()
                    tp[MOVEABLELAMPURL].hsv = ( 30, 0, 90)
                    tp[STRINGLIGHTSURL].turn_off()
            elif my is 16:
                if mx in range (60, 69):
                    # Movie
                    tp[DESKLAMPURL].turn_on()
                    tp[DESKLAMPURL].hsv = ( 30, 85, 5)
                    tp[FRIDGELAMPURL].turn_on()
                    tp[FRIDGELAMPURL].hsv = ( 30, 85, 5)
                    tp[MOVEABLELAMPURL].turn_on()
                    tp[MOVEABLELAMPURL].hsv = ( 30, 85, 5)
                    tp[STRINGLIGHTSURL].turn_on()
                    tp[LIVINGFANURL].turn_off()
            elif my is 18:
                    # All off
                    tp[DESKLAMPURL].turn_off()
                    tp[FRIDGELAMPURL].turn_off()
                    tp[MOVEABLELAMPURL].turn_off()
                    tp[STRINGLIGHTSURL].turn_off()
                    tp[LIVINGFANURL].turn_off()

        if candleMode is True:
            tp[ModBulbURL].hsv = CandleColor()
                
        
        time.sleep(max( 0, lastLoopTime - time.time() + 0.1))
        screen.addstr( 15, 0, " Looptime: " + "%.4f" % round(lastLoopTime - time.time(), 4), curses.color_pair(1))
        lastLoopTime = time.time()
        curses.doupdate()

    curses.endwin()

curses.wrapper(main)
