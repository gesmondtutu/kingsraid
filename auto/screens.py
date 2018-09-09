import random
import pyautogui
from msg import printd

click_min = 130
click_max = 160
click_div = 100

class Button:
  def __init__(self, l, t, w, h):
    self.left = l
    self.top = t
    self.width = w
    self.height = h
  def click(self=False):
    x = random.randrange(self.left, self.left + self.width)
    y = random.randrange(self.top, self.top + self.height)
    printd(f'Clicking x={x}, y={y}')
    pyautogui.click(x=x, y=y)
    pyautogui.PAUSE = random.randrange(click_min,click_max) / click_div
  def doubleClick(self=False):
    x = random.randrange(self.left, self.left + self.width)
    y = random.randrange(self.top, self.top + self.height)
    printd(f'Clicking x={x}, y={y}')
    pyautogui.doubleClick(x=x, y=y)
    pyautogui.PAUSE = random.randrange(click_min,click_max) / click_div

class Screen:
  def __init__(self, image_path, mask_path, buttons):
    self.image_path=image_path
    self.mask_path=mask_path
    self.buttons = {}
    for name, button in buttons.items():
      self.addButton(name, button)
  def addButton(self, name, button):
    self.buttons[name] = button

screens = {
  'WorldScreen': Screen(
    image_path = {'default':'screens/world.jpg'},
    mask_path = 'screens/mask0.jpg',
    buttons = {
    'inventoryButton':Button(313, 1497, 94, 88),
    'battleButton'   :Button(2479, 1488, 88, 64),
    'raidButton'     :Button(2494, 1224, 90, 78),
  }),
  'NoticeScreen': Screen(
    image_path = {
      'DisassemblingItems'  :'screens/inventory4.jpg',
      'RepeatNoticeScreen'  :'screens/repeat.jpg',
      'RepeatBattleLoss'    :'screens/autobattleloss.jpg',
      'RepeatFullInventory' :'screens/autoFullInventory.jpg',
      'GearFull'            :'screens/gearFull.jpg',
      'RaidRepeat'          :'screens/raidrepeat.jpg',
      'InsufficientPMScreen':'screens/insufficient.jpg',
      'Disconnected'        :'screens/disconnected.jpg',
    },
    mask_path = 'screens/mask2.jpg',
    buttons = {
      'okButton'  :Button(748, 1247, 1240, 67),
      'xButton'   :Button(1986, 505, 67, 67),
      'sellButton':Button(1264, 1244, 732, 70),
  }),
  'InventoryScreen': Screen(
    image_path = {
      'InventoryScreen':'screens/inventory1.jpg',
      'GrindScreen'    :'screens/inventory2.jpg',
    },
    mask_path = 'screens/mask5.jpg',
    buttons = {
      'toWorldButton'   :Button(270, 184, 65, 33),
      'undoFilterButton':Button(691, 1451, 60, 60),
      'selectAllButton' :Button(872, 1442, 315, 70),
      'filterButton'    :Button(1301, 1442, 315, 70),
      'grindButton'     :Button(1748, 1442, 315, 70),
      'sellButton'      :Button(2180, 1442, 315, 70),
      'grindAllButton'  :Button(1422, 1442, 292, 71),
  }),
  'GrindAllScreen': Screen(
    image_path = {'default':'screens/inventory3.jpg'},
    mask_path = 'screens/mask6.jpg',
    buttons = {
      'grindButton':Button(233, 1370, 2264, 65),
      'sellButton' :Button(1016, 1398, 1272, 74),
  }),
  'BattleScreen': Screen(
    image_path = {
      'BattleScreen1' :'screens/battle1.jpg',
      'BattleScreen1a':'screens/battle1sub.jpg',
      'HeroSelect' :'screens/battle2.jpg',
    },
    mask_path = 'screens/mask1.jpg',
    buttons = {
      'readyButton'     :Button(2046, 1502, 499, 78),
      'toWorldButton'   :Button(270, 184, 65, 33),
      'autoRepeatButton':Button(1653, 1532, 352, 53),
  }),
  'BattleLossScreen': Screen(
    image_path = {
      'DefeatScreen':'screens/defeat.jpg',
      'RepeatScreen':'screens/repeatafterloss.jpg',
    },
    mask_path = 'screens/mask3.jpg',
    buttons = {
      'retryButton' :Button(2508, 1152, 108, 93),
      'repeatButton':Button(1405, 1056, 583, 76),
      'exitButton'  :Button(2522, 1440, 88, 88),
  }),
  'RaidScreen': Screen(
    image_path = {'default':'screens/raid.jpg'},
    mask_path = 'screens/mask7.jpg',
    buttons = {
      'toWorldButton'      :Button(270, 184, 65, 19),
      'partyplayButton'    :Button(340, 1406, 462, 68),
      'dragonraidButton'   :Button(1131, 1406, 462, 68),
      'challengeraidButton':Button(1925, 1406, 462, 68),
  }),
  'DragonRaidScreen': Screen(
    image_path = {
      'fire'  :'screens/dragonmenu1.jpg',
      'frost' :'screens/dragonmenu1.jpg',
      'poison':'screens/dragonmenu1.jpg',
      'black' :'screens/dragonmenu1a.jpg',
    },
    mask_path = 'screens/mask8.jpg',
    buttons = {
      'toWorldButton':Button(270, 184, 65, 19),
      'hardButton'   :Button(1820, 293, 294, 70),
      'fire'         :Button(2113, 705, 212, 99),
      'frost'        :Button(2113, 1048, 212, 99),
      'poison'       :Button(2113, 1385, 212, 99),
      'black'        :Button(2113, 1468, 212, 99),
  }),
  'DragonScreen': Screen(
    image_path = {
      'fire'  :'screens/dragon_fire.jpg',
      'frost' :'screens/dragon_frost.jpg',
      'poison':'screens/dragon_poison.jpg',
      'black' :'screens/dragon_black.jpg',
    },
    mask_path = 'screens/mask9a.jpg',
    buttons = {}
  ),
  'DragonLevelScreen': Screen(
    image_path = {
      'fire'  :'screens/dragon_fire_{}.jpg',
      'frost' :'screens/dragon_frost_{}.jpg',
      'poison':'screens/dragon_poison_{}.jpg',
      'black' :'screens/dragon_black_{}.jpg',
    },
    mask_path = 'screens/mask9b.jpg',
    buttons = {
      'gatherRaidersButton':Button(864, 936, 62, 62),
      'levelDnButton'      :Button(1022, 745, 69, 69),
      'levelUpButton'      :Button(1641, 743, 69, 69),
      'enterButton'        :Button(1005, 1313, 718, 99),
  }),
  'DragonRaidReadyScreen': Screen(
    image_path = {
      'default':'screens/dragonraid.jpg',
      'afterBattle':'screens/raidfinish.jpg'
    },
    mask_path = 'screens/mask10.jpg',
    buttons = {
      'toWorldButton':Button(270, 184, 65, 19),
      'CH1Button'    :Button(226, 1234, 80, 80),
      'CH2Button'    :Button(475, 1234, 80, 80),
      'CH3Button'    :Button(692, 1234, 80, 80),
      'CH4Button'    :Button(226, 1461, 80, 80),
      'CH5Button'    :Button(475, 1461, 80, 80),
      'CH6Button'    :Button(692, 1461, 80, 80),
      'autoButton'   :Button(1848, 1382, 53, 53),
      'startButton'  :Button(2145, 1497, 373, 82),
  }),
  'BattleFinishScreen': Screen(
    image_path = {'default':'screens/battlefinish.jpg'},
    mask_path = 'screens/mask11.jpg',
    buttons = {
      'retryButton' :Button(2508, 1152, 108, 93),
      'exitButton'  :Button(2522, 1440, 88, 88),
  }),
}
