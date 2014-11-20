# -*- coding: utf-8 -*-
import spyral
import spyral.debug
import pygame
import math
import random

import objetos

splash_done = False

class Intro(spyral.View):
    def __init__(self, scene):
        spyral.View.__init__(self, scene)

        self.background = spyral.Image(size=self.size).fill((0,0,0))
        self.layers = ["fondo", "frente"]

        # Este es el fondo móvil.
        self.mapa = Fondo(self)

        self.personaje = Bahiya(self)

        spyral.event.register("director.update", self.chequea)

    def chequea(self):
        self.scale = self.mapa.scale_view

class Fondo(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(filename="images/ancientindia.jpg")
        self.image.scale = 3
        self.layer = "fondo"
        
        # Sappura
        #self.pos = -400, -1000
        #self.scale = 3

        self.avanzando = False

        spyral.event.register ("director.scene.enter", self.zoomin)

    def avanzo(self):
        if not self.avanzando:
            objetivo = (-1766, -95)
            animacion = spyral.Animation("pos", spyral.easing.LinearTuple(self.pos, objetivo), duration=30)
            self.animate(animacion)
            self.avanzando = True

    def zoomin(self):
        if not self.avanzando:
            animacion = spyral.Animation("scale_view", spyral.easing.Linear(1, 3), duration=30)
            self.animate(animacion)
            self.avanzando = True

    def reset(self):
        self.avanzando = False
        if self.lugar == 2:
            self.x = self.scene.width
        elif self.lugar == 1:
            self.x = 0
        self.avanzo()


class Bahiya(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(filename="images/brahmin.png")
        self.pos = (600, 150)
        self.scale = 0.3


class Mostro(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        #self.image = spyral.Image(size=(50,50)).fill((255,0,0))
        self.image = spyral.Image(filename="images/ninjastar_dave_pena_01.png")
        self.layer = "frente"
        self.ouch = pygame.mixer.Sound('sounds/confusion.ogg')

        self.pos = (scene.width, random.randint(60, scene.height - self.height))

        spyral.event.register ("director.update", self.chequea)
        spyral.event.register("Comodo.muere", self.fin)

    def mover(self):
        traslacion = spyral.Animation("x", spyral.easing.Linear(self.x, 0 - self.width), duration=5)
        self.animate(traslacion)
        #rotacion = spyral.Animation("angle", spyral.easing.Linear(2*math.pi,0), duration=1, loop=True)
        #self.animate(rotacion)

    def fin(self):
        self.stop_all_animations()

    def desaparecer(self):
        spyral.event.unregister("director.update", self.chequea)
        self.kill()
        del(self)

    def chequea(self):
        if self.collide_sprite(self.scene.comodo):
            spyral.event.unregister("director.update", self.chequea)
            self.desaparecer()
            self.ouch.play()
            self.scene.comodo.vida -= 5 
        if self.x==0 - self.width:
            self.desaparecer()


class Premio(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        #self.image = spyral.Image(size=(50,50)).fill((0,0,255))
        self.image = spyral.Image(filename="images/love-shield.png")
        self.layer = "frente"

        self.yay = pygame.mixer.Sound('sounds/heal.ogg')

        self.pos = (scene.width, random.randint(60, scene.height - self.height))

        self.estado = "normal"

        spyral.event.register ("director.update", self.chequea)
        #spyral.event.register ("Premio.pos.animation.end", self.desaparecer)
        spyral.event.register("Comodo.muere", self.fin)

    def mover(self):
        animacion = spyral.Animation("x", spyral.easing.Linear(self.x, 0 - self.width), duration=5)
        self.animate(animacion)

    def fin(self):
        self.stop_all_animations()

    def desaparecer(self):
        self.kill()
        del(self)

    def ascender(self):
        animacion = spyral.Animation("pos", spyral.easing.LinearTuple(self.pos, (-1*self.width, 0)), duration=1)
        self.animate(animacion)

    def chequea(self):
        if self.collide_sprite(self.scene.comodo):
            spyral.event.unregister("director.update", self.chequea)
            self.ascender()
            self.yay.play()
            if self.scene.comodo.vida <= 95:
                self.scene.comodo.vida += 5 
        if self.x==0 - self.width:
            self.desaparecer()


class Juego(spyral.Scene):
    def __init__(self, activity=None, SIZE=None, *args, **kwargs):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=self.size).fill((0,0,0))

        self.vista = Intro(self)

        # Define la función "chequea" para determinar el estado del juego
        # spyral.event.register("director.update", self.chequea)

        # Esto es para poder salir correctamente del juego
        spyral.event.register("system.quit", spyral.director.pop)

        # Este código es para salir de la imagen de inicio del juego
        if activity:
            activity.game_button.set_active(True)
            activity.box.next_page()
            activity._pygamecanvas.grab_focus()
            activity.window.set_cursor(None)
            self.activity = activity

    def chequea(self, delta):
        # Aquí creamos los objetos que van apareciendo
        pass
