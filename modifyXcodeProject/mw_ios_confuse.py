#coding=utf-8
import imp
import sys
imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

import chardet

# 导入 random(随机数) 模块
import random

genest_word=["ruminaddresseur","theseable","finaleur","perioder","phanerth","flavious","culturality","tachosion","irat","ectomyical","controlition","juvenuous","establishfication","ter","born",
             "narpeopleious","decisionory","hugehood","failkin","prettyation","nominetic","tactivity","consumerious","piececy","owneraneous","strigosohise","misce","health","androistic","fingerine","osteoty","signship","amatade","in1ics","mitial","non",
             "theroprocess","barb","intraacious","assume","tenssure","eph","cinality","faran","opoterent","corticoise","kakor","shot","withoutatory","pteryess","traagreeory","decortwo","takeize","axilability","sputmyselfress","roadar","trigesimadministrationtic","voluntseaaceous","mentionition","gastr","by","leisome","hyofaction","probule","mergen","whileible","myfold","amph","nationar","nugacical","velocair","cortico","gelatworkeracy","pathorganizational","villality","tomy","caesability","publiceer","cardinency","transth","untilish","respondatic","lifeence","admost","penive","polemization","TV","forward","kinoity","removeon","interesting","significantatory","gubernty","boload","listening","popularsion","periodth","TVon","gramatory","privenne","suivity","skinmost","misce","examplement","sebproduction","acerbeer","degreeer","rolelike","nespeechation","thusality","radiofold","felicitine","fundency","surfaceite","dreamition","argueian","limacenne","armit","falline","sexagesimhood",
             "fungory","acceptable","treeary","autoization","storyery","workeresque","relationshipit","plagi","directorible","sexity","trabwhileeer","aer","trachyite","lievsion","environmentlike","rhagbusinessitor","contronearlyian","inside","avision","could","clystify","awayaneity","noct","sisterence","lapssome","salvar","quisitage","pancreaticoouratory","orecticly","clos","personalfaction","hereeous","physicalitive","clystular","peculiary","centen","litheur","thalass","dayful","thermive","amount","lastsure","belliice","maintainad","newseer","theirel","probablyorium","pavise","suf",
             "tortaneous","circ","scrupulmodern","cytoaddressress","difficultade","ticeous","primation","phyllality","tableitor","eveningity","morningeer","specificling","circfaction","icosenne","takeward","orderproof","loseeer","manthpersonture","listenee","cosmo","skillous","belliproof","ludacy","customerivity","duringade","in2oldot","articleesque","tricenosity","fascsion","omoshe","ultimwise","tradeacious","barkin","phyllette","piteacity","fallac","floor","supinee","finishing","goator","laminoilfaction","tenast","uliginivity","heliopoormost","pollinfaction","algiaistic","beyondette","travel","himive","vocate","fandal","impactfication","followitude","drawaceous","oviacle","philehood","preventacious","cameratory","stinct","skillhood","valueast","hit","mirad","weaponaneity","a","pontonty","poieard","thenel","misceity","meterosity","liquosity","judicfederalsure","quassproof","novendecose","edrecognizeee","fessadditude","granish","importantly","oncy","issue","interest","collectionlet","frontster","acusive","jejunform","ran","pollicing","phalarsexual","volunt","statementify","lotability","nicefaction","temptier","senitor","dogmcareeratic","ficidifferenceical","partyade","flamproof","is","flulet","montfic","herselffication","effectise","hardan","pubertlet","satacle","siccee","ornith","tent","siphotion","meta","audacprepareeer","crutable","houseair","manyical","owny","apert","dextrful","scriptance","Mrance","proli","intoate","publicer","uvulokin",
             "orderible","neics","basiial","theywise","doxyetate","sculp","damnserveion","wrong","fearacity","largitude","detailion","hyoaceous","traneer","emesi","cityry","becomeetic","petrneverive","lawyerfaction","ectomyize","hiemise","peaceless","salin","synuous","earlyian","sometimes","foveth","posic","todayty","existary","systemative","tetanature","step","polic","bromoial","sessartior","manage","apertary","edization","caulstreetite","arriveuous","responseability","includingical","faciad","counter","censlike","glaciice","hemtheetic","physical","participanteer","similage","newsance","camerlistal","sumuous","heliot","noteitious","courtetic","meriteous","gestfier","quisitaster","similaror","virraceette","hyoress","focusfic","tachage","gelat","productite","tensette","ofdom","axilid","oedfic","undeneur","poseous","rhizlaughfy","fensice","officeress","givetion","quint","image","attentioneer","cordaire","howarian","platyent","magnid","jurisitive","proliess","feminress","nor","syltrue","painting","presential","issueular","boleer","cardior","pantoial","owning","pinncy","propertyible","evenence","fingerproof","heater","carcinive","otit","mitfier","standcy","cerebrofication","polliclossatic","therory","treeeous","eastie","budgetile","item","unguluous","dentorium","lystmost","ballostudent","loseality","admitlet","ovience","writeritude","superise","ontee","lecithetic","salinatic","whatty","cyclish","catenade","ander","throughtion","dinnerible","hypn","grat","relationshipia","claustrenne","dubacity","signsure","balo","foreignage","upion","sevenier","ossshoulderful","pleurtic","this","lessfication","roborious","oriite","angmost","storyally","experiuous","rugeer","soliule","opiist","hedratory","ornful","fineular","kitchen","vilmuch","claditor","visco","pungy","country","baseal","clavience","scientistic","trichoaceous","smileaneous","strong","uncper","sagittwise","everyonean","oncefaction","claustroawayaster","pathaneous","theirast","juern","macree","honorjobuous","totirightally","hoplaceous","dysify","executive","juriblackair","superward","ok","long","regionel","gonoard","raphospitalor","soonage","sol","market","momentitious","billiondom","senraiseetic","xiphbadar","newsacle","enterics","candivity","gardenenne","seiblueory","timacle","quisitard","require","sumptfier","nomiarium","hedoistic","concernon","recordsion","docible","plenette","parith","meet","catharery","sacrofindary","umbrress","lepidistic","mixtfaction","newspaperfaction","outsidement","tim","septuagesim","eph","genitial","silviine","treatmentproof","scabioing","gestose","whichness","mar","mesterety","parlly","ef","superor","ratefier","spersial","propertyent","cupacle","vag","ventrier","postulry","tortuion","individuallike","cerebro","micrie","cretet","sessfier","strigetic","generskillent","locoine","capel","operar","viscosiior","turnion","runsome","oplso","bookist","cenast","periast","fugality","famable","lacerics","pollinrealize","oncusoon","colorile","tomoling","frigitude","onize","writear","participant","pylel","epiform","scientistance","pauc","orexiabying","ofar","citizen","popular","whatatic",
             "phanee","bag","furtate","nunciling","tropsome","bradyacity","field","tuss","sidine","expectic","percreate","rancate","machineaire","trabtherean","thalassstudentistic","deadice","genuosity","receiveuous","oedern","in2eyelike","pharmacie","dropad","fugitia","callment","tractress","genar","speretic","tonight","findior","plutform","turpety","priviuous","whileen","gamb","photet","coise","malleo","mindage","pushity","homin","fullity","oeco","todayation","tenth","hepar","whileaneous","cruous","section","operance","manysome","plecnationarium","pic","lawyerous","manyature","threefold","otherly","dorspoorency","thusmost","fatuular","texly","heatacy","billion","null","treiskaidekdifficultular","Democratid","lect","bellisingleality","trichoise","bilotheron","zygly","dealhood","dich","lacrim","whato","vect","acuold","persicice","populationship","logywriteeer","irist","cancer","patternot","strigos","motherite","coldness","sonan","regal","cultureization","anthohood","equifearless","TVing","tremive","alreadyenne","groundage","timeetic","presentably","graphproperty","minhood","fallery","plagi","clement","januose","vestfold","pteroular","anyone","rhomb","voiceet","soleninterestate","playoon","war","tachoitor","curs","commonlike","mensurhomeing","frontor","machineitious","psych","enneaate","junct","motish","current","dipsyfic","thingress","archaify","radioform","mustor","phlegward","sili","certain","causeety","emesisatory","tenacfightenne","openfold","spuful","existence","agoist","ultimorium","psychity","sinuary","gamsion","ativity","fusise","bigth","ambdom","ternling","sheel","phas","myselfitive","dictacious","armesque","magazineit","towardose","volittableuous","sceneacle","recentward","dayistic","standization","sidusoneous","plegan","juxta","hexgeneralitude","dieform","sonous","onomaseasthood","friendive","riskard","pleasdom","sinusern","monstrat","temporent","glassivity","arthrity","boardibility","scabimeasure","individualar","testier","imageward","quinqueproof","dictical","flectan","muls","throughly","ordereer","dactyliooon","insideibility","pratform","heart","pugnalwaysive","some","scaphchooseory","seiics","numberuous","rapt","stopit","managearium","awayose","sonain","microal","otherproof","biten","color","anthraular","windacious","felicitsceneice","pictureant","sizeess","kudoacy","prehensad","someress","socition","bitwise","successeer","general","salvosity","effortress","stringature","minition","somni","toxreasonature","literen","secutty","agreelet","pessimthosefaction","lepidoetic","euness","obory","tradeeur","concernar","ennade","claustro","ballesque","nucassumeosity","motherly","somn","bilain","dichoator","polyoon","nunciess","liminture","ablecy","phesuous","cephal","listen","vali","fund","flecttic","axilia","microage","suddenlyfic","archsounden","sebiism","lawyereous","docureduceia","pubertette","sectionitor","visitward","platttic","manage","spondylmost","rhabdy","describe","tellivity","windot","shoot","relateior","paleency","typoyarden","film","myit","healthative","nicearium","whoseious","multaical","naturalible","largate","basiern","optionster","throw","amongproof","scene","pacin","nuchsure","sisterable","sitous","simul","treateous","gemmable","severalist","cinct","letenne","gladiitious","etymfication","boyior","sect","professionalair","newsitor","lysern","vidcontainling","extro","upard","cupitious","temptprove","hugeent","natural","leaderet","collivity","greatistic","hypnoent","micrthousandfold","foldsee","colice","kinyearful","pel","preterize","cupability","serfaction","chrysaster","small","elseity","cracyise","pinguwait","visia","passer","hippable","plesiade","preia","method","rav","blueish","civilhood","plebature","singatic","smileship","nodo","movementorium","punhood","feelsure","vendit","defenseade","six","fancaneous","pontful","greatty","electionard","weous","paleoality","errite","perreduceive","meaneous","thyretic","identifyar","conenne","im","oligard","extroaire","fieldor","trapezment","trophitious","archeoard","why","durist","family","ratherature","odontize","ownerot","felment","challengeetic","pilfreeation","prepareative","tentile","lamnlamellatory","interestition","finallyize","cotylain","salative","traditionalia","understandier","nomency","rangeion","bitette","uvdom","preacious","stigmatorium","youraceous","osair","thousandlet","passerwise","trophtrialior","plantment","stimulian","claustreer","audienceally","sonage","factibility","biblfold","puni","genyfier","ableetic","decorrise","first","olecranage","wantlet","life","liberling","bac","extrael","dow","themselvesite","mensesque","sixster","holdery","uttic","homeacity","theoress","librsive","scensate","heartitude","negmost","perform","caudad","respondorium","parentless","crasssuffercy","insideenne","trud","functparticularlyade","digmacity","memberive","animalitive","centesimible","put","growity","vulsstayar","urgile","emetoconsumer","patrplayize","stearing","stenless","angular","holitor","scopeincludeaneous","booket","alone","log","coprorium","raphious","sacroose","herlawyerator","pogonar","cantfication","simpleeous","turbin","decadeing","crut","electroant","reachify","irasc","nigrment","ledic","either","kudoless","pangist","valless","sexfold","financialize","sortical","plauset","althoughity","lookature","raiseet","nexization","labable","scoreast","lamino","altivity","juvenency","west","plectice","caldion","chirible","scendsome","segetette","howfy","covercy","ros","despiteproof","plur","scyphan","howeverenne","doctorability","lotarian","vehmost","cruccampaignacious","fromaster","frug","septiawayosity","exoate","creasfaction","rapac","scriptacious","gestcostency","northian","op","informationition","semblknowate","media","fungesque","clamsayature","malleo","igous","liqutruthia","courseine","plurimen","iratry","beautifulate","everyoneate","jursure","kakocatchence","ludacity","arriveion","tauraneity","psammosity","themselvesly","byair","notator","totaleur","muno","projectose","improve","buccseaably","nearlyile","cruci","a","paedate","using","work","focacle","pudeify","paternast","phyt","bibital","lexicoel","causemost","falctreatful","pancreatoitious","caten","areaial","ludprofessorible","ethuous","keyorium","phragmad","sceptward","methodeer","along","current","attorneyature","menilet","quinqueactuallyhood","squallayetic","autho","flav","scandature","colorian","movieite","cheiroistic","regkindlike","billionar","terrster","unguiic","capsputor","sparsism","octogen","misoory","ventr","here","almostful","higharium","ramably","spendie","allaneity","finally","sputless","dealot","nothitious","thyrcollectionior","mesterization","oncusial","revealor","toxfaction","hered","severalibility","faciian","reachule","debateial","edgeety","tersative","seniorsure","lystcontinueit","sinator","gnorness","participantit","countryive","scaphics","oner","finalar","habilably","aroundorium","conbeautifullet","puthour","peccesque","culinible","like","addsive","semiair","credia","fodize","autkin","fivecy","shoulderish","predability","likeise","popularern","studenter","mustcy","ptera","decaly","somebodyical","dis","environmentth","materlateward","section","herster","nubnaturalain","culinive","patientics","micrard","peccular","vestfication","hotelness","octavacy","opto","moreenne","offication","bookibility","bager","live","vigenosity","trop","chairarian","brontcommunity","cidose","animalaster","exist","evening","synsome","staffan","dign","manade","shareish","mens","knowatic","policain","vomyourselfise","necr","pugnably","chrom","betterose","mancyless","corporeur","quadrsendality","studwise","minim","voro","frontmeetie","dormic","desdata","dayia","diee","ligive","writer","ecclesofor","liveeous","part","phantory","treatmentress","oldage","ord","modelship","philedefenseing","nemalet","nothingfy","sapi","pacard","cornthank","cedbelieveose","crimeacy","machineivity","prettyatory","denlarge","viscosiry","oncoform","tomoeous","taxify","myrmecish","gonoet","phragmward","yeahhood","player","vellship","testast","amourice","scienceation","itinerency","productionator","transblood","gnarfier","audeur","telokitchen","manish","recordwise","scriptbestsion","soletsuddenly","phasyesque","pulllike","sortice","program","Mrice","availablester","audienceo","glabralongosity","ossive","windowesque","churchform","anthropside","tostite","brachyial","fulgsimplester","fricad","quadragesim","itemence","juvenmustess","anythingate","ticly","mereur","military","productionor","scanditive","tenaciship","plectality","nugatacious","expertcy","tropice","cut","tergimost","axieous","deacity","projectile","pterpartner","amountster","bursless","levely","American","student","hendecageeer","givetion","captacy","othersosity","paleostudyist","officeary","corollade","athlsive","creatproof","platinowise","anlet","half","logyion","continueaneous","ceptator","fringquestion","contrenetworkic","bothfication","phantaneous","eeconomyar","whiteo","baseally","firm","us","arch","pedojustmost","figaster","audi","opin","micbrotheraster","resourceee","candably","proximry","sinceaster","ethmI","than","pedocy","lesenne","stirpion","throwly","didactial","shorteous","vicoveritude","hairatory","laminator","silismilefic","attackade","both","awayade","lysoon","potibility","pneu","plecitive","cingular","phetcoldmost","dosaster","cheirosion","caulo","westernth","nugaible","smile","cinctoon","guttform","beid","its","acious","pendation","worryise","color","sali","lentshouldair","tetrage","ant","fric","exper","hieroo","biopracticeery","merward","xanthage","vertpartysure","ceramacy","trachylet","individualation","everyoneitude","travelern","buildmost","jug","plethmessagetion","captexplainine","rancation","xerative","practice","heavyite","perhapseer","vertard","significantation","nudast","horreallyaceous","vertproof","omasthing","bringate","axioeous","clavicoverion","theid","ed","planish","rhombry","orexiofficeation","nothingetic","paucitious","likeuous","volatwindosity","pluriming","peleer","falsamount","volitaceous","vigesimatic","calypaceous","situationette","auous","luminon","millenency","occuring","treatice","lookmost","iter","chelon","taskion","meile","curv","augad","workive","speakish","expect","sten","euory","sceneish","ornithoivity","floorlet","givement","beatess","arboriarium","acerblet","managead","billian","fant","legitimary","meretship","borance","idecustomer","peopleie","flux","moreality","pteraoon","productionar","northtic","graphyization","pyr","talidark","actionfic","barally","along","politine","palinance","proprieur","quickly","menern","found","vagaquestionship","tetanomethodfy","product","continueatory","foot","quinform","mayture","everythingability","longency","munofold","vulsmissionous","withinivity","autfication","photacious","ungulical","sinistrition","dermaneity","riskesque","miran","sorptise","couple","nodious","coranyone","pecchood","merition","pans","nigrty","wallity","theirian","becauseness","generalar","ctenie","squarrostaxacy","emesisfallate","onchoety","precly","phloearian","factorfic","menotask","centritive","comior","cruciant","templ","sembl","middleature","nightit","torristic","youoon","ecoia","somedom","auriuous","rightad","bronchast","opoterture","niceo","argentorium","hugeaneity","radicive","existeur","authorose","cipitalongible","bilster","whoth","crucior","accountless","theness","employeefier","difficulteous","fulminory","problearnful","themular","ideaitive","paternably","trochindeed","iqusion","sequeous","ominfold","actionen","gonAmerican","sell","flamaceous","willent","plur","conion","expert","threat","nevering","baselike","ursfinditude","Iarium","und","dactyloacy","caloring","pastent","circumize","motheritor","utry","untilacious","bol","placeibility","shortal","tedithoseia","pall","risant","puberably","nugatic","dinnerian","equinbabyile","duringatory","plupreventatory","scene","lapsbuildingeer","grav","fossative","PMaster","chant","traical","failable","backtion","collectionule","vitellnetworkeous","atid","herpnoror","storedom","ballo","soror","lightfier","fineistic","claustracle","maintaino","phylcoachivity","politics","bothitive","roborory","macrer","recently","desious","vulsatory","scutish","western","travel","cruactivityier","lossfold","applyeous","fligorium","traumar","away","picturesure","larveur","pansization","certain","arriveern","managementtion","pantoier","environmentitude","hugear","cusp","howative","scabiaster","ficency","gas","munard","earlyth","jurismost","agr","ocition","multatably","tedikitchenon","umbrosity","sexagenproof","her","coldally","orexiing","about","hundredaire","miasmat","algenne","recentee","tropoon","specialcy","policyatory","thingian","dyso","andity","creaspointitude","enterar","growent","pathy","spaceibility","lytling","ctenment","klept","fisseastery","hospital","hel","nugament","includingule","ali","vicesimular","gemule","clamious","pedoherselfward","beyondate","candidateture","dipsodeath","meningling","polresearchsion","chairsive","prav","rurister","spicety","duringize","bronchical","prepareosity","podally","care","mening","pteroern","nephrstorelike","tripscourtward","miasma","largetic","outsidester","countryard","coach","polemion","balloaceous","poor","courmost","rhynchical","theresque","recognizeine","comeion","townally","balo","palliics","brothersion","pastseaain","axiovoteard","Congressdom","lubrictheorysive","caldition","doctorition","througher","lithor","ternise","foreer","afterety","foenamongtion","kidry","norsome","securityeur","amountor","cytoitor","oscillment","nectagainain","carni","sorcie","belliorium","stin","measureproof","generier","campness","ishood","tertiain","entreette","tough","germin","hemification","vivior","junct","eitherist","hirsutlossfier","asative","elseality","tendic","oncoship","evidenceenne","typile","ogness","veni","politicsorium","salicize","munery","gontic","preterhope","rapaciparticipantality","agentence","group","timely","taskable","octogesimfic","everybodyot","clysmmusicesque","unitise","satia","restard","machineproof","whoseine","uberunitie","me","ruminacy","censcienceee","very","drawwise","tendature","scab","radary","liquidid","take","polickin","clarnationity","alteron","network","surdor","flig","uliginthrowess","PM","fundier","prehenswise","acrosslike","potamform","retauthor","halitage","crassitive","monstratous","nugactic","pandward","flamability","plicist","tenuise","buyaneity","teacherize","opiine","opacy","emetoagoful","church","centric","penitture","enoughible","ideaability","sagittment","anteness","treeosity","patot","walkenne","verain","paedo","sclerauthoritive","mediasive","eccles","athlative","thalass","caprpainory","subbornmost","chantmanyish","crispory","communityling","stalagmern","esoable","glabrarian","rigory","highacity","heia","praeture","egribyious","cardon","justfy","riskoon","ntorium","oical","conferenceial","hold","movieast","doorious","ornist","casresponsibilityitious","miss","aoon","nau","hit","answerable","sperier","wifeular","studyosity","alwaysly","hotel","orecticfaction","housearian","phascoursely","mord","corteer","pasccustomer","sacraitemular","goalast","orexally","rhombontoade","larvot","andory","opoter","sophyeur","septenwaterule","penoly","iterair","meta","veraci","redition","acerbical","signian","onto","stann","totihundredsome","hang","functast","turpitth","primo","stenid","jursave","prob","folial","pallitsome","several","obsation","bibitarian","cusreality","powerial","acuwise","gen","acuture","sparssure","half","annably","mechano","capical","agree","cuspcy","mammfication","fulg","individual","habiltownon","teamth","retroie","vot","compareise","catenmorning","transtic","terminize","etho","machinfloorness","property","dogent","votespeciallyacity","tentaery","schoolatory","cubance","mean","edency","col","clastmost","emesiproof","plum","malimostless","breakaster","nephrnotice","ergwise","umbilicaceous","meanade","seriession","raucish","du","nexstandardosity","girlarium","natureeur","syringmost","argueivity","situationitive","tenachood","shouldal","lekanputite","entireosity","caulresponsibilityy","overast","becomeesque","somaably","genator","fumuous","anyoneain","ethory","majarian","hotice","miasmine","clystmajor","versical","leonular","pyr","pingu","logformit","pedially","meetent","dataful","acance","ptychid","nonefaction","soundfy","dataation","rhach","goaleur","nothing","nasety","stageive","gemmsiteious","florot","radioie","stageth","instead","fundfic","patientition","viciious","dexiRepublicanless","stagead","keeptic","orexicety","isious","effortance","officer","computerly","artistain","reason","somnality","bulbness","horm","only","liqueel","passer","philoy","nightian","jurissouthence","near","fastice","youngling","firm","institutionetic","omniivity","pick","bisward","ting","democratic","axillwhatever","military","wishably","stirpid","representery","wall","bibituous","cutial","gelateveryone","buildingly","bank","leuker","plantkin","dipldrugable","vectosity","wonder","reduceability","quesitmaterialify","graphation","arster","truthitor","come","arrive","foot","pseudous","policyatic","acet","explainacy","joincy","produceent","nowsion","humanious","phetally","page","undentroublekin","development","groupsome","sutarian","generationing","performanceade","turbowould","flavical","very","solith","doctrlet","ostracetic","mindeer","brother","inside","orling","palmcertainlyibility","sac","ridaneity","unitia","yes","siphoacious","valuead","reason","state","veritude","vicade","experitor","fluar","federaire","sordeer","vuls","stichmost","fan","machine","domative","digmaire","quiteian","Mrair","colorally","ofast","cilily","ethmsonenne","cryptwise","seaile","amount","halfarium","during","vulphang","hedrise","vit","productionive","seeast","olecranexpecttic","censor","axilloeous","gnatitive","education","axiwhoseel","savear","moreism","sentiorium","sceloilial","foenade","emdom","acier","algiath","addressably","hiem","money","enjoy","few","fugarian","ontitive","once","oment","tostproof","claustroatory","evenant","everyonear","introaneous","aphie","glorior","eoscharacter","arriveish","narr","workerform","program","pepseer","analysisacious","positavailable","septuagesim","salvite","saccibility","tendacity","similarior","phetism","cribrsocialary","biobititive","ultraular","dreamance","four","fratrity","sitaneous","cenism","fluation","suggestet","jutsure","bitature","coriaire","fanmarriageen","sympicking","sagac","raceast","methodet","take","bulbism","superency","agyrty","calliitious","ophthalmdark","futilet","internationalion","commonary","collectionar","volatbodyade","segetoh","prettyture","theeer","wayast","quaternose","decen","dropeous","clinator","runarium","fugitaster","those","ran","gust","severalally","thisent","trogl","dysunderise","vitell","macrage","product","three","professoran","preventard","todayial","errdaughterage","earlyan","menaciular","pneustatewise","cochletic","ratherern","unipracticeory","unguichair","phonality","numberivity","stinguty","longine","dinoborn","vapitor","villacious","seasonfy","hospitalably","businessain","mesteror","be","dogwise","localous","comparehood","rosee","keyitude","allowite","such","alwaterward","allowety","knowledgeess","alternar","feminnationability","chanceer","malleoety","magnid","miasmless","coach","societyous","thelsmileation","wayice","myrmecen","salin","merg","teachereur","tersery","stereative","stateety","never","richess","membereous","somalongosity","andal","iteraceous","warivity","untilice","groupward","itslike","psammish","mammacity","movie","courttic","septimwise","squam","vehan","rhombaneity","score","veh","camera","emeti","prepareier","supin","grad","animalacious","prepareably","weekition","redyardaster","psammsaveivity","esnaturalice","uxorth","polisment","television","vulgain","save","repsensehood","newer","station","cause","onomatcivilette","sputable","octogenfication","pulchrid","word","magn","genily","lystmorningality","doctorness","hexfold","par","glass","udin;tude","thersorter","puniious","texhimfic","butably","legion","flammfication","dendrit","population","eightling","ossad","cystair","keyress","veryics","aboveary","quartpeaceacity","lyzaire","frictator","junct","pain","partikin","bilate","ctenoldious","laushairot","hopeesque","bac","trainingment","quistoryate","vivible","plas","solit","flacc","affect","pulmontic","rocktic","unific","dealette","PMity","light","soonality","rich","germinpersonon","rarfold","white","natee","democraticably","end","traumie","hippsometimesular","viice","fiveability","might","card","uvuless","thank","receiveture","reasonward","momentness","jobfication","callfaction","viccheckify","tendage","hostian","acr","penoot","sectionier","monness","containship","science","pedoitselfine","veruous","lunie","dulcth","wish","stuffor","autoary","clysmate","partnerarium","geneserviceical","venia","humanage","myair","rexiaeitherfold","emul","fidify","carcerress","halfile","ofic","soize","deictwise","nearard","scabioify","urs","Mrsatory","productth","season","amphaneous","hodhand","ownot","merister","scienceatic","fellor","legisward","scisstreatment","leteur","teamacle","designably","negally","tenacihotelial","offerth","artive","centrevealose","ceasal","cheiroture","passarium","histri","praefoodice","talogreatast","euruous","theoryistic","coeldifferent","servent","leftity","pediorium","iqu","treat","iter","relationship","landlet","halitcity","scope","minsome","ulodeal","statior","photoain","unitive","itsance","pellation","nomidead","edency","factorism","omenuntilette","nameth","ursier","hit","setist","body","aboutuous","arctel","mortuability","eoseous","natural","costarium","start","stereoward","orexiian","macrory","understandier","ters","minacistic","logyot","auth","moveacity","nonagesimrange","uligindevelopable","foodeous","breviency","oleade","uvair","absure","schisen","solitition","carpacross","pacto","nextot","ferto","minuteization","blennly","scabistic","meeting","quotneverive","spondture","valsonatic","quatern","degreeence","policyry","whomose","apfaction","call","etymible","fac","frugless","lysette","lax","zelature","feelingo","nomen","whyory","myrmecarticlesome","difrangeard","endfy","cost","pneuclassorium","it","societyence","afization","schooltion","paintingency","orecticen","challengeule","phileie","dealen","caedess","aboutible","pennance","summer","crevcareeribility","toughist","primia","hemisignate","conditionety","capaster","oligoacious","first","felinstateaceous","circument","productency","meet","sporthood","opisth","termics","axilloenne","donnew","trabize","archoproof","emetoee","bromoee","especiallyar","lotsion","liqujoinkin","eye","severalad","orexially","yetot","includeability","decafier","bigment","alg","eightary","bromoquicklyfold","arriveid","stepory","parentot","puratory","experienceful","paedpatient","controleous","stillful","buildingern","bromocultural","certainlyenne","aurless","penslearnen","eitherition","serveitive","archness","nihilous","vect","archaeuous","factorfold","cauloform","afterally","introforce","plutation","pamant","foreign","templaboveess","cen","regionier","frontform","addiscoveror","occur","increase","educationair","serviceical","gasize","messageer","sorpt","senseid","treatfication","languageia","opoterhundredern","hundredify","similararian","blastacle","statemention","educationency","mulctcy","vocally","vituular","eyeability","fewably","fendage",
             "phenite","carefication","avoid","in1ical","plean","shoulderit","volutage","prunid","myricustomeroon","boarditive","diplsoutherno","jungaster","fring","do","noxproof","right","fingerfier","ageful","ctenise","tricbeginice","anyoneain","panstype","texfication","specificious","pang","fornicdevelopmentment","exist","stopity","horofic","trips","atite",
             "withoutior","igyoung","expertise","somni","glans","phantad","cip","will","dipsoconsiderivity","parern","hydrodaughter","alternful","ser","clearatory","verbminuteition","keepive","cernon","market","ogdoatic","creas","soldierise","juriad","ocorium","bility","cinehood","therioably","equiical","treiskaideko","plicet","pageatory","figence","heency","actety","defenseitude","yet","present","pangreveal","lictdom","periodosity","knowledgeitor","anni","quiteial","politaster","habilaster","gramoety","sitenne","bolaproof","ductwriterally","phylacty","rhag","tremule","nonagenly","naissauthorfic","thusster","situationic","extremia","familying","megalization","costad",
             "mersexecutivekin","artistality","learnaceous","concern","imicsimple","rhynchier","valeforget","lysety","primence","cleithr","sentor","similic","meter","theirette","takesive","nephrage","politics","plurgeneral","cusress","exist","acristic","trudast","nictsure","politicalatory","off","seekible","free","thirdarium","drugan","tondy","continueee","andrmovementast","soph","figappearette","perhapsling","floor","hemiical","araceous","emeator","orththanator","sapi","anyster","alleloyes","dicial","benefitation","bioature","graphator","thank","plesiosity","terrontoitor","out","leprair","managementacy","beautifuldom","indicateair","fellster","speechade","commonance","systemade","blue","cup","institutionory","kinetship","stig","purposeaceous","hetero","prepare","heteroate","civilling","claudproducead","scaphatic","with","directorsion","gratform","situationitive","dextrivity","demity","carpth","legcameraship","time","they","ontanothertic","pallitwhich","cylindcy","middle","protectety","sesquiise","ontoate","can","Congressacle","heartel","simulansweracy","cogn","withtic","tranor","authorsure","accountant","involveie","rumpier","veluous","phanish","scopesome","felicitair","muncy","ntress","laughitor","dysdayful","without","plyacle","onceize","shoot","acrosslet","playerel","gamot","soporaster","service","along","raiseature","sacroize","vorit","hispidinside","dexteracy","butment","oenofficial","cruci","eastward","leaderarium","steghowern","ballodom","past","improveier","bloodics","dis","way","meriation","focusad","practiceship","redence","theoistic","positionaneity","saliic","medicalability","vilrealo","partally","seminar","Mr","egorast","byly","calori","herious","claimform","vertivity","circaneous","vorac","suddenlyster","currary","heise","fably","eofication","salacious","mill","gasose","soonot","salinous","memoryature","van","tendent","addresset","montstaff","talkship","hepar","peran","trecentacle","watereur","trancy","federalibility","failery","junctivity","punctaccordingorium","lactwhetherible","dexterth","earlyable","scrupuleous","soundward","uxoriard","rancous","typoness","matersive","housear","cineenne","listenate","fatid","awayarium","thefeelingad","agentary","para","saxtion","discussatic","noture","trabine","studyress","isfactage","uloesque","algomore","stopfold","thusition","pubator","magn","ultimization","trapez","astr","sorcadministrationsome","picteffect","babyful","tricesim","heavyive","cris","generationous","risesome","megamaterialuous","locut","lamino","heterwhoitive","carcinincludeize","sexability","roommost","affect","tomofinishibility","chordous","mulgseaian","pessim","everyoneaceous","nt","augibility","seaarium","stigbut","hedr","thanage","rangesion","gaslet","wife","phasybadess","quarttion","pickeer","difficultsure","cernition","myrmec","studsion","attentionform","uni","pecuitor","pygel","tonacity","doctrion","pressureose","archo","backism","interestast","cernition","graphoesque","meeteur","gravier","avoidian","determineally","legalator","better","produce","purion","octav","triboet","girleur","calcatic","matter","phrenety","patientproof"]

xcode_project_path = '/Users/ganyuanrong/iOSProject/game_mw_sdk_ios/MainSDK/MW_SDK.xcodeproj'


# cpp
cpp_all_path = ''
cpp_modify_path = ''
# cpp_modify_path = '/Users/gan/iospro/game/rongyaodg/app/Classes/game/model/template'  KKForeverSkyRun
cpp_old_prefix = ''
cpp_new_prefix = ''

# /Users/gan/Desktop/黑特篮球new2/SkyBetufi/SourceCode/SkySrc/CommonModule/GUtility/PKCategory
oc_all_path = '/Users/ganyuanrong/iOSProject/game_mw_sdk_ios/MainSDK/GameYooSDK/'
oc_modify_path = '/Users/ganyuanrong/iOSProject/game_mw_sdk_ios/MainSDK/GameYooSDK/'

handle_file_count = 0
file_count = 0

oc_exclude_files = ['AppDelegate.h', 'MWSDK.h', 'PayData.h', 'LoginData.h', 'AccountModel.h','CreateOrderResp.h']
oc_exclude_dirs = ['AFNetworking', 'Masonry', 'YYModel','Model']


def random_2word():#随机生成两个单词

    first_index = random.randint(0, len(genest_word) - 1)
    sec_index = random.randint(0, len(genest_word) - 1)
    while (first_index == sec_index):
        sec_index = random.randint(0, len(genest_word) - 1)

    first_word = genest_word[first_index]
    sec_word = genest_word[sec_index]

    return first_word, sec_word

def random_1word():

    first_index = random.randint(0, len(genest_word) - 1)
    first_word = genest_word[first_index]

    return first_word

word_oc_class_temp = []
def random_word_for_oc_class():

    first_word, sec_word = random_2word()
    new_word = first_word.capitalize() + sec_word.capitalize()

    while (new_word in word_oc_class_temp):
        first_word, sec_word = random_2word()
        new_word = first_word.capitalize() + sec_word.capitalize()

    word_oc_class_temp.append(new_word)
    return new_word

word_image_name_temp = []
def random_word_for_image():

    first_word, sec_word = random_2word()
    new_word = first_word.lower() + sec_word.lower()

    while (new_word in word_image_name_temp):
        first_word, sec_word = random_2word()
        new_word = first_word.lower() + "_" + sec_word.lower()

    word_image_name_temp.append(new_word)
    return new_word


def random_word_for_method():#产生方法名称替代代码方法，使用defind

    for i in range(300):

        first_index = random.randint(0, len(genest_word)-1)
        sec_index = random.randint(0, len(genest_word) - 1)
        if first_index == sec_index:
            sec_index = random.randint(0, len(genest_word) - 1)

        first_word = genest_word[first_index]
        sec_word = genest_word[sec_index]

        new_word = first_word.lower() + sec_word.capitalize()
        print new_word

word_oc_method_temp = []
def random_word_for_no_use_method():

    first_word, sec_word = random_2word()
    new_word = first_word.lower() + sec_word.capitalize()

    while (new_word in word_oc_method_temp):
        first_word, sec_word = random_2word()
        new_word = first_word.capitalize() + sec_word.capitalize()

    word_oc_method_temp.append(new_word)
    return new_word




def modify_oc_class_name(oc_path):
    global file_count, handle_file_count, fia

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_content = read_file_data(project_content_path)

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store" or file_name.endswith(".swift"):
                    continue

                file_count = file_count + 1

                aaa = 1
                for not_dir in oc_exclude_dirs:
                    if not_dir in root:
                        aaa = 2

                if aaa == 2:
                    continue


                if file_name.endswith('.m') or file_name.endswith('.mm'):#cpp文件

                    # if has_new_prefix_in_start(file_name):
                    #     continue
                    # if oc_new_prefix and file_name.startswith(oc_new_prefix): #已经存在前缀，不处理
                    #     continue

                    # if '+' in file_name:  # 分类
                    #     continue

                    file_name_no_extension = os.path.splitext(file_name)[0]

                    file_extension = os.path.splitext(file_name)[1]

                    header_file_name = file_name_no_extension + '.h'  #cpp对应的头文件名称
                    if header_file_name in oc_exclude_files: #特殊排除
                        continue

                    header_file_path = os.path.join(root, header_file_name)   #头文件路径
                    if os.path.exists(header_file_path):

                        print '正在处理文件：' + file_name
                        new_word = random_word_for_oc_class()

                        if '+' in file_name:  # 分类
                            fia = file_name_no_extension.split('+')
                            file_new_name = fia[0] + "+" + new_word + '.m'
                            header_file_new_name = fia[0] + "+" + new_word + '.h'



                        else:
                            file_new_name = new_word + '.m'
                            header_file_new_name = new_word + '.h'

                        file_old_path = os.path.join(root, file_name)
                        file_new_path = os.path.join(root, file_new_name)

                        try:
                            os.rename(file_old_path, file_new_path)  #更改文件名
                        except:
                            print '文件无法更改名称：' + file_old_path
                            continue


                        try:

                            header_file_new_path = os.path.join(root, header_file_new_name)

                            os.rename(header_file_path, header_file_new_path)  # 更改头文件名

                        except:
                            print '文件无法更改名称：' + header_file_path
                            continue

                        if '+' in file_name:  # 分类
                            file_new_name_no_extension = fia[0] + "+" + new_word
                        else:
                            file_new_name_no_extension = new_word


                        modify_oc_class_reference(oc_all_path, file_name_no_extension, file_new_name_no_extension)

                        # 更改xproject文件中的.m
                        project_content = replace_xproject_data_reference(project_content, file_name, file_new_name)

                        # 更改xproject文件中的.h
                        project_content = replace_xproject_data_reference(project_content, header_file_name, header_file_new_name)

                        handle_file_count = handle_file_count + 1
                        print '处理完成' + file_name

        wite_data_to_file(project_content_path, project_content)
        print '修改完成 file_count:' + str(file_count) + "  handle_file_count:" + str(handle_file_count)


#oc_path 所有源文件，置于一个单独目录最好
def modify_oc_class_reference(oc_path, old_ref, new_ref):

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm') \
                        or file_name.endswith('.h') or file_name.endswith('.pch') or \
                    file_name.endswith('.storyboard') or file_name.endswith('.xib'):    #oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    # if have_the_word_in_data(file_data, old_ref):

                    file_new_data = replace_data_by_word(file_data, old_ref, new_ref)
                    if (file_name.endswith('.m') or file_name.endswith('.h')) and new_ref in file_name and '+' in old_ref and '+' in new_ref: #分类
                        old_ref_categery = old_ref.split('+')[1]
                        new_ref_categery = new_ref.split('+')[1]
                        file_new_data = file_new_data.replace('(' + old_ref_categery + ')', '(' + new_ref_categery + ')')
                    wite_data_to_file(file_path, file_new_data)

def modify_storyboard_reference(oc_path, old_ref, new_ref):

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm'):    #oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    # if have_the_word_in_data(file_data, old_ref):
                    file_new_data = file_data.replace(old_ref, new_ref)

                    # file_new_data = replace_data_by_word(file_data, old_ref, new_ref)
                    wite_data_to_file(file_path, file_new_data)

def modify_image_name_reference(oc_path, old_ref, new_ref):

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm') \
                        or file_name.endswith('.h') or file_name.endswith('.pch') or \
                    file_name.endswith('.storyboard') or file_name.endswith('.xib'):    #oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    if file_name.endswith('.m') or file_name.endswith('.mm') \
                            or file_name.endswith('.h') or file_name.endswith('.pch'):
                        # imageNamed:@"icon_add_collection"
                        old_ref_b = '@"%s"' % old_ref
                        new_ref_b = '@"%s"' % new_ref
                        file_new_data = file_data.replace(old_ref_b, new_ref_b)


                    elif file_name.endswith('.storyboard') or file_name.endswith('.xib'):
                        old_ref_m = '<image name="%s"' % old_ref
                        new_ref_m = '<image name="%s"' % new_ref
                        file_new_data = file_data.replace(old_ref_m, new_ref_m)

                        # image = "icon_add_collection"

                        old_ref_c = 'image="%s"' % old_ref
                        new_ref_c = 'image="%s"' % new_ref
                        file_new_data = file_new_data.replace(old_ref_c, new_ref_c)

                        # highlightedImage =
                        old_ref_h = 'highlightedImage="%s"' % old_ref
                        new_ref_h = 'highlightedImage="%s"' % new_ref
                        file_new_data = file_new_data.replace(old_ref_h, new_ref_h)

                    wite_data_to_file(file_path, file_new_data)

# highlightedImage="
def find_highlightedImage(res_path):

    if os.path.exists(res_path):
        list_dirs = os.walk(res_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm') \
                        or file_name.endswith('.h') or file_name.endswith('.pch') or \
                        file_name.endswith('.storyboard') or file_name.endswith('.xib'):  # oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)
                    if 'highlightedImage=' in file_data:
                        print file_name


storyboard_new_prefix = "FaCai"
storyboard_old_prefix = "UKRosRed"
def rename_storyboard_name(storyboard_path):

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_content = read_file_data(project_content_path)

    if os.path.exists(storyboard_path):
        list_dirs = os.walk(storyboard_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name.endswith(".storyboard"):

                    if storyboard_new_prefix and file_name.startswith(storyboard_new_prefix): #已经存在前缀，不处理
                        continue

                    file_name_no_extension = os.path.splitext(file_name)[0]
                    file_extension = os.path.splitext(file_name)[1]

                    if not storyboard_new_prefix and not storyboard_old_prefix:  # 此种情况为删除前缀
                        continue

                    print '正在处理文件：' + file_name
                    file_new_name = get_new_file_name_for_oc(file_name, storyboard_old_prefix, storyboard_new_prefix)  # 新文件名字
                    file_old_path = os.path.join(root, file_name)
                    file_new_path = os.path.join(root, file_new_name)

                    try:
                        os.rename(file_old_path, file_new_path)  # 更改文件名

                        file_new_name_no_extension = os.path.splitext(file_new_name)[0]

                        old_xxx = 'kLoadStoryboardWithName(@"' + file_name_no_extension + '")'

                        new_xxx = 'kLoadStoryboardWithName(@"' + file_new_name_no_extension + '")'

                        modify_storyboard_reference(oc_all_path, old_xxx, new_xxx)

                        project_content = replace_xproject_data_reference(project_content, file_name, file_new_name)

                        print '处理完成' + file_name
                    except:
                        print '文件无法更改名称：' + file_old_path
                        continue


        wite_data_to_file(project_content_path, project_content)
        # print '修改完成 file_count:' + str(file_count) + "  handle_file_count:" + str(handle_file_count)

def replace_xproject_data_reference(xproject_data, old_file_name, new_file_name):
    return replace_data_by_word(xproject_data, old_file_name, new_file_name)


def get_new_file_name(file_name, old_prefix, new_prefix): #new_prefix为空表示去掉前缀

    if new_prefix and file_name.startswith(new_prefix):  # 已经存在前缀，不处理
        return file_name

    if old_prefix.strip() and file_name.startswith(old_prefix):  # 存在旧前缀，替换掉
        new_file_name = file_name.replace(old_prefix, new_prefix)
    else:

        new_file_name = new_prefix + file_name
    return new_file_name



def get_new_file_name_for_oc(file_name, old_prefix, new_prefix): #new_prefix为空表示去掉前缀

    if '+' in file_name: #分类
        file_name_s = file_name.split('+')
        category_class = file_name_s[0]
        category_name = file_name_s[1]
        if new_prefix and category_name.startswith(new_prefix):  # 已经存在前缀，不处理
            return file_name

        if old_prefix.strip() and category_name.startswith(old_prefix):  # 存在旧前缀，替换掉
            category_name_new = category_name.replace(old_prefix, new_prefix)
        else:

            category_name_new = new_prefix + category_name

        return category_class + '+' + category_name_new


    if new_prefix and file_name.startswith(new_prefix):  # 已经存在前缀，不处理
        return file_name

    if old_prefix.strip() and file_name.startswith(old_prefix):  # 存在旧前缀，替换掉
        new_file_name = file_name.replace(old_prefix, new_prefix)
    else:

        new_file_name = new_prefix + file_name
    return new_file_name



def replace_file_content_by_word(file_path, old_content, new_content):

    file_data = read_file_data(file_path)

    # have_the_word_in_data(file_data, old_content)
    old_content = '\\b' + old_content + '\\b'
    png_old_name_re = re.compile(old_content)
    result2 = re.sub(png_old_name_re, new_content, file_data)
    # new_f_all_txt = file_data.replace(png_old_name, png_new_name)

    f_obj = open(file_path, 'w')  # 首先先创建一个文件对象
    f_obj.write(result2)
    f_obj.flush()
    f_obj.close()

def wite_data_to_file(file_path, data):
    f_obj = open(file_path, mode='w')  # 首先先创建一个文件对象
    f_obj.write(data)
    f_obj.flush()
    f_obj.close()


def replace_data_by_word(data, old_content, new_content):

    if '+' in old_content:
        new_data = data.replace(old_content, new_content)
    else:

        old_content = '\\b' + old_content + '\\b'
        png_old_name_re = re.compile(old_content)
        new_data = re.sub(png_old_name_re, new_content, data)
    return new_data

def replace_image_data(data, old_content, new_content):
    old_content = '"' + old_content + '"'
    new_content = '"' + new_content + '"'
    # png_old_name_re = re.compile(old_content)
    # new_data = re.sub(png_old_name_re, new_content, data)
    new_data = data.replace(old_content, new_content)
    return new_data


def replace_data_content(data, old_content, new_content):

    png_old_name_re = re.compile(old_content)

    new_data = re.sub(png_old_name_re, new_content, data)
    return new_data


def replace_data_content22(data, old_content, new_content, delete):

    png_old_name_re = re.compile(old_content)

    if delete:
        aaa = png_old_name_re.match(data)
        new_data = data.replace(old_content, aaa.group(0))

    else:
        new_data = re.sub(png_old_name_re, new_content, data)
    return new_data


def have_the_word_in_data(data, the_str):

    word_pattern = '\\b' + the_str + '\\b'
    match_obj = re.search(re.compile(word_pattern), data)
    # if match_obj:
    #     print match_obj.group()
    return match_obj

def read_file_data(file_path):
    f_obj = open(file_path, mode="r")  # 首先先创建一个文件对象
    f_data = f_obj.read()  # 用read()方法读取文件内容
    f_obj.close()
    return f_data


def modify_sdk_bundle_image_name(image_dir_path, src_dir_path, image_exclude_files):

    if os.path.exists(image_dir_path):
        list_dirs = os.walk(image_dir_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                file_path = os.path.join(root, file_name)  # 文件路径

                # match_obj = re.findall(re.compile('\"\w+\(%s|%d\)\w+\.png\\b'), file_data)
                if file_name.endswith(".png"):
                    print 'find png file match =>' + file_name
                    file_name_no_extension = os.path.splitext(file_name)[0]
                    file_extension = os.path.splitext(file_name)[1]

                    if file_name_no_extension in image_exclude_files:
                        pass
                    else:
                        # 开始修改图片
                        new_image_name_no_extension = random_word_for_image()
                        new_image_name = new_image_name_no_extension + file_extension

                        file_old_path = os.path.join(root, file_name)
                        file_new_path = os.path.join(root, new_image_name)
                        os.rename(file_old_path, file_new_path)

                        modify_image_name_reference(src_dir_path,file_name_no_extension,new_image_name_no_extension)


                # print 'no match'
        # print image_exclude_files

def deleteComments():#还有问题

    source_dir = '/Users/gan/iospro/game/rongyaodg/app/Classes/device'

    if os.path.exists(source_dir):
        list_dirs = os.walk(source_dir)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if 'google' in root or 'bind' in root:
                    continue

                if file_name.endswith('.h') or file_name.endswith('.m') or file_name.endswith('.mm') or file_name.endswith('.cpp'):

                    file_path = os.path.join(root, file_name)
                    file_data = read_file_data(file_path)

                    file_data_0 = replace_data_content(file_data,'/\\*\\*/', '')
                    file_data_1 = replace_data_content(file_data_0,'([^:/])//.*', '\\1')
                    file_data_2 = replace_data_content(file_data_1,'^//.*', '')
                    file_data_3 = replace_data_content(file_data_2,'/\\*{1,2}[\\s\\S]*?\\*/', '')
                    file_data_4 = replace_data_content(file_data_3,'\\s*\\n', '\\n')

                    wite_data_to_file(file_path, file_data_4)

def addNewComments(src_dir_path, comment_file_path):

    if not os.path.exists(comment_file_path):
        print("comment_file_path not exist")
        return
    aaa_data = read_file_data(comment_file_path)

    # str2 = aaa_data.decode('windows-1252')
    # comment_data = str2.encode('utf-8')
    print chardet.detect(aaa_data)
    # comment_data = aaa_data
    comment_data = aaa_data.decode('utf-8')
    comment_data_length = len(comment_data)


    # wite_data_to_file('/Users/gan/iospro/game/afaefae22222.txt', aaa_data)
    # fencoding = chardet.detect(aaa_data)
    # print 'fencoding ' + fencoding
    # aa = 'eee'
    # if aa:
    #     return

    # mmm_not = ['#ifndef','#import','#include','#endif','#define']

    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if 'google' in root or 'bind' in root:
                    continue

                if file_name.endswith('.h') or file_name.endswith('.m') or file_name.endswith(
                        '.mm') or file_name.endswith('.cpp'):
                    file_path = os.path.join(root, file_name)

# ============
                    src_data = read_file_data(file_path)
                    print chardet.detect(src_data)
                    src_data = src_data.decode('utf-8')

                    # 删除原来的注释
                    file_data_0 = replace_data_content(src_data, '/\\*\\*/', '')
                    file_data_1 = replace_data_content(file_data_0, '([^:/])//.*', '\\1')
                    file_data_2 = replace_data_content(file_data_1, '^//.*', '')
                    file_data_3 = replace_data_content(file_data_2, '/\\*{1,2}[\\s\\S]*?\\*/', '')
                    file_data_4 = replace_data_content(file_data_3, '\\s*\\n', '\\n')

                    src_data = file_data_4
                    #删除注释完成

                    data_list = list(src_data)

                    huan_hang_pos = []
                    for m in re.finditer('\n', src_data):
                        # print(m.start(), m.end())
                        # print(m.end())
                        huan_hang_pos.append(m.end())

                    for pos in reversed(huan_hang_pos):
                        # print(m.start(), m.end())

                        isneed = random.randint(1, 20)  # 随机决定是否改行需要添加注释
                        if 5 <= isneed <= 10:  # 添加注释
                            new_comment_len = random.randint(10, 400)  # 随机产生注释长度,最少10，最长不超400字符
                            new_comment_start_index = random.randint(0, comment_data_length - 401)  # 随机注释文章的起始位置
                            new_comment = comment_data[new_comment_start_index: new_comment_start_index + new_comment_len]

                            comment_type = random.randint(1, 3)  # 随机注释类型

                            if comment_type == 2:

                                comment_data_2 = new_comment.replace('\n', '\n//')
                                comment_data_2 = comment_data_2 + '\n'
                                data_list.insert(pos, '//' + comment_data_2)

                            else:

                                comment_data_2 = '\n/**\n  ' + new_comment + ' \n**/\n'
                                # content = content + line + comment_data_2
                                data_list.insert(pos, comment_data_2)

                    content = ''.join(data_list)
                    # content = unicode(content, "utf-8")

                    try:
                        content = content.encode("utf-8")
                    except:
                        print "encode error:" + file_path
                        pass
                    wite_data_to_file(file_path, content)
# =========

                    # f_obj = open(file_path, "r")
                    # text_lines = f_obj.readlines()
                    #
                    # content = ''
                    # print '处理中  ' + file_name
                    # for line in text_lines:
                    #     print chardet.detect(line)
                    #     line = line.decode('utf-8')
                    #
                    #     isneed = random.randint(1, 20) #随机决定是否改行需要添加注释
                    #     if isneed <= 5  and isneed <= 10:#添加注释
                    #         new_comment_len = random.randint(10, 400) #随机产生注释长度,最少10，最长不超400字符
                    #         new_comment_start_index = random.randint(0, comment_data_length - 401) #随机注释文章的起始位置
                    #         new_comment = comment_data[new_comment_start_index : new_comment_start_index + new_comment_len]
                    #
                    #         comment_type = random.randint(1, 3) #随机注释类型
                    #
                    #         if comment_type == 2:
                    #
                    #             comment_data_2 = new_comment.replace('\n', '\n//')
                    #             comment_data_2 = comment_data_2 + '\n'
                    #             content = content + line + '//' + comment_data_2
                    #
                    #         else:
                    #
                    #             comment_data_2 = '\n/**\n  ' + new_comment + ' \n**/\n'
                    #             content = content + line + comment_data_2
                    #
                    #     else:
                    #         content = content + line
                    #
                    #         # start = random.randint(1, data_length - 600)
                    #         # comment_length = random.randint(1, 300)
                    #         # comment_data = aaa_data[start: start + comment_length]
                    #
                    # wite_data_to_file(file_path, content)

method_return_type = ['void', 'NSString *', 'BOOL', 'CGFloat', 'NSUInteger']
method_params_type = ['NSString *', 'BOOL', 'CGFloat', 'NSUInteger']
def addNoUseMethod(src_dir_path):
    if not os.path.exists(src_dir_path):
        print("src_dir_path not exist")
        return

    list_dirs = os.walk(src_dir_path)
    for root, dirs, files in list_dirs:
        for file_name in files:

            if file_name == ".DS_Store":
                continue

            if 'google' in root or 'bind' in root:
                continue

            if file_name.endswith('.m'):
                file_path = os.path.join(root, file_name)

                f_obj = open(file_path, "r")
                text_lines = f_obj.readlines()

                content = ''
                print '处理中  ' + file_name
                for line in text_lines:
                    print chardet.detect(line)
                    line = line.decode('utf-8')

                    if line.startswith('+') or line.startswith('-'):

                        method_public = '+'
                        if line.startswith('+'):
                            method_public = '+'
                        else:
                            method_public = '-'

                        isneed = random.randint(1, 20) #随机决定是否改行需要添加无用方法
                        if 5 <= isneed <= 10:#添加

                            method_count = random.randint(1, 3) #随机产生插入的方法数量
                            new_add_method_content = ''
                            for i in range(method_count):

                                return_type = method_return_type[random.randint(0, len(method_return_type)-1)] #随机方法返回类型
                                noUserMethod_name = random_word_for_no_use_method()

                                method_content = '\n' + method_public + ' ' + '(' + return_type + ')' + noUserMethod_name


                                params_counts = random.randint(0, 5) #随机参数个数,最大5个
                                if params_counts == 0:

                                    if return_type == 'void':
                                        params_word1 = random_1word()
                                        params_word2 = random_1word()
                                        method_some_things = '[NSString stringWithFormat:@"%s", @"%s" , @"%s"];' % ('%@%@', params_word1, params_word2)
                                        method_content =  method_content + '\n{\n    %s \n}' % (method_some_things)

                                    elif return_type == 'NSString *':
                                        params_word1 = random_1word()
                                        params_word2 = random_1word()
                                        method_some_things = 'return [NSString stringWithFormat:@"%s", @"%s" , @"%s"];' % ('%@%@',params_word1, params_word2)
                                        method_content = method_content + '\n{\n    %s \n}' % (method_some_things)
                                    elif return_type == 'BOOL' or return_type == 'CGFloat' or return_type == 'NSUInteger':
                                        params_word1 = random.randint(1, 10000000)
                                        params_word2 = random.randint(0, 10000000)
                                        params_word3 = random.randint(0, 10000000)
                                        method_some_things = 'return %s * %s + %s ;' % (params_word1, params_word2, params_word3)
                                        method_content = method_content + '\n{\n    %s \n}' % (method_some_things)



                                else:
                                    for m in range(params_counts):
                                        params_word = random_1word()
                                        params_type = method_params_type[random.randint(0, len(method_params_type)-1)] #随机参数类型
                                        if m == 0:
                                            method_content = method_content + ':(' + params_type + ')' + params_word
                                        else:
                                            method_content = method_content + " " + params_word + ':(' + params_type + ')' + params_word

                                    if return_type == 'void':
                                        params_word1 = random_1word()
                                        params_word2 = random_1word()
                                        method_some_things = '[NSString stringWithFormat:@"%s", @"%s" , @"%s"];' % ('%@%@', params_word1, params_word2)
                                        method_content =  method_content + '\n{\n    %s \n}' % (method_some_things)

                                    elif return_type == 'NSString *':
                                        params_word1 = random_1word()
                                        params_word2 = random_1word()
                                        method_some_things = 'return [NSString stringWithFormat:@"%s", @"%s" , @"%s"];' % ('%@%@',params_word1, params_word2)
                                        method_content = method_content + '\n{\n    %s \n}' % (method_some_things)
                                    elif return_type == 'BOOL' or return_type == 'CGFloat' or return_type == 'NSUInteger':
                                        params_word1 = random.randint(1, 10000000)
                                        params_word2 = random.randint(0, 10000000)
                                        params_word3 = random.randint(0, 10000000)
                                        method_some_things = 'return %s * %s + %s ;' % (params_word1, params_word2, params_word3)
                                        method_content = method_content + '\n{\n    %s \n}' % (method_some_things)

                                    # method_content = method_content + '\n{\n    %s \n}' % (" ")

                                new_add_method_content = new_add_method_content + method_content
                            content = content + new_add_method_content + '\n' + line



                        else:
                            content = content + line
                    else:
                        content = content + line

                wite_data_to_file(file_path, content)




def haveOfforceInSources(oc_path, xofforce):
    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm'):  # oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)
                    if xofforce in file_data:
                        return True

        return False

    return False

def fix_oc_catgery_class_name(oc_path):

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_content = read_file_data(project_content_path)

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store" or file_name.endswith(".swift"):
                    continue

                if 'Masonry' in root:
                    continue

                if file_name.endswith('.m') or file_name.endswith('.h'):#cpp文件

                    if '+' in file_name and 'GlodBule' in file_name: #分类

                        file_new_name = file_name.replace('GlodBule','')
                        file_old_path = os.path.join(root, file_name)
                        file_new_path = os.path.join(root, file_new_name)
                        try:
                            os.rename(file_old_path, file_new_path)  # 更改文件名

                            # file_new_name_no_extension = os.path.splitext(file_new_name)[0]
                            # modify_oc_class_reference(oc_all_path, file_name_no_extension, file_new_name_no_extension)

                            # 更改xproject文件中的文件名
                            project_content = replace_xproject_data_reference(project_content, file_name, file_new_name)

                        except:
                            print '文件无法更改名称：' + file_old_path
                            continue
        wite_data_to_file(project_content_path, project_content)


if __name__ == '__main__':


    # modify_oc_class_name(oc_modify_path)
    # random_word_for_method()

    #修改图片
    # image_exclude_files = []
    # modify_sdk_bundle_image_name("/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/Resources/GOT/SDKResourcesV2.bundle/", "", image_exclude_files)

    #添加垃圾方法
    addNoUseMethod('/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/FLSDK/SdkHelper/Res/')

    #添加随机注释
    # comment_src_path = '/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/FLSDK/SdkHelper/Res'
    # addNewComments(comment_src_path, '/Users/ganyuanrong/Desktop/sdk_confuse/ofc.log')
