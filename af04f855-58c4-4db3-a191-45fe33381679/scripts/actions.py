#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------
Faith = ("Faith", "2138972e-68ee-4aa8-a803-1b4bd7de183b")
Resource = ("Resource", "906bc3a2-9315-4473-8671-7ece287de4a8")
Damage = ("Damage", "22adcef9-414c-4e96-8381-f155283e170e")
FstPlanet = ("FstPlanet", "9e9aceca-516f-43f4-8590-48068298af6f")
SixPlanet = ("SixPlanet", "8e41b199-b00c-4009-b94c-f10eb25cbaa2")
Infest = ("Infest", "5b35b6b8-aa47-4e70-934c-db3b7e64941a")
Snots = ("Snotlings", "177f3172-7098-4732-868e-afc9f0fb62fa")
PlanetList=[]

#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------

def setupPlanet(group):
	alt=""
	pset=askChoice("Choose a planet set ",['Traxis Sector','Veros Sector','Gardis Sector'], customButtons =["Let the Chaos Gods decide"])
	if pset == -1 :
		pset=rnd(1,2,3)		
	if pset == 2 : alt="veros"
	if pset == 3 : alt="gardis"
	group.create("5e423620-6663-4198-8cdc-df0fabf876c8")
	group.create("12fea3b0-be4e-4142-89db-316c56956c8f")
	group.create("89b18d3e-431e-4889-94d1-0948f73a4b2a")
	group.create("9657b143-06c2-45fe-bd6e-4a3d131e1689")
	group.create("8ec7354b-eef5-4997-82ed-d7ed66a93c15")
	group.create("8fcab463-9c8c-4745-a49e-38f56bc49e6d")
	group.create("1a35a54a-0f21-44d0-ab40-b3ec7ac5cadc")
	group.create("e0c7e2e6-711d-4704-8e38-182d113c6282")
	group.create("3e58dd21-00fe-499e-87e9-7bb52bb66b95")
	group.create("36221c3a-591c-41e8-a4c9-fc71c89cac12")
	X =-682
	k=7
	notify("The planets for this game are :")
	for i in range(2):
		card =group.random()
		card.moveToTable(X,-43)
		card.alternate=alt
		setGlobalVariable("Planet{}".format(k), card.name)
        	card.isFaceUp = False
		card.markers[SixPlanet] = k
		k-=1		
		X+=200
	for i in range(5):
		card =group.random()
		card.moveToTable(X,-43)
		card.alternate=alt
		setGlobalVariable("Planet{}".format(k), card.name)
		k-=1
		X+=200
		notify("**{}**".format(card))
	card.markers[FstPlanet] = 1
	for card in group:
		PlanetList.append(card.model)
		card.delete()
	fp=askChoice("Who'll be the first player ? ",['Me','My opponent'], customButtons =["Let the Chaos Gods decide"])
	if fp != 1 and fp!=2 : 
		fp = rnd(1,2)
		notify("The Chaos Gods choose")
	else: notify("{} decides to put".format(me))
	if len(getPlayers()) == 1 : fp =1
	if fp==1: 
		play=me
		if me.isInverted:Y2=-176
		else: Y2=88
	else : 
		play=players[1]
		if me.isInverted:Y2=88
		else: Y2=-176
	table.create("29133845-cfae-4d83-ba1b-8c7dc3dbbabe",668,Y2,persist=True)
	play.counters['Initiative'].value=1
	notify("{} as the first player.".format(play))
	setGlobalVariable("OutPlanets",str(PlanetList))



def setup(group, x = 0, y = 0):
	mute()
	var = me.getGlobalVariable("setupOk")
	if var == "1":
		notify("You already did your Setup")
		return
	if len(me.hand) == 0:
		notify("You need to load a deck first") 
		return
	var="1"
	me.setGlobalVariable("setupOk", var)
	notify("**{} has started setup, please wait**".format(me))
	set=(card for card in me.hand)
	if me.isInverted: 
		X1=-532
		X2=-432
		X3=694
		X4=632
		Y1=-288
		Y2=-88
	else:
		X1=468
		X2=368
		X3=632
		X4=694
		Y1=200
		Y2=0
	for card in set: 
		if card.Type == "Warlord":
			me.counters['Resources'].value = int(card.StartingResources)
			SHand=int(card.StartingHand)
			me.deck.shuffle()
			notify("**{}'s warlord is {}**".format(me,card))
			card.moveToTable(X1, Y1)
			if card.Faction == "Tyranid" : 
				table.create("124d3e0b-621a-4eb7-bb34-e4163794989f",X3,Y2,persist=True)
				table.create("a53b9f48-6ae2-4cd7-ba8a-6bfcf47bca3c",X4,Y2,persist=True)
			elif card.Faction == "Necron" :
				table.create("86fd3c0f-d1a0-4ded-a1a6-ec9ffc90f7f9",X3,Y2,persist=True)
				table.create("5c352ba9-9b70-4071-ae47-e2bed96d1e01",X4,Y2,persist=True)
			else : table.create("5c352ba9-9b70-4071-ae47-e2bed96d1e01",668,Y2,persist=True)
		if card.Type == "Synapse":
			notify("**{}'s Synapse is {}**".format(me,card))
			card.moveToTable(X2, Y1)
	for card in me.deck.top(SHand): card.moveTo(me.hand)
	notify("**{} is ready**".format(me))
	if not me.isInverted:setupPlanet(me.Planets)		

def flipCoin(group, x = 0, y = 0):
	mute()
	n = rnd(1, 2)
	if n == 1:
		notify("**{} flips heads.**".format(me))
	else:
		notify("**{} flips tails.**".format(me))

	
def xSided(group, x = 0, y = 0):
	mute()
	sides = askInteger("Roll a how many sided die? (minimum 3)", 3)
	if sides == None: return
	elif sides < 3:
		whisper("Please choose a number greater than or equal to 3.")
		return
	else:
		n = rnd(1,sides)
		notify("**{} rolls a {} on a {}-sided die.**".format(me, n, sides))


def restoreAll(group,x = 0, y=0): 
	mute()
	myCards = (card for card in table if card.controller == me and card.Type!="Planet")
	for card in myCards:
		if card.isFaceUp:
			card.orientation &= ~Rot90
			card.highlight = None
	notify("{} readies all his or her cards.".format(me))

def holdOn(group, x = 0, y = 0):
	mute()
	notify("***PLEASE WAIT.  {} has an action/reaction.***".format(me))

def imDone(group, x = 0, y = 0):
	mute()
	notify("***{} is Done.***".format(me))

def createToken(group, x = 0, y = 0):
	mute()	
	guid,quantity=askCard({'Type':'Token'})
	if guid == None: return
	if me.isInverted: 
		X1=-150
		for i in range(quantity):
			cards=table.create(guid, X1, -288)
			X1+=50	
	else:
		X1=150
		for i in range(quantity):
			cards=table.create(guid, X1, 200)
			X1-=50
	notify("{} creates {} {} Token(s)".format(me,quantity,cards))

def createSynapse(group, x = 0, y = 0):
	mute()	
	guid,quantity=askCard({'Type':'Synapse'})
	if guid == None: return
	if me.isInverted: 
		X1=-150
		for i in range(quantity):
			cards=table.create(guid, X1, -288)
			X1+=50	
	else:
		X1=150
		for i in range(quantity):
			cards=table.create(guid, X1, 200)
			X1-=50
	notify("{} creates {} Token(s)".format(me,cards))



def ServoSkull(group, x=0,y=0):
	mute()
	servo= (card for card in table if card.controller == me and card.Type == "Skull")
	notify("{} is choosing his or her Warlord destination.".format(me))
	choiceList = ['Planet 1', 'Planet 2', 'Planet 3', 'Planet 4', 'Planet 5']
	unit = "warlord"
	for card in servo:		
		choice = askChoice("To which planet do you want to commit your {} ? ".format(unit), choiceList)			
		if card.isFaceUp: card.isFaceUp = False
		card.peek()
		if choice == 0 : 
			notify("{} didn't change his or her Skull".format(me))
			return		
		elif choice == 1 : card.alternate=""
		elif choice == 2 : card.alternate="Skull2"
		elif choice == 3 : card.alternate="Skull3"
		elif choice == 4 : card.alternate="Skull4"
		else : card.alternate="Skull5"
		notify("{} has chosen where to commit his or her {}".format(me,unit))
		unit = "synapse"

def NecronDial(group, x=0,y=0):
	mute()
	dial= (card for card in table if card.controller == me and card.Name == "Enslavement Dial")
	notify("{} is choosing his or her Enslaved Faction.".format(me))
	choiceList = ['Astra Militarum', 'Chaos', 'Dark Eldar', 'Eldar', 'Space Marine', 'Ork', 'Tau']
	for card in dial:		
		choice = askChoice("Which faction do you want to enslave ? ", choiceList)			
		if choice == 1 : 
			card.alternate=""
			fact="the soldiers of the Astra Militarum"
		elif choice == 2 : 
			card.alternate="Chaos"
			fact="the dark servants of Chaos"
		elif choice == 3 : 
			card.alternate="Dark"
			fact="the sadistic Dark Eldars"
		elif choice == 4 : 
			card.alternate="Eldar"
			fact="the prideful Eldars"
		elif choice == 5 : 
			card.alternate="Marine"
			fact="the righteous Space Marines"
		elif choice == 6 : 
			card.alternate="Ork"
			fact="the brutal Orks"
		elif choice == 7 : 
			card.alternate="Tau"
			fact="the Tau conquerors"			
		else : 
			notify("{} didn't change his or her enslavement dial".format(me))
			return	
		notify("{} enslaved {}".format(me,fact))
		
	
def capture(group, x=0, y=0):
	mute()
	turn= getGlobalVariable("Turn")
	fstP= getGlobalVariable("Planet{}".format(turn))
	plan=(card for card in table if card.name == fstP)
	for card in plan:
		capt = confirm("Are you sure you want to capture {} ?".format(card.name))
		if capt == False : return
		if card.PlanetMaterial == "1" : me.counters['Material'].value += 1
		if card.PlanetStrongpoint == "1" : me.counters['Strongpoint'].value += 1
		if card.PlanetTech == "1" : me.counters['Tech'].value += 1
		card.moveTo(me.Planets)
		notify("**{} captures the first planet, {}**".format(me,card))
	if me.counters['Tech'].value >= 3 or me.counters['Strongpoint'].value >= 3 or me.counters['Material'].value >= 3 : notify ("**{} HAS WON THE GAME ! CONGRATULATIONS ! **".format(me))

def endTurn(group, x=0, y=0):
	mute()
	turn = int(getGlobalVariable("Turn"))
	if not confirm("Resolve the Turn {} HeadQuarter phase ? ".format(turn)) :return
	pturn= int(me.getGlobalVariable("Pturn"))
	if turn!=pturn : return
	notify("{} activates the resolution of Turn {} HeadQuarter phase.".format(me,turn))
	turn+=1
	setGlobalVariable("Turn",str(turn))
	HQRes(turn)
	if me.isInverted:Y= -176
	else:Y= 88
	if len(getPlayers()) != 1 :
		remoteCall(players[1],"HQRes",turn)
		if me.counters['Initiative'].value==0: 
			me.counters['Initiative'].value=1
			players[1].counters['Initiative'].value=0
			notify("{} has initiative for Turn {}.".format(me,turn))
		else: 
			me.counters['Initiative'].value=0
			players[1].counters['Initiative'].value=1
			notify("{} has initiative for Turn {}.".format(players[1],turn))
			if Y== -176: Y=88
			else: Y= -176
		init=(card for card in table if card.model == "29133845-cfae-4d83-ba1b-8c7dc3dbbabe")
		for card in init: card.moveToTable(668,Y)
	update()
	if turn==8: 
		notify("End of the game ! The last players to have captured a planet win !")
		return
	fstP= getGlobalVariable("Planet{}".format(turn))
	plan=(card for card in table if card.name == fstP)
	for card in plan: card.markers[FstPlanet] = 1 
	for card in table: card.markers[Faith] = 0
	notify("** Turn {} HQ Phase Complete**".format(turn-1))
 	if turn <= 3 :
		fstP=(card for card in table if card.markers[SixPlanet] == turn+4)
		for card in fstP: 
			card.isFaceUp=True
			card.markers[SixPlanet] = 0
			notify("The 5th planet is now {}.".format(card))

	
def HQRes(turn):
	mute()
	draw(me.deck)
	draw(me.deck)
	restoreAll(Table)
	me.counters['Resources'].value += 4
	notify("{} gains 4 resources.".format(me))
	me.setGlobalVariable("Pturn",str(turn))


def winC(group,x=0,y=0):
	mute()
	com=(card for card in table if card.targetedBy==me and (card.ResourceBonus!="" or card.CardBonus!=""))
	conf=0
	conf=askChoice("What do you want to do with targeted cards? ", ['Take all resources and draw bonuses.','Select for each.'])
	resB=0
	cardB=0
	if conf==0:return
	elif conf==1:
		for card in com: 
			if card.ResourceBonus!="": resB+=int(card.ResourceBonus)
			if card.CardBonus!="": cardB+=int(card.CardBonus)
		notify("{} chooses to take all bonuses".format(me))
	else:
		for card in com:
			bon=askChoice("For {} : {} Resources, {} Cards".format(card.name,card.ResourceBonus,card.CardBonus), ['Resources','Draw','Both','None'])
			if bon==1:
				if card.ResourceBonus!="":resB+=int(card.ResourceBonus)
				notify("{} chooses to only take resources from {}.".format(me,card))
			elif bon==2:
				if card.CardBonus!="":cardB+=int(card.CardBonus)
				notify("{} chooses to only take draw from {}.".format(me,card))
			elif bon==3:
				if card.ResourceBonus!="":resB+=int(card.ResourceBonus)
				if card.CardBonus!="":cardB+=int(card.CardBonus)
				notify("{} chooses to take both resources and draw from {}.".format(me,card))
			else: notify("{} chooses to take nothing from {}".format(me,card))
	notify("{} draws {} cards and take {} resources.".format(me, cardB,resB))
	if len(me.deck) <= cardB:
		notify("**{} was lost in the warp, he looses the game (last card drawn).**".format(me))
		return	
	for card in me.deck.top(cardB):
		card.moveTo(me.hand)
	me.counters['Resources'].value += resB

				

#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def disc(card, x=0, y=0):
	mute()
	if card.Type != "Planet":
		if not confirm("Discard {} ?".format(card.name)): return
		group=card.group
		card.moveTo(me.piles['Discard pile'])
		notify("{} discards {} from his or her {}.".format(me, card,group.name))
	else:
		turn= getGlobalVariable("Turn")
		fstP= getGlobalVariable("Planet{}".format(turn))
		if card.name!=fstP: return
		if not confirm("Are you sure you want to destroy {} ? There is no going back !".format(card.name)): return
		notify("{} destroys {}.".format(me,card))
		PlanetList=eval(getGlobalVariable("OutPlanets"))		
		PlanetList.append(card.model)
		setGlobalVariable("OutPlanets",str(PlanetList))
		card.delete()

def addMarker(card, x=0, y=0):
	mute()
	marker, qty = askMarker()
	if qty == 0 or marker== None: return
	card.markers[marker] += qty
	notify("{} adds {} {} marker on {}".format(me,qty,marker[0],card))

def subMarker(card, x=0, y=0):
	mute()
	marker, qty = askMarker()
	if qty == 0 or marker== None: return
	card.markers[marker] -= qty
	notify("{} removes {} {} marker on {}".format(me,qty,marker[0],card))



def displayErrata(card, x = 0, y = 0):
	mute()	
	notify('{} - Errata Text:'.format(card.name))
	notify('{}'.format(card.ErrataText))
	
	
def kneel(card, x = 0, y = 0):
	mute()
	key=card.Keywords
	if not card.isFaceUp and "Deep Strike" in key:
		cost=int(key[13])
		if not confirm("Deep strike {} ?".format(card.name)): return
		if me.counters['Resources'].value < cost :
			whisper("You don't have enough Resources to deep strike {}.".format(card.name))
			return		
		card.isFaceUp=True
		notify("{} deep strikes {} for {} resources).".format(me,card,cost))
		me.counters['Resources'].value -= cost
		return
	card.orientation ^= Rot90
	if card.orientation & Rot90 == Rot90:
		notify('{} exhausts {}.'.format(me, card))
	else:
		notify('{} readies {}.'.format(me, card))

def flipcard(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} turns {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} turns {} face up.".format(me, card))

def addDamage(card, x = 0, y = 0):
	mute()
	notify("{} adds a Damage to {}.".format(me, card))
	card.markers[Damage] += 1
    
def addResource(card, x = 0, y = 0):
    mute()
    notify("{} adds a Resource to {}.".format(me, card))
    card.markers[Resource] += 1
	
    
def subDamage(card, x = 0, y = 0):
    mute()
    notify("{} removes a Damage from {}.".format(me, card))
    card.markers[Damage] -= 1
    
def subResource(card, x = 0, y = 0):
    mute()
    notify("{} subtracts a Resource to {}.".format(me, card))
    card.markers[Resource] -= 1 

def addFaith(card, x = 0, y = 0):
	mute()
	notify("{} adds a Faith to {}.".format(me, card))
	card.markers[Faith] += 1

def subFaith(card, x = 0, y = 0):
	mute()
	notify("{} removes a Faith from {}.".format(me, card))
	card.markers[Faith] -= 1

def infest(card, x = 0, y = 0):
	mute()
	if card.Type == "Planet": 
		notify("{} Infested {}.".format(me, card))
		card.markers[Infest] = 1

def uninfest(card, x = 0, y = 0):
	mute()
	if card.Type == "Planet": 
		notify("{} cleared the infestation on {}.".format(me, card))
		card.markers[Infest] = 0

def bloodied(card, x = 0, y = 0):
	mute()
	if card.Type != "Warlord" or card.alternate == "bloodied" : return
	notify("{} is now Bloodied.".format(card))
	card.alternate="bloodied"
	card.markers[Damage] = 0
	card.orientation = Rot90


def restore(card, x = 0, y = 0):
	mute()
	if card.Type != "Warlord" or card.alternate != "bloodied": return
	notify("{} is no longer Bloodied.".format(card))
	card.alternate=""
	card.markers[Damage] = 0

def replace(card, x =0, y = 0):
	mute()
	if card.Type != "Planet" : return
	if not card.isFaceUp : return
	x,y=card.position
	alt=card.alternate
	choice=askChoice("What do you want to do with {} ?".format(card.Name),["Declare the Crusade","Warp Rift"])
	if choice == 0: return
	elif choice == 1 :
		PlanetList=eval(getGlobalVariable("OutPlanets"))
		notify("{} is choosing a new planet to replace {}.".format(me,card))
		guid,quantity=askCard({'model':PlanetList})
		if guid == None: 
			notify("{} didn't replace {}".format(me,card))
			return
		PlanetList.append(card.model)
		PlanetList.remove(guid)
		planet=table.create(guid,x,y,persist=True)
		planet.alternate=alt
		notify("{} is now replacing {}".format(planet,card))
		for i in range(7):
			if card.name==getGlobalVariable("Planet{}".format(i+1)) : setGlobalVariable("Planet{}".format(i+1),planet.name)	
		card.delete()
		setGlobalVariable("OutPlanets",str(PlanetList))
	elif choice == 2 :
		for i in range(7):
			if card.name==getGlobalVariable("Planet{}".format(i+1)) : plan=i+1
		notify("{} is choosing with which planet to switch {}.".format(me,card))
		plan1=""
		plan2=""
		if plan!=1 : 
			plan1=getGlobalVariable("Planet{}".format(plan-1))
		if plan!=7 : 
			plan2=getGlobalVariable("Planet{}".format(plan+1))
		PlanetList=(card for card in table if (card.Name==plan1 or card.Name==plan2) and card.isFaceUp)
		dlg = cardDlg(PlanetList)
		dlg.title = "With which planet do you want to switch {} ?".format(card.Name)
		planets = dlg.show()
		if planets != None:
			for p in planets :
				x1,y1=p.position
				p.moveToTable(x,y)
				setGlobalVariable("Planet{}".format(plan),p.Name)
				if p.Name==plan1: plan=plan-1
				if p.Name==plan2: plan=plan+1
				notify("{} switched place with {}".format(p,card))
			card.moveToTable(x1,y1)
			setGlobalVariable("Planet{}".format(plan),card.Name)		
		else : notify("{} didn't move anything.".format(me))

#---------------------------
#movement actions
#---------------------------

#------------------------------------------------------------------------------
# Hand Actions
#------------------------------------------------------------------------------

def randomDiscard(group):
	mute()
	card = group.random()
	if card == None: return
	card.moveTo(me.piles['Discard pile'])
	notify("{} randomly discards {}.".format(me, card))
 
def discardMany(group):
	count = 0
	discAmount = None
	
	mute()
	if len(group) == 0: return
	if discAmount == None: discAmount = askInteger("Randomly discard how many cards?", 2)
	if discAmount == None: return
	
	for index in range(0,discAmount):
		card = group.random()
		if card == None: break
		card.moveTo(me.piles['Discard pile'])
		count += 1
		notify("{} randomly discards {}.".format(me,card))
	notify("{} randomly discards {} cards.".format(me, count))

def mulligan(group):
	count = None
	draw = None
	mute()
	draw = askInteger("How many cards would you like to draw for your Mulligan?", len(me.hand))
	if draw == None: return
	
	for card in group:
		card.moveToBottom(me.deck)
	update()
	me.deck.shuffle()
	update()
	for card in me.deck.top(draw):
		card.moveTo(me.hand)
	notify("{} mulligans and draws {} new cards.".format(me, draw))


def play(card, x=0, y=0):
	mute()
	if "Deep Strike" in card.Keywords:
		if confirm("Do you want to put {} into reserve ? ".format(card.name)):
			if me.counters['Resources'].value < 1 :
				whisper("You don't have enough Resources to put {} into reserve.".format(card.name))
				return		
			if me.isInverted: card.moveToTable(0,-288,True)
			else : 	card.moveToTable(0,200,True)
			notify("{} puts a card into reserve).".format(me))
			card.peek()
			me.counters['Resources'].value -= 1
			return
	if card.cost == "" : 
		whisper("You can't play this card")
		return
	if card.Cost == "X": cost=askInteger("How much do you want to pay to play {} ? ".format(card.name),0)
	else : cost=int(card.Cost)
	reduc=askInteger("Reduce Cost by ?",0)
	if reduc == None or cost == None: return
	if reduc>cost: reduc=cost
	cost-=reduc
	if me.counters['Resources'].value < cost :
		whisper("You don't have enough Resources to pay for {}.".format(card.name))
		return		
	if me.isInverted: card.moveToTable(0,-288)
	else : 	card.moveToTable(0,200)
	notify("{} plays {} for {} resources (Cost reduced by {}).".format(me,card,cost,reduc))
	me.counters['Resources'].value -= cost

#------------------------------------------------------------------------------
# Pile Actions
#------------------------------------------------------------------------------

def shuffle(group):
	group.shuffle()

def draw(group):
	mute()
	if len(group) == 0: return
	group[0].moveTo(me.hand)
	notify("{} draws a card.".format(me))
	if len(group) == 0: notify("**{} was lost in the warp, he looses the game (last card drawn).**".format(me))
	
def drawRandom(group):
	mute()
	
	card = group.random()
	if card == None: return
	card.moveTo(me.hand)
	notify("{} randomly draws a plot card.".format(me))
	if len(group) == 0: notify("**{} was lost in the warp, he looses the game (last card drawn).**".format(me))

def drawMany(group):
	drawAmount = None
	
	mute()
	if len(group) == 0: return
	if drawAmount == None: drawAmount = askInteger("Draw how many cards?", 7)
	if drawAmount == None: return
	
	if len(group) < drawAmount:
		drawAmount = len(group)
	
	for card in group.top(drawAmount):
		card.moveTo(me.hand)
	notify("{} draws {} cards.".format(me, drawAmount))
	if len(group) == 0: notify("**{} was lost in the warp, he looses the game (last card drawn).**".format(me))
 
def discardManyFromTop(group):
	count = 0
	discAmount = None
	
	mute()
	if len(group) == 0: return
	if discAmount == None: discAmount = askInteger("Discard how many from top?", 4)
	if discAmount == None: return
	
	for card in group.top(discAmount):
		card.moveTo(me.piles['Discard pile'])
		count += 1
		if len(group) == 0: break
	notify("{} discards {} cards from the top of their Deck.".format(me, count))

def searchTop(group):
	mute()
	searchAmount = askInteger("How many cards do you want to look ?",1)
	if searchAmount == None:return
	if len(group) < searchAmount: searchAmount = len(group)
	if searchAmount == 0 : return
	notify("{} is searching the top {} card(s) of his or her {}".format(me,searchAmount,group.name))
	list=[]
	for card in group.top(searchAmount): list.append(card)
	dlg = cardDlg(list)
	dlg.min=0
	dlg.max=searchAmount
	dlg.title = "Select a card"
	cards = dlg.show()
	if me.isInverted:
		x1=-150
		y1=-288
		i=50
	else: 
		x1=150
		y1=200
		i=-50
	if cards != None:
		for card in cards :
			card.moveToTable(x1,y1,True)
			x1+=i
			card.peek()
			searchAmount-=1
			card.select()
		notify("{} picked {} cards".format(me,len(cards)))
	else:notify("{} didn't find what he or she was looking for.".format(me))
	for cards in group.top(searchAmount): cards.moveToBottom(group)
	notify("{} placed the {} remaining cards to the bottom of his or her deck.".format(me,searchAmount))
	if len(me.deck) == 0: notify("**{} was lost in the warp, he looses the game (last card drawn).**".format(me))

			

 
	
def reshuffle(group):
	count = None
	
	mute()
	if len(group) == 0: return
	if not confirm("Are you sure you want to reshuffle the {} back into your Deck?".format(group.name)): return
	
	myDeck = me.deck
	for card in group:
		card.moveTo(myDeck)
	myDeck.shuffle()
	notify("{} shuffles thier {} back into their deck.".format(me, group.name))
	
def moveOneRandom(group):
	mute()
	if len(group) == 0: return
	if not confirm("Are you sure you want to move one random card from your {} to your Hand?".format(group.name)): return
	
	card = group.random()
	if card == None: return
	card.moveTo(me.hand)
	notify("{} randomly moves {} from their discard to their hand.".format(me, card.name))
	
