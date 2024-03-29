import triffid as cipher #put in here name of file for particular cipher, must have a "decrypt" function "decrypt(ciphertext,key"

import cipher_text_analyser as analysis

import random
import cipher_tools
import time


key_length = cipher.Properties.key_length  #cipher file needs a Properties class instance with a value of keylength (25 or 26)
key_alphabet = cipher.Properties.key_alphabet #the alphabet for a particular cipher, eg one without j or q for the playfair



#_______________________________transformations_________________________________

def swap(key,current_key_score,keylength,ciphertext):
	#swaps pairs of characters in the key, taking sample analysis and returns the best key
	analyse = analysis.analyse #stores analyse function as local for faster access
	key_to_return = key
	score = current_key_score
	key_list = list(key)       #stores a list of keys outside of loop for easy access
	for i in xrange(keylength):
		for j in xrange(i,keylength):
			trial_key = list(key_list)

			temp = trial_key[i]
			trial_key[i] = trial_key[j]
			trial_key[j] = temp   #swaps two characters
			
			trial_key = ''.join(trial_key)
			
			sample_plaintext = cipher.decrypt(ciphertext,trial_key)
			this_score = analysis.analyse(sample_plaintext)
			#print this_score
			
			if this_score >= score:
				score = this_score
				key_to_return = trial_key

	return key_to_return,score

def rotate(key,current_key_score,keylength,ciphertext): #shifts thekey around
	analyse = analysis.analyse #stores analyse function as local for faster access
	key_to_return = key
	score = current_key_score
	trial_key = key
	for i in xrange(keylength):
		trial_key = trial_key[1:]+trial_key[:1]
		sample_plaintext = cipher.decrypt(ciphertext,trial_key)
		this_score = analysis.analyse(sample_plaintext)
		if this_score >= score:
			score = this_score
			key_to_return = trial_key
			#print "rotating"
	return key_to_return,score

def flip(key,current_key_score, keylength,ciphertext):
	key_list = list(key)
	key_list.reverse()
	sample_plaintext = cipher.decrypt(ciphertext,''.join(key_list))
	this_score = analysis.analyse(sample_plaintext)
	if this_score > current_key_score:
		return ''.join(key_list),this_score
	else:
		return key,current_key_score


def hill_climb(ciphertext):
	ciphertext = cipher.Properties.preprocess(ciphertext)
	key_length = cipher.Properties.key_length  #cipher file needs a Properties class instance with a value of keylength (25 or 26)
	key_alphabet = cipher.Properties.key_alphabet #the alphabet for a particular cipher, eg one without j or q for the playfair
	#local_maxima = []
	score = analysis.analyse(cipher.decrypt(ciphertext,key_alphabet))

	while score< -2.4: #while score not high enough to constitute a plaintext
		shuffled_key = list(key_alphabet)
		random.shuffle(shuffled_key)#creates a random key at the start of each round
		current_key = ''.join(shuffled_key)
		previous_key = key_alphabet
		new_score = analysis.analyse(cipher.decrypt(ciphertext,current_key))
		while current_key != previous_key: #"until best key is current key"
			previous_key = str(current_key)
			for i in xrange(10):  #runs a swap round 10 times
				current_key,new_score = swap(current_key,new_score,key_length,ciphertext)
				#if current_key == previous_key:
				#	print "keys are equal"
			print current_key, new_score
			

			current_key,new_score = rotate(current_key,new_score,key_length,ciphertext) #runs a rotate round once
			current_key,new_score = flip(current_key,new_score,key_length,ciphertext) #runs a flip round once

			if current_key == previous_key:
				print "keys are equal"

			#print current_key, new_score
		#local_maxima.apppend([new_score,current_key])
		score = new_score

	return current_key,cipher.decrypt(ciphertext,current_key)


def partial_hill_climb(ciphertext,key):
	#runs a partial hill climb to to attempt to improve an imperfect key
	ciphertext = cipher.Properties.preprocess(ciphertext)
	key_length = cipher.Properties.key_length  #cipher file needs a Properties class instance with a value of keylength (25 or 26)
	key_alphabet = cipher.Properties.key_alphabet #the alphabet for a particular cipher, eg one without j or q for the playfair

	shuffled_key = list(key_alphabet)
	random.shuffle(shuffled_key) #creates a random key at the start of each round
	previous_key = ''.join(shuffled_key)
	current_key = key
	new_score = analysis.analyse(cipher.decrypt(ciphertext,current_key))
	while current_key != previous_key: #"until best key is current key"
		previous_key = current_key
		for i in xrange(5):  #runs a swap round 5 times
			current_key,new_score = swap(current_key,new_score,key_length,ciphertext)

		current_key,new_score = rotate(current_key,new_score,key_length,ciphertext) #runs a rotate round once
		current_key,new_score = flip(current_key,new_score,key_length,ciphertext) #runs a flip round once

	return current_key,cipher.decrypt(ciphertext,current_key)	


plaintext = '''
WHENIARRIVEDTHESTUDIOWASALREADYSTOCKEDWITHPAINTS
ANDCANVASBUTTHEPROFESSORHELPEDMEEXPLAINTODANIELTHATTHEFORGERIESWOULDBEQUICKLYDET
ECTEDIFWEUSEDTHEMSHEWASPAINTEDONAPOPLARBOARDRATHERTHANASTRETCHEDCANVASANDTHEPIGM
ENTSUSEDBYTHEMASTERWEREVERYDIFFERENTFROMTHEONESWEUSETODAYNOWTHEYBRINGMETHEPIGMEN
TSIASKFORSOFTCHALKYBLOODREDSANGUINEANDMUSTARDYELLOWOCHRESFROMTHESOILSOFITALYIMIX
THEMWITHLINSEEDOILBOILEDANDAGEDINAKETTLEPROPERLYPREPAREDTHESEPAINTSAREINDISTINGU
ISHABLEFROMTHEONESUSEDONTHEORIGINALANDTHECOPYISMORELIKELYTOBEBETRAYEDBYACARELESS
BRUSHSTROKEORAMISPLACEDHIGHLIGHTTHEPROFESSORSEESQUICKLYWHENMYTIREDEYESHAVEMISSED
ATONEANDIHAVEMADEENOUGHDELIBERATEMISTAKESTOCONVINCETHEMTOMOVEMYSTUDIOTOTHEATTICW
HERETHELIGHTISBETTERFROMTHEREIHAVEAVIEWOFTHECITYANDAREMINDEROFFREEDOMTHEYSTILLIN
SISTTHATISLEEPHEREINTHECELLARBUTTHATGIVESMEANOTHERFREEDOMTHEFLICKERINGCANDLESCAS
TDEEPSHADOWSWHICHHIDEMYOTHERWORKIFICANNOTBEFREEPERHAPSSHECAN
'''
ciphertext = cipher.encrypt(plaintext,"theroncwasbyldmfgijkpquvxz/")
#ciphertext = '''
#SYIEZ LKKZR IVPYI MPQVZ FSLML CKILV WMPFU BIVSZ PYHLZ EPMLE VULER LMOQP PYIHK FGIMM FKYIC HIVDI ITHCL ZEPFV LEZIC PYLPP YIGFK NIKZI MSFQC VOIJQ ZUBCW VIPIU PIVZG SIQMI VPYID MYISL MHLZE PIVFE LHFHC LKOFL KVKLP YIKPY LELMP KIPUY IVULE RLMLE VPYIH ZNDIE PMQMI VOWPY IDLMP IKSIK IRIKW VZGGI KIEPG KFDPY IFEIM SIQMI PFVLW EFSPY IWOKZ ENDIP YIHZN DIEPM ZLMBG FKMFG PUYLC BWOCF FVKIV MLENQ ZEILE VDQMP LKVWI CCFSF UYKIM GKFDP YIMFZ CMFGZ PLCWZ DZTPY IDSZP YCZEM IIVFZ COFZC IVLEV LNIVZ ELBIP PCIHK FHIKC WHKIH LKIVP YIMIH LZEPM LKIZE VZMPZ ENQZM YLOCI GKFDP YIFEI MQMIV FEPYI FKZNZ ELCLE VPYIU FHWZM DFKIC ZBICW PFOIO IPKLW IVOWL ULKIC IMMOK QMYMP KFBIF KLDZM HCLUI VYZNY CZNYP PYIHK FGIMM FKMII MJQZU BCWSY IEDWP ZKIVI WIMYL RIDZM MIVLP FEILE VZYLR IDLVI IEFQN YVICZ OIKLP IDZMP LBIMP FUFER ZEUIP YIDPF DFRID WMPQV ZFPFP YILPP ZUSYI KIPYI CZNYP ZMOIP PIKGK FDPYI KIZYL RILRZ ISFGP YIUZP WLEVL KIDZE VIKFG GKIIV FDPYI WMPZC CZEMZ MPPYL PZMCI IHYIK IZEPY IUICC LKOQP PYLPN ZRIMD ILEFP YIKGK IIVFD PYIGC ZUBIK ZENUL EVCIM ULMPV IIHMY LVFSM SYZUY YZVID WFPYI KSFKB ZGZUL EEFPO IGKII HIKYL HMMYI ULE
#'''
#print analysis.analyse(cipher_tools.preprocess(plaintext))
#ciphertext = '''NKRSA ZYIUA YOTYG XKOYA VVUYK QOTJO TZNKO XUCTC GEHAZ ZNKXK OYROZ ZRKCG XSZNO TZNKQ OTJTK YYOXK IKOBK GTTGZ XOKYZ USGQK SKIUS LUXZG HRKHA ZYNKO YGLXG OJZNK YYULL OIKXC NUHXO TMYAY ZNKVG OTZOT MYOYI XAKRG TJIUC GXJRE GTJNK HKGZY GTTGO LSECU XQOYT UZMUU JKTUA MNNKO YYIGX KJZNG ZOLNK HKGZY SKNKS OMNZJ GSGMK SENGT JYGTJ ZUUYI GXKJZ UHKGZ NKXNA YHGTJ JGTOK RGHKG XULGS GTCNU ZUCKX YUBKX NOSOZ JUKYT ZSGZZ KXZNK XKGRV UCKXR OKYCO ZNZNK HARRE NKIUA RJNGB KAYGR RYNUZ GTJCK GRRQT UCOZJ GTOKR YIGXK YSKZU UHAZU TREHK IGAYK NKXKS OTJYS KULNK RSAZG TJZNG ZXKSO TJYSK ULZNK IGSVN KTKBK XYVKG QYTKB KXRUU QYSKO TZNKK EKGTJ TKBKX CGTZY GTEZN OTMLX USSKO ZNOTQ NKNGZ KYSKL UXHXO TMOTM ZNKYY ZUNOY NUAYK HAZLU XGTTG YYGQK NKHXO TMYSK CNGZO TKKJC NGZOS UYZTK KJOYG CGEUA ZULNK XKCNK TOGSM UTKGT TGYHK GZOTM YCORR YZUVG TJSGE HKJGT OKRCO RRYZU VNGZO TMSKH AZOGS CGZIN KJGRR JGEGT JZNKN UAYKO YRUIQ KJGZT OMNZZ NGZCO RRTUZ YZUVS KLXUS ZXEOT M'''
start = time.time()
print hill_climb(ciphertext)
print "Time taken: ", time.time()-start,"seconds"





