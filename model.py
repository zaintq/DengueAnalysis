import MySQLdb
db = MySQLdb.connect(user="root", passwd="", db="containment", host="127.0.0.1")
c  = db.cursor()
BLOCKS = 257
def totalPopulationByBlock():
    c.execute('SELECT block, COUNT(*) FROM `irs_patients` WHERE district = "Lahore" GROUP BY block ORDER BY `irs_patients`.`block`  DESC')
    _dict = {}
    for x in range(0,BLOCKS): _dict[x] = 0
    for row in c.fetchall(): _dict[int(row[0])] = int(row[1])
    return _dict
    
def susceptiblePopulationByBlock():
    c.execute('SELECT block, COUNT(*) FROM `irs_patients` WHERE district = "Lahore" AND tag="irs" GROUP BY block ORDER BY `irs_patients`.`block`  DESC')
    _dict = {}
    for x in range(0,BLOCKS): _dict[x] = 0
    for row in c.fetchall(): _dict[int(row[0])] = int(row[1])
    return _dict

# transmission rate from mosquito to human, estimated: 0.06 - 0.24, average = 0.15, another source = 0.375
# transmission rate from human to mosquito, estimated: 0.30 - 0.51, average = 0.41, another source = 0.375
# biting rate: 0.33 - 1, per day; average = 0.65
# Assumption: Susceptible population = 0.75 * total population of the block
# Average number of female aedes mosquitoes in a house = 7.8

lambdav2h  = lambda s, t: 0.375 * 0.65 * (float(s)/float(t)) * 7.8
tpop, spop = totalPopulationByBlock(), susceptiblePopulationByBlock()
infections = {}

for block in range(0,BLOCKS):
    print block,
    if tpop[block] > 0: print lambdav2h(spop[block], tpop[block])
    else: print 0
    