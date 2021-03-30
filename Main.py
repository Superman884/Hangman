from random import randrange
import pygame
from time import sleep
import string
import keyboard
def make_circles(arr):
	circles=[letter(300,20,28,15,'hint',False,(255,255,255))]
	x=50
	y=500
	for i in range(len(arr)):
		circles.append(letter(x,y,15,15,arr[i]))
		x+=50
		if x>=510:
			x=50
			y+=50
		if i==len(arr)//10*10-1:
			x=(10-len(arr)%10)//2*50+50
	return circles
def makescreen(bg,arr,dots,showy,word,health,images):
	win.fill(bg)
	str1=''
	for i in arr:
		str1+=i+' '
	str1 = otherfont.render(str1, True, (0, 0, 0))
	nummy=len(word)
	win.blit(str1,(1000/(nummy),showy))
	win.blit(images[health],(170,50))
	for i in dots:
		if i.color==(255,255,255):
			continue
		pygame.draw.ellipse(win, i.color, (i.x, i.y,i.width*2,i.height*2))
		textsurface = myfont.render(i.name, True, (255, 255, 255))
		amount=5
		if i.name=='m' or i.name=='w':
			amount=8
		elif i.name=='l' or i.name=='f' or i.name=='j' or i.name=='i' or i.name=='hint':
			amount=3
		win.blit(textsurface,(i.x-amount+15,i.y-17+15))
	pygame.display.update()
def hint():
	i=word[randrange(len(word))]
	while i=='_':
		i=word[randrange(len(word))]
	while i in word:
		guessy[word.index(i)]=i
		word[word.index(i)]='_' 
class letter:
	def __init__(self,x,y,width,height,name,state=True,color=(50,103,201)): 
		self.x=x-20
		self.y=y-20
		self.width=width 
		self.height=height
		self.name=name 
		self.state=state
		self.color=color
	def clicked(self): 
		global word
		global guesses 
		if self.state: 
			self.state=False 
			self.color=(255,255,255) 
			if self.name=='hint':
				hint()
			else:
				if self.name not in word: 
					guesses-=1 
				while self.name in word:
					guessy[word.index(self.name)]=self.name
					word[word.index(self.name)]='_'
					self.color=(255,0,255)
pygame.init()
pygame.font.init()
win=pygame.display.set_mode((550,700))
myfont = pygame.font.SysFont('Arial', 25)
otherfont = pygame.font.SysFont('Arial', 50)
run=True
words=[]
guesses=6
images=[pygame.image.load('images/'+str(i)+'.png') for i in range(7)]
letters=list(string.ascii_lowercase)
bgcol=(255,255,255)
with open('words.txt','r') as f:
	data=f.readlines()
	for i in data:
		i=i[:-1]
		wordu=i.split(' ')[1]
		if len(wordu)>5 and len(wordu)<9:
			words.append(wordu)
main_word=words[randrange(len(words))]
word=list(main_word)
main_word=list(main_word)
guessy=['_' for i in word]
circles=make_circles(letters)
hinting=True
delay=0
while run and guessy!=main_word and guesses>0:
	if delay==0 and keyboard.is_pressed('alt'):
		hint()
		delay=5
	if delay>0:
		delay-=1
	if guesses==1 and hinting:
		hinting=False
		circles[0].state=True
		circles[0].color=(50,103,201)
	makescreen(bgcol,guessy,circles,350,word,guesses,images)
	ev = pygame.event.get()
	for event in ev:
		if event.type == pygame.QUIT:
			run=False
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			clicked_sprites = [s for s in circles if (pos[0]>s.x and pos[0]<s.x+s.width*2 and pos[1]>s.y and pos[1]<s.y+s.width*2)]
			for i in clicked_sprites:
				i.clicked()
if run:
	if guesses==0:
		images=[pygame.image.load('images/dead.png')]
	else:
		images=[pygame.image.load('images/alive.png')]
makescreen(bgcol,guessy,circles,350,word,0,images)