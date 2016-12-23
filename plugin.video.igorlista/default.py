#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,base64
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
from BeautifulSoup import BeautifulSoup
h = HTMLParser.HTMLParser()

versao = '3.0.0'
addon_id = 'plugin.video.igorlista'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.png'
url_base = base64.b64decode('aHR0cHM6Ly9kb2NzLmdvb2dsZS5jb20vdWM/ZXhwb3J0PWRvd25sb2FkJmlkPQ==')
url_base2 = base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vY2FuYWlzLmh0bWw=')
url_base3 = base64.b64decode('aHR0cDovL3d3dy50di1tc24uY29tL3BsYXllci9wbGF5ZXIuc3dm')
url_base4 = base64.b64decode('aHR0cHM6Ly9kb2NzLmdvb2dsZS5jb20vdWM/ZXhwb3J0PWRvd25sb2FkJmlkPTBCeE4wRHpGakllQ2FhRWhRUmxKUk4yZElVWGM=')
url_base5 = base64.b64decode('aHR0cDovL3BwY2FzdC5vcmcvZW1iZWRQL2p3cGxheWVyL2p3cGxheWVyLmZsYXNoLnN3Zg==')
url_base6 = base64.b64decode('aHR0cDovL3BwY2FzdC5vcmcvZW1iZWRQLw==')
url_base7 = base64.b64decode('aHR0cDovL3R2LW1zbi5jb20vbWVzdHJlLnBocA==')
###############################################################################################################
#                                                   MENUS                                                     #
###############################################################################################################


def  categorias():
	abrir_url('http://j.mp/asessosaddonigor')
	addDir('TV ONLINE BR','-',13,'http://goo.gl/PumvSm')
	addDir('CANAIS INTERNACIONAIS',url_base+'0BxN0DzFjIeCabW4zLTNveUdwOXM',5,'http://goo.gl/vNVkoZ')
	addDir('FILMES ONLINE','-',9,'http://goo.gl/ZiWMZU')
        addDir('SERIES ONLINE','-',6,'http://goo.gl/KyoeaS')		
        addDir('FUTEBOL AO VIVO','-',14,'http://goo.gl/S4C9LD')
        addDir('SERIES 24HRS',url_base+'0BxN0DzFjIeCaY2Nlc1NqNFJDajQ',1,'http://goo.gl/VIlrvY')	
        addDir('DESENHOS 24HRS',url_base+'0BxN0DzFjIeCaVldOcVpJaFp1SW8',1,'http://goo.gl/rBsS8A')
	addDir('RADIOS',url_base+'0BxN0DzFjIeCaWkxvUS1ZeHh3OWc',1,'http://goo.gl/pMM1Bg')
       

def  futebol_ao_vivo():

	addDir('JOGOS DE HOJE','-',10,'http://goo.gl/Yn4NOh')
	addDir('PFC DIA DE JOGOS','-',11,'http://goo.gl/9ttIS6')	
        addDir('ESPORTES INTERNACIONAIS',url_base+'0BxN0DzFjIeCaaHA1ZEF6ZTdLdG8',5,'http://goo.gl/eJLrmG')	
	
def listar_canais(url):
      for line in urllib2.urlopen(url).readlines():
            params = line.split(',')
            try:
                  nome = params[0]
                  print 'Nome: ' + nome
                  rtmp = params[1].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http').replace(' http','http')
                  print 'Link: ' + rtmp
                  img = params[2].replace(' http','http')
                  print 'Img: ' + img
                  addLink(nome,rtmp,img)
            except:
                  pass
      xbmc.executebuiltin("Container.SetViewMode(500)")		
	
def listar_categorias():
	html = gethtml(url_base4)
	soup = html.find("div",{"class":"canais"})
	canais = soup.findAll("li")
	for canal in canais:
		titulo = canal.a.text
		url = canal.a["href"]
		iconimage = canal.img["src"]
		addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,2,iconimage)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
	xbmc.executebuiltin('Container.SetViewMode(500)')	

def canais_master(name,url,iconimage):
	html = gethtml(url)
	soup = html.find("div",{"class":"canais"})
	canais = soup.findAll("li")
	for canal in canais:
		titulo = canal.a.text
		url = canal.a["href"]
		iconimage = canal.img["src"]
		addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,3,iconimage,False)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
	xbmc.executebuiltin('Container.SetViewMode(500)')
		
def player_master(name,url,iconimage):
	pg = 0
        caixastatus = xbmcgui.DialogProgress()
	caixastatus.create('IGOR LISTA', 'Abrindo link...','Aguarde...')
	caixastatus.update(pg)
        playlist = xbmc.PlayList(0)
	playlist.clear()
	params = url.split(',')
	pg +=30 
	caixastatus.update(pg)
	try:
		ip = params[0]
		playpath = params[1]
                pg +=30 
		caixastatus.update(pg)
		link = 'rtmp://'+ip+'/live?wmsAuthSign='+get_wms() +' playpath='+playpath+' swfUrl='+url_base3+' live=1 pageUrl='+url_base7+' token='+gettoken() +' '
		pg +=30 
		caixastatus.update(pg)
                listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(link,listitem)	
		pg=100
		caixastatus.update(pg)
		caixastatus.close()
                xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except:	
		caixastatus.close()
		player_normal(name,url,iconimage)

def player_normal(name,url,iconimage):
        pg = 0
        caixastatus = xbmcgui.DialogProgress()
	caixastatus.create('IGOR LISTA', 'Abrindo link...','Aguarde...')
	caixastatus.update(pg)
        playlist = xbmc.PlayList(1)
        playlist.clear()
	params = url.split(',')
	pg +=30 
	caixastatus.update(pg)
        try:
		rtmp = params[0]
                pg +=30 
		caixastatus.update(pg)		
                link = ''+rtmp+''
		pg +=30 
		caixastatus.update(pg)		
                listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(link,listitem)	
		pg=100
		caixastatus.update(pg)
		caixastatus.close()
                xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)	
	except:
		caixastatus.close()
		xbmcgui.Dialog().ok('IGOR LISTA', 'Erro !!!.')	
				
def listar_canais_outros(url):
      for line in urllib2.urlopen(url).readlines():
            params = line.split(',')
            try:
                  nome = params[0]
                  print 'Nome: ' + nome
                  rtmp = params[1].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http')
                  print 'Link: ' + rtmp
                  img = params[2].replace(' http','http')
                  print 'Img: ' + img
                  addLink(nome,rtmp,img)
            except:
                  pass
      xbmc.executebuiltin("Container.SetViewMode(53)")		
		

def player_lista_series(url):
      for line in urllib2.urlopen(url_base+'0BxN0DzFjIeCaLXR2NmltS2hDbW8').readlines():
            params = line.split(',')
            print params
            try:
                  nome = params[0]
                  print 'Nome: ' + nome
                  rtmp = params[1]
                  print 'Link: ' + rtmp
                  img = params[2].replace(' http','http').replace(' https','https')
                  print 'Img: ' + img
                  addDir(nome,rtmp,7,img)
            except:
                pass
		xbmc.executebuiltin("Container.SetViewMode(500)")

def lista_temporada(url):
      for line in urllib2.urlopen(url).readlines():
            params = line.split(',')
            print params
            try:
                  nome = params[0]
                  print 'Nome: ' + nome
                  rtmp = params[1]
                  print 'Link: ' + rtmp
                  img = params[2].replace(' http','http').replace(' https','https')
                  print 'Img: ' + img
                  addDir(nome,rtmp,8,img)
            except:
                pass
		xbmc.executebuiltin("Container.SetViewMode(500)")

def player_lista_series_episodios(url):	
      for line in urllib2.urlopen(url).readlines():
            params = line.split(',')
            try:
                  nome = params[0]
                  print 'Nome: ' + nome
                  rtmp = params[1].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http').replace(' http','http').replace(' plugin','plugin')
                  print 'Link: ' + rtmp 
                  img = params[2].replace(' http','http')
                  print 'Img: ' + img
                  addLink(nome,rtmp,img)
            except:
                  pass
      xbmc.executebuiltin("Container.SetViewMode(50)")		


def player_lista_filmes(url):
      for line in urllib2.urlopen(url_base+'0BxN0DzFjIeCaVGFGVlNmNW1ZeWs').readlines():
            params = line.split(',')
            print params
            try:
                  nome = params[0]
                  print 'Nome: ' + nome
                  rtmp = params[1]
                  print 'Link: ' + rtmp
                  img = params[2].replace(' http','http').replace(' https','https')
                  print 'Img: ' + img
                  addDir(nome,rtmp,1,img)
            except:
                pass
		xbmc.executebuiltin("Container.SetViewMode(500)")

def futebol_ao_vivo_jogos(name,url,iconimage):
	abrir_url('http://bit.ly/assesosjogosaovivo')
	html = gethtml(base64.b64decode('aHR0cHM6Ly9kb2NzLmdvb2dsZS5jb20vdWM/ZXhwb3J0PWRvd25sb2FkJmlkPTBCeE4wRHpGakllQ2FUVWRmV0ZGR2NUWkhSbGs='))
	soup = html.find("div",{"class":"canais"})
	canais = soup.findAll("li")
	for canal in canais:
		titulo = canal.a.text
		url = canal.a["href"]
		iconimage = canal.img["src"]
		addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,12,iconimage,False)
		
	
def canais_futebol_ao_vivo_m(name,url,iconimage):
	html = gethtml(base64.b64decode('aHR0cHM6Ly9kb2NzLmdvb2dsZS5jb20vdWM/ZXhwb3J0PWRvd25sb2FkJmlkPTBCeE4wRHpGakllQ2FObEZ2ZEhvM1dFOTVVMnM='))
	soup = html.find("div",{"class":"canais"})
	canais = soup.findAll("li")
	for canal in canais:
		titulo = canal.a.text
		url = canal.a["href"]
		iconimage = canal.img["src"]
		addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,12,iconimage,False)

def player_futebol_ao_vivo_m(name,url,iconimage):
	pg = 0
        caixastatus = xbmcgui.DialogProgress()
	caixastatus.create('IGOR LISTA', 'Abrindo link...','Aguarde...')
	caixastatus.update(pg)
        playlist = xbmc.PlayList(0)
	playlist.clear()
	params = url.split(',')
	pg +=30 
	caixastatus.update(pg)
	try:
	        ip = params[0]
		playpath = params[1]
                pg +=30 
		caixastatus.update(pg)
		link = 'rtmp://'+ip+'/live?wmsAuthSign='+get_wms() +' playpath='+playpath+' swfUrl='+url_base3+' live=1 pageUrl='+url_base7+' token='+gettoken() +' '
		pg +=30 
		caixastatus.update(pg)
                listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/mp4')
		playlist.add(link,listitem)	
		pg=100
		caixastatus.update(pg)
		caixastatus.close()
                xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except:	
		caixastatus.close()
		player_normal(name,url,iconimage)
		
def player_youtube(url):
	xbmcPlayer = xbmc.Player()
	xbmcPlayer.play('plugin://plugin.video.youtube/play/?video_id=' +url)			

###############################################################################################################
#                                                 FUNÇÕES                                                     #
###############################################################################################################

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	
def gethtml(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    soup = BeautifulSoup(link)
    return soup	

def real_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.geturl()
	response.close()
	return link

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

#def addDir(name,url,mode,iconimage,pasta=True,total=1):
	#u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	#ok=True
	#liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	#liz.setProperty('fanart_image', fanart)
	#ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	#return ok
	
def addDir(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok	
	
def get_wms():
	req = urllib2.Request(url_base7)
	req.add_header('referer', url_base2)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	wms = re.compile(r"AuthSign=(.+?)&auto").findall(link)[0]
	return wms	
	
def gettoken():
	req = urllib2.Request(base64.b64decode('aHR0cHM6Ly9kb2NzLmdv­b2dsZS5jb20vdWM/­ZXhwb3J0PWRvd25sb2FkJ­mlkPTBCeE4wRHpGakllQ­2FPWGR1ZVc0MVJFMVBXb­XM='))
	response = urllib2.urlopen(req)
	token=response.read()
	response.close()
	return token	
	
def jogos_hoje():
	req = urllib2.Request(base64.b64decode('aHR0cHM6Ly9kb2NzLmdvb2dsZS5jb20vdWM/ZXhwb3J0PWRvd25sb2FkJmlkPTBCeE4wRHpGakllQ2FUVWRmV0ZGR2NUWkhSbGs='))
	response = urllib2.urlopen(req)
	token=response.read()
	response.close()
	return token	

def configurar():
	xbmcaddon.Addon(addon_id).openSettings()
	return categorias()
		
def mensagem():
	html = abrir_url(base64.b64decode('aHR0cHM6Ly9kb2NzLmdvb2dsZS5jb20vdWM/ZXhwb3J0PWRvd25sb2FkJmlkPTBCeE4wRHpGakllQ2FaekpOU0VSd05GaG1TVFE='))
	local = open(msg,'r').read()
	if html != local:
		limp = open(msg, 'w')
		limp.write(html) 
		limp.close()
		xbmcgui.Dialog().ok(addon_name,html)
	else:
		pass	
############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
 
params=get_params()
url=None
name=None
mode=None
iconimage=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################



if mode==None or url==None or len(url)<1:
        print ""
        categorias()
	
elif mode==1:
	print ""
	listar_canais(url)	

elif mode==2:
        print ""
        canais_master(name,url,iconimage)
	
elif mode==3:
        print ""
        player_master(name,url,iconimage)
	
elif mode==4:
        print ""
        player_normal(name,url,iconimage)

elif mode==5:
        print ""
        listar_canais_outros(url)

elif mode==6:
	player_lista_series(url)
    
elif mode==7:
        print ""
        lista_temporada(url)
    
elif mode==8:
	print ""
	player_lista_series_episodios(url)	

elif mode==9:
        print ""
        player_lista_filmes(url)
	
elif mode==10:
        print ""
        futebol_ao_vivo_jogos(name,url,iconimage)
    
elif mode==11:
        print ""
        canais_futebol_ao_vivo_m(name,url,iconimage)
    
elif mode==12:
        print ""
        player_futebol_ao_vivo_m(name,url,iconimage)
 
elif mode==13:
        print ""
        listar_categorias()	

elif mode==14:
        print ""
        futebol_ao_vivo()

elif mode==15:
	player_youtube(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))