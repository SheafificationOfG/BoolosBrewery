from itertools import permutations, product
from strats import Foo, Bar, Baz, Default, Easy, Hard, Mathematician, Physicist, Engineer, Philosopher, Alice, Bob, Charlie, Dan, Expr, Math, Engg, Phys, Phil


from math import comb as comb_number

#viliml solution was too "complex" so i did this
#We can reduce each question to ask if some scenario out of a list of scenarios is the actual one
#One scenario, for example, would be (A: Phys, B: Phil, C: Engg, D: Math, Math: Foo, Phys: Boo, Phil: Baz)
#So we end up with a list of lenght <= 144 for every question. For example [0, 1] (Question is only true if this is scenario 0 or 1)
#This list can be encoded. As every list correspond to an index of the combination of 144 integers.
#For example, if our list is [0, 1] then our index is 144. Since the combinations are as following
#(), (0), (1), (2), ..., (143), (0, 1), ...

#I also have to specify who am i asking the question. I write the index of the person after a ","
#Then "260921280343613508858417787459715793582625,2" is asking to [Alice, Bob, Charlie, Dan][2] wich is Charlie about the list of scenarios encoded as 260921280343613508858417787459715793582625

#The keys are: 1 for the initial question. Then 3*last_question_key + index_of_response for the next question/answer, where index_of_response is 0 if Foo, 1 if Bar, 2 if Baz
#If the node is an answer then i write the index of an scenario wich order of fields is the correct answer. So if the answer is A: Math, B: Phys, C: Phil, D: Engg then the index is 0, as the scenario 0 has that order.



data = {
  "1": "260921280343613508858417787459715793582625,2",
  "3": "841411308272750671623757569173550866527295,3",
  "9": "14978546109522134555124641560575532973100,1",
  "27": "14277958740259809519326149717142067013424116,0",
  "82": "13",
  "83": "22300672741619926704831511229401816123982481,1",
  "249": "15",
  "250": "13",
  "28": "797940980354365187085349142751247904,0",
  "84": "3",
  "85": "22300745198051213981430374619339989292514373,0",
  "256": "0",
  "257": "6",
  "86": "22263036537446511546780181048374259680637901,0",
  "258": "9",
  "259": "1",
  "260": "7",
  "29": "4960086978934383594793941193906450900425,2",
  "87": "2",
  "88": "22291220830615394694005797966969740721793549,2",
  "264": "22",
  "265": "8",
  "89": "22300579340369068977383594486073322788282027,2",
  "267": "14",
  "269": "12",
  "10": "40990047226188525682547251446591164713,0",
  "30": "20565424356906036912297664906961922173782208,1",
  "90": "7",
  "91": "15",
  "92": "22300745194395685282333824565739479219068367,0",
  "276": "9",
  "277": "3",
  "278": "1",
  "31": "2668897766487880317576536916483726739,0",
  "93": "8",
  "94": "22300738727865686082960751420118985332240411,2",
  "282": "14",
  "283": "2",
  "284": "12",
  "95": "22300745186887383143685305432147567626419510,1",
  "285": "3",
  "286": "6",
  "287": "0",
  "32": "16234875123489465436874174516340122733288,0",
  "96": "10",
  "97": "22300374030551938890344695330389195844680963,0",
  "292": "5",
  "293": "11",
  "98": "22300745198373140157387157632556047032212843,2",
  "294": "17",
  "295": "16",
  "296": "4",
  "11": "55433253841838657993688116007613645373647,1",
  "33": "4358841205527549855070531796350910340650069,3",
  "99": "15",
  "100": "9",
  "101": "21807559945139622800982639383880927141401604,0",
  "303": "1",
  "304": "7",
  "305": "9",
  "34": "1825702485526884779154822473284176591018132,1",
  "102": "18",
  "103": "22200712253922129125029721218060216699596801,2",
  "309": "23",
  "310": "20",
  "311": "22",
  "104": "22300403524263126147150468377618395791595497,0",
  "312": "13",
  "313": "6",
  "314": "0",
  "35": "21308971020217283433751572274425249921880,1",
  "105": "12",
  "106": "22300745036062237616249070155419449620752024,1",
  "319": "21",
  "320": "19",
  "107": "22300743192136159772005934617093926821826497,2",
  "321": "2",
  "322": "8",
  "323": "14",
  "4": "13361694140280146956033940828434260014,0",
  "12": "1000074474530928418615973222332284806,3",
  "36": "21205979207307851644484050106049704498201319,1",
  "108": "21",
  "109": "18",
  "110": "22300714345441884644964030348954971828009536,1",
  "330": "19",
  "331": "20",
  "332": "3",
  "37": "5821582845926426950398001521137068922,3",
  "111": "23",
  "112": "22300730933615568009764897418176691247113750,0",
  "336": "7",
  "337": "3",
  "338": "1",
  "113": "22300728649229390846258394499714963929126827,3",
  "340": "13",
  "341": "15",
  "38": "33880997140791186618462808257493242559368,3",
  "114": "11",
  "115": "22290278810871284778959708549476930700182270,3",
  "346": "17",
  "347": "16",
  "116": "22299119115735612601707115716242525600135542,0",
  "348": "7",
  "349": "4",
  "350": "5",
  "13": "107623669586600748362526137036990,3",
  "39": "16231413539936968775202597889285240516357359,1",
  "117": "2",
  "118": "18",
  "119": "22294556049942304996738726964682149910680846,1",
  "357": "19",
  "358": "20",
  "359": "21",
  "40": "161266874776048543164322166447703042986,0",
  "120": "23",
  "121": "7016167915772941664091901884745470371631224,3",
  "363": "23",
  "364": "9",
  "365": "3",
  "122": "22300744333386859260295933764193579424447279,1",
  "366": "2",
  "368": "23",
  "41": "409537622583563663464597195290911077965,0",
  "123": "10",
  "124": "22300632714788879333130715566078049619891738,1",
  "372": "13",
  "373": "1",
  "374": "15",
  "125": "2",
  "14": "9563557798875229365906322727699394228,1",
  "42": "3144466096046955209959723389191015570592533,0",
  "126": "0",
  "127": "8",
  "128": "21254333380567135572682024799262566441224520,1",
  "384": "12",
  "385": "14",
  "386": "6",
  "43": "3555819850852517503539460392713107882744,0",
  "129": "9",
  "130": "22300745193243853383353374923527802479215155,0",
  "391": "7",
  "392": "1",
  "131": "22300551763174774738583482229851346826165239,3",
  "393": "13",
  "394": "15",
  "395": "3",
  "44": "60596884402323628212574059220043302,2",
  "132": "23",
  "133": "22289099649843277231179320462254589987271588,3",
  "399": "19",
  "401": "21",
  "134": "22243931138090171511678277472363426532100447,2",
  "403": "20",
  "404": "18",
  "5": "75914411715730524847998984627345564651370,1",
  "15": "252888134122828533256095664822623024450,3",
  "45": "11652667249784295685041187518429126600360961,2",
  "135": "16",
  "136": "4",
  "137": "22275958700737346967317886081999546124150570,0",
  "411": "11",
  "412": "5",
  "413": "10",
  "46": "3814971940031002117074461966875998453197,2",
  "138": "18",
  "139": "22298651175603924106221347790857263844956792,2",
  "418": "23",
  "419": "22",
  "140": "22300726417536957113241900659274848885417047,1",
  "420": "19",
  "421": "21",
  "422": "20",
  "47": "4578297944191139923404649304417216088859,3",
  "141": "17",
  "142": "22297023000115591586233764039548234402322247,0",
  "427": "3",
  "428": "9",
  "143": "22300732875556862043478608332697128951648736,1",
  "429": "13",
  "430": "1",
  "431": "15",
  "16": "27490544266600467733700266700807857294458,0",
  "48": "1602317626895267717089595515976047503637191,2",
  "144": "2",
  "145": "12",
  "146": "22278062420623746497630591313942158491470090,0",
  "438": "6",
  "439": "0",
  "440": "8",
  "49": "281471632939109083272448918209611699872075,3",
  "147": "17",
  "148": "22296988580629712647716687824469793827251047,3",
  "444": "11",
  "445": "5",
  "149": "22300690394298297558389305524709723157988299,3",
  "447": "16",
  "449": "7",
  "50": "614917349741827844117546675760945861865641,0",
  "150": "9",
  "151": "22300649194018948939306006165870701814889166,2",
  "454": "4",
  "455": "10",
  "152": "22300742896208940801267700417324719631951335,3",
  "456": "13",
  "457": "15",
  "458": "3",
  "17": "12790377225386209966524760500847998528540,0",
  "51": "111262601708676531585344860020176941679130,1",
  "153": "1",
  "154": "14",
  "155": "22300745198523374879550450432818704052967816,3",
  "465": "3",
  "466": "13",
  "467": "15",
  "52": "39294189108962703377833411619585556389,3",
  "156": "5",
  "157": "22300581385396690248821744618473217958007447,3",
  "471": "11",
  "472": "9",
  "158": "22300664417318391052133164663673219798319155,3",
  "474": "16",
  "476": "17",
  "53": "1414878349319839141322185973011713136285,0",
  "159": "7",
  "160": "22300743717215678358014216260397256992623536,1",
  "481": "1",
  "482": "7",
  "161": "3106655979575648570560098741967680839424952,2",
  "484": "10",
  "485": "4"
}

def get_combination_by_index(n, index):
	combination = []
	current_index = index
	k = 0
	
	while True:
		if current_index < comb_number(n, k):
			break
		current_index -= comb_number(n, k)
		k += 1
	
	remaining_elements = k

	for i in range(n):
		if remaining_elements == 0:
			break
		
		comb_with_i = comb_number(n - i - 1, remaining_elements - 1)
		if comb_with_i <= current_index:
			current_index -= comb_with_i
		else:
			combination.append(i)
			remaining_elements -= 1

	return tuple(combination)

data_table = {}

for k, dat in data.items():
	if len(dat.split(",")) == 1:
		data_table[k] = {"R": int(dat)}
	else:
		data_table[k] = {
			"P": get_combination_by_index(144, int(dat.split(",")[0])),
			"Ask": int(dat.split(",")[1])
		}


s = Solver()

cantidad_de_preguntas = 5

respuestas_list = [
	"Foo",
	"Bar",
	"Baz"
]
fields_list = [
	"Math",
	"Phys",
	"Phil",
	"Engg",
]
personas_list = [
	"Alice",
	"Bob",
	"Charlie",
	"Dan",
]

#Must be equal to the ones above
game_personas_list = [
	Alice,
	Bob,
	Charlie,
	Dan
]
game_fields_list = [
	Math,
	Phys,
	Phil,
	Engg,
]
game_responses_list = [
	Foo,
	Bar,
	Baz,
]

perm_fields = list(permutations(range(len(fields_list))))
perm_respuestas = list(permutations(range(len(respuestas_list))))

#f = order of responses      i = the order of the persons
perm_escenarios = [(f, i) for f in perm_respuestas for i in (perm_fields)]
cantidad_de_respuestas = len(respuestas_list) 


def get_answer(value):
	return perm_escenarios[data_table[str(value)]["R"]][1]


def get_question(node):
	variables_verdaderas = data_table[str(node)]["P"]
	question_maker = data_table[str(node)]["Ask"]
	
	final_question = f"False"
	for var in variables_verdaderas:
		orden_respuestas, orden_fields = perm_escenarios[var]
	  
	  
		question = "True"
		for per_index in range(len(personas_list)):
		  
			question += f" and ({personas_list[per_index]} studies {fields_list[orden_fields[per_index]]})"
			if fields_list[per_index] != "Engg":
				question += f' and ("{fields_list[per_index]}: 1?" is {respuestas_list[orden_respuestas[per_index]]})'
		  

		final_question += f" or ({question})"
  
	return question_maker, final_question


def is_nodo_leaf(value):
	return "R" in data_table[str(value)]


index_problema = 0

class Strategy(Hard):
	question_limit = cantidad_de_preguntas
	
	def solve(self):
		global index_problema
		
		nodo_actual = 1
		index_problema += 1
		
		print(f"------RESOLVIENDO PROBLEMA {index_problema}-------------")
		
		while True:
		
			# print(f"En nodo {nodo_actual}, es leaf: {is_nodo_leaf(nodo_actual)}")
			if not is_nodo_leaf(nodo_actual):
				asker, question = get_question(nodo_actual)
				asker = game_personas_list[asker]
				# print(f"Hice pregunta a {asker}")
				
				respuesta = self.get_response(asker.ask(Expr(question)))
				respuesta = game_responses_list.index(respuesta)
				
				nodo_actual = nodo_actual * 3 + respuesta

			
			else:
				orden_de_fields = get_answer(nodo_actual)
				# print("orden fields ", orden_de_fields)
				for i, g in enumerate(personas_list):
					self.guess[game_personas_list[i]] = game_fields_list[orden_de_fields[i]]
				
				break
		  
		  