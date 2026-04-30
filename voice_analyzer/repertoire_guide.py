"""
Müzik Tür Önerileri ve Repertuvar Rehberi
Ses türüne göre uygun müzik tarzları ve örnek eserler
"""

# Her ses türü için detaylı repertuvar önerileri
# Şarkı isimleri ve besteci bilgileri telife tabi DEĞİLDİR
# (sözler ve ses kayıtları telife tabidir, ama referans verebiliriz)

REPERTOIRE_GUIDE = {
    'Coloratura Soprano': {
        'tr_description': 'En yüksek ve en çevik kadın ses türü. Süsleme (koloratur) pasajları, hızlı geçişler ve yüksek notalarda parlaklık ile karakterizedir.',
        'classical_genres': ['Bel Canto Opera', 'Barok Aryalar', 'Mozart Operaları', 'Lied', 'Oratoryo'],
        'modern_genres': ['Klasik Crossover', 'Caz (light, kafa registeri ağırlıklı)', 'Disney/Müzikal (Ariel, Glinda)'],
        'famous_examples': [
            'Mozart — "Der Hölle Rache" (Sihirli Flüt, Gece Kraliçesi aryası)',
            'Donizetti — "Una furtiva lagrima" repertuvarı, "Lucia di Lammermoor" çılgınlık sahnesi',
            'Bellini — "Casta Diva" (Norma)',
            'Verdi — "Sempre libera" (La Traviata)',
            'Strauss — Zerbinetta aryası (Ariadne auf Naxos)'
        ],
        'modern_examples': [
            'Sarah Brightman repertuvarı',
            'Disney filmlerinde "Let It Go" (Idina Menzel - belt mix)',
            'Müzikallerde "Glitter and Be Gay" (Candide)'
        ],
        'avoid': 'Düşük register ağırlıklı blues, gospel, ağır rock vokali. Aşırı göğüs sesi gerektiren parçalar.',
        'tips': 'Koloratur çevikliği için günlük "messa di voce" ve trill çalışmaları yapın. Yüksek registerde bile metnin anlamını kaybetmemeye özen gösterin.'
    },
    
    'Lirik Soprano': {
        'tr_description': 'Sıcak, yumuşak ve lirik karakterli soprano sesi. Romantik melodilerde ve duygusal pasajlarda parlar.',
        'classical_genres': ['Romantik Opera', 'Italian Lirik Repertuvarı', 'Lied', 'Oratoryo', 'Operetta'],
        'modern_genres': ['Müzikal Tiyatro', 'Klasik Crossover', 'Pop (lirik)', 'Caz Standartları'],
        'famous_examples': [
            'Puccini — "O mio babbino caro" (Gianni Schicchi), "Un bel dì vedremo" (Madama Butterfly)',
            'Verdi — "Caro nome" (Rigoletto)',
            'Mozart — Susanna ve Pamina aryaları',
            'Gounod — Juliette aryaları (Roméo et Juliette)',
            'Dvořák — "Song to the Moon" (Rusalka)'
        ],
        'modern_examples': [
            'Müzikallerde "I Could Have Danced All Night" (My Fair Lady)',
            '"Think of Me" (Phantom of the Opera)',
            'Disney "A Whole New World" (kadın partisi)',
            'Norah Jones, Diana Krall tarzı caz'
        ],
        'avoid': 'Aşırı koloratur gerektiren parçalar, ağır dramatik repertuvar (genç yaşta sesi yorabilir).',
        'tips': 'Legato ve cantabile çizgisini geliştirin. Frazlar arası nefes desteğini güçlendirin.'
    },
    
    'Dramatik Soprano': {
        'tr_description': 'Güçlü, dolgun ve geniş kapsamlı soprano. Wagner ve Verdi\'nin ağır rollerini taşıyabilir.',
        'classical_genres': ['Wagner Operaları', 'Geç Verdi', 'Strauss', 'Verismo'],
        'modern_genres': ['Power Ballad', 'Müzikal (dramatik roller)', 'Sembolik Rock'],
        'famous_examples': [
            'Wagner — Brünnhilde, Isolde rolleri',
            'Verdi — "Pace, pace, mio Dio" (La Forza del Destino), Aida aryaları',
            'Puccini — Tosca, Turandot rolleri',
            'Strauss — Salome, Elektra'
        ],
        'modern_examples': [
            '"Defying Gravity" (Wicked)',
            'Celine Dion power ballad\'ları',
            'Aretha Franklin benzeri büyük orkestra eşliği parçalar'
        ],
        'avoid': 'Hafif, çevik koloratur eserler — sesinizin doğal ağırlığına ters düşer.',
        'tips': 'Sesi zorlamadan kullanın — büyük ses doğal olarak orada, "iterek" çıkartmaya çalışmayın. Düzenli teknik çalışma şart.'
    },
    
    'Mezzo-Soprano': {
        'tr_description': 'Sıcak ve dolgun orta-kadın sesi. Hem soprano hem alto repertuvarına uzanabilir.',
        'classical_genres': ['Bel Canto Mezzo Rolleri', 'Mozart (Cherubino, Dorabella)', 'Carmen tarzı', 'Lied', 'Barok'],
        'modern_genres': ['Pop (Adele tarzı)', 'Müzikal', 'Caz', 'Soul', 'R&B'],
        'famous_examples': [
            'Bizet — "Habanera" (Carmen)',
            'Saint-Saëns — "Mon coeur s\'ouvre à ta voix" (Samson et Dalila)',
            'Rossini — Rosina aryaları (Il Barbiere di Siviglia)',
            'Mozart — "Voi che sapete" (Le Nozze di Figaro)'
        ],
        'modern_examples': [
            'Adele — "Hello", "Rolling in the Deep"',
            'Amy Winehouse repertuvarı',
            '"Memory" (Cats müzikali)',
            'Norah Jones, Sade'
        ],
        'avoid': 'Çok yüksek soprano notaları zorlamayın. Düşük registerlerinizin de gücünü sergileyin.',
        'tips': 'Mezzo sesi orta registerde maksimum etki yapar. Adele\'in başarısı tessitura kullanımında — siz de kendi tessitura\'nızda ısrarcı olun.'
    },
    
    'Kontralto': {
        'tr_description': 'En düşük ve en nadir kadın sesi. Koyu, dolgun ve karizmatik bir tını.',
        'classical_genres': ['Barok Oratoryolar (Bach, Handel)', 'Wagner Kontralto Rolleri', 'Erden Sesleri'],
        'modern_genres': ['Soul', 'Blues', 'Jazz', 'Gospel', 'Folk'],
        'famous_examples': [
            'Bach — Matthäus-Passion ve Magnificat alto aryaları',
            'Handel — "He was despised" (Messiah)',
            'Wagner — Erda rolü (Ring of the Nibelung)'
        ],
        'modern_examples': [
            'Cher — "If I Could Turn Back Time"',
            'Tracy Chapman — "Fast Car" tarzı',
            'Toni Braxton tarzı koyu balladlar',
            'Nina Simone repertuvarı'
        ],
        'avoid': 'Yüksek soprano ari\'leri; sesin doğal ergonomisine uygun değil.',
        'tips': 'Düşük register büyük zenginliğiniz — onu zorlamadan, doğal rezonansla kullanın. Cher tarzı koyu, dolgun tınıyı keşfedin.'
    },
    
    'Kontratenor': {
        'tr_description': 'Erkek vokalistlerin alto/mezzo registerinde söylediği, falsetto tabanlı bir teknik. Barok döneminde altın çağını yaşadı.',
        'classical_genres': ['Barok Opera (Handel, Vivaldi)', 'Erken Müzik', 'Çağdaş Bestelenmiş Eserler'],
        'modern_genres': ['Art Pop (Anohni tarzı)', 'Sınırlı R&B', 'Avant-garde'],
        'famous_examples': [
            'Handel — "Ombra mai fù" (Serse), Rinaldo ve Giulio Cesare aryaları',
            'Vivaldi — Stabat Mater',
            'Pergolesi — Stabat Mater'
        ],
        'modern_examples': [
            'Anohni (Antony and the Johnsons) repertuvarı',
            'Klaus Nomi tarzı avant-garde',
            'Jeff Buckley\'nin yüksek register\'da kullandığı parçalar'
        ],
        'avoid': 'Tenor/bariton ağır rolleri. Falsetto tekniğini doğru kullanmadan zorlama.',
        'tips': 'Modal ve falsetto register arasında yumuşak geçiş çok önemli. Düzenli tekrar kullanma stratejisi geliştirin.'
    },
    
    'Lirik Tenor': {
        'tr_description': 'Romantik, parlak ve esnek erkek sesi. Aşk şarkılarının ve lirik aryaların doğal sahibi.',
        'classical_genres': ['Italian Bel Canto', 'Mozart Tenor Rolleri', 'Fransız Operası', 'Lied'],
        'modern_genres': ['Pop (lirik tenor)', 'Klasik Crossover', 'Müzikal', 'Müzikal Romantik'],
        'famous_examples': [
            'Puccini — "Che gelida manina" (La Bohème), "E lucevan le stelle" (Tosca)',
            'Donizetti — "Una furtiva lagrima" (L\'elisir d\'amore)',
            'Bizet — "La fleur que tu m\'avais jetée" (Carmen)',
            'Mozart — Tamino aryaları'
        ],
        'modern_examples': [
            'Andrea Bocelli — "Con te partirò"',
            'Josh Groban repertuvarı',
            'Il Divo tarzı klasik crossover',
            'Sam Smith — "Stay With Me"',
            'Ed Sheeran — "Perfect"'
        ],
        'avoid': 'Çok ağır dramatik tenor rolleri (Otello, Tristan), aşırı baritonal repertuvar.',
        'tips': 'Squillo (parlak yüksek nota) ve dolce (yumuşak) tonlar arasındaki dengeyi koruyun. Pavarotti, Gigli, Björling sesleri model alınabilir.'
    },
    
    'Dramatik Tenor': {
        'tr_description': 'Heroik, güçlü ve dolgun tenor. En ağır opera rollerini taşıyabilir.',
        'classical_genres': ['Wagner Operaları (Heldentenor)', 'Geç Verdi', 'Verismo', 'Strauss'],
        'modern_genres': ['Rock Vokali', 'Power Ballad', 'Metal'],
        'famous_examples': [
            'Wagner — Tristan, Siegfried, Parsifal',
            'Verdi — Otello, Manrico (Il Trovatore — "Di quella pira")',
            'Puccini — "Nessun dorma" (Turandot)',
            'Leoncavallo — "Vesti la giubba" (Pagliacci)'
        ],
        'modern_examples': [
            'Freddie Mercury (Queen) — "Bohemian Rhapsody"',
            'Steve Perry (Journey)',
            'Robert Plant (Led Zeppelin) — yüksek register parçaları',
            'Bruce Dickinson (Iron Maiden)'
        ],
        'avoid': 'Erken yaşta ağır dramatik repertuvar (sesi yorma riski). Lirik koloratur.',
        'tips': 'Sesinizin doğal gücünü itmeyin — destekli nefes ile gelmeli. "Squillo" ile parlaklığı koruyun.'
    },
    
    'Bariton': {
        'tr_description': 'Erkek seslerinin "altın orta noktası". Hem dramatik hem lirik geniş bir yelpazede.',
        'classical_genres': ['Verdi Bariton Rolleri', 'Mozart', 'Wagner', 'Lied'],
        'modern_genres': ['Pop (Frank Sinatra tarzı)', 'Caz Standartları', 'Country', 'Soul'],
        'famous_examples': [
            'Verdi — Rigoletto, "Cortigiani, vil razza dannata"; Iago, "Credo in un Dio crudel"',
            'Mozart — "Madamina, il catalogo è questo" (Don Giovanni - Leporello)',
            'Rossini — "Largo al factotum" (Il Barbiere di Siviglia)',
            'Wagner — Wolfram aryaları (Tannhäuser)'
        ],
        'modern_examples': [
            'Frank Sinatra — "My Way", "Fly Me to the Moon"',
            'Michael Bublé repertuvarı',
            'Elvis Presley — bariton tarafı',
            'Johnny Cash — düşük bariton',
            'Hozier — "Take Me to Church"'
        ],
        'avoid': 'Çok yüksek tenor notaları zorlamayın. Bariton zenginliği kendi tessituranızdadır.',
        'tips': 'Bariton "konuşma sesi şarkı söylemenin uzantısıdır" prensibiyle gelişir. Net diksiyon ve doğal ergonomi anahtardır.'
    },
    
    'Bas-Bariton': {
        'tr_description': 'Basın derinliği ile baritonun esnekliğini birleştirir. Otoriter karakterler için ideal.',
        'classical_genres': ['Mozart (Don Giovanni, Figaro)', 'Wagner (Wotan)', 'Lied', 'Oratoryo'],
        'modern_genres': ['Crooner Pop', 'Country', 'Folk Rock', 'Gospel'],
        'famous_examples': [
            'Mozart — Don Giovanni rolü',
            'Wagner — Wotan rolü (Ring)',
            'Mussorgski — Boris Godunov (alt versiyonu)',
            'Verdi — Filippo II (Don Carlos)'
        ],
        'modern_examples': [
            'Leonard Cohen — "Hallelujah", "Suzanne"',
            'Nick Cave repertuvarı',
            'Tom Waits tarzı',
            'Johnny Cash — derin parçaları'
        ],
        'avoid': 'Yüksek lirik tenor repertuvarı, koloratur tarzı parçalar.',
        'tips': 'Sesin derinliği büyük armağan — onu sergileyin ama zorlama. Söz aktarımı (declamation) çok güçlü olabilir.'
    },
    
    'Bas': {
        'tr_description': 'En düşük erkek sesi. Görkemli, otoriter ve dini eserlerin temel taşı.',
        'classical_genres': ['Russian Bass Repertoire', 'Bach Pasyonları', 'Mozart Bass Rolleri', 'Wagner', 'Verdi Bass'],
        'modern_genres': ['Gospel (Bass)', 'Doo-Wop', 'Bazı Country', 'Drone Music'],
        'famous_examples': [
            'Mussorgski — Boris Godunov, Khovanshchina',
            'Mozart — "O Isis und Osiris" (Sihirli Flüt - Sarastro)',
            'Verdi — Filippo II ("Ella giammai m\'amò" — Don Carlos)',
            'Bach — bas aryaları (örn. Matthäus-Passion)',
            'Rossini — Don Basilio aryaları'
        ],
        'modern_examples': [
            'Barry White — derin spoken-sung tarzı',
            'Johnny Cash — en düşük register parçaları',
            'Tennessee Ernie Ford — "Sixteen Tons"',
            'Russian Orthodox Choir bas\'ları'
        ],
        'avoid': 'Tenor repertuvarı, yüksek bariton aryalar. Aşırı yüksek notalar zorlanabilir.',
        'tips': 'Bas sesi çok nadir — onu özenle koruyun. Düşük rezonansı maksimize eden teknikler geliştirin (Russian school referans alınabilir).'
    }
}


def get_repertoire_guide(voice_type):
    """Belirli bir ses türü için repertuvar önerileri döndürür"""
    if voice_type in REPERTOIRE_GUIDE:
        return REPERTOIRE_GUIDE[voice_type]
    return None


def get_genre_recommendations(voice_type):
    """Ses türüne uygun müzik tarzlarının yapılandırılmış listesi"""
    guide = REPERTOIRE_GUIDE.get(voice_type)
    if not guide:
        return None
    
    return {
        'description': guide['tr_description'],
        'classical_genres': guide['classical_genres'],
        'modern_genres': guide['modern_genres'],
        'classical_repertoire': guide['famous_examples'],
        'modern_repertoire': guide['modern_examples'],
        'avoid': guide['avoid'],
        'training_tips': guide['tips']
    }
