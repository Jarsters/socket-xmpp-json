const { timeStamp } = require("console")
let net = require("net")
let utf8 = require("utf8")

let quote = [
    "Di belakang pria yang hebat ada wanita yang memutar matanya",
    "Karena nila setitik rusak susu sebelanga. Peribahasa ini nggak berlaku kalau susunya adalah susu bubuk",
    "Kalau saja mulutmu itu BPKB, pasti sudah ku gadaikan",
    "Rumah tangga itu rumit. Kalau sederhana itu namanya rumah makan",
    "Saat gerimis datang ingat mantan, waktu hujan turun ingat kenangan, pas banjir menyerbu baru ingat Tuhan",
    "Jangan berharap pada TIM SAR untuk menemukan jodoh mu",
    "Berhentilah mencari orang yang sempurna. Cukup cari orang yang punya uang, mobil, dan rumah",
    "Cantik itu relatif tergantung posisi kamera serta intensitas cahayanya",
    "Jika seseorang melempar mu dengan batu, balaslah dengan bunga tapi sekalian dengan potnya",
    "Terus-terusan mengenang mantan adalah cara terbaik menuju rumah sakit jiwa",
    "Cantik itu relatif, photoshop itu alternative",
    "Aku mau dimadu, asal kamu mau diracun",
    "Tuhan pasti memberi jalan buat kita, tapi belum dicor",
    "Pekerjaan seberat apapun akan lebih terasa ringan jika kita tidak mengerjakannya",
    "Sepandai-pandai menyimpan istri muda, akhirnya tua juga",
    "Yang jomblo jangan pernah merasa malu. Jomblo bukan berarti gak laku, tapi emang nggak ada yang mau",
    "Jangan suka membohongi diri sendiri. Karena membohongi dirimu sudah jadi tugas orang lain",
    "Terkadang ketika aku menutup mata, aku tidak bisa melihat",
    "Kesuksesan seseorang selalu berawal dari mimpi. Jadi marilah kita tidur",
    "Selama masih makan mie instan campur nasi, enggak usah janji bahagiakan anak orang",
    "Selalu ikuti kata hatimu. Tapi ingat, bawalah otak mu juga",
    "Carilah uang, karena dia tak punya kaki untuk datang padamu",
    "Saat semua pekerjaan dirasa makin tidak menyenangkan, ingatlah akan cicilan",
    "Cinta tak mengenal warna kulit, tapi mengenal warna duit",
    "Jika kita memimpikan seseorang, itu tandanya kita sedang tidur",
    "Jadilah seperti bulu ketiak, meskipun hidup terhimpit, terjepit, dan tertekan, tetapi tetap tumbuh subur",
    "Kenapa kau melakukannya hari ini jika bisa melakukannya besok?",
    "Teruslah bermimpi sampai jam alarm membangunkan mu",
    "Seberat apa pun masalah mu, jangan ditimbang, gak bakalan laku",
    "Hati-hati memilih teman bercerita. Jangan sampai kau cerita ubi, sampai ke orang lain sudah jadi kolak",
    "Hidup itu cuma sebentar, ngejomblonya yang kelamaan",
    "Jodoh memang gak ke mana, tapi saingan ada di mana-mana",
    "Kerja keraslah sampai tetangga berpikir rezeki mu hasil dari pesugihan",
    "Duit memang nggak dibawa mati. Tapi kalau nggak ada duit, berasa mau mati",
    "Cowoknya cool, ceweknya hot, anaknya pasti dispenser",
    "Menggapai dunia itu kayak makan kuaci, kenyangnya minimal tapi lelahnya maksimal",
    "Contohlah tukang parkir. Meskipun punya banyak mobil, ia tak pernah sombong karena tahu itu semua hanya titipan",
    "Cara terbaik dan ampuh untuk membuat orang mengingat kita adalah dengan meminjam uang",
    "Tadi saya beli obat tidur. Pas dibawa pulang harus pelan-pelan, soalnya takut obatnya bangun",
    "Nggak ada bahu pacar? Tenang aja, masih ada bahu jalan buat bersandar",
    "Selingkuh terjadi bukan karena ada niat, selingkuh terjadi karena pacar kamu masih laku",
    "Kamu emang penyuka binatang ya? Udah tahu buaya, masih aja disayang",
    "Dear mantan, hidup tanpa kamu ternyata jauh lebih mudah daripada hidup tanpa handphone",
    "Kamu pacar apa sandal jepit. Gampang banget diambil orang",
    "Badan lemas, tenggorokan sakit, mata berkunang-kunang, kata dokter: Keracunan janji manis",
    "Setiap hari, kasur dan kamar mandi selalu berusaha untuk merebut perhatianmu",
    "Rasanya aku selalu salah di mata kamu, kalau gitu aku pindah aja ke hidung",
    "Muka jangan ditinggal kalau pergi kerja, jadi pas di kantor tidak usah cari muka lagi",
    "Secinta-cintanya kamu dengan Tuhan, jangan pernah berinisiatif untuk menemui-Nya terlebih dahulu",
    "Pusing karena tugas menumpuk? Coba dijejerin biar tidak menumpuk lagi",
    "Jatuh cinta itu pakai perasaan, tapi memeliharanya harus pakai penghasilan",
    "Aku diputusin karena beda keyakinan. Aku yakin kalau aku ganteng, tapi dia enggak",
    "Aku ini bukan pemalas, tapi hanya sedang menjalankan mode hemat energi saja",
    "Masih berharap dan selalu berharap, lama-lama aku jadi juara harapan",
    "Motor ku jelek tapi punya sejuta cerita. Motor mu bagus tapi sejuta sebulan",
    "Bercandanya bikin sayang, tapi sayangnya cuma bercanda",
    "Kunci tubuh yang sehat sebenarnya cuma satu, jangan sakit",
    "Sekali terjatuh, bangunlah, dua kali, tetaplah tegar, jika jatuh lagi juga, makanya kalau jalan pakai mata",
    "Saya menemukan hanya ada satu cara untuk terlihat kurus: Kumpul bersama orang gendut",
    "Tidur siang terdengar sangat kekanak-kanakan. Aku lebih suka menyebutnya jeda kehidupan horizontal",
    "Ketika cinta memandang lewat teleskop, cemburu malah melihat dari mikroskop",
    "Konon jika jodoh adalah tulang rusuk, maka mantan sudah menjadi fosil alias tulang belulang",
    "Sebagian orang itu ibarat awan mendung, saat mereka tidak ada, dunia akan menjadi lebih cerah",
    "Sepandai-pandainya tupai melompat, pasti akan jatuh juga. Sejomblo-jomblonya seseorang, pasti akan nikah juga",
    "Hidup itu hanya sekali. Maka tersenyumlah selagi kamu punya gigi",
    "Hari ini aku jadi sangat rajin. Rajinnya untuk malas-malasan",
    "Mau mandi, tapi sedang bosan, karena gerakan saat mandi monoton terus",
    "Yang baik baik ditolak, yang berandalan dipacarin, giliran disakiti ngomongnya: Semua cowok sama aja",
    "Itu pintu hati atau pintu tol, yang masuk hanya yang bermobil saja",
    "Itu yang pacaran nangis mulu, pacaran sama orang atau bawang",
    "Hidup itu banyak cobaan, kalau banyak saweran ya dangdutan",
    "Kacang itu rasanya guring, tapi dikacangain rasanya perih",
    "Secapek-capeknya kerja, lebih capek nganggur",
    "Nabung setengah mati, habisinnya setengah sadar",
    "Manusia menciptakan ponsel. Ponsel makin pintar, manusia tidak",
    "Cuma mau mengingatkan, sudah musim hujan, hati-hati alis hilang",
    "Sekali mendayung, dua tiga hari pegelnya nggak ilang-ilang",
    "Tuhan tolong jaga dia ketika aku sedang bersama yang lain",
    "Kambing yang tidak pernah mandi banyak banget yang nyari. Gimana kamu yang mandinya sampai tiga kali dalam sehari",
    "Cinta bisa mengalahkan segalanya, kecuali kemiskinan dan sakit gigi",
    "Jika kamu terlalu berpikiran terbuka, otakmu akan jatuh",
    "Otakku seperti segitiga bermuda. Informasi masuk, namun kemudian mereka tidak bisa ditemukan lagi",
    "Jika kamu merasa sulit menertawakan dirimu sendiri, aku akan dengan senang hati melakukannya untukmu",
    "Menikahlah dengan pria seusia mu. Saat kecantikanmu memudar, penglihatannya juga akan berkurang",
    "Seberat apa pun masalah mu, jangan lupa mengeluh",
    "Tahukah Anda? Ternyata pedagang kaki lima itu kakinya cuma ada dua",
    "Pasangan yang ideal adalah pasangan yang saling melengkapi. Dia melengkapi hidup Anda, Anda melengkapi penderitaannya",
    "Ketahuilah, pria yang mencium istrinya setiap hari akan memiliki hubungan lebih lama dibandingkan pria yang mencium istri tetangganya",
    "Kalau zombie menyerbu, kamu bakal aman. Karena yang mereka incar adalah otak",
    "Ketika kamu merasa cobaan hidupmu terlalu berat, itu karena Tuhan tau kamu bisa mengatasinya. Kalo masih berat juga, diet dong",
    "Sebenernya gue termasuk anak nongkrong, soalnya kebetulan WC di rumah gue WC jongkok",
    "Saat aku sedih kau di samping ku, saat aku marah kau ada di dekat ku. Saat aku menangis kau di sisiku, Sekarang aku sadar, jangan-jangan kau adalah pembawa sial untukku",
    "Jika orang itu menyebut mu jelek, janganlah berputus asa, belum tentu orang itu berkata bohong",
    "Jika kamu merasa kesepian, matikan lampu dan tontonlah film horor. Maka kamu tidak akan merasakan kesepian lagi",
    "Berakit-rakit dahulu, berenang-renang ke tepian. Bersakit-sakit dahulu, meriang-meriang kemudian",
    "Jangan suka jadi orang serakah. Karena orang yang serakah itu pasti ditaksir KPK",
    "Hari mu buruk? Teruslah semangat menjalani hidup karena siapa tahu besok lebih buruk",
    "Uang tidak bisa membawa kebahagiaan kalau uangnya tidak di rekening kita",
    "Jangan mengulangi kesalahan yang sama karena kesalahan yang lain masih ada",
    "Tidak apa-apa mendapat nilai jelek, asal ada teman yang nilainya lebih jelek",
]

let IP_TRACKER = "192.168.1.5"

let json_text = {"ip_local": "192.168.1.5", "port": 60618, "type": "client", "is_private": true}
let register = {"type": "auth", "username": "joker", "password": "yttaygy", "register": 1}
let login = {"type": "auth", "username": "joker", "password": "yttaygy"}
let packet_hello_relay = {username: "joker", message: "hello!"}
let balasan_untuk_relay = {stanza: "message", from: "joker", to: "someone", body: "messages", lang: "id", time_send: Date.now()}
let ip_manager = {}
let ip_relay = {}
let has_manager = false

let client_tracker = new net.Socket()
let client_manager = new net.Socket()
let client_relay = new net.Socket()

function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

const send_message = async (connection, msg) => {
    connection.write(utf8.encode(JSON.stringify(msg)))
    await sleep(2000)
}

const get_random_quote = (number) => {
    let choosen = number
    if(!number){
        choosen = Math.floor(Math.random() * quote.length)
    }
    return quote[choosen]
}

const action_tracker = (IP_TRACKER) => {
    // Melakukan koneksi ke tracker
    client_tracker.connect(5000, IP_TRACKER, function() {
        // Mengirimkan pesan json_text kepada tracker
        send_message(client_tracker, json_text)
        console.log("Connected to Tracker")
    })
    
    // Menerima data dari tracker
    client_tracker.on('data', async (data)=>{
        let datas = Buffer.from(data)
        let dataJSON = JSON.parse(datas.toString())
        for (let index = 0; index < dataJSON.length; index++) {
            const d = dataJSON[index]
            if(d.type == "manager"){
                console.log("Manager sudah ada")
                ip_manager = {ip: d.ip_local, port: d.port}
                console.log(dataJSON)
                console.log(ip_manager)
                action_manager(ip_manager.ip, ip_manager.port)
                has_manager = true
                break
            }
        }
        await sleep(2000)
        if(!has_manager){
            console.log("Manager belum tersedia!")
            send_message(client_tracker, {"message": "get components"})
        }
    })    
}

const action_manager = (ip, port) => {
    // Melakukan koneksi kepada manager
    client_manager.connect(port, ip, () => {
        // Mengirimkan pesan json_text kepada manager
        send_message(client_manager, json_text)
        console.log("Connected to manager")
        // Melakukan registrasi otomatis kepada manager
        send_message(client_manager, register)
    })

    // Menerima data dari manager
    client_manager.on('data', async (data)=>{
        let datas = Buffer.from(data)
        datas = JSON.parse(datas.toString().replace('\x80\x81\x82', ""))
        console.log(datas)
        // Melakukan login jika sudah registrasi
        if(datas.code != 200 && datas.code != 201){
            send_message(client_manager, login)
        }
        else {
            ip_relay = {ip: datas.component[0].ip_local, port: datas.component[0].port}
            console.log(`Ini IP Relay:`)
            console.log(ip_relay)
            action_relay(ip_relay.ip, ip_relay.port)
        }
        await sleep(3000)
    })
}

const action_relay = (ip, port) => {
    // Melakukan koneksi kepada relay
    client_relay.connect(port, ip, () => {
        // Mengirimkan pesan inisiasi kepada relay
        send_message(client_relay, packet_hello_relay)
        console.log("Connected to relay")
    })

    // Menerima data dari relay
    client_relay.on('data', async (data)=>{
        let datas = Buffer.from(data)
        datas = JSON.parse(datas.toString().replace('\x80\x81\x82', ""))
        console.log(`${datas.from}: ${datas.body}`)
        balasan_untuk_relay["to"] = datas.from
        let permintaan = datas.body.toLowerCase()
        console.log(datas)
        // Cek kata "mau quote"
        if(permintaan.substring(0, 9) == "mau quote"){
            let nomor = permintaan.replace("mau quote", "")
            if(nomor == 0 || nomor) {
                nomor = parseInt(nomor)
            }
            balasan_untuk_relay["body"] = get_random_quote(nomor)
            send_message(client_relay, balasan_untuk_relay)
        }
        // Jika tidak diawali dengan "mau quote"
        else {
            balasan_untuk_relay["body"] = "Permintaan tidak dapat diproses"
            send_message(client_relay, balasan_untuk_relay)
        }
        console.log("======================================")
    })
}

const connect_to_server = (IP_TRACKER) => {
    action_tracker(IP_TRACKER)
}

var prompt = require("prompt");
prompt.start();
console.log("Local?")
prompt.get(["y/n"], function(err, res){
    katakan = res["y/n"]
    if(katakan.toLowerCase() == "y"){ 
        connect_to_server(IP_TRACKER)
    } else {
        IP_TRACKER = "103.149.177.78"
        connect_to_server(IP_TRACKER)
    }
});