from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import random
import os
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ego_jatek_2024'
socketio = SocketIO(app)

kerdesek = [
    {
        "kerdes": "Mi jellemez leginkább egy konfliktusos helyzetben?",
        "valaszok": [
            "Megpróbálom elkerülni a konfrontációt",
            "Szembenézek a problémával azonnal",
            "Időt kérek és átgondolom"
        ]
    },
    {
        "kerdes": "Mit csinálsz hétvégén legszívesebben?",
        "valaszok": [
            "Otthon pihenek és töltődöm",
            "Barátokkal találkozom",
            "Új dolgokat fedezek fel, kirándulok"
        ]
    },
    {
        "kerdes": "Mi a legnagyobb erősséged?",
        "valaszok": [
            "Kreativitás és ötletesség",
            "Megbízhatóság és pontosság",
            "Empátia és odafigyelés"
        ]
    },
    {
        "kerdes": "Mi a véleményed a meglepetésekről?",
        "valaszok": [
            "Imádom, izgalmas és örülök nekik",
            "Attól függ, milyen jellegű",
            "Inkább kerülöm, szeretem ha előre tudok dolgokat"
        ]
    },
    {
        "kerdes": "Hogyan töltöd fel magad, ha fáradt vagy?",
        "valaszok": [
            "Egyedül pihenek, csend és nyugalom kell",
            "Barátokkal vagy családdal töltök időt",
            "Sportolok vagy mozgok egyet"
        ]
    },
    {
        "kerdes": "Mi a hozzáállásod a szabályokhoz?",
        "valaszok": [
            "Betartom őket, a szabályok rendet teremtenek",
            "Rugalmasan kezelem, a helyzettől függ",
            "Inkább a saját fejem után megyek"
        ]
    },
    {
        "kerdes": "Milyen utas vagy?",
        "valaszok": [
            "Mindent előre megtervezek",
            "Van egy vázlatos tervem, de improvizálok is",
            "Spontán vagyok, menet közben döntök"
        ]
    },
    {
        "kerdes": "Mi motivál leginkább?",
        "valaszok": [
            "Elismerés és visszajelzés másoktól",
            "Belső elégedettség és fejlődés",
            "Anyagi biztonság és stabilitás"
        ]
    },
    {
        "kerdes": "Hogyan kezeled a stresszt?",
        "valaszok": [
            "Elvonulok és magamba fordulok",
            "Beszélek róla valakivel",
            "Fizikai aktivitással vezelem le"
        ]
    },
    {
        "kerdes": "Mi a véleményed a pénzről?",
        "valaszok": [
            "Eszköz, nem cél – de fontos a biztonsághoz",
            "Minél több, annál jobb",
            "Csak annyit kell amennyiből jól élek"
        ]
    },
    {
        "kerdes": "Milyen vagy csoportos munkában?",
        "valaszok": [
            "Szívesen veszem át az irányítást",
            "Beilleszkedem és támogatom a csapatot",
            "Inkább egyedül dolgozom hatékonyabban"
        ]
    },
    {
        "kerdes": "Mi a fontos számodra egy barátságban?",
        "valaszok": [
            "Őszinteség és bizalom",
            "Közös élmények és szórakozás",
            "Támogatás nehéz helyzetekben"
        ]
    },
    {
        "kerdes": "Hogyan reagálsz ha igazságtalanság ér?",
        "valaszok": [
            "Azonnal szót emelek ellene",
            "Átgondolom és utána reagálok",
            "Inkább elkerülöm a konfrontációt"
        ]
    },
    {
        "kerdes": "Milyen vagy reggel?",
        "valaszok": [
            "Azonnal éber és energikus vagyok",
            "Lassan ébredek, kell egy kis idő",
            "Rém álmos vagyok amíg meg nem iszom a kávém"
        ]
    },
    {
        "kerdes": "Mi a véleményed a közösségi médiáról?",
        "valaszok": [
            "Aktívan használom, szeretem",
            "Csak mértékkel és célzottan",
            "Inkább kerülöm, több kárt okoz mint hasznot"
        ]
    },
    {
        "kerdes": "Hogyan hozol fontos döntéseket?",
        "valaszok": [
            "Az érzéseimre hallgatok",
            "Logikusan végigelemzem a lehetőségeket",
            "Kikérem mások véleményét és utána döntök"
        ]
    },
    {
        "kerdes": "Mi jellemez leginkább evés közben?",
        "valaszok": [
            "Mindent megeszek, nem vagyok válogatós",
            "Vannak dolgok amiket nem szeretek",
            "Nagyon válogatós vagyok"
        ]
    },
    {
        "kerdes": "Milyen kapcsolatod van az idővel?",
        "valaszok": [
            "Mindig pontos vagyok",
            "Általában pontos vagyok, néha késem",
            "Sűrűn elkések"
        ]
    },
    {
        "kerdes": "Mi a hozzáállásod a változáshoz?",
        "valaszok": [
            "Szeretem, izgalmasnak találom",
            "Elfogadom ha szükséges",
            "Inkább a megszokott dolgokat preferálom"
        ]
    },
    {
        "kerdes": "Hogyan viseled a kritikát?",
        "valaszok": [
            "Nyitottan fogadom és tanulok belőle",
            "Attól függ ki mondja és hogyan",
            "Nehezen viselem, személyesnek érzem"
        ]
    },
    {
        "kerdes": "Mi a kedvenc évszakod?",
        "valaszok": [
            "Nyár – meleg, fény, szabadság",
            "Tél – hangulatos, ünnepek, csend",
            "Tavasz vagy ősz – mérsékelt és változatos"
        ]
    },
    {
        "kerdes": "Milyen vagy vásárlás közben?",
        "valaszok": [
            "Impulzívan veszek, ha megtetszik valami",
            "Átgondolom és összehasonlítom az árakat",
            "Csak azt veszem meg amire tényleg szükségem van"
        ]
    },
    {
        "kerdes": "Mi a véleményed a segítségkérésről?",
        "valaszok": [
            "Természetes dolog, szívesen kérek segítséget",
            "Csak végszükség esetén kérek segítséget",
            "Inkább egyedül oldom meg a dolgokat"
        ]
    },
    {
        "kerdes": "Hogyan viselkedsz ha valaki megbánt?",
        "valaszok": [
            "Azonnal elmondom hogy bántott",
            "Magamban feldolgozom és elengedem",
            "Sokáig magamban hordom"
        ]
    },
    {
        "kerdes": "Mi a véleményed a bocsánatkérésről?",
        "valaszok": [
            "Könnyen kérek bocsánatot ha hibáztam",
            "Nehezen megy, de megcsinálom",
            "Nagyon nehezen kérek bocsánatot"
        ]
    },
    {
        "kerdes": "Milyen tanuló voltál iskolában?",
        "valaszok": [
            "Szorgalmas és lelkiismeretes",
            "Átlagos, megcsináltam amit kellett",
            "Inkább a minimumra törekedtem"
        ]
    },
    {
        "kerdes": "Mi a véleményed a kompromisszumokról?",
        "valaszok": [
            "Fontos, mindenki nyerjen valamit",
            "Csak ha muszáj",
            "Inkább ragaszkodom az álláspontomhoz"
        ]
    },
    {
        "kerdes": "Hogyan viselkedsz idegenek között?",
        "valaszok": [
            "Könnyen beilleszkedem és ismerkedem",
            "Visszafogott vagyok de nyitott",
            "Zárkózott vagyok, nehezen nyílok meg"
        ]
    },
    {
        "kerdes": "Mi a hozzáállásod a sporthoz?",
        "valaszok": [
            "Rendszeresen sportolok, fontos az életemben",
            "Néha mozgok ha kedvem van",
            "Nem igazán érdekel a sport"
        ]
    },
    {
        "kerdes": "Milyen zenét hallgatsz legszívesebben?",
        "valaszok": [
            "Energikus, gyors zenét",
            "Nyugodt, melankolikus zenét",
            "Attól függ a hangulatom"
        ]
    },
    {
        "kerdes": "Mi a véleményed a magányról?",
        "valaszok": [
            "Szeretem, szükségem van az egyedüllétre",
            "Néha jó, de sokáig nem bírom",
            "Kerülöm, mindig kell valaki körülöttem"
        ]
    },
    {
        "kerdes": "Hogyan reagálsz ha elveszíted az irányítást egy helyzetben?",
        "valaszok": [
            "Megpróbálom visszaszerezni az irányítást",
            "Alkalmazkodom és elfogadom",
            "Pánikba esek és stresszelek"
        ]
    },
    {
        "kerdes": "Mi a véleményed az állatokról?",
        "valaszok": [
            "Imádom őket, van vagy szeretnék háziállatot",
            "Kedvelem de nem akarok háziállatot",
            "Nem érdekelnek különösebben"
        ]
    },
    {
        "kerdes": "Milyen vagy ha beteg vagy?",
        "valaszok": [
            "Panaszkodok és figyelmet igénylek",
            "Csendben szenvedek és pihenek",
            "Tovább csinálom a dolgaimat mintha mi sem történt volna"
        ]
    },
    {
        "kerdes": "Mi a véleményed a hazugságról?",
        "valaszok": [
            "Soha nem hazudok, az igazság mindennél fontosabb",
            "Néha szükséges az emberek védelme érdekében",
            "Kis hazugságok néha elkerülhetetlenek"
        ]
    },
    {
        "kerdes": "Hogyan ünnepeled a születésnapodat?",
        "valaszok": [
            "Nagy bulit szervezek, mindenkit meghívok",
            "Csak a szűk baráti körrel ünneplek",
            "Inkább csendben töltöm, nem szeretem a feltűnést"
        ]
    },
    {
        "kerdes": "Mi a véleményed a reggeli evésről?",
        "valaszok": [
            "A nap legfontosabb étkezése, sosem hagyom ki",
            "Ha van időm megeszem, ha nincs kihagyom",
            "Általában nem eszem reggel"
        ]
    },
    {
        "kerdes": "Hogyan viselkedsz ha valaki segítséget kér tőled?",
        "valaszok": [
            "Mindig segítek, bármit kér",
            "Segítek ha tudom és van időm",
            "Csak a közeli barátaimnak segítek"
        ]
    },
    {
        "kerdes": "Mi a véleményed a rendetlenségről?",
        "valaszok": [
            "Nem bírom, mindent rendben tartok",
            "Egy kis rendetlenség belefér",
            "Nem zavar a rendetlenség"
        ]
    },
    {
        "kerdes": "Milyen vagy ha unatkozol?",
        "valaszok": [
            "Azonnal keresek valamit ami leköt",
            "Hagyom magam unatkozni, néha jó",
            "Általában nem unatkozom, mindig van mit csinálni"
        ]
    },
    {
        "kerdes": "Mi a véleményed a filmekről és sorozatokról?",
        "valaszok": [
            "Sokat nézek, ez az egyik fő szórakozásom",
            "Néha nézek ha ajánlanak valamit",
            "Ritkán nézek, más szórakozást preferálok"
        ]
    },
    {
        "kerdes": "Hogyan viselkedsz ha valaki vitatkozik veled?",
        "valaszok": [
            "Kitartok az álláspontom mellett",
            "Meghallgatom és átgondolom a véleményét",
            "Inkább feladom hogy ne legyen konfliktus"
        ]
    },
    {
        "kerdes": "Mi a véleményed a természetről?",
        "valaszok": [
            "Imádom, minden szabadidőmet kint töltöm",
            "Szeretem, néha kimegyek kirándulni",
            "Inkább a városi élethez vonzódom"
        ]
    },
    {
        "kerdes": "Milyen vagy ha valaki elkésik?",
        "valaszok": [
            "Nagyon zavar, nem tolerálom a késést",
            "Egy kicsit zavar de megértem",
            "Nem zavar, magam is szoktam késni"
        ]
    },
    {
        "kerdes": "Mi a véleményed a könyvekről?",
        "valaszok": [
            "Sokat olvasok, az egyik kedvenc időtöltésem",
            "Néha olvasok ha érdekes a téma",
            "Ritkán olvasok, más médiumot preferálok"
        ]
    },
    {
        "kerdes": "Hogyan viselkedsz ha valaki dicsér?",
        "valaszok": [
            "Örülök neki és elfogadom",
            "Kicsit zavarba jövök de örülök",
            "Kellemetlenül érzem magam tőle"
        ]
    },
    {
        "kerdes": "Mi a véleményed a technológiáról?",
        "valaszok": [
            "Imádom, mindig a legújabb kütyük érdekelnek",
            "Használom amit kell, de nem rajongok érte",
            "Inkább kerülöm ahol lehet"
        ]
    },
    {
        "kerdes": "Milyen vagy ha valami nem sikerül?",
        "valaszok": [
            "Azonnal újra próbálom",
            "Átgondolom mi ment rosszul és utána próbálom újra",
            "Nehezen viselem a kudarcot"
        ]
    },
    {
        "kerdes": "Mi a véleményed a főzésről?",
        "valaszok": [
            "Szeretek főzni, kreatív kikapcsolódás",
            "Megcsinálom ha kell de nem szenvedélyem",
            "Inkább rendelen vagy mások főznek nekem"
        ]
    },
    {
        "kerdes": "Hogyan viselkedsz egy partin?",
        "valaszok": [
            "Az élet lelke vagyok, mindenkit felvidítok",
            "Jól érzem magam de nem tolom magam előtérbe",
            "Inkább a sarokban ülök és figyelem az embereket"
        ]
    },
    {
        "kerdes": "Mi a véleményed az álmokról?",
        "valaszok": [
            "Fontosak, sokat gondolkozom rajtuk",
            "Érdekesek de nem tulajdonítok nekik különösebb jelentőséget",
            "Általában nem emlékszem az álmaimra"
        ]
    },
]


jatekterem = {
    "jatekosok": [],
    "tabla_zsetonok": 0,
    "aktualis": 0,
    "allapot": "varakozas",
    "aktualis_kerdes": None,
    "sajat_valasz": None,
    "tippek": {},
    "tetek": {}
}

def kuldd_kerdes_kepernyo():
    aktiv = jatekterem['jatekosok'][jatekterem['aktualis']]
    kerdes = random.choice(kerdesek)
    jatekterem['aktualis_kerdes'] = kerdes
    emit('kerdes_kepernyo', {
        'aktiv': aktiv['nev'],
        'kerdes': kerdes['kerdes'],
        'valaszok': kerdes['valaszok'],
        'jatekosok': jatekterem['jatekosok'],
        'tabla': jatekterem['tabla_zsetonok']
    }, to='jatek')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lobby')
def lobby():
    return render_template('lobby.html')

@app.route('/jatek')
def jatek():
    return render_template('jatek.html')

@app.route('/reset')
def reset():
    jatekterem['jatekosok'] = []
    jatekterem['tabla_zsetonok'] = 0
    jatekterem['aktualis'] = 0
    jatekterem['allapot'] = 'varakozas'
    jatekterem['aktualis_kerdes'] = None
    jatekterem['sajat_valasz'] = None
    jatekterem['tippek'] = {}
    jatekterem['tetek'] = {}
    return "Játék nullázva!"

@app.route('/reset_es_fooldal')
def reset_es_fooldal():
    jatekterem['jatekosok'] = []
    jatekterem['tabla_zsetonok'] = 0
    jatekterem['aktualis'] = 0
    jatekterem['allapot'] = 'varakozas'
    jatekterem['aktualis_kerdes'] = None
    jatekterem['sajat_valasz'] = None
    jatekterem['tippek'] = {}
    jatekterem['tetek'] = {}
    return render_template('index.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

@socketio.on('csatlakozas')
def csatlakozas(data):
    nev = data['nev']
    
    # Ha már bent van, ne adja hozzá újra
    for j in jatekterem['jatekosok']:
        if j['nev'] == nev:
            gazda = request.sid == jatekterem['jatekosok'][0]['sid']
            emit('jatekosok_frissitese', {
                'jatekosok': jatekterem['jatekosok'],
                'gazda': gazda
            }, to='jatek')
            emit('csatlakozva', {}, to=request.sid)
            return

    jatekterem['jatekosok'].append({
        'nev': nev,
        'zsetonok': 10,
        'sid': request.sid
    })
    join_room('jatek')
    gazda = request.sid == jatekterem['jatekosok'][0]['sid']
    emit('jatekosok_frissitese', {
        'jatekosok': jatekterem['jatekosok'],
        'gazda': gazda
    }, to='jatek')
    emit('csatlakozva', {}, to=request.sid)

@socketio.on('jatek_inditasa')
def jatek_inditasa():
    jatekterem['tabla_zsetonok'] = len(jatekterem['jatekosok']) * 25
    jatekterem['allapot'] = 'kerdes'
    emit('jatek_indul', {}, to='jatek')

@socketio.on('jatek_csatlakozas')
def jatek_csatlakozas(data):
    nev = data['nev']
    join_room('jatek')
    
    for j in jatekterem['jatekosok']:
        if j['nev'] == nev:
            j['sid'] = request.sid
            break
    
    if len(jatekterem['jatekosok']) == 0:
        emit('redirect', {'url': '/'}, to=request.sid)
        return
    
    if jatekterem['aktualis_kerdes'] is None:
        kuldd_kerdes_kepernyo()
    else:
        aktiv = jatekterem['jatekosok'][jatekterem['aktualis']]
        kerdes = jatekterem['aktualis_kerdes']
        if jatekterem['allapot'] == 'kerdes':
            emit('kerdes_kepernyo', {
                'aktiv': aktiv['nev'],
                'kerdes': kerdes['kerdes'],
                'valaszok': kerdes['valaszok'],
                'jatekosok': jatekterem['jatekosok'],
                'tabla': jatekterem['tabla_zsetonok']
            }, to=request.sid)
        elif jatekterem['allapot'] == 'tippeles':
            emit('tippeles_kepernyo', {
                'aktiv': aktiv['nev'],
                'kerdes': kerdes['kerdes'],
                'valaszok': kerdes['valaszok'],
                'jatekosok': jatekterem['jatekosok'],
                'tabla': jatekterem['tabla_zsetonok']
            }, to=request.sid)

@socketio.on('sajat_valasz')
def sajat_valasz(data):
    jatekterem['sajat_valasz'] = data['valasz']
    jatekterem['allapot'] = 'tippeles'
    jatekterem['tippek'] = {}
    jatekterem['tetek'] = {}
    aktiv = jatekterem['jatekosok'][jatekterem['aktualis']]
    kerdes = jatekterem['aktualis_kerdes']
    emit('tippeles_kepernyo', {
        'aktiv': aktiv['nev'],
        'kerdes': kerdes['kerdes'],
        'valaszok': kerdes['valaszok'],
        'jatekosok': jatekterem['jatekosok'],
        'tabla': jatekterem['tabla_zsetonok']
    }, to='jatek')

@socketio.on('tipp_elkuldese')
def tipp_elkuldese(data):           

   
    def tipp_elkuldese(data):
        print("TIPP ÉRKEZETT:", data)

    nev = None
    for j in jatekterem['jatekosok']:
        if j['sid'] == request.sid:
            nev = j['nev']
            break

    if nev:
        jatekterem['tippek'][nev] = data['tipp']
        jatekterem['tetek'][nev] = data['tet']

    aktiv = jatekterem['jatekosok'][jatekterem['aktualis']]
    tippeloк = [j for j in jatekterem['jatekosok'] if j['nev'] != aktiv['nev']]
    mindenki_tippelt = all(j['nev'] in jatekterem['tippek'] for j in tippeloк)

    if mindenki_tippelt:
        szamol_eredmeny()

def szamol_eredmeny():
    aktiv = jatekterem['jatekosok'][jatekterem['aktualis']]
    sajat_valasz = jatekterem['sajat_valasz']
    eredmenyek = []
    helyes_tippek = 0

    for j in jatekterem['jatekosok']:
        if j['nev'] == aktiv['nev']:
            continue
        tipp = jatekterem['tippek'].get(j['nev'])
        tet = jatekterem['tetek'].get(j['nev'], 0)
        if tipp == sajat_valasz:
            helyes_tippek += 1
            nyeremeny = tet * 2
            j['zsetonok'] += nyeremeny
            jatekterem['tabla_zsetonok'] -= nyeremeny
            eredmenyek.append({'nev': j['nev'], 'helyes': True, 'tet': tet, 'nyeremeny': nyeremeny})
        else:
            j['zsetonok'] -= tet
            jatekterem['tabla_zsetonok'] += tet
            eredmenyek.append({'nev': j['nev'], 'helyes': False, 'tet': tet, 'nyeremeny': 0})

    aktiv['zsetonok'] += helyes_tippek
    jatekterem['tabla_zsetonok'] -= helyes_tippek

    if jatekterem['tabla_zsetonok'] < 0:
        jatekterem['tabla_zsetonok'] = 0

    kerdes = jatekterem['aktualis_kerdes']
    emit('eredmeny_kepernyo', {
        'aktiv': aktiv['nev'],
        'sajat_valasz': sajat_valasz,
        'valaszok': kerdes['valaszok'],
        'eredmenyek': eredmenyek,
        'jatekosok': jatekterem['jatekosok'],
        'tabla': jatekterem['tabla_zsetonok']
    }, to='jatek')

@socketio.on('kovetkezo_kor')
def kovetkezo_kor():
    jatekterem['aktualis'] = (jatekterem['aktualis'] + 1) % len(jatekterem['jatekosok'])
    jatekterem['allapot'] = 'kerdes'
    kuldd_kerdes_kepernyo()

if __name__ == '__main__':
    jatekterem['jatekosok'] = []
    jatekterem['tabla_zsetonok'] = 0
    jatekterem['aktualis'] = 0
    jatekterem['allapot'] = 'varakozas'
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)