import sys
from random import randint
from pygame import *
 
init()
 
window = display.set_mode((1280, 720))
running = True
 
tela = 0
num  = ''
 
num_cats = [5, 7, 4]
 
listas = [
    [randint(0, 100) for _ in range(60)],

    [72, 85, 91, 63, 78, 56, 88, 44, 95, 67,
     73, 81, 50, 62, 84, 77, 93, 58, 70, 86,
     41, 69, 75, 89, 52, 64, 82, 97, 48, 76],
    
    []
]
 
info_listas = [[], [], []]
lista_total = [[], [], []]
cores       = [[], [], []]
 
fonte_mini   = font.SysFont("Arial", 12)
fonte_menor  = font.SysFont("Arial", 15)
fonte_media  = font.SysFont("Arial", 20)
fonte_titulo = font.SysFont("Arial", 36, True)
fonte_sub    = font.SysFont("Arial", 15)
 
FUNDO          = (245, 245, 252)
BRANCO         = (255, 255, 255)
PRETO          = ( 22,  22,  32)
CZ_CLARO       = (218, 218, 228)
CZ             = (150, 150, 162)
CZ_ESC         = ( 75,  75,  90)
AZUL           = ( 58, 124, 240)
RETANGULAO_BG  = (255, 255, 255)
SOMBRA         = (210, 210, 222)
 

PALETA = [
    (255,  85,  85),
    (255, 168,  38),
    ( 72, 199, 142),
    ( 52, 152, 219),
    (155,  89, 182),
    (241, 196,  15),
    (230,  52, 126),
    ( 26, 188, 156),
]
 
GX = 112
GY = 122
GW = 1046
GH = 385
 
#calculo
 
def calcula_limites(id):
    n       = num_cats[id]
    num_min = min(listas[id])
    num_max = max(listas[id])
 
    if num_max == num_min:
        num_min = 0
 
    tam_cat = (num_max - num_min) / n
    faixas  = [[num_min + i * tam_cat, num_min + (i + 1) * tam_cat] for i in range(n)]
 
    info_listas[id] = [num_min, num_max, tam_cat, faixas]
    lista_total[id] = [0] * n
 
 
def contabiliza_totais(id):
    calcula_limites(id)
 
    for numero in listas[id]:
        if numero == info_listas[id][1]:
            lista_total[id][-1] += 1
            continue
        for i_cat in range(num_cats[id]):
            lim_inf = info_listas[id][0] + i_cat * info_listas[id][2]
            lim_sup = lim_inf + info_listas[id][2]
            if lim_inf <= numero < lim_sup:
                lista_total[id][i_cat] += 1
                break
 
 
def gera_contagens_aleatorias(id):
    total    = len(listas[id])
    n        = num_cats[id]
    restante = total
    contagens = []
 
    for _ in range(n - 1):
        maximo = min(restante, total // n * 2)
        qtd    = randint(0, maximo)
        contagens.append(qtd)
        restante = max(0, restante - qtd)
 
    contagens.append(randint(0, restante))
    lista_total[id] = contagens
 
 
def encher_lista_cores(id, n):
    for i in range(n):
        cores[id].append(PALETA[i % len(PALETA)])
 
 
#Desenho
 
def desenha_retangulao():
    draw.rect(window, SOMBRA,        ( 38, 96, 1208, 478), border_radius=16)
    draw.rect(window, RETANGULAO_BG, ( 34, 92, 1208, 478), border_radius=16)
 
 
def desenha_eixos(maximo):
    NUM_Y = 5
 
    for i in range(NUM_Y + 1):
        valor = round(maximo * i / NUM_Y)
        y     = GY + GH - int(GH * i / NUM_Y)
        surf  = fonte_menor.render(str(valor), True, CZ)
        window.blit(surf, (GX - 10 - surf.get_width(), y - surf.get_height() // 2))
 
    draw.line(window, CZ_ESC, (GX, GY - 14), (GX, GY + GH), 2)
    draw.line(window, CZ_ESC, (GX, GY + GH), (GX + GW, GY + GH), 2)
 
    surf_y = transform.rotate(fonte_menor.render('Frequência', True, CZ), 90)
    window.blit(surf_y, (GX - 68, GY + GH // 2 - surf_y.get_height() // 2))
 
 
def desenha_barras(id):
    lista  = lista_total[id]
    maximo = max(lista)
    if maximo == 0:
        return
 
    if not cores[id]:
        encher_lista_cores(id, len(lista))
 
    n      = len(lista)
    GAP    = 10
    MARG   = 40
    barra_w = (GW - 2 * MARG - (n - 1) * GAP) // n
    inicio  = GX + MARG
 
    for i in range(n):
        x   = inicio + i * (barra_w + GAP)
        h   = int(GH * lista[i] / maximo)
        y   = GY + GH - h
        cor = cores[id][i]
 
        if h > 0:
            draw.rect(window, SOMBRA, (x + 4, y + 4, barra_w, h), border_radius=7)
            draw.rect(window, cor,    (x, y, barra_w, h),          border_radius=7)
 
        
        surf_f = fonte_menor.render(str(lista[i]), True, CZ_ESC)
        fx = x + barra_w // 2 - surf_f.get_width() // 2
        fy = (y - 22) if h > 0 else (GY + GH - 22)
        window.blit(surf_f, (fx, fy))
 
        lim_inf = info_listas[id][3][i][0]
        lim_sup = info_listas[id][3][i][1]
        rotulo  = (f'{int(lim_inf)}-{int(lim_sup)}'
                   if info_listas[id][2] >= 1
                   else f'{lim_inf:.1f}-{lim_sup:.1f}')
 
        surf_r = fonte_menor.render(rotulo, True, CZ)
        rx = x + barra_w // 2 - surf_r.get_width() // 2
        window.blit(surf_r, (rx, GY + GH + 10))
 
 
def desenha(id):
    if not lista_total[id] or max(lista_total[id]) == 0:
        msg = fonte_media.render('Nenhum dado inserido ainda.', True, CZ)
        window.blit(msg, (640 - msg.get_width() // 2, GY + GH // 2 - 10))
        return
 
    desenha_eixos(max(lista_total[id]))
    desenha_barras(id)
 
 
def desenha_nav():
    for cx, pontas in [(40, [(53, 349), (30, 360), (53, 371)]),
                       (1240, [(1227, 349), (1250, 360), (1227, 371)])]:
        draw.circle(window, CZ_CLARO, (cx, 360), 26)
        draw.circle(window, CZ,       (cx, 360), 26, 1)
        draw.polygon(window, CZ_ESC, pontas)
 
    for i in range(3):
        cx  = 628 + i * 18
        cor = AZUL if i == tela else CZ_CLARO
        draw.circle(window, cor, (cx, 697), 6)
        draw.circle(window, CZ,  (cx, 697), 6, 1)
 
 
def desenha_header(t):
    titulos = ['Lista Aleatória', 'Lista Estática', 'Lista do Usuário']
    subs    = [
        f'{len(listas[0])} números  ·  {num_cats[0]} faixas',
        f'{len(listas[1])} números fixos  ·  {num_cats[1]} faixas  ·  contagens aleatórias',
        f'{len(listas[2])} números  ·  {num_cats[2]} faixas',
    ]
 
    surf_t = fonte_titulo.render(titulos[t], True, PRETO)
    window.blit(surf_t, (640 - surf_t.get_width() // 2, 20))
 
    surf_s = fonte_sub.render(subs[t], True, CZ)
    window.blit(surf_s, (640 - surf_s.get_width() // 2, 67))
 
 #corrigir ta bugando
def desenha_input():
    ir = Rect(492, 578, 296, 44)
    draw.rect(window, BRANCO, ir, border_radius=8)
    draw.rect(window, AZUL,   ir, 2, border_radius=8)
 
    window.blit(fonte_media.render(num + '|', True, PRETO), (ir.x + 12, ir.y + 10))
 
    dica = fonte_mini.render(
        'Digite um número e pressione  ENTER  para adicionar  ·  aceita decimais com "."',
        True, CZ
    )
    window.blit(dica, (640 - dica.get_width() // 2, 632))
 
    if listas[2]:
        ultimos = listas[2][-10:]
        partes  = (['...'] if len(listas[2]) > 10 else []) + [
            str(int(v)) if v == int(v) else f'{v:.1f}'
            for v in ultimos
        ]
        surf_l = fonte_menor.render('  '.join(partes), True, CZ_ESC)
        window.blit(surf_l, (640 - surf_l.get_width() // 2, 658))
 
 
def tela_geral(t):
    window.fill(FUNDO)
    desenha_retangulao()
    desenha_header(t)
    desenha(t)
    desenha_nav()
    if t == 2:
        desenha_input()
 
 

contabiliza_totais(0)
calcula_limites(1)
gera_contagens_aleatorias(1)
 
 

 
while running:
    x, y = mouse.get_pos()
 
    for ev in event.get():
 
        if ev.type == QUIT:
            running = False
            sys.exit()
 
        if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
            if 14 <= x <= 66 and 334 <= y <= 386:
                tela = 2 if tela == 0 else tela - 1
            elif 1214 <= x <= 1266 and 334 <= y <= 386:
                tela = 0 if tela == 2 else tela + 1
 
        if ev.type == KEYDOWN:
            if ev.key == K_BACKSPACE:
                num = num[:-1]
            elif ev.key == K_RETURN and num:
                listas[2].append(float(num))
                num = ''
                info_listas[2] = []
                lista_total[2] = []
                cores[2]       = []
                contabiliza_totais(2)
            elif ev.unicode.isdigit() or ev.unicode == '.':
                num += ev.unicode
 
    tela_geral(tela)
    display.update()
 
quit()