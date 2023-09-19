import pygame as pg, json, os, math, sys
from sys import exit

pg.init()
# screen size
dim = (1400, 720)
currDir = os.getcwd()
if hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)

defaultSettings = {
  "resetKey" : "right shift",
  "--------- key for instantly resetting all counters": None,
  "size" : 50,
  "--------- size of the key squares and other miscellaneous": None,
  "gap" : -1,
  "--------- gap between them": None,
  "fps" : 240,
  "rainSpeed" : 600,
  "accMaxTime" : 15000,
  "--------- maximum time for kps to be accumulating inputs": None,
  "accTimeout" : 1000,
  "--------- timeout for kps before resetting": None,
  "seqTimeout" : 25000,
  "--------- timeout for sequencer before resetting" : None,
  "seqAcc" : 20,
  "--------- maximum amount of inputs stored in sequencer" : None,
  "heightMtp" : 2,
  "--------- height of the sequencer bars" : None,
  "decPlaces" : 2,
  "--------- number of decimal places in kps" : None,

  "colorDown" : [140, 0, 0],
  "colorUp" : [100, 100, 100],
  "rainColor" : [100, 0, 0]
}

iconPath = "icon32.png"
path = "settings.json"
keyPath = "keys.json"
validity = True
defaultKeys = [97, 115, 100, 118, 110, 107, 108, 59]

stg = {
       "resetKey": "right shift",
       "size": 50,
       "gap": 5,
       "fps": 240,
       "rainSpeed": 600,
       "accMaxTime": 15000,
       "accTimeout": 1000,
       "seqTimeout": 25000,
       "seqAcc": 20,
       "heightMtp": 2,
       "decPlaces": 2,
       "colorDown" : [140, 0, 0],
       "colorUp" : [100, 100, 100],
       "rainColor" : [100, 0, 0]
       }
path = currDir+"\\"+path
keyPath = currDir+"\\"+keyPath

if not os.path.isfile(path):
    file = open(path, "w+")
    json.dump(defaultSettings, file, indent=4)
    file.close()

if not os.path.isfile(keyPath):
    file = open(keyPath, "w+")
    json.dump({"keys": defaultKeys}, file)
    file.close()

if os.path.isfile(path) and os.path.isfile(keyPath):
    try:
        tempDict = {}
        settingKeys = stg.keys()
        file = open(path)
        keysFile = open(keyPath)
        data = json.load(file)
        for setting in settingKeys:
            tempDict.update({setting: data[setting]})
        stg = tempDict
        stg.update(json.load(keysFile))
        file.close()
        keysFile.close()
    except Exception:
        validity = False
        stg.update({"keys":defaultKeys})

else:
    stg.update({"keys":defaultKeys})
    validity = False



keys = stg["keys"] if stg["keys"] else defaultKeys
try:
    resetKey = pg.key.key_code(stg["resetKey"])  # key for instantly resetting all counters
except ValueError:
    resetKey = pg.key.key_code("right shift")

setKeys = False
size = 50
font = pg.font.SysFont("Arial", 1)
def setSize(keys):
    global size, font, startPos
    size = stg["size"]*4/math.sqrt(len(keys)+1)  # size of the key squares
    font = pg.font.SysFont("Arial", int(math.sqrt(size*5)))
    startPos = (size, dim[1] - size*2 - 50)

gap = stg["gap"]  # gap between them
fps = stg["fps"]
rainSpeed = stg["rainSpeed"]
accMaxTime = stg["accMaxTime"]  # maximum time for kps to be accumulating inputs
accTimeout = stg["accTimeout"]  # timeout for kps before resetting
seqTimeout = stg["seqTimeout"]  # timeout for sequencer before resetting
seqAcc = stg["seqAcc"]  # maximum amount of inputs stored in sequencer
heightMtp = stg["heightMtp"]  # height of the sequencer bars
decPlaces = stg["decPlaces"]  # number of decimal places in kps

colorDown = stg["colorDown"]
colorUp = stg["colorUp"]
rainColor = stg["rainColor"]

# # # # code # # # #
shorten = {
    "backspace": "bkspc",
    "page down": "pgdn",
    "page up": "pgup",
    "numlock": "numL",
    "left shift": "Lshift",
    "right shift": "Rshift",
    "caps lock": "caps"
}

setSize(keys)
icon = pg.image.load(iconPath)
pg.display.set_caption("Roll Analyzer")
screen = pg.display.set_mode(dim)
pg.display.set_icon(icon)
clock = pg.time.Clock()
rainSpeed = round(rainSpeed / fps)
miscFont = pg.font.SysFont("Arial", 25)
keyArray = []
currList = []


def setK():
    global setKeys, keys, validity
    sizeSet = stg["size"] * 4 / math.sqrt(len(keys)+1)
    txt = miscFont.render(f"Press \"{pg.key.name(resetKey)}\" to finish", True, (255,255,255))
    txtPos = (dim[0]/2 - txt.get_rect().width/2, 5)
    currList = []
    while setKeys:
        screen.fill((0, 0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                id = event.__dict__["key"]
                if id == resetKey:
                    try:
                        file = open(keyPath, "r+")
                        data = json.load(file)
                        data["keys"] = currList
                        keys = currList if currList else defaultKeys
                        file.truncate(0)
                        file.seek(0)
                        file.write(json.dumps(data, ensure_ascii=False))
                        file.close()
                        setSize(currList)
                        setKeys = False
                        break
                    except Exception:
                        validity = False
                        break
                if id in currList:
                    currList.remove(id)
                else:
                    currList.append(id)
                sizeSet = stg["size"] * 4 / math.sqrt(len(currList)+1)
        if currList:
            pos = [dim[0]/2 - len(currList)*(sizeSet+gap)/2, dim[1]/2-sizeSet/2]
            for key in currList:
                keyName = pg.key.name(key)
                label = shorten[keyName] if keyName in shorten.keys() else keyName
                text = font.render(label, True, (255, 255, 255))
                rect = pg.Rect(pos, (sizeSet, sizeSet))
                pg.draw.rect(screen, colorUp, rect)
                screen.blit(text,
                            (rect.centerx - text.get_rect().centerx,
                             rect.centery - text.get_rect().centery)
                            )
                pos[0] += sizeSet + gap

        screen.blit(txt, txtPos)
        pg.display.flip()



def foo(pos, key, arr):
    if key < len(keys):
        arr.append(KeyRect(keys[key], (size, size), pos))
        foo((pos[0] + size + gap, pos[1]), key + 1, arr)

def setup():
    global keysStrArr, keyCount, keyArray, kps, fpsC, seq, changeBtn
    keyArray = []
    foo(startPos, 0, keyArray)
    keysStrArr = [pg.key.name(key) for key in keys]
    keyCount = len(keys)
    kps = KPS(decPlaces, (dim[0] - 2 * size - gap, dim[1] - size - gap))
    fpsC = FPS()
    seq = KeySequencer(keyArray, keys)
    changeBtn = KeyChange((keyArray[0].Rect.left, keyArray[-1].Rect.right), keyArray[0].Rect.bottom)

class Rain:
    def __init__(self, pos, xsize):
        self.pos = [pos[0], pos[1]]
        self.size = [xsize, 0]
        self.rect = pg.Rect(self.pos, self.size)
        self.color = rainColor
        self.held = 1

    def move(self, state):
        if not state:
            self.held = 0
        self.rect.y -= rainSpeed
        if self.held:
            self.rect.h += rainSpeed

    def draw(self):
        pg.draw.rect(screen, self.color, self.rect)


class KeyRect:
    def __init__(self, id, size, pos):
        self.id = id
        keyName = pg.key.name(id)
        self.label = shorten[keyName] if keyName in shorten.keys() else keyName
        self.text = font.render(self.label, True, (255, 255, 255))
        self.Rect = pg.Rect(pos, size)
        self.color = colorUp
        self.raindrops = []
        self.state = False

    def draw(self):
        pg.draw.rect(screen, self.color, self.Rect)
        screen.blit(self.text,
                    (self.Rect.centerx - self.text.get_rect().centerx,
                     self.Rect.centery - self.text.get_rect().centery)
                    )

    def addRain(self):
        self.raindrops.append(Rain(self.Rect.topleft, self.Rect.size[0]))

    def rain(self, state):
        if self.raindrops:
            for drop in self.raindrops:
                drop.move(state)
                drop.draw()
                if drop.rect.size[1] + drop.rect.y < -200:
                    self.raindrops.pop(self.raindrops.index(drop))



class KPS:
    def __init__(self, dec, pos):
        self.dec = dec
        self.kps = 0
        self.pressArr = []
        self.diffArr = []
        self.avg = 0
        self.Rect = pg.Rect(pos, (size, size))
        self.bpmtext, self.kpstext = "", ""

    def add(self, time):
        self.pressArr.append(time)
        if len(self.pressArr) > 1:
            self.diffArr.append(self.pressArr[-1] - self.pressArr[-2])

        self.avg = sum(self.diffArr) / len(self.diffArr) if self.diffArr else 0

    def check(self, currTime):
        if self.pressArr:
            if self.pressArr[-1] < currTime - accTimeout:
                self.pressArr = []
                self.diffArr = []
            elif self.pressArr[0] < currTime - accMaxTime:
                self.pressArr.pop(0)
                self.diffArr.pop(0)
                self.check(currTime)

    def calc(self):
        if self.avg and (len(self.diffArr) > keyCount * 3 or self.avg > 100 / keyCount):
            self.kpstext = str(round(1000 / self.avg, self.dec))
            self.bpmtext = str(round(60000 / self.avg, self.dec))
        else:
            self.kpstext, self.bpmtext = "0", "0"
        self.kpstext = "KPS: " + self.kpstext
        self.bpmtext = "BPM: " + self.bpmtext

    def render(self):

        self.calc()
        textRect = miscFont.render(self.kpstext, True, (255, 255, 255))
        screen.blit(textRect,
                    (self.Rect.centerx - textRect.get_rect().midleft[0] - 110,
                     self.Rect.centery - textRect.get_rect().centery)
                    )

        textbpmRect = miscFont.render(self.bpmtext, True, (255, 255, 255))
        screen.blit(textbpmRect,
                    (self.Rect.centerx - textbpmRect.get_rect().topleft[0] - 110,
                     self.Rect.centery - textbpmRect.get_rect().centery - 40)
                    )


class FPS:
    def __init__(self):
        self.fpsArr = []
        self.frames = 120

    def tick(self, num):
        self.fpsArr.append(num)
        if len(self.fpsArr) > self.frames:
            self.fpsArr.pop(0)

    def render(self):
        text = str(round(
            1000 / (
                    sum(self.fpsArr) / len(self.fpsArr)
            )
        ))
        textRect = miscFont.render(text, True, (255, 255, 255))
        screen.blit(textRect, (dim[0] - textRect.get_rect().midleft[0] - size,
                               textRect.get_rect().centery))


class KeySequencer:
    def __init__(self, keyArray, keys):
        width = (keyArray[-1].Rect.right - keyArray[0].Rect.left) / 2
        self.keys = keys
        self.barWidth = round(width / len(keyArray))
        self.startPts = [dim[0] - size - width + self.barWidth * n for n in range(len(keyArray))]
        self.sequence = {}
        self.timing = {}
        self.avgErr = {}
        self.avg = 0
        self.timings = []
        self.height = 100
        self.endLinePos = (dim[0] - size, self.height), width
        self.msFont = pg.font.SysFont('Arial', int(self.barWidth / 3))

    def render(self):

        for dot in range(len(self.startPts)):
            text = ""
            errText = ""
            h = 1
            avgH = self.avg * heightMtp
            if self.keys[dot] in self.timing.keys():
                if self.timing[self.keys[dot]]:
                    h = self.timing[self.keys[dot]] * heightMtp
                    text = str(round(self.timing[self.keys[dot]], 1))
                    errText = str(round(self.avgErr[self.keys[dot]], 1))

            pg.draw.rect(screen, (255, 255, 255), pg.Rect((self.startPts[dot], self.height, self.barWidth, h)), 2)

            pg.draw.line(screen, (100,255,100),
                                 (self.startPts[0], self.height+avgH),
                                 (self.startPts[-1]+self.barWidth, self.height+avgH))


            textRect = self.msFont.render(text, True, (255, 255, 255))
            pos = (self.startPts[dot] + self.barWidth / 2 - textRect.get_rect().width / 2,
                   self.height - self.msFont.get_height())
            screen.blit(textRect, pos)


            textRect = self.msFont.render(errText, True, (255, 255, 255))
            pos = (self.startPts[dot] + self.barWidth / 2 - textRect.get_rect().width / 2,
                   self.height + h + self.msFont.get_height())
            screen.blit(textRect, pos)



    def check(self, time):
        if self.timings:
            if time - self.timings[-1] > seqTimeout:
                self.reset()

    def clearOld(self, key, time):
        if len(self.sequence[key]) > seqAcc:
            self.sequence[key].pop(0)
            self.clearOld(key, time)

        elif self.timings[0] < time - seqTimeout:
            self.timings.pop(0)
            self.clearOld(key, time)

        else:
            return

    def addKey(self, key):
        if not self.sequence or key not in self.sequence.keys():
            self.sequence.update({key: []})
            self.timing.update({key: 0})
            self.avgErr.update({key: 0})



    def update(self, key, time):
        self.timings.append(time)

        self.addKey(key)

        self.clearOld(key, time)

        if len(self.timings) >= 2:
            self.sequence[key].append(self.timings[-1] - self.timings[-2])
            s = 0
            for n in self.sequence[key]:
                s += n
            self.timing[key] = s / len(self.sequence[key])

        if len(self.timing) > 1:
            self.avg = 0
            for n in list(self.timing.values()):
                self.avg += n
            self.avg /= len(self.timing.keys())
            for k in list(self.avgErr.keys()):
                self.avgErr[k] = self.timing[k] - self.avg



    def reset(self):
        self.sequence = {}
        self.timing = {}
        self.timings = []
        self.avgErr = {}
        self.avg = 0


class KeyChange:
    def __init__(self, bar, height):
        size = 50
        center = (bar[1]+bar[0])/2, height+size
        self.size = (size*4,size)
        self.rect = pg.Rect((0,0),self.size)
        self.rect.center = center
        self.hover = [int(c/3) for c in colorUp]
        self.color = colorUp
        self.text = miscFont.render("Change keys", True, (255,255,255))

    def render(self):
        pg.draw.rect(screen, self.color, self.rect)
        pg.draw.rect(screen, (255,255,255), self.rect, 3)
        screen.blit(self.text,
                    (self.rect.centerx - self.text.get_rect().centerx,
                     self.rect.centery - self.text.get_rect().centery)
                    )

    def checkClick(self):
        global setKeys
        pos = pg.mouse.get_pos()
        state = pg.mouse.get_pressed()[0]
        if self.rect.collidepoint(pos):
            self.color = self.hover
            if state:
                setKeys = True
        else:
            self.color = colorUp




def main():
    setK()
    setup()

    vdtyCounter = None
    vdtyTime = 2500 * 50 / fps
    if not validity:
        vdtyCounter = 0

    while 1:
        if setKeys:
            setK()
            setup()

        screen.fill((0, 0, 0))
        changeBtn.checkClick()
        changeBtn.render()
        if vdtyCounter is not None:
            if vdtyCounter < vdtyTime:
                opacity = -((vdtyCounter / vdtyTime) ** 8) + 1
                vdtyCounter += 1
                textRect = miscFont.render("Invalid json or doesnt exist! (settings.json / keys.json)", True,
                                       (int(255 * opacity), int(255 * opacity), int(255 * opacity)))
                screen.blit(textRect, (dim[0] / 2 - textRect.get_rect().midleft[0] - textRect.get_rect().width / 2,
                                       dim[1] / 2 - textRect.get_rect().topleft[1] - textRect.get_rect().height / 2))

        fpsC.tick(clock.tick(fps))
        for event in pg.event.get():
            id = 0
            key = None
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                id = event.__dict__["key"]
                if id in keys:
                    place = keys.index(id)
                    key = keyArray[place]
            if id == resetKey:
                kps.check(9999999999)  # reset
                seq.reset()
            if id in keys:
                if not key.state:
                    seq.update(id, pg.time.get_ticks())
                    key.addRain()
                    key.color = colorDown
                    kps.add(pg.time.get_ticks())
                    key.state = 1
                else:
                    key.color = colorUp
                    key.state = 0
        for key in keyArray:
            key.rain(key.state)
            key.draw()

        kps.check(pg.time.get_ticks())
        seq.check(pg.time.get_ticks())
        fpsC.render()
        seq.render()
        kps.render()
        pg.display.flip()


if __name__ == "__main__":
    main()
