import os
import sys
#from nltk import FreqDist
try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""
try:
    import es_core_news_md
except (ModuleNotFoundError,ImportError):
    sys.path.insert(0,MODULE)
    import es_core_news_md
    sys.path.pop(0)
try:
    from .classifier import extract_opinion
except (ModuleNotFoundError,ImportError):
    sys.path.insert(0,MODULE)
    from classifier import extract_opinion
    sys.path.pop(0)
    

nlp = es_core_news_md.load()
nlp.remove_pipe('tagger')
nlp.remove_pipe('parser')

ENTITIES_TYPES = {
    'ORG': 'Organizacion',
    'LOC': 'Localizacion',
    'PER': 'Persona',
    'MISC': 'Miscelanea'
}

def entity_detection(text: str):
    """
    param: text: str: recibe el texto para extraer entidades \n
    ret: list: retorna las entidades detectadas en el texto

    Detecta las entidades en el texto y las procesa para eliminar los signos de puntuacion
    """

    doc = nlp(text)

    return [str(e).strip() for e in doc.ents]

def entities_classification(text: str):
    doc = nlp(text)
    ents = []

    for e in doc.ents:
        e_str = str(e).strip()
        e_type = e.label_
        if not _filter_entity(e_str):
            continue
        ents.append({'entity':e_str, 'type':e_type})

    return ents

def pipe_ents_detect(texts, nthreads = 2):
    """ optimiacion de  entity_detection para procesar varios textos"""
    res = []
    for doc in nlp.pipe(texts, n_threads=nthreads, batch_size=nthreads*4):
        res.append([str(e).strip() for e in doc.ents])
    return res


def pipe_ents_class(texts, nthreads=2):
    """ optimiacion de  entities_classification para procesar varios textos"""
    res = []
    for doc in nlp.pipe(texts, n_threads=nthreads, batch_size=nthreads*4):
        ents = []
        for e in doc.ents:
            e_str = str(e).strip()
            e_type = e.label_
            if not _filter_entity(e_str):
                continue
            ents.append({'entity': e_str, 'type': e_type})

    return res


def _filter_entity(entity:str):
    return len(entity) > 1 and not entity.isnumeric()

# def extract_main_entity(comment):
#     """ Esto no me queda claro que cumpla con su proposito, 
#     corregido dentro pipe_opinion_main_entity y debjo """
#     entities_list = entity_detection(comment)
#     # main_entity = ''
#     # best_freq = -1
#     # for word in entities_list:
#     #     if FreqDist(word).N()/len(comment) > best_freq:
#     #         main_entity = word
#     main_entity = entities_list[0]
#     best_freq = -1
#     ff = FreqDist(entities_list)
#     for word in entities_list:
#         if ff[word] > best_freq:
#             best_freq = ff[word]
#             main_entity = word

#     return main_entity


# def opinion_main_entity(comments):
#     '''
#     param: lista de str (comentarios)
#     return: lista de tuplas de tipo -> (main_ent del comentario, opinion de main_ent)
#     '''
#     me = [extract_main_entity(comment) for comment in comments]
#     op = extract_opinion(comments)
#     return [(me[i], op[i]) for i in range(len(op))]


# def pipe_opinion_main_entity(comments):
#     '''
#     param: lista de str (comentarios)
#     return: lista de tuplas de tipo -> (main_ent del comentario, opinion de main_ent)
#     '''
#     me = pipe_ents_detect(comments)
#     me2 = []
#     for nn,entities_list in enumerate(me):
#         main_entity = entities_list[0]
#         best_freq = -1
#         ff = FreqDist(entities_list)
#         for word in entities_list:
#             if ff[word] > best_freq:
#                 best_freq = ff[word]
#                 main_entity = word
#         me2.append(main_entity)
#     op = extract_opinion(comments)
#     return [(me2[i], op[i]) for i in range(len(op))]

if __name__ == '__main__':
    import time
    txt = ['Un disparo de Emil Forsberg desde fuera del área, que para mala suerte del arquero y de Suiza fue desviado por el defensor Manuel Akanki, bastó a Suecia para clasificar este martes a los cuartos de final del Mundial de Fútbol y ser parte de un club que ya forman Brasil, Francia, Rusia, Bélgica, Croacia y Uruguay.','En un partido igualado entre dos equipos de fuerza y defensa organizada, ese momento en que el centrocampista Forsberg quedó con espacio cerca del área suiza fue suficiente para marcar la diferencia, luego de una primera mitad en que ambos equipos trataron sin lograr concretar.', 'El VAR volvió a ser protagonista cuando ya casi terminaba el partido y Michael Lang hizo una falta sobre Martin Olson, escapado en solitario muy cerca de la puerta suiza. Se trataba de verificar si fue dentro o fuera la infracción, pero finalmente quedó establecido que fuera, por lo que quedó en tiro libre, aunque se mantuvo la expulsión para Lang.']
    t=time.time()
    entity_detection(txt[0])
    print('entity_detection: '+str(time.time()-t))
    t = time.time()
    entities_classification(txt[0])
    print('entities_classification: '+str(time.time()-t))
    t = time.time()
    pipe_ents_detect(txt)
    print('pipe_ents_detect: '+str(time.time()-t))
    t = time.time()
    pipe_ents_class(txt)
    print('pipe_ents_class: '+str(time.time()-t))
    t = time.time()
    # extract_main_entity(txt[0])
    # print('extract_main_entity: '+str(time.time()-t))
    # t = time.time()
    # opinion_main_entity(txt)
    # print('opinion_main_entity: '+str(time.time()-t))
    # t = time.time()
    # pipe_opinion_main_entity(txt)
    # print('pipe_opinion_main_entity: '+str(time.time()-t))
