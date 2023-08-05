import turtle

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class L_SpaceCurves():
    import turtle
    def __init__(self, leng=None, letter='S', iter=1, speed=0, tipe=None, origin=(0, 0)):
        self.len = leng
        self.speed = speed
        self.tipe = tipe
        self.origin = origin
        self.size = leng
        self.x, self.y, self.z = origin[0], origin[1], 0
        self.letter = letter
        self.iter = iter

    def sierspinski_curve(self):
        # Defining letters
        def S(iter=1):
            if iter == 1:
                t.left(45)
                t.forward(self.len)
                t.right(45)
                t.forward(self.len)
                t.right(45)
                t.forward(self.len)
                t.left(45)
            else:
                G1(iter - 1)

        def R(iter=1):
            if iter == 1:
                t.left(135)
                t.forward(self.len)
                t.right(45)
                t.forward(self.len)
                t.right(45)
                t.forward(self.len)
                t.right(45)
            else:
                G2(iter - 1)

        def Z(iter=1):
            if iter == 1:
                t.right(135)
                t.forward(self.len)
                t.right(45)
                t.forward(self.len)
                t.right(45)
                t.forward(self.len)
                t.right(135)
            else:
                G4(iter - 1)

        def P(iter):
            if iter == 1:
                t.right(45)
                t.forward(self.len)
                t.right(45)
                t.forward(self.len)
                t.right(45)
                t.forward(self.len)
                t.left(135)
            else:
                G3(iter - 1)

        # defining constants
        def c():
            # walk up
            t.left(90)
            t.forward(self.len)
            t.right(90)
        def e():
            # walk left
            t.right(180)
            t.forward(self.len)
            t.right(180)
        def d():
            # walk right
            t.forward(self.len)
        def b():
            # walk down
            t.right(90)
            t.forward(self.len)
            t.left(90)
        def Ddc():
            # walk diagonal right up
            t.left(45)
            t.forward(self.len)
            t.right(45)
        def Ddb():
            # walk diagonal right down
            t.right(45)
            t.forward(self.len)
            t.left(45)
        def Dec():
            # walk diaginal left up
            t.left(135)
            t.forward(self.len)
            t.right(135)
        def Deb():
            # walk diaginal left down
            t.right(135)
            t.forward(self.len)
            t.left(135)

        # grammar
        def G1(iter, var="S"):
            # S <-
            S(iter)
            Ddc()
            R(iter)
            d()
            P(iter)
            Ddb()
            S(iter)
        def G2(iter, var="R"):
            # R <-
            R(iter)
            Dec()
            Z(iter)
            c()
            S(iter)
            Ddc()
            R(iter)
        def G3(iter, var="P"):
            P(iter)
            Ddb()
            S(iter)
            b()
            Z(iter)
            Deb()
            P(iter)
        def G4(iter, var="Z"):
            Z(iter)
            Deb()
            P(iter)
            e()
            R(iter)
            Dec()
            Z(iter)

        self.tipe = "2D"  # save the dimension of curve
        t = turtle.Turtle()
        # move the start point
        t.up()
        t.setpos(self.origin)
        t.down()
        # change the turtle speed
        t.speed(self.speed)
        print(self.letter)
        if self.letter == "S":
            print('oi')
            S(self.iter)
        elif self.letter == "R":
            R(self.iter)
        elif self.letter == "Z":
            Z(self.iter)
        elif self.letter == "P":
            P(self.iter)
        else:
            raise "Use the letters definided at Github"
        # to exit the plot need to click at screen
        turtle.exitonclick()

    def hilbert_curve(self):
        import turtle
        t = turtle.Turtle()
        # set the origin point
        t.up()
        t.setpos(self.origin)
        t.down()
        #set the speed of turtle
        t.speed(self.speed)

        # Definig letters
        def H(iter):
            if iter == 1:
                t.left(90)
                t.forward(self.len)
                t.right(90)
                t.forward(self.len)
                t.right(90)
                t.forward(self.len)
                t.left(90)
            else:
                G1(iter - 1)
        def A(iter):
            if iter == 1:
                t.forward(self.len)
                t.left(90)
                t.forward(self.len)
                t.left(90)
                t.forward(self.len)
                t.right(180)
            else:
                G2(iter - 1)
        def B(iter):
            if iter == 1:
                t.left(180)
                t.forward(self.len)
                t.left(90)
                t.forward(self.len)
                t.left(90)
                t.forward(self.len)
            else:
                G3(iter - 1)
        def C(iter):
            if iter == 1:
                t.right(90)
                t.forward(self.len)
                t.right(90)
                t.forward(self.len)
                t.right(90)
                t.forward(self.len)
                t.right(90)
            else:
                G4(iter - 1)

        # Definig constants
        def d():
            "Walk right"
            t.forward(self.len)
        def e():
            "Walk left"
            t.right(180)
            t.forward(self.len)
            t.left(180)
        def c():
            "walk up"
            t.left(90)
            t.forward(self.len)
            t.right(90)
        def b():
            "walk down"
            t.right(90)
            t.forward(self.len)
            t.left(90)

        # Grammar
        def G1(iter, var="H"):
            A(iter)
            c()
            H(iter)
            d()
            H(iter)
            b()
            B(iter)
        def G2(iter, var="A"):
            H(iter)
            d()
            A(iter)
            c()
            A(iter)
            e()
            C(iter)
        def G3(iter, var="B"):
            C(iter)
            e()
            B(iter)
            b()
            B(iter)
            d()
            H(iter)
        def G4(iter, var='C'):
            B(iter)
            b()
            C(iter)
            e()
            C(iter)
            c()
            A(iter)

        if self.letter == "S" or self.letter == "H":
            H(self.iter)
        elif self.letter == "A":
            A(self.iter)
        elif self.letter == "B":
            B(self.iter)
        elif self.iter == "C":
            C(self.iter)
        else:
            raise "Use the letters definided at Github"
        turtle.exitonclick()

    def peano_curve(self):
        import turtle
        t = turtle.Turtle()
        t.speed(self.speed)
        # set the start point
        t.up()
        t.setpos(self.origin)
        t.down()

        # Definig letters
        def P(iter):
            if iter == 1:
                t.left(90)
                t.forward(self.len)
                t.right(90)
                t.forward(self.len)
                t.right(90)
                t.forward(self.len)
                t.left(90)
                t.forward(self.len)
                t.left(90)
                t.forward(self.len)
                t.right(90)
            else:
                G1(iter - 1)
        def Q(iter):
            if iter == 1:
                t.left(90)
                t.forward(self.len)
                t.left(90)
                t.forward(self.len)
                t.left(90)
                t.forward(self.len)
                t.right(90)
                t.forward(self.len)
                t.right(90)
                t.forward(self.len)
                t.right(90)
            else:
                G2(iter - 1)
        def R(iter):
            if iter == 1:
                t.right(90)
                t.forward(self.len)
                t.right(90)
                t.forward(self.len)
                t.right(90)
                t.forward(self.len)
                t.left(90)
                t.forward(self.len)
                t.left(90)
                t.forward(self.len)
                t.left(90)
            else:
                G3(iter - 1)
        def S(iter):
            if iter == 1:
                t.right(90)
                t.forward(self.len)
                t.left(90)
                t.forward(self.len)
                t.left(90)
                t.forward(self.len)
                t.right(90)
                t.forward(self.len)
                t.right(90)
                t.forward(self.len)
                t.left(90)
            else:
                G4(iter - 1)

        # defining constants
        def c():
            "Walk up"
            t.left(90)
            t.forward(self.len)
            t.right(90)
        def b():
            "Walk down"
            t.right(90)
            t.forward(self.len)
            t.left(90)
        def d():
            "Walk right"
            t.forward(self.len)
        def e():
            "Walk left"
            t.right(180)
            t.forward(self.len)
            t.right(180)

        # Grammar
        def G1(iter, var="P"):
            P(iter)
            c()
            Q(iter)
            c()
            P(iter)
            d()
            S(iter)
            b()
            R(iter)
            b()
            S(iter)
            d()
            P(iter)
            c()
            Q(iter)
            c()
            P(iter)
        def G2(iter, var="Q"):
            Q(iter)
            c()
            P(iter)
            c()
            Q(iter)
            e()
            R(iter)
            b()
            S(iter)
            b()
            R(iter)
            e()
            Q(iter)
            c()
            P(iter)
            c()
            Q(iter)
        def G3(iter, var="Q"):
            R(iter)
            b()
            S(iter)
            b()
            R(iter)
            e()
            Q(iter)
            c()
            P(iter)
            c()
            Q(iter)
            e()
            R(iter)
            b()
            S(iter)
            b()
            R(iter)
        def G4(iter, var="Q"):
            S(iter)
            b()
            R(iter)
            b()
            S(iter)
            d()
            P(iter)
            c()
            Q(iter)
            c()
            P(iter)
            d()
            S(iter)
            b()
            R(iter)
            b()
            S(iter)

        if self.letter == "S" or self.letter == "P":
            P(self.iter)
        elif self.letter == "Q":
            Q(self.iter)
        elif self.letter == "R":
            R(self.iter)
        elif self.letter == "S":
            S(self.iter)
        else:
            raise "Use the letters definided at Github"

        turtle.exitonclick()

    def gosper_Flowsnake_curve(self):
        import turtle
        t = turtle.Turtle()
        t.speed(self.speed)
        t.up()
        t.setpos(self.origin)
        t.down()

        # Definig letters
        def G(iter):
            if iter == 1:
                t.forward(self.len)
                t.left(120)
                t.forward(self.len)
                t.left(60)
                t.forward(self.len)
                t.right(150)
                t.forward(self.len)
                t.right(30)
                t.forward(self.len)
                t.right(60)
                t.forward(self.len)
            else:
                G1(iter - 1)
        def R(iter):
            if iter == 1:
                t.forward(self.len)
                t.left(60)
                t.forward(self.len)
                t.left(60)
                t.forward(self.len)
                t.left(120)
                t.forward(self.len)
                t.right(60)
                t.forward(self.len)
                t.right(120)
                t.forward(self.len)
            else:
                G2(iter - 1)

        # definig constants
        def c():
            # walk forward
            t.forward(self.len)
        def l():
            # turn left 60º
            t.left(60)
        def r():
            # turn right 60º
            t.right(60)

        # Grammar
        def G1(iter):
            G(iter)
            l()
            c()
            R(iter)
            l()
            c()
            R(iter)
            c()
            r()
            G(iter)
            c()
            r()
            G(iter)
            l()
            c()
            G(iter)
            c()
            r()
            R(iter)
        def G2(iter):
            G(iter)
            l()
            c()
            R(iter)
            c()
            r()
            R(iter)
            l()
            c()
            R(iter)
            l()
            c()
            G(iter)
            c()
            r()
            G(iter)
            c()
            r()
            R(iter)

        if self.letter == "G" or self.letter == "S":
            G(self.iter)
        elif self.iter == "R":
            R(self.iter)
        else:
            raise "Use the letters definided at Github"
        turtle.exitonclick()

    def dragon(self, level=4, size=200, direction=45):
        from turtle import right, left, forward, exitonclick
        if not level:
            forward(size)
        else:
            right(direction)
            self.dragon(level - 1, size / 1.41421356237, 45)
            left(direction * 2)
            self.dragon(level - 1, size / 1.41421356237, -45)
            right(direction)
        exitonclick()

    def pablo_curve(self):
        import turtle
        from turtle import exitonclick
        t = turtle.Turtle()
        t.speed(self.speed)
        t.up()
        t.setpos(self.origin)
        t.down()

        # definig letters
        def A(iter):
            if iter == 1:
                t.right(90)
                t.forward(self.len)
                t.left(90)
            else:
                G1(iter - 1)
        def B(iter):
            if iter == 1:
                t.forward(self.len)
            else:
                G2(iter - 1)
        def C(iter):
            if iter == 1:
                t.right(180)
                t.forward(self.len)
                t.right(180)
            else:
                G3(iter - 1)
        def D(iter):
            if iter == 1:
                t.left(90)
                t.forward(self.len)
                t.right(90)
            else:
                G4(iter - 1)

        # defining grammar
        def G1(iter):
            B(iter)
            A(iter)
            C(iter)
            D(iter)
            A(iter)

            C(iter)
            A(iter)
            B(iter)
            D(iter)
            A(iter)

            B(iter)
            A(iter)
            C(iter)
            D(iter)
            A(iter)
        def G2(iter):
            D(iter)
            B(iter)
            A(iter)
            C(iter)
            B(iter)

            A(iter)
            B(iter)
            D(iter)
            C(iter)
            B(iter)

            B(iter)
            D(iter)
            C(iter)
            A(iter)
            B(iter)
        def G3(iter):
            D(iter)
            C(iter)
            A(iter)
            B(iter)
            C(iter)

            A(iter)
            C(iter)
            D(iter)
            B(iter)
            C(iter)

            D(iter)
            C(iter)
            A(iter)
            B(iter)
            C(iter)
        def G4(iter):
            C(iter)
            D(iter)
            B(iter)
            A(iter)
            D(iter)

            B(iter)
            D(iter)
            C(iter)
            A(iter)
            D(iter)

            C(iter)
            D(iter)
            B(iter)
            A(iter)
            D(iter)

        if self.letter == "S" or self.letter == "A":
            A(self.iter)
        elif self.letter == "B":
            B(self.iter)
        elif self.letter == "C":
            C(self.iter)
        elif self.letter == "D":
            D(self.iter)
        else:
            raise "Use the letters definided at Github"
        exitonclick()

    def hilbert_3D(self):
        """this class will build the hilbert curve in Blender
        """
        import numpy as np
        if len(self.origin)<3:
            raise "Set a origin in a tuple with three components"

        self.x, self.y, self.z = np.array([self.x]), np.array([self.y]), np.array([self.z])
        self.len = len(self.x)

        # defining letters
        def A(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
            else:
                G1(iter - 1)
        def B(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
            else:
                G2(iter - 1)
        def C(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
            else:
                G3(iter - 1)
        def D(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
            else:
                G4(iter - 1)
        def E(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z,
                    self.z[
                        -1])
            else:
                G5(iter)
        def F(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z,
                    self.z[
                        -1])
            else:
                G6(iter - 1)
        def G(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.size + self.x[-1]), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
            else:
                G7(iter - 1)
        def H(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
            else:
                G8(iter - 1)
        def I(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                             self.y[-1]), np.append(
                    self.z, self.z[-1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
            else:
                G9(iter - 1)
        def J(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
            else:
                G10(iter - 1)
        def K(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z,
                    self.z[
                        -1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z,
                    self.z[
                        -1])
            else:
                G11(iter - 1)
        def L(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z, self.z[-1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] - self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z, self.z[-1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                              self.y[-1]), np.append(
                    self.z, self.z[-1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] + self.size), np.append(
                    self.z, self.z[-1])
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1] + self.size)
                self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                                  self.y[-1] - self.size), np.append(
                    self.z, self.z[-1])
            else:
                G12(iter - 1)

        # Definig constants
        def c():
            "Walk up"
            self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(
                self.z, self.z[-1] + self.size)
        def b():
            "Walk down"
            self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(
                self.z, self.z[-1] - self.size)
        def e():
            "Walk left"
            self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                          self.y[-1]), np.append(
                self.z,
                self.z[-1])
        def d():
            "Walk right"
            self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                          self.y[-1]), np.append(
                self.z,
                self.z[-1])
        def f():
            "Walk forward"
            self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                              self.y[-1] + self.size), np.append(
                self.z,
                self.z[
                    -1])
        def back():
            "Walk backward"
            self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                              self.y[-1] - self.size), np.append(
                self.z,
                self.z[
                    -1])

        # Defining grammar
        def G1(iter):
            A(iter)
            back()
            E(iter)
            d()
            E(iter)
            f()
            H(iter)
            c()
            H(iter)
            back()
            K(iter)
            e()
            K(iter)
            f()
            D(iter)
        def G2(iter):
            D(iter)
            f()
            F(iter)
            d()
            F(iter)
            back()
            G(iter)
            b()
            G(iter)
            f()
            L(iter)
            e()
            L(iter)
            b()
            C(iter)
        def G3(iter):
            E(iter)
            d()
            A(iter)
            c()
            A(iter)
            e()
            I(iter)
            back()
            I(iter)
            d()
            B(iter)
            b()
            B(iter)
            e()
            L(iter)
        def G4(iter):
            F(iter)
            d()
            B(iter)
            b()
            B(iter)
            e()
            J(iter)
            f()
            J(iter)
            d()
            A(iter)
            c()
            A(iter)
            e()
            K(iter)
        def G5(iter):
            A(iter)
            c()
            C(iter)
            back()
            C(iter)
            b()
            F(iter)
            d()
            F(iter)
            c()
            J(iter)
            f()
            J(iter)
            b()
            G(iter)
        def G6(iter):
            B(iter)
            b()
            D(iter)
            f()
            D(iter)
            f()
            E(iter)
            d()
            E(iter)
            b()
            I(iter)
            back()
            I(iter)
            c()
            H(iter)
        def G7(iter):
            I(iter)
            back()
            K(iter)
            e()
            K(iter)
            f()
            B(iter)
            b()
            B(iter)
            back()
            E(iter)
            d()
            E(iter)
            f()
            J(iter)
        def G8(iter):
            J(iter)
            f()
            L(iter)
            e()
            L(iter)
            back()
            A(iter)
            c()
            A(iter)
            f()
            F(iter)
            d()
            F(iter)
            back()
            I(iter)
        def G9(iter):
            K(iter)
            e()
            G(iter)
            b()
            G(iter)
            d()
            C(iter)
            back()
            C(iter)
            e()
            H(iter)
            c()
            H(iter)
            d()
            F(iter)
        def G10(iter):
            L(iter)
            e()
            H(iter)
            c()
            H(iter)
            d()
            D(iter)
            f()
            D(iter)
            e()
            G(iter)
            b()
            G(iter)
            d()
            E(iter)
        def G11(iter):
            G(iter)
            b()
            I(iter)
            back()
            I(iter)
            c()
            L(iter)
            e()
            L(iter)
            b()
            D(iter)
            f()
            D(iter)
            c()
            A(iter)
        def G12(iter):
            H(iter)
            c()
            J(iter)
            f()
            b()
            K(iter)
            e()
            K(iter)
            c()
            C(iter)
            back()
            C(iter)
            b()
            B(iter)

        if self.letter == "S" or self.letter == "A":
            A(self.iter)
        elif self.letter == "B":
            B(self.iter)
        elif self.letter == "C":
            C(self.iter)
        elif self.letter == "D":
            D(self.iter)
        elif self.letter == "E":
            E(self.iter)
        elif self.letter == "F":
            F(self.iter)
        elif self.letter == "G":
            G(self.iter)
        elif self.letter == 'H':
            H(self.iter)
        elif self.letter == "I":
            I(self.iter)
        elif self.letter == "J":
            J(self.iter)
        elif self.letter == "K":
            K(self.iter)
        elif self.letter == "L":
            L(self.iter)

        self.tipe = "3D"

    def peano_3D(self):
        """this class will build the hilbert curve in Blender
        """
        import numpy as np

        self.x, self.y, self.z = np.array([self.x]), np.array([self.y]), np.array([self.z])
        self.len = len(self.x)

        # Definig letters
        def P(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y, self.y[
                    -1] + self.size), np.append(self.z, self.z[-1] + self.size)
            else:
                G1(iter - 1)
        def R( iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y, self.y[
                    -1] - self.size), np.append(self.z, self.z[-1] - self.size)
            else:
                G2(iter - 1)
        def Q(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y, self.y[
                    -1] - self.size), np.append(self.z, self.z[-1] + self.size)
            else:
                G3(iter - 1)
        def S(iter):
            if iter == 1:
                self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y, self.y[
                    -1] + self.size), np.append(self.z, self.z[-1] - self.size)
            else:
                G4(iter - 1)

        def py(iter, var="P"):
            P(iter)
            back()
            R(iter)
            back()
            P(iter)
        def ry(iter, var="R"):
            R(iter)
            f()
            P(iter)
            f()
            R(iter)
        def qy(iter, var="Q"):
            Q(iter)
            f()
            S(iter)
            f()
            Q(iter)
        def sy(iter, var="S"):
            S(iter)
            back()
            Q(iter)
            back()
            S(iter)
        def pyz(iter):
            py(iter)
            c()
            qy(iter)
            c()
            py(iter)
        def ryz(iter):
            ry(iter)
            b()
            qy(iter)
            b()
            ry(iter)
        def qyz(iter):
            qy(iter)
            c()
            ry(iter)
            c()
            qy(iter)
        def syz(iter):
            sy(iter)
            b()
            py(iter)
            b()
            sy(iter)

        # Defining constants
        def c():
            self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(
                self.z, self.z[-1] + self.size)
        def b():
            self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y, self.y[-1]), np.append(
                self.z, self.z[-1] - self.size)
        def e():
            self.x, self.y, self.z = np.append(self.x, self.x[-1] - self.size), np.append(self.y,
                                                                                          self.y[-1]), np.append(
                self.z,
                self.z[-1])
        def d():
            self.x, self.y, self.z = np.append(self.x, self.x[-1] + self.size), np.append(self.y,
                                                                                          self.y[-1]), np.append(
                self.z,
                self.z[-1])
        def f():
            self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                              self.y[-1] + self.size), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1])
        def back():
            self.x, self.y, self.z = np.append(self.x, self.x[-1]), np.append(self.y,
                                                                              self.y[-1] - self.size), np.append(self.z,
                                                                                                                 self.z[
                                                                                                                     -1])

        # Gramatics
        def G1(iter):
            pyz(iter)
            d()
            ryz(iter)
            d()
            pyz(iter)
        def G2(iter):
            qyz(iter)
            e()
            syz(iter)
            e()
            qyz(iter)
        def G3(iter):
            ryz(iter)
            d()
            pyz(iter)
            d()
            ryz(iter)
        def G4(iter):
            syz(iter)
            e()
            qyz(iter)
            e()
            syz(iter)

        if self.letter == "S" or self.letter == "P":
            P(self.iter)
        elif self.letter == "R":
            R(self.letter)
        elif self.letter == "Q":
            Q(self.letter)
        elif self.letter == "S":
            S(self.letter)
        self.tipe = "3D" # change the curve type to 3D

    def plot(self):
        if self.tipe != "3D":
            raise "The function plot works only with 3D plots, to plot 2D don't need this function"
        fig = plt.figure(figsize=(10, 10))
        ax = fig.gca(projection="3d")
        ax.plot(self.x, self.y, self.z)
        plt.show()

