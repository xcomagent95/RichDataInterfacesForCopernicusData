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
