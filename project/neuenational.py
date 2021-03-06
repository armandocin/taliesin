#! /usr/bin/python

from larlib import *
from myfunctions import *

""" Costruzione della struttra di travi del tetto tramite pyplasm """
V=[[0,0],[0,64.85]]
EV = [[0,1]]
beambase = OFFSET([.5,0])(STRUCT(MKPOLS([V,EV])))
#VIEW(beambase)
beambase = STRUCT(NN(2)([PROD([OFFSET([.5,0])(STRUCT(MKPOLS([V,EV]))),INTERVALS(.05)(1)]),T(3)(1.8)]))
beamcentre = T(1)(.2)(PROD([OFFSET([.1,0])(STRUCT(MKPOLS([V,EV]))),INTERVALS(1.8)(1)]))
#VIEW(STRUCT([beambase,beamcentre]))
beam = STRUCT([beambase,beamcentre])
beamsX = STRUCT(NN(19)([beam,T(1)(3.575)])) #3.575 distanza tra inizio di una trave e inizio trave successiva(compresa larghez trave)
beamsY = T(1)(64.85)(R([1,2])(PI/2)(beamsX))
beams = T(3)(8.6)(STRUCT([beamsY,beamsX]))

""" Costruzione della copertura del tetto """
cover = T(3)(10.45)(CUBOID([ 64.85 , 64.85 , .1 ])) ##lo traslo di 10.25 ovvero 8.4 delle mura + 1.85 lo s spessore del tetto
cover = COLOR(GRAY)(cover)
#VIEW(cover)
#VIEW(STRUCT([cover,beams]))

""" griglia interna """
V,FV = larCuboids([4,4])
V,EV = larCuboidsFacets([V,FV])
trasl = 2*3.577 +.25 + .107 
V = (mat(V)*.810).tolist()
V = (mat(V) + [trasl,trasl]).tolist()
#VIEW(STRUCT(MKPOLS((V,EV))))
smallGrid = T(3)(8.75)(STRUCT(MKPOLS((V,EV))))
smallGrid = OFFSET([.05,.05,.05])(smallGrid)
grid = STRUCT(NN(14)([smallGrid,T(1)((8*.416)+.25)]))
grid = STRUCT(NN(14)([grid,T(2)((8*.416)+.25)]))
#VIEW(grid)

roof = STRUCT([beams,cover,grid])

""" Mura Pianoterra """

filename = "lines/pianoterra.lines"
lines_pt = lines2lines(filename)
V,EV = lines2lar(lines_pt) ##creo Vertici e Spigoli del piano terra
VV = AA(LIST)(range(len(V)))
submodel = STRUCT(MKPOLS((V,EV)))
#VIEW(larModelNumbering(1,1,1)(V,[VV,EV],submodel,0.07))

""" trasform1azione di scala """
assert EV[32] == (30,69) ##spigolo di un muro del pianoterra. 30 e 69 sono i vertici
assert V[30],V[69] == ([0.1155, 0.1169], [0.8828, 0.1169])
V = ((mat(V) - [V[111][0],V[46][1]]) * (50.3/(V[69][0]-V[30][0]))).tolist() ##voglio allineare i pilastri in modo corretto e i vertici 8 e 4 sono quelli che prendo per trovare il vettore di traslazione su x e y

""" Divido i muri di altezza diversa """
#stairsEdges = [4,8,3,84,51,136,73,21,123,116,87,113,5,125,27,127,2,107] ##spigoli elle ringhiere delle scale
#lines_stairs = [[V[EV[e][0]],V[EV[e][1]]] for e in stairsEdges]
ductsEdges = [91,25,78,126,24,26,95,89] ##spigoli dei condotti dell'aria
panelsEdges = [63,10,47,40,58,131,9,17,75,142,132,59,129,114,12,94,33,104,151,46,39,14,134,64,77,147] ##spigoli dei pannelli
wallsEdges = [32,61,106,45]
#pillarsEdges = set(range(len(EV))).difference(panelsEdges+ductsEdges+stairsEdges+wallsEdges)
#pt = (V,[EV[k] for k in panelsEdges+ductsEdges+stairsEdges+wallsEdges])

""" pilastri """
lines = lines2lines("lines/pilastri.lines")
P,EP = lines2lar(lines)
#VIEW(larModelNumbering(1,1,1)(P,[AA(LIST)(range(len(P))),EP],STRUCT(MKPOLS((P,EP))),0.01))
P = ((mat(P) - [P[56][0],P[57][1]])*(50.3/(0.8828-0.1155))).tolist()

""" Faccio l'OFFSET """
#pillarsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in pillarsEdges]))
pillarsHPCs = STRUCT(MKPOLS((P,EP)))
#stairsHPCs = STRUCT(AA(POLYLINE)(lines_stairs))
ductsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in ductsEdges]))
panelsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in panelsEdges]))
#wallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in wallsEdges]))
pillars = COLOR(BLACK)(OFFSET([.05,.05])(pillarsHPCs))
#stairs = COLOR(RED)(OFFSET([.025,.025])(stairsHPCs))
ducts = COLOR(GREEN)(OFFSET([.5,.5])(ductsHPCs))
panels = COLOR(YELLOW)(OFFSET([.25,.25])(panelsHPCs))
#walls = COLOR(CYAN)(OFFSET([.02,.02])(wallsHPCs))

"""Estrusione delle mura piano terra"""
pillarsE = PROD([ pillars, INTERVALS(8.35)(1) ])
#stairsE = PROD([ stairs, INTERVALS(0.9)(1) ])
ductsE = PROD([ ducts, INTERVALS(8.4)(1) ])
panelsE = PROD([ panels, INTERVALS(4.4)(1) ]) ###mettere altezza reale pannelli
#wallsE = PROD([ walls, INTERVALS(8.4)(1) ])
#VIEW(STRUCT([pillarsE,panelsE, ductsE]))

""" Costruzione parte finale pilastri su cui poggia il tetto"""
C,FC = larCuboids([3,1])
C,EC = larCuboidsFacets([C,FC])
#VIEW(larModelNumbering(1,1,1)(C,[AA(LIST)(range(len(C))),EC,FC],STRUCT(MKPOLS((C,EC))),0.7))
scaling = mat([[1.1570376645379952/3,0,0],[0,0.38021634302098306,0]])
C = (mat(C)*scaling).tolist()
cross2 = OFFSET([.05,.05,.05])(STRUCT(MKPOLS((C,FC))))
cross2 = R([1,2])(-PI/2)(STRUCT(MKPOLS((C,FC))))
cross2 = T([1,2])([0.38841066075850605,0.38841066075850605+0.38021634302098306])(cross2)
cross = STRUCT([STRUCT(MKPOLS((C,FC))),cross2])
cross = OFFSET([.05,.05,.05])(cross)
cyl1 = T(3)(.07)(CYLINDER([.16,.06])(100))
cyl2 = T(3)(.13)(CYLINDER([.22,.07])(100))
cyl3 = CYLINDER([.22,.07])(100)
cyl = STRUCT([cyl1,cyl2,cyl3])
cyl = T([1,2,3])([1.1570376645379952/2,0.38021634302098306/2,.05])(cyl)
top = STRUCT([cyl,cross])
tops = STRUCT([T([1,2])(P[k])(top) for k in [57,85,53,79,44,92,101,69]])
tops = T(3)(8.35)(tops)

pillarsE = STRUCT([tops, pillarsE])

""" Costruzione del telaio """
lines = lines2lines("lines/telaiopt.lines")
Z,FZ,EZ,poly = larFromLines(lines)
HH = AA(LIST)(range(len(Z)))
#VIEW(larModelNumbering(1,1,1)(Z,[HH,EZ,FZ],STRUCT(MKPOLS([Z,EZ])),0.1)) 
Z = (mat(Z)-Z[60]).tolist()
sx = 50.15/Z[53][0]; sy = 8.4/Z[53][1]
scaling = mat([[sx,0,0],[0,sy,0]])
Z = ( mat(Z)*scaling ).tolist()

#vetriHPC = STRUCT(MKPOLS((Z,FZ)))
#VIEW(EXPLODE(1.2,1.2,1.2)(MKPOLS([Z,FZ])))
#vetri1 = T(3)(0.075)(OFFSET([0.0,0.0,0.03])(vetriHPC))
telaioHPC = STRUCT(MKPOLS([Z,EZ]))
telaioN = STRUCT([OFFSET([0.1,0.2,0.25])(telaioHPC)])
telaioN = R([2,3])(PI/2)(telaioN) ##mi sposto su x,z in modo da "estrudere" su y
telaioS = T([1,2])([0.25,50.25])(telaioN)
telaioO = R([1,2])(PI/2)(telaioN)

lines = lines2lines("lines/telaiopt2.lines")
Z,FZ,EZ,poly = larFromLines(lines)
HH = AA(LIST)(range(len(Z)))
#VIEW(larModelNumbering(1,1,1)(Z,[HH,EZ,FZ],STRUCT(MKPOLS([Z,EZ])),0.1)) 
Z = (mat(Z)-Z[20]).tolist()
sx = 50.15/Z[80][0]; sy = 8.4/Z[80][1]
scaling = mat([[sx,0,0],[0,sy,0]])
Z = ( mat(Z)*scaling ).tolist()

#vetriHPC = STRUCT(MKPOLS((Z,FZ)))
#VIEW(EXPLODE(1.2,1.2,1.2)(MKPOLS([Z,FZ])))
#vetri2 = T(3)(0.11)(OFFSET([0.0,0.0,0.03])(vetriHPC))
doorsEdges = [43,69,35,12,67,4,109,40,102,28]
doorsHPC = STRUCT(MKPOLS([Z,[EZ[i] for i in doorsEdges]]))
talaioEdges = set(range(len(EZ))).difference(doorsEdges)
telaioHPC = STRUCT(AA(POLYLINE)([[Z[EZ[e][0]],Z[EZ[e][1]]] for e in talaioEdges]))
doors = OFFSET([0.2,0.25,0.25])(doorsHPC)
telaioE = OFFSET([0.1,0.2,0.25])(telaioHPC)
telaioE = STRUCT([STRUCT([doors,telaioE])])
telaioE = R([2,3])(PI/2)(telaioE)
telaioE = T([1,2])([50.25,-0.05])(R([1,2])(PI/2)(telaioE))

telaio = STRUCT([telaioN,telaioE,telaioO,telaioS])
telaio = T([1,2])(SUM([[7.132334158738434, 7.237221425778705],[0,.25]]))(telaio) ##V[30]= [7.132334158738434, 7.237221425778705] (v30 e' il vertice in basso a sinistra delle mura)

"""Visualizzazione Pianoterra completo"""
upLevel = T([1,2,3])([43.5,21.7,5.5])(STRUCT([pillarsE, panelsE, telaio, ductsE, roof]))
#VIEW(upLevel)

""" Creazione mura seminterrato """
filename = "lines/mura-semint.lines"
lines_ps = lines2lines(filename)
V,EV = lines2lar(lines_ps) ##creo Vertici e Spigoli del piano terra
VV = AA(LIST)(range(len(V)))
submodel = STRUCT(MKPOLS((V,EV)))
#VIEW(larModelNumbering(1,1,1)(V,[VV,EV],submodel,0.04))

""" Traslazione nell'origine e scalamento """
V = ((mat(V) - V[299])*108).tolist()
submodel = STRUCT(MKPOLS((V,EV)))
#VIEW(larModelNumbering(1,1,1)(V,[VV,EV],submodel,5))

""" Separazione tipi di muro """
tallWallsEdges = [254,95,140,265,151,7,42,292,274,167,117,244,153,323,296,99,284,271,213,133,315,31]
thickWallsEdges = [134,98,138,58,14,23,175,37,306,142,162,145,260,233,21,236,191,65,108,74,83,12,160,41,169,203,280,18,245,222,27,131,239,127,78,55,310,120,320,261,10,157,132,47,43,221,154,252,46,0,49,170,130,90,29,228]
perimeterWallsEdges = [225,297,224,96,247,180,165,307,235,79,116,291,211,22,281,146,220,192,276,176,87,204,208,311,107,89,45,88,19]
gardenWallsEdges = [66,86,17]
wallsEdges = set(range(len(EV))).difference(perimeterWallsEdges+tallWallsEdges+[328,72,94,231,139]+thickWallsEdges+gardenWallsEdges) #328 spigolo che devo sostituire con la vetrata

tallWallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in tallWallsEdges]))
thickWallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in thickWallsEdges]))
perimeterWallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in perimeterWallsEdges]))
gardenWallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in gardenWallsEdges]))
wallsHPCs = STRUCT(AA(POLYLINE)([[V[EV[e][0]],V[EV[e][1]]] for e in wallsEdges]))

""" Faccio l'OFFSET """
walls = OFFSET([.3,.3])(wallsHPCs)
perimeterWalls = COLOR(BLUE)(OFFSET([.5,.5])(perimeterWallsHPCs))
tallWalls = COLOR(CYAN)(OFFSET([.5,.5])(tallWallsHPCs))
thickWalls = COLOR(GREEN)(OFFSET([.5,.5])(thickWallsHPCs))
gardenWalls = COLOR(YELLOW)(OFFSET([.5,.5])(gardenWallsHPCs))

""" Estrusione muri """
walls = PROD([ walls, INTERVALS(4)(1) ])
perimeterWalls = PROD([ perimeterWalls, INTERVALS(4)(1) ])
tallWalls = T(3)(-2.3)(PROD([ tallWalls, INTERVALS(6.3)(1) ]))
thickWalls = PROD([ thickWalls, INTERVALS(4)(1) ])
gardenWalls = PROD([ gardenWalls, INTERVALS(5.65)(1) ])

""" Creazioni pannelli seminterrato """
filename = "lines/pannelli-semint.lines"
lines_ps = lines2lines(filename)
U,EU = lines2lar(lines_ps)
UU = AA(LIST)(range(len(U)))
submodel = STRUCT(MKPOLS((U,EU)))
#VIEW(larModelNumbering(1,1,1)(U,[UU,EU],submodel,0.04))
assert U[45][0] - U[57][0] == 0.1061
U = ((mat(U) - U[57])*(8.7372/0.1061)).tolist()
U = (mat(U) + [23.6088, 21.481199999999998]).tolist()
basementPanels =  COLOR(YELLOW)(OFFSET([.2,.2])(STRUCT(MKPOLS([U,EU]))))
basementPanels = PROD([ basementPanels, INTERVALS(3)(1) ])

basementWalls = STRUCT([walls, thickWalls, basementPanels, tallWalls, gardenWalls,perimeterWalls])

""" Creazione colonne piccole """
C,FC,EC = createColumns([12,12],[7.2,7.2],.5)
C = (mat(C)+ [(V[309][0]+1.4),7.4]).tolist()
#CC = AA(LIST)(range(len(C)))
#VIEW(larModelNumbering(1,1,1)(C,[CC,EC,FC],STRUCT(MKPOLS((C,EC))),0.1))
tallColumns = (C,[FC[k] for k in [112,113,124,125,40,41,52,53]])
regularColumns = (C, [FC[k] for k in set(range(len(FC))).difference([112,113,124,125,40,41,52,53])])
tallColumnsHPCs = T(3)(-2.2)(PROD([ STRUCT(MKPOLS(tallColumns)), INTERVALS(6.2)(1) ]))
regularColumnsHPCs = PROD([ STRUCT(MKPOLS(regularColumns)), INTERVALS(4)(1) ])
smallColumns = STRUCT([regularColumnsHPCs,tallColumnsHPCs])

""" Creazione colonne grandi """
##colonne grandi verticali
C,FC,EC = createColumns([2,2],[28.8,64.8])
bigColumnsVertical = T([1,2])([61.1,21.1216])(STRUCT(MKPOLS((C,FC))))
C,FC,EC = createColumns([2,2],[64.8,28.8])
bigColumnsOriz = T([1,2])([43.05,39.122])(STRUCT(MKPOLS((C,FC))))
bigColumnsVertical = PROD([ bigColumnsVertical, INTERVALS(4)(1) ])
bigColumnsOriz = PROD([ bigColumnsOriz, INTERVALS(4)(1) ])
bigColumns = STRUCT([bigColumnsOriz,bigColumnsVertical])

""" Costruzione scale interne """
sx = 0.32; sy = V[95][1]-V[257][1]-.5; sz = 2.2/12
stairsOrigin = R([1,2])(PI)(createSteps(11,[sx,sy,sz],True))
stairs1 = T([1,2,3])(V[95]+[-2*sz])(stairsOrigin)
stairs2 = T([1,2,3])(V[231]+[-2*sz])(stairsOrigin)

""" Pavimento del Seminterrato """
lines = lines2lines("lines/pavimento-semint.lines")
W,FW,EW,poly = larFromLines(lines)
WW = AA(LIST)(range(len(W)))
submodel = STRUCT(MKPOLS((W,EW)))
#VIEW(larModelNumbering(1,1,1)(W,[WW,EW,FW],submodel,0.07))
W = ((mat(W) - W[1])*108).tolist()

floors = (W,[FW[k] for k in range(len(FW)) if k!=5 and k!=4])
lower_floors = DIFFERENCE([STRUCT(MKPOLS([W,FW])),STRUCT(MKPOLS(floors))])
lower_floors = T(3)(-2.3)(PROD([ (lower_floors), INTERVALS(.1)(1) ]))
walls_behind_stairs = OFFSET([.5,0])(STRUCT(MKPOLS((W,[EW[5],EW[15]])))) ##muri dietro le scale
walls_behind_stairs = T(3)(-2.3)(PROD([walls_behind_stairs, INTERVALS(2.3)(1) ]))
regular_floors = PROD([STRUCT(MKPOLS(floors)), INTERVALS(.1)(1) ])
basementFloors = STRUCT([regular_floors,lower_floors])

basementWalls = STRUCT([basementWalls,walls_behind_stairs])

""" Costruzione telaio e vetrata seminterrato """
lines = lines2lines("lines/telaio-semint.lines")
P,FP,EP,polygons = larFromLines(lines)
#VIEW(larModelNumbering(1,1,1)(P,[AA(LIST)(range(len(P))),EP,FP],STRUCT(MKPOLS((P,EP))),0.1))
P = (mat(P)-P[71]).tolist()
sx = 93.5328/P[2][0]; sy = 3.75/P[2][1]
scaling = mat([[sx,0,0],[0,sy,0]])
P = ( mat(P)*scaling ).tolist()

#glassWallsHPC = STRUCT(MKPOLS((P,FP)))
#vetri3 = T(3)(0.11)(OFFSET([0.0,0.0,0.03])(glassWallsHPC))
telaio_semint = OFFSET([.1,.25,.25])(STRUCT(MKPOLS([P,EP])))
vetrata_semint = R([2,3])(PI/2)(STRUCT([COLOR(GRAY)(telaio_semint)]))
vetrata_semint = T([1,2])([20.4,94.1328])(R([1,2])(-PI/2)(vetrata_semint))

lowerLevel = STRUCT([basementFloors,vetrata_semint,basementWalls,bigColumns,smallColumns,stairs1,stairs2])
#VIEW(lowerLevel)

""" Costruzione pavimento podio/tetto seminterrato """
lines = lines2lines("lines/tetto-semint.lines")
U,FU,EU,poly = larFromLines(lines)
#VIEW(larModelNumbering(1,1,1)(U,[AA(LIST)(range(len(U))),EU,FU],STRUCT(MKPOLS((U,EU))),5))

U = (mat(U)-U[3]).tolist()
U = ((mat(U)*(94.6328/U[2][1]))+ [20, 0.0]).tolist()

stairsHoles = (U,[FU[5],FU[6]])
basementCeiling = DIFFERENCE([STRUCT(MKPOLS((U,FU))), STRUCT(MKPOLS(stairsHoles))])
basementCeiling = T(3)(4)(PROD([basementCeiling, INTERVALS(0.15)(1)]))

staircase1 = (U,[FU[k] for k in range(4)])
upFloorHPC = DIFFERENCE([STRUCT(MKPOLS((U,FU))), STRUCT([STRUCT(MKPOLS(staircase1)),STRUCT(MKPOLS(stairsHoles))])])
#VIEW(EXPLODE(1.2,1.2,1.2)(MKPOLS(staircase1)))

upFloor = T(3)(4.15)(PROD([upFloorHPC, INTERVALS(1.5)(1)]))
upFloor=STRUCT([basementCeiling,upFloor])

"""
scalinata esterna 1
"""
sx = (U[10][0]-U[7][0])/8; sy=U[7][1]-U[1][1]; sz=1.44/8
steps = createSteps(8,[sx,sy,sz])
steps = T([1,2,3])([U[1][0],U[1][1],5.65-2*sz])(steps)
lastStep = STRUCT(MKPOLS((U,[FU[3]])))
lastStep = T(3)(4.15)(PROD([lastStep, INTERVALS(0.06)(1)]))

ramps = (U,[FU[0],FU[1]])
tri = SIMPLEX(2)
sx1 = U[10][0]-U[7][0]
sy1 = U[8][1]-U[7][1]
ramp1 = T(2)(1)(R([2,3])(PI/2)(PROD([tri,INTERVALS(1)(1)])))
ramp1 = S([1,2,3])([sx1,sy1,1.44])(ramp1)
ramp1 = T([1,2,3])([U[7][0],U[7][1],4.21])(ramp1) ##4mt le mura, 0.15 il tetto, 0.6 l ultimo step = 4.21
sy2 = U[1][1]-U[0][1]
ramp2 = T(2)(1)(R([2,3])(PI/2)(PROD([tri,INTERVALS(1)(1)])))
ramp2 = S([1,2,3])([sx1,sy2,1.44])(ramp2)
ramp2 = T([1,2,3])([U[0][0],U[0][1],4.21])(ramp2)

staircase1 = STRUCT([lastStep,steps,ramp1,ramp2])

#VIEW(STRUCT([basementFloors,frameAndWindows,basementWalls,bigColumns,smallColumns, staircase1,upFloor]))

""" Costruzione scale interne """
sy=(U[20][0]-U[18][0])/2; sz=5.55/32
flight1origin = createSteps(15,[.27,sy-.1,sz],True)

tanBeta = (sz*15)/(.27*15)
tensor = MAT([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,-tanBeta,0,1]])
sideStair = STRUCT(NN(2)([tensor(CUBOID([.27*15,.05,sz*2])),T(2)(sy-.05)]))
flight1origin = R([1,2])(PI/2)(STRUCT([T(2)(.05)(flight1origin),sideStair]))

flight2origin = R([1,2])(-PI)(flight1origin)

flight1 = T([1,2,3])([U[18][0]+sy,U[18][1],(5.65-sz*2)])(flight1origin)
flight2 = T([1,2,3])([U[18][0]+sy,U[18][1]+.27*15,(.1+sz*14)])(flight2origin)
sx = (U[19][1]-U[18][1])-.27*15
largeStep1 = T([1,2,3])([U[19][0],U[19][1]-sx,(.1+sz*15)-sz])(CUBOID([(U[20][0]-U[18][0]),sx,2*sz]))

flight3 = T([1,2,3])([U[14][0],U[14][1],(5.65-sz*2)])(flight2origin)
flight4 = T([1,2,3])([U[15][0],U[15][1]-.27*15,(.1+sz*14)])(flight1origin)
largeStep = T(2)(U[16][1]-U[19][1]+sx)(largeStep1)

stair1 = STRUCT([largeStep1,flight1,flight2])
stair2 = STRUCT([flight3,flight4,largeStep])
#VIEW(STRUCT([stair1,stair2]))

""" Ringhiera """
paletto = CUBOID([.04,.04,1])
dx = ((U[21][0]-U[19][0])+0.04)/3
dx2 = (U[21][0]-U[19][0])/4
dy = ((U[19][1]-U[18][1])+0.04)/5
paletti = STRUCT(NN(4)([paletto, T(1)(dx)]))
paletti = T([1,2,3])([U[19][0]-.04,U[19][1],5.65])(paletti)
palettiY = STRUCT(NN(5)([paletto, T(2)(-dy)]))
palettiY = STRUCT(NN(2)([palettiY, T(1)(dx*3)]))
palettiY = T([1,2,3])([U[19][0]-.04,U[19][1]-dy,5.65])(palettiY)
palettiX = STRUCT(NN(2)([paletto, T(1)(dx2)]))
palettiX = T([1,2,3])([U[18][0]+(2*dx2-.04),U[18][1]-.04,5.65])(palettiX)

orizontalRail = CUBOID([(U[21][0]-U[19][0])+0.08,.04,.02])
orizontalRail = STRUCT(NN(2)([orizontalRail,T(3)(-.8)]))
orizontalRail = T([1,2,3])([U[19][0]-.04,U[19][1],6.65])(orizontalRail)

orizontalRail2 = CUBOID([dx2*2+.04,.04,.02])
orizontalRail2 = STRUCT(NN(2)([orizontalRail2,T(3)(-.8)]))
orizontalRail2 = T([1,2,3])([U[18][0]+(2*dx2-.04),U[18][1]-.04,6.65])(orizontalRail2)

verticalRail = CUBOID([.04,(U[19][1]-U[18][1])+0.04,.02])
verticalRail = STRUCT(NN(2)([STRUCT(NN(2)([verticalRail,T(3)(-.8)])),T(1)(dx*3)]))
verticalRail = T([1,2,3])([U[18][0]-.04,U[18][1]-.04,6.65])(verticalRail)

railing1 = STRUCT([paletti,palettiX,palettiY,orizontalRail2,orizontalRail,verticalRail])

paletto2 = CUBOID([.04,.04,1.02])
palettiS = STRUCT(NN(4)([T(2)((.27*15-.08)/4),paletto]))
railingS = T(3)(1)(STRUCT(NN(2)([CUBOID([.04,.27*15-0.04,.02]),T(3)(-.8)])))
tensor = MAT([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,-tanBeta,1]])
handrail = T(2)(.04)(tensor(STRUCT([palettiS,railingS])))
handrailA = T([1,2,3])([U[18][0],U[18][1]-.04,5.65])(STRUCT([paletto2,handrail]))
handrailB = T([1,2,3])([U[18][0]+(2*dx2-.04),U[18][1]-.04,5.65])(handrail)
handrailC = STRUCT([T([1,2])([-.04,-.04])(paletto2),R([1,2])(PI)(handrail)])
handrailC = T([1,2,3])([U[18][0]+(2*dx2+.04),U[18][1]+(.27*15)+.04,(.1+sz*16)])(handrailC)

handrail1 = STRUCT([handrailA,handrailB,handrailC,railing1])
handrail2 = T(2)(U[14][1])(S(2)(-1)(T(2)(-U[18][1])(handrail1)))

stair1 = STRUCT([largeStep1,flight1,flight2,handrail1])
stair2 = STRUCT([flight3,flight4,largeStep,handrail2])

""" Costruzione seconda parte del podio """
lines = lines2lines("lines/podio.lines")
P,FP,EP,polygons = larFromLines(lines)
#VIEW(larModelNumbering(1,1,1)(P,[AA(LIST)(range(len(P))),EP,FP],STRUCT(MKPOLS((P,EP))),0.07))
P = ((mat(P)-P[19])*(83.71803810292634/(P[19][1]-P[2][1]))).tolist()
#assert U[3] == [108.4258050454087, 94.6328]
P = (mat(P)+[108.4258050454087, 94.6328]).tolist()

staircases = (P,[FP[k] for k in range(1,6)+[7]])
podium = DIFFERENCE([STRUCT(MKPOLS((P,FP))), STRUCT(MKPOLS(staircases))])
podium = PROD([podium,INTERVALS(5.65)(1)])
#VIEW(STRUCT([podium,basementWalls,upFloor]))

""" Costruzione delle scalinate """

sx = (P[7][0]-P[1][0])/15
sy = P[7][1]-P[8][1]
sz = 5.65/29
sc2p1 = createSteps(15,[sx, sy, sz])
sc2p1 = T([1,2,3])([P[7][0], P[7][1],(5.65-2*sz)])(R([1,2])(PI)(sc2p1))

largeStep = PROD([STRUCT(MKPOLS((P,[FP[1]]))), INTERVALS(sz)(1)])
largeStep = T(3)(sz*12)(largeStep)

sc2p2 = createSteps(10,[sx, sy, sz])
sc2p2 = T([1,2,3])([ P[0][0], P[0][1], sz*11 ])(R([1,2])(PI)(sc2p2))

secondLastStep = createSteps(1,[(sx+0.1269078748692274) , (sy+.2), sz])
lastStep = createSteps(1,[(2*sx+0.1269078748692274), (sy+.6), sz])
secondLastStep = T([2,3])([-0.4,sz])(R([1,2])(PI)(secondLastStep))
lastStep = R([1,2])(PI)(lastStep)
last2steps = T(2)((sy+.6))(STRUCT([secondLastStep,lastStep]))

staircase2 = STRUCT([sc2p1,sc2p2,largeStep, T([1,2])(P[22])(last2steps)])

""" Creazione scalinata frontale """
sx = (P[4][0]-P[5][0])/3
sy = P[14][1]-P[5][1]
sz = 1.5/7
staircase3 = T([1,2,3])([ P[5][0], P[5][1], (5.65 - 2*sz)])(createSteps(3,[sx,sy,sz]))

middleStep = T(3)(5.65-5*sz)(PROD([STRUCT(MKPOLS([P,[FP[5]]])), INTERVALS(sz)(1)])) 

secondLastStep = createSteps(1,[(sx+0.25724569230249017) , (sy+1.34), sz]) #P[20][0]-P[9][0]=0.25724569230249017
lastStep = createSteps(1,[(2*sx+0.25724569230249017), (sy+(1.17*2)), sz]) #P[11][1]-P[12][1] = 0.771737076907506
secondLastStep = T([2,3])([.5,sz])(secondLastStep)
last2steps = T([1,2,3])([P[12][0],P[12][1]-.4,4.15])(STRUCT([secondLastStep,lastStep]))

staircase3 = STRUCT([staircase3,middleStep,last2steps])

""" Creazione cornicione del podio """
c1 = STRUCT([T([1,3])([20,5.77])(CUBOID([1.2, 94.6328, .5])), 
	T([1,2,3])([20.2,0.2,5.65])(CUBOID([.8,94.2328,.12]))]) #U[3] = [20.0, 0.0]
c2 = STRUCT([T([1,2,3])([21.2,1.2,5.77])(R([1,2])(-PI/2)(CUBOID([1.2, 81.09520387487387, .5]))), 
	T([1,2,3])([21,1,5.65])(R([1,2])(-PI/2)(CUBOID([.8, 81.09520387487387, .12])))]) #U[12][0]-U[3][0] = 82.29520387487388
c3 = STRUCT([T([1,2,3])([21.2,94.6328,5.77])(R([1,2])(-PI/2)(CUBOID([1.2, 20.636420209853284, .5]))), 
	T([1,2,3])([21,(94.6328-.2),5.65])(R([1,2])(-PI/2)(CUBOID([.8, 20.636420209853284, .12])))]) #P[8][0]-U[2][0] = 20.636420209853284
c4 = STRUCT([T([1,2,3])([U[8][0]-1.2,(U[8][1]+1.2),5.77])(R([1,2])(-PI/2)(CUBOID([1.2, P[3][0]-U[8][0], .5]))), 
	T([1,2,3])([U[8][0]-1,(U[8][1]+1),5.65])(R([1,2])(-PI/2)(CUBOID([.8, P[3][0]-U[8][0], .12])))]) #U[8]=[93.92053529767912, 10.952958789101919] P[3][0]-U[24][0] = 36.26825531652128
c5 = STRUCT([T([1,2,3])([P[3][0]-1.2,P[3][1],5.77])(CUBOID([1.2, P[23][1]-P[3][1], .5])), 
	T([1,2,3])([P[3][0]-1,P[3][1]+.2,5.65])(CUBOID([.8,(P[23][1]-P[3][1])-.4,.12]))]) #P[23][1]-P[3][1] = 
c6 = STRUCT([T([1,2,3])([P[9][0]-1.2,P[9][1],5.77])(CUBOID([1.2, P[17][1]-P[9][1], .5])), 
	T([1,2,3])([P[9][0]-1,P[9][1]+.2,5.65])(CUBOID([.8,(P[17][1]-P[9][1])-.4,.12]))])
c7 = STRUCT([T([1,2,3])([P[18][0],P[18][1],5.77])(R([1,2])(-PI/2)(CUBOID([1.2, (P[17][0]-P[18][0])-1.2 , .5]))), 
	T([1,2,3])([P[18][0]+.2,P[18][1]-.2,5.65])(R([1,2])(-PI/2)(CUBOID([.8, (P[17][0]-P[18][0])-.8, .12])))])
pattern = (P[14][1]-P[5][1])+1.2
c8 = STRUCT(NN(2)([R([1,2])(-PI/2)(CUBOID([1.2, (P[11][0]-P[5][0])-1.2 , .5])), T(2)(pattern)]))
p8 = STRUCT(NN(2)([R([1,2])(-PI/2)(CUBOID([.8, (P[11][0]-P[5][0])-1.2 , .12])), T(2)(pattern)]))
c8 = STRUCT([T([1,2,3])([P[5][0],P[5][1],5.77])(c8), 
	T([1,2,3])([P[5][0]+.2,P[5][1]-.2,5.65])(p8)])

cornicione = STRUCT([c1,c2,c3,c4,c5,c6,c7,c8])
podiumAll = STRUCT([upFloor,podium,cornicione,staircase1,staircase2,staircase3,stair1,stair2])

VIEW(STRUCT([upLevel, lowerLevel, podiumAll]))
"""
hpcs = [roof, pillarsE, ductsE, panelsE, STRUCT([gardenWalls, perimeterWalls]) , STRUCT([basementPanels,walls,tallWalls,thickWalls,
 smallColumns,bigColumns]),basementFloors, basementCeiling, STRUCT([podium,upFloor]),
  STRUCT([staircase1,staircase2,staircase3]), STRUCT([stair1,stair2]),STRUCT([handrail1,handrail2]), cornicione, 
  STRUCT([telaio,frameAndWindows])] 

exportObjs(hpcs)"""
