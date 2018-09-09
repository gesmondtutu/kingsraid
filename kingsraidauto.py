# pip install opencv-python
# pip install Pillow
# pip install scipy
# pip install scikit-image
# pip install pyautogui

import os
import cv2
import numpy as np
import time
import pyautogui
import argparse
from PIL import ImageGrab
from skimage.measure import _structural_similarity as ssim
from screens import screens
import msg
from msg import printd
import dragons
import heroes

SSIM_cutoff     = 0.99
max_snaps       = 20
screensnap_ind  = max_snaps
resize_percent  = 0.25
snap_dir        = 'snaps'
lost            = 0
disconnect      = 0
tick            = 0
pyautogui.PAUSE = 1.5

if not os.path.isdir(snap_dir):
  os.makedirs(snap_dir)

def printStatus():
  message = f'Loop Index: {tick} Battles lost: {lost} Server disconnect: {disconnect}'
  printd(message)
  if not msg.debug:
    print(message, end='\r')

def applyMaskToImage(mask_path, img_path):
  img = cv2.imread(img_path)
  mask = cv2.imread(mask_path, 0)
  dst = cv2.bitwise_and(img,img,mask=mask)
  return cv2.resize(dst, (0,0), fx=resize_percent, fy=resize_percent)

def checkScreens():
  for sname, screen in screens.items():
    for imagename, image_path in screen.image_path.items():
      try:
        s = cv2.imread(image_path, cv2.IMREAD_COLOR)
        for name, rect in screen.buttons.items():
          pt1 = (rect.left, rect.top)
          pt2 = (rect.left + rect.width, rect.top + rect.height)
          cv2.rectangle(s, pt1, pt2, (0, 0, 255), -1)
          cv2.putText(s, name, (rect.left, rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 3)
          small = cv2.resize(s, (0,0), fx=0.5, fy=0.5)
        cv2.namedWindow(imagename, cv2.WINDOW_NORMAL)
        cv2.imshow(imagename, small)
        cv2.moveWindow(imagename, 0, 0)
        cv2.waitKey(0)
        small = applyMaskToImage(screen.mask_path, image_path)
        cv2.imshow(imagename, small)
        cv2.moveWindow(imagename, 0, 0)
        cv2.waitKey(0)

      except:
        print(f'Could not find: {imagename}')

def compareDisplayScreen(match_image, mask, match_image_alt=None, mask_alt=None, similarity=SSIM_cutoff):
  global screensnap_ind
  matched = False
  matched_alt = False

  screensnap_ind+=1
  if screensnap_ind >= max_snaps:
    screensnap_ind = 0

  t = time.time()
  savepath = os.path.join(snap_dir,f'test{screensnap_ind}.jpg')
  screen_image = ImageGrab.grab()
  screen_image.save(savepath)
  delta_t = time.time() - t
  printd(f'Time to save desktop image: {delta_t}')

  t = time.time()
  s_cv = applyMaskToImage(mask, savepath)
  delta_t = time.time() - t
  printd(f'Time to apply image mask: {delta_t}')

  t = time.time()
  delta = ssim.compare_ssim(s_cv, match_image, multichannel=True)
  delta_t = time.time() - t
  printd(f'Time to compare ssim: {delta_t}')
  printd(f'SSIM - {delta}')

  if delta > similarity:
    printd(f'Match found - {delta}')
    matched = True

  if not match_image_alt is None:
    s_cv = applyMaskToImage(mask_alt, savepath)
    delta_alt = ssim.compare_ssim(s_cv, match_image_alt, multichannel=True)
    printd(delta_alt)

    if delta_alt > similarity:
      printd(f'Match found (alternative)  - {delta_alt}')
      if matched:
        matched_alt = delta_alt > delta
      else:
        matched = True
        matched_alt = True

  return matched, matched_alt


def waitUntilScreenMatch(screen, subscreen='default', screenalt=None, subscreenalt='default'):
  printd(f'Waiting for screen: {screen}')
  matched = False
  matched_alt = False

  mask = screens[screen].mask_path
  t = time.time()
  match_image = applyMaskToImage(mask, screens[screen].image_path[subscreen])
  delta = time.time() - t
  printd(f'Time to apply image mask: {delta}')

  mask_alt = None
  match_image_alt = None
  if not screenalt is None:
    printd(f'Alternative screen match: {screenalt}')
    mask_alt = screens[screenalt].mask_path
    match_image_alt = applyMaskToImage(mask_alt, screens[screenalt].image_path[subscreenalt])

  while not matched:
    t = time.time()
    matched, matched_alt = compareDisplayScreen(
      match_image=match_image,
      mask=mask,
      match_image_alt=match_image_alt,
      mask_alt=mask_alt,
    )
    delta = time.time() - t
    printd(f'Time to compare images: {delta}')
    time.sleep(0.5)

  return matched_alt

def grind():
  # From inventory screen
  screens['InventoryScreen'].buttons['grindButton'].click()
  screens['InventoryScreen'].buttons['grindAllButton'].click()
  screens['GrindAllScreen'].buttons['grindButton'].click()
  screens['NoticeScreen'].buttons['okButton'].click()
  time.sleep(3)
  screens['InventoryScreen'].buttons['selectAllButton'].click()
  screens['InventoryScreen'].buttons['toWorldButton'].click()

def sell():
  # From inventory screen
  screens['InventoryScreen'].buttons['sellButton'].click()
  screens['InventoryScreen'].buttons['grindAllButton'].click()
  screens['GrindAllScreen'].buttons['sellButton'].click()
  screens['NoticeScreen'].buttons['sellButton'].click()
  time.sleep(3)
  screens['InventoryScreen'].buttons['toWorldButton'].click()

def dragonRaid(dragon='fire', level=69, action='g'):
  waitUntilScreenMatch('WorldScreen')
  screens['WorldScreen'].buttons['raidButton'].click()
  waitUntilScreenMatch('RaidScreen')
  screens['RaidScreen'].buttons['dragonraidButton'].click()
  if dragon=='black':
    pyautogui.moveTo(1378, 1427, duration=0)
    pyautogui.dragRel(0, -800, duration=1.5)
  screens['DragonRaidScreen'].buttons[dragon].click()
  screens['DragonLevelScreen'].buttons['gatherRaidersButton'].click()
  for x in range(level, dragons.level[dragon]):
    screens['DragonLevelScreen'].buttons['levelDnButton'].click()
  screens['DragonLevelScreen'].buttons['enterButton'].click()
  waitUntilScreenMatch('DragonRaidReadyScreen')
  screens['DragonRaidReadyScreen'].buttons['autoButton'].click()
  screens['NoticeScreen'].buttons['okButton'].click()
  heroes.raidHeroes.selectHeroes()
  screens['DragonRaidReadyScreen'].buttons['startButton'].click()
  screens['NoticeScreen'].buttons['okButton'].click()

  global disconnect
  server_disconnected = True
  while server_disconnected:
    server_disconnected = waitUntilScreenMatch(
      screen      ='NoticeScreen',
      subscreen   ='RepeatFullInventory',
      screenalt   ='NoticeScreen',
      subscreenalt='Disconnected',
     )
    if server_disconnected:
      screens['NoticeScreen'].buttons['okButton'].click()
      waitUntilScreenMatch('DragonRaidReadyScreen')
      screens['DragonRaidReadyScreen'].buttons['startButton'].click()
      screens['NoticeScreen'].buttons['okButton'].click()
      disconnect+=1
      printStatus()

  # Inventory full
  screens['NoticeScreen'].buttons['okButton'].click()
  screens['BattleFinishScreen'].buttons['exitButton'].click()
  waitUntilScreenMatch('DragonRaidReadyScreen', subscreen='afterBattle')
  screens['DragonRaidReadyScreen'].buttons['toWorldButton'].click()
  if action == 'g':
    screens['WorldScreen'].buttons['inventoryButton'].click()
    grind()
  elif action == 's':
    screens['WorldScreen'].buttons['inventoryButton'].click()
    sell()

def worldBattle(boss=False, action='g'):
  waitUntilScreenMatch('WorldScreen')
  screens['WorldScreen'].buttons['battleButton'].click()
  if boss:
    waitUntilScreenMatch('BattleScreen', subscreen='BattleScreen1')
  else:
    waitUntilScreenMatch('BattleScreen', subscreen='BattleScreen1a')
  screens['BattleScreen'].buttons['readyButton'].click()
  waitUntilScreenMatch('BattleScreen', subscreen='HeroSelect')
  screens['BattleScreen'].buttons['autoRepeatButton'].click()
  screens['NoticeScreen'].buttons['okButton'].click()

  global lost
  battle_lost = True
  while battle_lost:
    battle_lost = waitUntilScreenMatch(
      screen      ='NoticeScreen',
      subscreen   ='RepeatFullInventory',
      screenalt   ='NoticeScreen',
      subscreenalt='RepeatBattleLoss',
     )
    if battle_lost:
      screens['NoticeScreen'].buttons['okButton'].click()
      screens['BattleLossScreen'].buttons['retryButton'].click()
      screens['BattleLossScreen'].buttons['repeatButton'].click()
      screens['NoticeScreen'].buttons['okButton'].click()
      lost+=1
      printStatus()

  # Inventory full
  screens['NoticeScreen'].buttons['okButton'].click()
  screens['NoticeScreen'].buttons['okButton'].click()
  waitUntilScreenMatch('InventoryScreen', subscreen='InventoryScreen')
  if action == 'g':
    grind()
  elif action == 's':
    sell()

def compare():
  file = r"raid.jpg"
  screen = 'RaidScreen'
  subscreen = 'default'

  mask = screens[screen].mask_path
  comp_image = applyMaskToImage(mask, file)
  match_image = applyMaskToImage(mask, screens[screen].image_path[subscreen])

  delta = ssim.compare_ssim(comp_image, match_image, multichannel=True)
  print(delta)

  vis = np.concatenate((comp_image, match_image), axis=0)
  cv2.imshow('stuff', vis)
  cv2.moveWindow('stuff', 0, 0)
  cv2.waitKey(0)

if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Example list of options')
  parser.add_argument('-b', '--battle', help='Specify option:\nwb - battle\nbb - boss battle\ndr - dragon raid')
  parser.add_argument('-d', '--dragon', help='Specify dragon (fire, frost, poison or black)', default='black')
  parser.add_argument('-l', '--level', help='Level of dragon', default=70, type=int)
  parser.add_argument('-a', '--action', help='Specify option:\ng - grind\ns - sell\nn - none', default='n')
  parser.add_argument('--loop',help='Loop N times, 0 for infinite', type=int, default=1)
  parser.add_argument('--check',help='Check screens',action='store_true')
  parser.add_argument('--debug',help='Enable debug logging',action='store_true')
  args = parser.parse_args()

  if args.check:
    checkScreens()

  tick = 0
  if args.loop == 0:
    inf = True
  else:
    inf = False

  msg.debug = args.debug

  printd('Debug on')
  printd(f'Infinite loop: {inf}')

  while inf or tick < args.loop:
    tick+=1
    printStatus()

    if args.battle == 'wb':
      worldBattle(boss=False, action=args.action)
    elif args.battle == 'bb':
      worldBattle(boss=True, action=args.action)
    elif args.battle == 'dr':
      dragonRaid(dragon=args.dragon, level=args.level, action=args.action)
