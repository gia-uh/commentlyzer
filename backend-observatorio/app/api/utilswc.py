from collections import Counter
import re
from io import BytesIO

stopwordsd = set(["de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "no", "una", "su", "al", "lo", "como", "m\\u00e1s", "pero", "sus", "le", "ya", "o", "este", "s\\u00ed", "porque", "esta", "entre", "cuando", "muy", "sin", "sobre", "tambi\\u00e9n", "me", "hasta", "hay", "donde", "quien", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "m\\u00ed", "antes", "algunos", "qu\\u00e9", "unos", "yo", "otro", "otras", "otra", "\\u00e9l", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi", "mis", "t\\u00fa", "te", "ti", "tu", "tus", "ellas", "nosotras", "vosostros", "vosostras", "os", "m\\u00edo", "m\\u00eda", "m\\u00edos", "m\\u00edas", "tuyo", "tuya", "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras", "esos", "esas", "estoy", "est\\u00e1s", "est\\u00e1", "estamos", "est\\u00e1is", "est\\u00e1n", "est\\u00e9", "est\\u00e9s", "estemos", "est\\u00e9is", "est\\u00e9n", "estar\\u00e9", "estar\\u00e1s", "estar\\u00e1", "estaremos", "estar\\u00e9is", "estar\\u00e1n", "estar\\u00eda", "estar\\u00edas", "estar\\u00edamos", "estar\\u00edais", "estar\\u00edan", "estaba", "estabas", "est\\u00e1bamos", "estabais", "estaban", "estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron", "estuviera", "estuvieras", "estuvi\\u00e9ramos", "estuvierais", "estuvieran", "estuviese", "estuvieses", "estuvi\\u00e9semos", "estuvieseis", "estuviesen", "estando", "estado", "estada", "estados", "estadas", "estad", "he", "has", "ha", "hemos", "hab\\u00e9is", "han", "haya", "hayas", "hayamos", "hay\\u00e1is", "hayan", "habr\\u00e9", "habr\\u00e1s", "habr\\u00e1", "habremos", "habr\\u00e9is", "habr\\u00e1n", "habr\\u00eda", "habr\\u00edas", "habr\\u00edamos", "habr\\u00edais", "habr\\u00edan", "hab\\u00eda", "hab\\u00edas", "hab\\u00edamos", "hab\\u00edais", "hab\\u00edan", "hube", "hubiste", "hubo", "hubimos", "hubisteis", "hubieron", "hubiera", "hubieras", "hubi\\u00e9ramos", "hubierais", "hubieran", "hubiese", "hubieses", "hubi\\u00e9semos", "hubieseis", "hubiesen", "habiendo", "habido", "habida", "habidos", "habidas", "soy", "eres", "es", "somos", "sois", "son", "sea", "seas", "seamos", "se\\u00e1is", "sean", "ser\\u00e9", "ser\\u00e1s", "ser\\u00e1", "seremos", "ser\\u00e9is", "ser\\u00e1n", "ser\\u00eda", "ser\\u00edas", "ser\\u00edamos", "ser\\u00edais", "ser\\u00edan", "era", "eras", "\\u00e9ramos", "erais", "eran", "fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron", "fuera", "fueras", "fu\\u00e9ramos", "fuerais", "fueran", "fuese", "fueses", "fu\\u00e9semos", "fueseis", "fuesen", "sintiendo", "sentido", "sentida", "sentidos", "sentidas", "siente", "sentid", "tengo", "tienes", "tiene", "tenemos", "ten\\u00e9is", "tienen", "tenga", "tengas", "tengamos", "teng\\u00e1is", "tengan", "tendr\\u00e9", "tendr\\u00e1s", "tendr\\u00e1", "tendremos", "tendr\\u00e9is", "tendr\\u00e1n", "tendr\\u00eda", "tendr\\u00edas", "tendr\\u00edamos", "tendr\\u00edais", "tendr\\u00edan", "ten\\u00eda", "ten\\u00edas", "ten\\u00edamos", "ten\\u00edais", "ten\\u00edan", "tuve", "tuviste", "tuvo", "tuvimos", "tuvisteis", "tuvieron", "tuviera", "tuvieras", "tuvi\\u00e9ramos", "tuvierais", "tuvieran", "tuviese", "tuvieses", "tuvi\\u00e9semos", "tuvieseis", "tuviesen", "teniendo", "tenido", "tenida", "tenidos", "tenidas", "tened"])

key_words = set(['dr','estados','msc','santa'])

default_color = 'red'

def max_color(data):
    data2 = data.pop('total')
    polarity = sorted(data.items(),key=lambda x: x[1],reverse=True)[0][0]
    if polarity=='Positivo':
        return 'green'
    elif polarity=='Negativo':
        return 'blue'
    elif polarity=='Objetivo':
        return 'orange'
    else:
        return 'red'

def parse_gen_colors(coms, return_words=True):
    words = Counter()
    wordspol = {}

    def add_word(j, op):
        if not(j.lower() in stopwordsd) and re.search('[^\w]',j) is None and len(j)>=2:
                words[j]+=1
                if j in wordspol:
                    wordspol[j][op]+=1
                    wordspol[j]['total']+=1
                else:
                    wordspol[j]={ "total": 0,
                        'Positivo': 0,
                        'Neutro': 0,
                        'Negativo': 0,
                        'Objetivo': 0}
                    wordspol[j][op]+=1
                    wordspol[j]['total']+=1

    skip_upto = 0
    for c, op in coms:
        ws = c.split(' ')
        for n, j in enumerate(ws):
            j = j.strip()
            if skip_upto and n<=skip_upto:
                continue
            if j.lower()==key_words:
                if n+1<len(ws):
                    if j.lower()=='estados' and ws[n+1].lower()=='unidos':
                        skip_upto = n+1
                        j = j+' '+ws[n+1]
                        add_word(j, op)
                    elif j.lower()=='santa' and ws[n+1].lower()=='clara':
                        skip_upto = n+1
                        j = j+' '+ws[n+1]
                        add_word(j, op)
                    else:
                        cont = 1
                        while n+cont<len(ws) and re.match('[A-Z]',ws[n+cont]):
                            cont+=1
                            j = j+' '+ws[n+cont]
                        add_word(j, op)
                        skip_upto=n+cont
            else:
                add_word(j, op)
    if return_words:
        return wordspol
    color_to_words={'red':[], 'green':[],'blue':[],'orange':[]}
    for i,data in wordspol.items():
        cl = max_color(data)
        color_to_words[cl].append(i)
    return color_to_words

def gen_word_cloud_data(coms, max_words=100):
    words = parse_gen_colors(coms)
    data = []
    for n,(w,wdata) in enumerate(sorted(words.items(),key=lambda x: x[1]['total'], reverse=True)):
        if n>=max_words:
            break
        word={  'name': w,
                'value': wdata['total'],
                'color': max_color(wdata)
                #'html': {'class': 'wc'+max_color(wdata)}
            }
        data.append(word)
    return data
