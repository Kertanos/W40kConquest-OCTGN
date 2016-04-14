import collections


def wilkommen():
	notify("Hi Boyz, i'm working on the deck check, so if you get any error message, please copy/paste it on my blog : http://octgngames.com/wh40kc/ or my github : https://github.com/Kertanos/W40kConquest-OCTGN/    Enjoy your game, good luck and have fun !")


def deckCheck(groups):
	mute()
	if groups.player !=me:return
	deckOk=True
	group=me.deck
	syna=False
	faction=""
	lord=""
	maxAlly=1
	nSquad=0
	notify("Checking {}'s deck".format(me))
	for card in me.hand:
		if card.Type != "Warlord" and card.Type != "Synapse":
			whisper("**WARNING, you're not supposed to have a non warlord, non synapse card in your hand. Be sure to move these cards away from warlord and synapse deckbuilder section. **")
			card.moveToBottom(group)
			continue
		elif card.Type == "Warlord":
			if faction=="":faction=card.Faction
			else:
				notify("{}'s deck error, multiple warlord detected.".format(me))
				return		
			lord=card.name
			sig=card.Squad
		elif card.Type == "Synapse": 
			if syna:
				notify("{}'s deck error, multiple synapse detected.".format(me))
				return
			else: syna=True
	if faction =="Space Marine": allianceCheck=["Neutral","Astra Militarum","Tau"]
	elif faction =="Astra Militarum": allianceCheck=["Neutral","Space Marine","Ork"]
	elif faction =="Ork":
		if lord =="Gorzod": 
			allianceCheck=["Neutral","Astra Militarum","Space Marine"]
			maxAlly=2
		else : allianceCheck=["Neutral","Astra Militarum","Chaos"]
	elif faction =="Chaos": allianceCheck=["Neutral","Ork","Dark Eldar"]
	elif faction =="Dark Eldar": allianceCheck=["Neutral","Chaos","Eldar"]
	elif faction =="Eldar": allianceCheck=["Neutral","Dark Eldar","Tau"]
	elif faction =="Tau":
		if lord=="Commander Starblaze" : allianceCheck=["Neutral","Astra Militarum"]
		else : allianceCheck=["Neutral","Eldar","Space Marine"]
	elif faction =="Tyranid": allianceCheck=["Neutral"]
	elif faction =="Necron": 
		allianceCheck=["Neutral","Space Marine","Astra Militarum","Ork","Chaos","Dark Eldar","Eldar","Tau"]
		maxAlly=7
	else:
		notify("{}'s deck is invalid, no warlord detected, please reset and reload a legal deck".format(me))
		return
	if syna and faction!="Tyranid":
		whisper("Deck error, Synapse can't be included in non Tyranid deck.")
		deckOk=False
	if len(group)<50:
		whisper("Deck error, it has less than 50 cards.")		
		deckOk=False
	counts=collections.defaultdict(int)
	alliance=collections.defaultdict(int)
	for card in group:
		n=3
		if card.Type!="Army" and card.Type!="Attachment" and card.Type!="Support" and card.Type!="Event":
			whisper("Deck error, {} is obviously lost, it should not be here".format(card.Name))
			deckOk=False
			continue			
		if card.Faction!=faction and allianceCheck.count(card.Faction)==0:
			whisper("Deck error, {} isn't related to your faction or allies".format(card.Name))
			deckOk=False
			continue
		if card.Faction!=faction and allianceCheck.count(card.Faction):
			if card.Loyalty !="":
				whisper("Deck error, {} is loyal".format(card.Name))
				deckOk=False
				continue
			if card.Type =="Army" and faction=="Tyranid":
				whisper("Deck error, you can't include neutral army unit like {}".format(card.Name))
				deckOk=False
				continue
			if card.Faction !="Neutral":
				if (card.Type!="Army" or "Vehicle." not in card.Traits) and lord=="Gorzod":
					whisper("Deck error, {} is not a SM or AM vehicle army unit".format(card.Name))
					deckOk=False
					continue
				alliance[card.Faction]+=1
		counts[card.Name]+=1
		if "Squad" in card.Loyalty:
			if card.Squad==sig: 
				n=int(card.Copies)
				nSquad+=1
			else:
				whisper("Deck error, {} comes from another signature squad".format(card.Name))
				deckOk=False
				continue				
		if counts[card.Name]>n :
			whisper("Deck error, more than {} copies of {} ".format(n,card.Name))
			deckOk=False
	if len(alliance)>maxAlly:
		whisper("Deck error, too much different ally faction")
		deckOk=False
	if nSquad!=8:
		whisper("Deck error, you need to include the full signature squad of you warlord")
		deckOk=False	
	if deckOk: notify("{}'s deck is OK".format(me))
	else : notify("{}'s deck is NOT OK, please fix It".format(me))