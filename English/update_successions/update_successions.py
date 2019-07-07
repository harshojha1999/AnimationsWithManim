from big_ol_pile_of_manim_imports import *

class AddUpdaterFail(Scene):
	def construct(self):
		dot = Dot()
		text = TextMobject("Label")\
		       .next_to(dot,RIGHT,buff=SMALL_BUFF)

		self.add(dot,text)

		self.play(dot.shift,UP*2)
		self.wait()

class AddUpdater1(Scene):
	def construct(self):
		dot = Dot()
		text = TextMobject("Label")\
		       .next_to(dot,RIGHT,buff=SMALL_BUFF)

		self.add(dot,text)

		# Update function
		def update_text(object):
			text.next_to(dot,RIGHT,buff=SMALL_BUFF)

		# Add update function to the objects
		text.add_updater(update_text)

		# Add the object again
		self.add(text)

		self.play(dot.shift,UP*2)

		# Remove update function
		text.remove_updater(update_text)

		self.wait()

class AddUpdater2(Scene):
	def construct(self):
		dot = Dot()
		text = TextMobject("Label")\
		       .next_to(dot,RIGHT,buff=SMALL_BUFF)

		self.add(dot,text)

		# Add update function to the objects
		text.add_updater(lambda m: m.next_to(dot,RIGHT,buff=SMALL_BUFF))

		# Add the object again
		self.add(text)

		self.play(dot.shift,UP*2)

		# Remove update function
		text.clear_updaters()

		self.wait()

class AddUpdater3(Scene):
	def construct(self):
		dot = Dot()
		text = TextMobject("Label")\
		       .next_to(dot,RIGHT,buff=SMALL_BUFF)

		self.add(dot,text)

		def update_text(text):
			text.next_to(dot,RIGHT,buff=SMALL_BUFF)

		# Only works in play
		self.play(
				dot.shift,UP*2,
				UpdateFromFunc(text,update_text)
			)

		self.wait()

class UpdateNumber(Scene):
	def construct(self):
		number_line = NumberLine(x_min=-1,x_max=1)
		triangle = RegularPolygon(3,start_angle=-PI/2)\
		           .scale(0.2)\
		           .next_to(number_line.get_left(),UP,buff=SMALL_BUFF)
		decimal = DecimalNumber(
				0,
				num_decimal_places=3,
				include_sign=True,
				unit="\\rm cm", # Change this with None
			)

		decimal.add_updater(lambda d: d.next_to(triangle, UP*0.1))
		decimal.add_updater(lambda d: d.set_value(triangle.get_center()[0]))

		self.add(number_line,triangle,decimal)

		self.play(
				triangle.shift,RIGHT*2,
				rate_func=there_and_back, # Change this with: linear,smooth
				run_time=5
			)

		self.wait()

class UpdateValueTracker1(Scene):
	def construct(self):
		theta = ValueTracker(PI/2)
		line_1= Line(ORIGIN,RIGHT*3,color=RED)
		line_2= Line(ORIGIN,RIGHT*3,color=GREEN)

		line_2.rotate(theta.get_value(),about_point=ORIGIN)
		line_2.add_updater(
				lambda m: m.set_angle(
									theta.get_value()
								)
			)

		self.add(line_1,line_2)

		self.play(theta.increment_value,PI/2)

		self.wait()

class UpdateValueTracker2(Scene):
	CONFIG={
		"line_1_color":ORANGE,
		"line_2_color":PINK,
		"lines_size":3.5,
		"theta":PI/2,
		"increment_theta":PI/2,
		"final_theta":PI,
		"radius":0.7,
		"radius_color":YELLOW,
	}
	def construct(self):
		theta = ValueTracker(self.theta)
		line_1= Line(ORIGIN,RIGHT*self.lines_size,color=self.line_1_color)
		line_2= Line(ORIGIN,RIGHT*self.lines_size,color=self.line_2_color)

		line_2.rotate(theta.get_value(),about_point=ORIGIN)
		line_2.add_updater(
				lambda m: m.set_angle(
									theta.get_value()
								)
			)

		angle= Arc(
					#radius=self.radius,
					#start_angle=line_1.get_angle(),
					angle =line_2.get_angle(),
					#color=self.radius_color,
			)

		angle.add_updater(
					lambda m: m.become(
							Arc(
								radius=self.radius,
								start_angle=line_1.get_angle(),
								angle =line_2.get_angle(),
								color=self.radius_color
							)
						)
			)

		self.add(line_1,line_2,angle)

		self.play(theta.increment_value,self.increment_theta)
		# self.play(theta.set_value,self.final_theta)

		self.wait()

class UpdateFunctionWithAlphaFail(Scene):
    CONFIG={
    "amp":2.3,
    "t_offset":0,
    "rate":0.1,
    "x_min":TAU/2,
    "x_max":TAU,
    "wait_time":15,
    }
 
    def construct(self):
        def update_curve(c, dt):
            other_mob = FunctionGraph(
                lambda x: self.amp*np.sin((x - (self.t_offset + self.rate))),
                    x_min=0,x_max=self.x_max
                ).shift(LEFT*self.x_min)
            c.become(other_mob)
            self.t_offset += self.rate

       
        c = FunctionGraph(
            lambda x: self.amp*np.sin((x)),
            x_min=0,x_max=self.x_max
            ).shift(LEFT*self.x_min)

        self.play(ShowCreation(c))

        c.add_updater(update_curve)
        self.add(c)

        self.wait(3)
        
        c.remove_updater(update_curve)
 
        self.wait()

class UpdateFunctionWithAlpha(Scene):
    CONFIG={
    "amp":2.3,
    "t_offset":0,
    "rate":TAU/4,
    "x_min":TAU/2,
    "x_max":TAU,
    "wait_time":15,
    }
 
    def construct(self):
        frame_rate = self.camera.frame_rate
        rate_per_second=1/frame_rate
        real_rate=self.rate*rate_per_second
        def update_curve(c, dt):
            other_mob = FunctionGraph(
                lambda x: self.amp*np.sin((x - (self.t_offset + real_rate)+real_rate*2)),
                    x_min=0,x_max=self.x_max
                ).shift(LEFT*self.x_min)
            c.become(other_mob)
            self.t_offset += real_rate

       
        c = FunctionGraph(
            lambda x: self.amp*np.sin((x)),
            x_min=0,x_max=self.x_max
            ).shift(LEFT*self.x_min)

        self.play(ShowCreation(c))

        print("coord_x_in:",c.points[0][1])

        c.add_updater(update_curve)
        self.add(c)

        self.wait(12)
        
        print("coord_x_fin:",c.points[0][1])
        c.remove_updater(update_curve)
 
        self.wait()

class RatePerSecond(Scene):
	def construct(self):
		frame_rate = self.camera.frame_rate
		rate_per_second=1/frame_rate
		number_line = NumberLine(x_min=-1,x_max=1)
		triangle = RegularPolygon(3,start_angle=-PI/2)\
		           .scale(0.2)\
		           .next_to(number_line.get_left(),UP,buff=SMALL_BUFF)
		def update_t(triangle,dt):
			triangle.shift(RIGHT*rate_per_second)

		self.add(number_line,triangle)

		self.wait(0.3)
		triangle.shift(LEFT*rate_per_second*2)
		triangle.add_updater(update_t)

		self.wait(2)

		triangle.clear_updaters()
		self.wait()

class UpdateCurve(Scene):
    def construct(self):
        a=1
        c = FunctionGraph(lambda x: 2*np.exp(-2*(x-a*1)**2))
        axes=Axes(y_min=-3,y_max=3)
 
        def update_curve(c, alpha):
            dt=interpolate(1,4,alpha)
            c_c = FunctionGraph(lambda x: 2*np.exp(-2*(x-a*dt)**2))
            c.become(c_c)
 
        self.play(ShowCreation(axes),ShowCreation(c))
        self.wait()
        self.play(UpdateFromAlphaFunc(c,update_curve),rate_func=there_and_back,run_time=4)
        self.wait()
        
class SuccessionExample1Fail(Scene):
	def construct(self):
		number_line=NumberLine(x_min=-2,x_max=2)
		text=TextMobject("Text")\
			 .next_to(number_line,DOWN)
		dashed_line=DashedLine(
								number_line.get_left(),
								number_line.get_right(),
								color=YELLOW,
							  ).set_stroke(width=11)

		self.add(number_line)
		self.wait(0.3)
		self.play(
				ShowCreationThenDestruction(
								dashed_line,
								submobject_mode="lagged_start"
											),
				run_time=5
			)
		self.play(Write(text))

		self.wait()

class SuccessionExample1(Scene):
	def construct(self):
		number_line=NumberLine(x_min=-2,x_max=2)
		text=TextMobject("Text")\
			 .next_to(number_line,DOWN)
		dashed_line=DashedLine(
								number_line.get_left(),
								number_line.get_right(),
								color=YELLOW,
							  ).set_stroke(width=11)

		self.add(number_line)
		self.wait(0.3)
		
		self.play(
                    ShowCreationThenDestruction(dashed_line,submobject_mode="lagged_start",run_time=5),
                    Succession(Animation, Mobject(), {"run_time" : 2.1},
                    Write,text)
			)

		self.wait()

class SuccessionExample2(Scene):
	def construct(self):
		number_line=NumberLine(x_min=-2,x_max=2)
		text_1=TextMobject("Theorem of")\
			 .next_to(number_line,DOWN)
		text_2=TextMobject("Beethoven")\
			 .next_to(number_line,DOWN)
		dashed_line=DashedLine(
								number_line.get_left(),
								number_line.get_right(),
								color=YELLOW,
							  ).set_stroke(width=11)

		self.add(number_line)
		
		self.play(
					ShowCreationThenDestruction(dashed_line,submobject_mode="lagged_start",run_time=5),
                    Succession(Animation,text_1, {"run_time" : 2},
                    ReplacementTransform,text_1,text_2),
			)

		self.wait()