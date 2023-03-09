#!/usr/bin/env python
import pygame

import sys
from Box2D.b2 import *

import egs

engine = egs.Engine("Mario 1-1")

scene = egs.Scene("Scene 1")

engine.start_game()
