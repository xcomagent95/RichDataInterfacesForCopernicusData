# Rich Data Interfaces for Copernicus Data

## Proposal

### 1 Motivation
Im Rahmen des von der European Space Agency (ESA) gestarteten Erdbeobachtungsprogramms
Copernicus werden unterschiedlichste Fernerkundungsdaten unter anderem
von den Satelliten der Sentinel-Reihe aufgenommen. Diese zeichnen sich durch
hohe räumliche und zeitliche Auflösung aus und eigenen sich daher für eine Vielzahl
von Anwendungen in der Geoinformatik [1]. Besonders das Krisen- und Risikomanagement
kann von diesen Daten profitieren. Bevor die Rohdaten korrekt interpretiert und
genutzt werden können, bedarf es häufig einer teilweise aufwendigen Vorverarbeitung
und entsprechender Infrastrukturen. Um den Anwendern den Zugriff auf einsatzbereite
Daten so einfach wie möglich zu machen und so eine vereinfachte Sicht auf die Daten
zu erlauben, kann der OGC API - Processes - Part 1: Core Standard genutzt werden,
um eine Datenschnittstelle zu entwerfen, welche reich an Interaktionsmöglichkeiten
ist. Dieser Standard bedient sich des RESTful Paradigmas und ist von Konzepten des
OGC Web Processing Service 2.0 beeinflusst. Eine vollständige Implementierung des
Letzteren ist jedoch nicht mehr erforderlich [2]. Eine API bietet sowohl für Entwickler
als auch Anwender einige Vorteile. Als Entwickler kann auf viele Aspekte der Prozessierung
sowie auf die Eigenschaften der Resultate Einfluss genommen werden. Für
Anwender bietet eine API, in Abgrenzung zu simpleren Diensten, häufig die Möglichkeit
Anfragen zu parametrisieren und so exakt auf ihre Fragestellung anzupassen.

### 2 Zielsetzung
Ziel der Arbeit ist das Implementieren eines leichtgewichtigen, OGC API - Processes - 
Part: 1 Core Standard konformen Application Programming Interface (API). Um
einen praktischen Bezug zu schaffen, soll die API einen Prozess anbieten, welcher
Überschwemmungsmonitoring auf Basis von Copernicus-Daten ermöglicht. Die API
wird sämtliche Vorverarbeitungsschritte durchführen und als Resultat einsatzbereite
Geodaten liefern, die sich für das Überschwemmungsmonitoring eignen. Neben der
eigentlichen Implementierung der API soll untersucht werden, welche Möglichkeiten
der Kopplung von Copernicus Daten mit der zu implementierenden API bestehen.
Ein besonderes Augenmerk liegt dabei auf Aspekten wie Einfachheit, Wartbarkeit und
Erweiterbarkeit der API und der Eignung des OGC API - Processes - Part 1: Core
Standards für die Entwicklung von Datenschnittstellen zu Copernicus-Daten mit zahlreichen
Interaktionsmöglichkeiten.

### 3 Methoden
Damit eine möglichst leichtgewichtige, simple, aber erweiterbare API entworfen werden
kann, wird die Programmiersprache Python und das Web Framework Flask zum
Einsatz kommen. Für die eigentliche Prozessierung sollen möglichst nur bewährte Programme
und Python Packages verwendet werden, um eine möglichst hoheWartbarkeit
zu gewährleisten. Die Versionierung erfolgt mit Git. Das Überschwemmungsmonitoring
soll auf Basis von Radardaten der Sentinel-1 Mission erfolgen, da diese wetterund
tageszeitunabhängig Messungen durchführen können [1]. Die notwendigen Kalibrierungen
und Filterungen sollen ebenfalls Teil der bereitgestellten Prozessierung
sein. Anschließend soll der Normalized Difference Sigma-Naught Index (NDSI) berechnet
werden [3]. Aus diesem können mithilfe eines automatischen Grenzwertverfahrens
Überflutungsmasken abgeleitet werden.

### Literatur
[1] M. Bourbigot, H. Johnson, R. Piantanida. (2016, März
25). Sentinel-1 Product Definition [Online]. Verfügbar unter:
https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar/document-library/-
/asset_publisher/1dO7RF5fJMbd/content/sentinel-1-product-definition (Zugriff
am: 2. März 2022).

[2] B. Pross und P. A. Vretanos. (2021, Dezember 20). OGC API – Processes – Part
1: Core [Online]. Verfügbar unter: https://docs.opengeospatial.org/is/18-062r2/18-
062r2.html (Zugriff am: 1. März 2022).

[3] N. I. Ulloa, S.-H. Chiang und S.-H. Yun (2020, April 27). Flood Proxy Mapping
with Normal-ized Difference Sigma-Naught Index and Shannon’s Entropy [Online].
Verfügbar unter: https://doi.org/10.3390/rs12091384 (Zugriff am: 1. März
2022).

## Installation
Um die Anwendung starten zu können wird ein Python-Environment mit der Python Version 3.6 benötigt. 
Die benötigten Packages können der environment.yaml entnommen werden. 
Zusätzlich muss die von der ESA kostenlos zur Verfügung gestellten Software SNAP installiert und der 
Python-Wrapper snappy konfiguriert sein. Für eine Vereinfachte Installation werden Plattformen wie 
Anaconda empfohlen.

## Betrieb
Die Anwendung kann mit der run.py getstartet werden. Zum Testen der Anwendeung kann ein beliebiger Browser oder das
Kommandozeilen-Werkzeug cURL verwendet werden. 

### Landing-Page
Ersten Anlaufpunkt für Nutzer sollte die Landig-Page der API sein. Über diese können alle anderen Endpints erreicht werden. 
Die Landing-Page kann unter folgendem URL erreicht werden:
```
#Retrieve Landing-Page as HTML
curl -X GET "localhost:5000/?f=text/html"

#Retrieve Landing-Page as JSON
curl -X GET "localhost:5000/?f=application/json"
```

### API-Definition
Der API-Definition kann entnommen wie die Endpoints der API zu verwenden sind, welchen Schemata die 
Ressourcen entsprechen und welche Responses zu erwarten sind. 
Die API-Definition kann unter folgendem URL erreicht werden:
```
#Retrieve API-Definition as HTML
curl -X GET "localhost:5000/api?f=text/html"

#Retrieve API-Definition as JSON
curl -X GET "localhost:5000/api?f=application/json"
```

Alternativ kann die API-Definition unter folgendem Link 
eingesehen werden: https://app.swaggerhub.com/apis/RDIForCopernicusData/RichDataInterfaceForCopernicusData/1.0.0

### Conformance-Declaration
Nutzer können die Standardkonformietät der API über den Conformance Endpoint einsehen. 
Dort werden alle Requirements-Classes gelistet weclhe von der Anwendung implementiert werden.
Die Conformance Declaration kann unter folgendem URL erreicht werden:
```
#Retrieve Conformance Declaration as HTML
curl -X GET "localhost:5000/conformance?f=text/html" 

#Retrieve Conformance Declaration as JSON
curl -X GET "localhost:5000/conformance?f=application/json" 
```

### Process List
Nutzer können über den Process List Endpoint detaillierte Informationen zu den 
von Anwendung bereitgesteöllten Prozessen erhalten. 
Die Process List kann unter folgendem URL erreicht werden:
```
#Retrieve Process List as HTML
curl -X GET "localhost:5000/processes?f=text/html" 

#Retrieve Process List as JSON
curl -X GET "localhost:5000/processes?f=application/json" 
```
### Process Description
Eine detaillierte Beschreibung der Prozesse kann über den Process Description
Endpoint angefragt werden. 
Die Process Beschreibungen können unter folgendem URL erreicht werden:
```
#Retrieve Echo Process Description as HTML 
curl -X GET "localhost:5000/processes/Echo?f=text/html" 

#Retrieve Echo Process Description as JSON
curl -X GET "localhost:5000/processes/Echo?f=application/json" 

#Retrieve Echo Process Description as HTML 
curl -X GET "localhost:5000/processes/FloodMonitoring?f=text/html" 

#Retrieve Echo Process Description as JSON
curl -X GET "localhost:5000/processes/FloodMonitoring?f=application/json" 
```
### Process Excecution
Nutzer können über den Process Execution Endpoint Prozesse Instanziieren
und so Jobs generieren.
Das erzeugen eines Jobs kann über folgenden URL erfolgen:

#### Echo
```
#Echo with raw Output
curl -X POST -H "Content-Type:application/json" -d "{'inputs':{'echo':'test'}, 'outputs':{'outgoingEcho': {'format': {'mediaType': 'application/json'}, 'transmissionMode': 'value'}}, 'response': 'raw'}" "localhost:5000/processes/Echo/execution"
#Echo with document Output
curl -X POST -H "Content-Type:application/json" -d "{'inputs':{'echo':'test'}, 'outputs':{'outgoingEcho': {'format': {'mediaType': 'application/json'}, 'transmissionMode': 'value'}}, 'response': 'document'}" "localhost:5000/processes/Echo/execution"
```
#### Flood Monitoring
```
Flood Monitoring wih ndsi as raw Output
curl -X POST -H "Content-Type:application/json" -d "{'inputs':{'preDate':'20220305', 'postDate':'20220329', 'username':'xcomagent95', 'password':'alex@copernicus95', 'bbox': {'bbox': [45.39797509700767, 12.508695088734772, 45.51987960173298, 12.155327635797713]}}, 'outputs':{'ndsi': {'format': {'mediaType': 'application/tiff'}, 'transmissionMode': 'value'}}, 'response': 'raw'}" "localhost:5000/processes/FloodMonitoring/execution"

Flood Monitoring wih bin as raw Output
curl -X POST -H "Content-Type:application/json" -d "{'inputs':{'preDate':'20220305', 'postDate':'20220329', 'username':'xcomagent95', 'password':'alex@copernicus95', 'bbox': {'bbox': [45.39797509700767, 12.508695088734772, 45.51987960173298, 12.155327635797713]}}, 'outputs':{'bin': {'format': {'mediaType': 'application/tiff'}, 'transmissionMode': 'value'}}, 'response': 'raw'}" "localhost:5000/processes/FloodMonitoring/execution"

Flood Monitoring wih ndsi and bin as raw Output
curl -X POST -H "Content-Type:application/json" -d "{'inputs':{'preDate':'20220305', 'postDate':'20220329', 'username':'xcomagent95', 'password':'alex@copernicus95', 'bbox': {'bbox': [45.39797509700767, 12.508695088734772, 45.51987960173298, 12.155327635797713]}}, 'outputs':{'ndsi': {'format': {'mediaType': 'application/tiff'}, 'transmissionMode': 'value'}, 'bin': {'format': {'mediaType': 'application/tiff'}, 'transmissionMode': 'value'}}, 'response': 'raw'}" "localhost:5000/processes/FloodMonitoring/execution"

Flood Monitoring wih ndsi as document Output
curl -X POST -H "Content-Type:application/json" -d "{'inputs':{'preDate':'20220305', 'postDate':'20220329', 'username':'xcomagent95', 'password':'alex@copernicus95', 'bbox': {'bbox': [45.39797509700767, 12.508695088734772, 45.51987960173298, 12.155327635797713]}}, 'outputs':{'ndsi': {'format': {'mediaType': 'application/tiff'}, 'transmissionMode': 'value'}}, 'response': 'document'}" "localhost:5000/processes/FloodMonitoring/execution"

Flood Monitoring wih bin as document Output
curl -X POST -H "Content-Type:application/json" -d "{'inputs':{'preDate':'20220305', 'postDate':'20220329', 'username':'xcomagent95', 'password':'alex@copernicus95', 'bbox': {'bbox': [45.39797509700767, 12.508695088734772, 45.51987960173298, 12.155327635797713]}}, 'outputs':{'bin': {'format': {'mediaType': 'application/tiff'}, 'transmissionMode': 'value'}}, 'response': 'document'}" "localhost:5000/processes/FloodMonitoring/execution"

Flood Monitoring wih ndsi and bin as document Output
curl -X POST -H "Content-Type:application/json" -d "{'inputs':{'preDate':'20220305', 'postDate':'20220329', 'username':'xcomagent95', 'password':'alex@copernicus95', 'bbox': {'bbox': [45.39797509700767, 12.508695088734772, 45.51987960173298, 12.155327635797713]}}, 'outputs':{'ndsi': {'format': {'mediaType': 'application/tiff'}, 'transmissionMode': 'value'}, 'bin': {'format': {'mediaType': 'application/tiff'}, 'transmissionMode': 'value'}}, 'response': 'document'}" "localhost:5000/processes/FloodMonitoring/execution"
```

### Job List
In der Job Liste werden alle von Nutzern algelegte Jobs aufgeführt. 
Die Liste kann nach unterschiedlichen Kriterien eingeschränkt werden.
Die Job List ist unter folgendem URL abrrufbar:
```
#Retrieve Job List as HTML
curl -X GET "localhost:5000/jobs?f=text/html" 

#Retrieve Job List as JSON
curl -X GET "localhost:5000/jobs?f=application/json" 

#Additional Parameters
type:
- process
process: 
- Echo
- FloodMonitoring
status: 
- accepted
- running
- successful
- failed
- dismissed
datetime:
- date-time: yyyy"-"mm"-"dd"T"hh":"mm":"ss2
- date-time: date-time / interval
- interval: interval-closed / interval-open-start / interval-open-end
- interval-closed: date-time "/" date-time
- interval-open-start: [".."] "/" date-time
- interval-open-end: date-time "/" [".."]
minDuration: integer
maxDuration: integer
```
### Job Status
Detailierte Informationen zum Bearbeitungsstand eines Jobs können Nutzer über 
den Job Status Endpoint erhalten. 
Der Status eines Jobs ist unter folgendem URL abrrufbar:
```
#Retrieve Job Status as HTML
curl -X GET "localhost:5000/jobs/<jobID>?f=text/html" 

#Retrieve Job Status as JSON
curl -X GET "localhost:5000/jobs/<jobID>?f=application/json" 
```
### Job Results
Wurde ein Job erfolgreich abgeschlossen können die Ergebnisse der 
Prozesierung unter folgendem URL abgerufen werden:
```
#Retrieve Job Results
curl -X GET "localhost:5000/jobs/<jobID>/results
```
### Coverage
Um einzusehen welche Sentinel-1 Datensätze persistent von der Anwendung gespeichert wurden und 
daher nicht heruntergeladen werden müssen, kann der Coverage Endpoint angefragt werden.
Die Coverage kann unter folgendem URL erreicht werden:
```
#Retrieve Coverage as HTML
curl -X GET "localhost:5000/coverage?f=text/html"

#Retrieve Coverage as JSON
curl -X GET "localhost:5000/coverage?f=application/json"
```
## Example 1 
:
Währedn der Invasion der Ukraine durch die rissische Föderation haben sich manche ukrainischen Gemeinden dazu entschieden ihre Äcker und 
Wiesen zu überfluten um das vorrücken russischer Truppen mit schwerem militärischem Gerät zu erschweren.
Eine dieser Gemeinden ist der Ort Demydow. Das Ausmaß der Überflutung lässt sich mit dieser Anwendung untersuchen: 
```
curl -X POST -H "Content-Type:application/json" -d "{'inputs':{'preDate':'20220102', 'postDate':'20220604', 'username':'xcomagent95', 'password':'alex@copernicus95', 'bbox': {'bbox': [50.68209876799218, 30.373870053936805, 50.75296226636879, 30.29868237792831]}}, 'outputs':{'ndsi': {'format': {'mediaType': 'application/tiff'}, 'transmissionMode': 'value'}, 'bin': {'format': {'mediaType': 'application/tiff'}, 'transmissionMode': 'value'}}, 'response': 'document'}" "localhost:5000/processes/FloodMonitoring/execution"	
```


## Example 2
Der Monsun sort in weiten Teile Asiens für das anschwellen der Flüsse und für Überschwemmungen. So auch im in Bagladesch gelegenen Ort Zakiganj.
Wie weit der Fluss Kushiyara 2022 über die Ufer getreten ist kann mit dieser Anwendung untersucht werden:
```
curl -X POST -H "Content-Type:application/json" -d "{'inputs':{'preDate':'20220429', 'postDate':'20220523', 'username':'xcomagent95', 'password':'alex@copernicus95', 'bbox': {'bbox': [24.88758327590919, 92.32762841659967, 24.930683245328627, 92.25032491801463]}}, 'outputs':{'ndsi': {'format': {'mediaType': 'application/tiff'}, 'transmissionMode': 'value'}, 'bin': {'format': {'mediaType': 'application/tiff'}, 'transmissionMode': 'value'}}, 'response': 'document'}" "localhost:5000/processes/FloodMonitoring/execution"	

```