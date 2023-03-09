#!/usr/bin/env python
import pygame

import sys
from Box2D import *
import sprites

import egs

engine = egs.Engine("Mario 1-1")

scene = egs.Scene("Scene 1")

ground = sprites.Ground(2000, 35)
mario = sprites.SuperMario()
scene.add(ground)
scene.add(mario)

engine.start_game()
