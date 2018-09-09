import numpy as np
import pyautogui
from screens import screens

hero_list = [
  'Frey',
  'Epis',
  'Maria',
  'Demia',
  'Morrah',
  'Nyx',
  'Tanya',
  'Priscilla',
  'Yanne',
  'Miruru',
  'Shea',
  'Selena',
  'Rodina',
  'Aisha',
  'Lewisa',
  'Annette',
  'Mediana',
  'Mitra',
  'Kasel',
  'Cleo',
  'Roi',
  'Clause',
  'Reina',
  'Sonia',
  'Artemia',
  'Rephy',
  'Gau',
]

hero_activate = ['Frey','Maria','Morrah','Yanne']

raid_x        =  562
raid_y        =  1451
raid_ydrag    = -280
raid_dragtime = 1.5

#           x
# __|_____________
#   |   1   2   3
#   | 1|.   .   .
# y | 2|.   .   .
#   | 3|-   -   -
#   | ...
class Hero:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.isActive=False
    if y == 0:
      if x == 0:
        self.button = 'CH1Button'
      elif x == 1:
        self.button = 'CH2Button'
      else:
        self.button = 'CH3Button'
    else:
      if x == 0:
        self.button = 'CH4Button'
      elif x == 1:
        self.button = 'CH5Button'
      else:
        self.button = 'CH6Button'

  def activate(self):
    self.isActive=True


class HeroList:
  def __init__(self):
    self.heroes = {}
    self.grid = {}
    self.executor = None
    self.lastActiveRow = -1

    #add heroes
    x = 0
    y = 0
    for i in range(len(hero_list)):
      hero_name = hero_list[i]
      if x == 3:
        x=0
        y+=1
      self.heroes[hero_name] = Hero(x=x,y=y)
      x+=1

    #hero grid
    self.grid = np.empty(shape=(y+1, 3), dtype=object)
    for hero in self.heroes:
      self.grid[self.heroes[hero].y][self.heroes[hero].x] = hero


  def activateHeroes(self, heroes:list):
    for hero in heroes:
      self.heroes[hero].activate()
      self.lastActiveRow = max(self.heroes[hero].y, self.lastActiveRow)
    self.setExecutor()

  def setExecutor(self):
    self.executor = np.empty(shape=(self.lastActiveRow+1, 3), dtype=object)
    for hero in self.heroes:
      if self.heroes[hero].isActive:
        self.executor[self.heroes[hero].y][self.heroes[hero].x] = self.heroes[hero].button

  def selectHeroes(self=False):
    row = 0
    for y in self.executor:
      if row >= 2:
        pyautogui.moveTo(raid_x, raid_y, duration=0)
        pyautogui.dragRel(0, raid_ydrag, duration=raid_dragtime)
      for x in y:
        if not x is None:
          screens['DragonRaidReadyScreen'].buttons[x].click()
      row+=1

  def dump(self):
    print('Hero grid:')
    print(self.grid)
    print('\nExecutor grid:')
    print(self.executor)


raidHeroes = HeroList()
raidHeroes.activateHeroes(hero_activate)
