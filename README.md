# stay smart Timereporter
![Application](img/logo.png)

![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/flask?label=flask) ![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/jinja2?label=jinja2) ![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/requests?label=requests) 



## Ausgangslage

### Demo 
Eine kurze Demo vom stay smart Timereport befindet sich auf Youtube unter folgendem Link:
[Demo](https://youtu.be/qn90utTD-dI)

Für Demozwecke wurden drei Testkonten in MeisterTask eröffnet. Die Zugangsdaten haben Sie in einem separaten Mail erhalten. 

### Abstract
Im Verein stay smart arbeiten wir mit MeisterTask. Dort verteilen wir die Aufgaben und erfassen die Zeit. Leider ist der Export der Zeiterfassung mühsam. Da das CSV-Format nicht eine einfache Umwandlung im Excel ermöglicht. Zudem gibt es keine Möglichkeit pro Projekt eine Auswertung zu machen (ohne die Pro Version zu kaufen), ebenfalls ist das auch nicht über mehrere Projekte möglich. Daher ergibt sich für den Verein einen unnötigen Aufwand, den man mit einer Software umgehen könnte. 

### Projekt- Idee
Meine Idee ist es eine Webapplikation zu entwickeln, die es mir und dem Verein ermöglicht eine Auswertung über mehrere Projekte in MeisterTask zu erstellen und somit viel Aufwand zu ersparen. Dazu möchte ich die API Schnittstelle von Meistertask als Datenquelle benützen. Zuerst muss man sich mit seinem persönlichen Token authenzieren. Folglich soll man in meiner Webapp per Forumlar auswählen welche Projekte man in der Auswertung beachten möchte, es könnte sein, dass man nicht alle Projekte vom Verein sind. Als nächstes  gibt man in das Forumlar, was für eine Stundenlohn angewendet werden soll. Dann kann man die Auswertung starten und man gelangt auf eine Übersicht Seite mit allen Personen aus den Projekten. Dort sieht man pro Person das Total an Arbeitstunden und die zu bezahlende Entschädigung. Ebenfalls ist ersichtlich was der Verein gesamthaft bezahlen muss und wie viele Stunden gearbeitet wurde. Wenn man drauf klickt sieht man die Auswertung pro Person (Stunden und Entschädigung). 

### Anforderung an das Projekt
- Eingabe von Stundenlohn und Auswahl von Projekten die ausgewertet werden sollen. 
- Einlesen und speichern von Projekten, Tasks, Projektmitgliedern und Arbeitsintervallen durch die API von Meistertaks
- Auswerten der Arbeitszeit. (pro Person, pro Projekt und pro Task)
- Ausgabe der Zeit pro Projekt als CSV für die Buchhaltung (Summe pro Projekt und Gesamt)

## Workflow


### Dateneingabe und Datenquelle
Die Daten für die Zeiterfassung stammen direkt aus der Projektmanagment Software MeisterTask. Dazu wurde die API von Meistertask verwendet. Die Applikation greift direkt mittels OAuth2-Authentifizierung auf die Daten zu. Im Benutzermenü von stay smart Timereporter kann der Benutzer dann auswählen, welche Projekte ausgewertet werden sollen.


### Datenverarbeitung
MeisterTask liefert nur Rohdaten. Daher muss die Applikation die Daten verarbeiten. Das geschieht mit den Funktionen in der Libary report.py. Dort werden vier Datenquellen verwendet. Folglich wird mit den Arbeitsintervallen gearbeitet. In den Intervallen hat es jeweils die Startzeit, Endzeit, die Person und das Projekt gespeichert. Anhand dieser Informationen wird ein Zeitreport erstellt. 


### Datenausgabe 
Der Zeitreport wird dann in ein JSON-File gespeichert und man wird weitergeleitet zur Ansicht der Auswertung. Wenn man möchte kann man den Report im CSV-Format auf den PC herunterladen. Das kann zum Beispiel dazu verwendet werden, um den Zeitreport an die Buchhaltung weiterzugeben. 

### Ablauf

![Application](img/staysmart_timereporter.png)

## Benutzeranleitung

### Requirements
Damit staysmart timereport einwandfrei läuft sollte folgendes installiert sein. 
- `Python 3.7.3`


Folgende Packages müssen Installiert sein:
- `requests`
- `json`
- `os`
- `flask`
- `Jinja2`
- `csv`


### Installation der Applikation

1. Laden Sie das Repository von Github herunter.

2. Entzippen Sie den Ordner

3. Fügen Sie in den Ordner prog2-master/staysmart_timereporter/data/auth das Authentifizierungs File ein. (Dieses haben Sie in einem seperaten E-Mail erhalten.)

![Application](img/installation1.png)

4. Rufen Sie den Anaconda Prompt auf und navigieren sie zum Speicherort des Ordner
![Application](img/insta4.png)

5. Navigieren Sie zu staysmart_timereporter und führen sie **python main.py** aus. Nun ist das Tool vollständig installiert. 
![Application](img/insta5.png)

Anwendung der Applikation
====
**Erstellen eines neuen Reports**

1. Rufen Sie in Ihrem Browser **https://127.0.0.1:5000**

![Application](img/step1.png)

2. Vertrauen Sie der Webseite. Diese Meldung können Sie ignoriern. 

![Application](img/step2.png)

3. Klicken Sie auf **Login**.

![Application](img/step3.png)

4. Nun werden Sie auf eine Loginseite von Meistertask weitergeleitet. Geben Sie dort ihre Zugriffdaten ein. (@fabod diese haben Sie in einem separaten Mail erhalten.)

![Application](img/step4.png)

5. Erlauben Sie der Applikation den Zugriff.

![Application](img/step5.png)

6. Folglich sehen Sie eine Auswahl von Projekten, die Projekt die Sie selektieren werden ausgewertet.Danach können sie unterhalb noch den Studenlohn definiern und den Mitgliederbeitrag das jedes Mitglied bezahlen soll.

![Application](img/step6.png)

7. Alles eingegeben? Dann klicken Sie auf **Projekte auswerten**

![Application](img/step7.png)

8. Dann werden Sie auf die erste Auswertung weitergeleitet. Sie sehen nun die Auswertung pro Projekt.

![Application](img/step8.png) 

**Ansehen eines bereits erstellten Reports**

1. Wählen Sie aus dem Dropdown Menü, unter dem Titel Bestehende Auswertung, einen voherigen Report aus. 

![Application](img/stepa1.png)

2. Folglich klicken Sie auf **Auswertung ansehen**

![Application](img/stepa2.png)

3. Dann werden Sie auf die erste Auswertung weitergeleitet. Sie sehen nun die Auswertung pro Projekt.

![Application](img/stepa3.png)

**Auswertung pro Projekt**

In der Auswertung pro Projekt sehen sie die Projekte, die Sie für die Auswertung selektiert haben. Sie gelangen über den Menüpunkt **Projekte** zu dieser Ansicht. In der Tabelle können Sie drei Informationen pro Projekt entnehmen. In der ersten Spalte sehen sie den Projektnamen, in der zweiten Spalte sehen sie die Zeit die für dieses Projekt aufgezeichnet wurde und in der letzten Spalte können Sie die Kosten sehen die das Projekt verursacht. Der Mitgliederbeitrag wurde hier nicht abgezogen, da Mitglieder an meherern Projekten arbeiten können. 

![Application](img/projekte.png)

**Auswertung pro Person**

In der Auswertung pro Person sehen sie die Personen, die Sie für die Projekte gearbeitet haben. Sie gelangen über den Menüpunkt **Personen** zu dieser Ansicht. In der Tabelle können Sie vier Informationen direkt pro Projekt entnehmen. Zudem haben Sie die Option eine detailierte Ansicht einzusehen. In der ersten und zweiten Spalte sehen sie den Vornamen und Nachnamen der Person. In der nächsten Spalte sehen Sie die Zeit, die die Person inverstierte.In der vierten Spalte können Sie den Lohn sehen die diese Person erhalten sollte. Der Mitgliederbeitrag wurde hier abgezogen. In der letzten Spalte finden Sie den **Detail** Button durch diesen gelangen sie in die Detail ansicht des Mitgliedes

![Application](img/personen.png)

In der Detailansicht sehen eine detailierte Abrechnung. Zu einem kann man sehen wie viel Stunden die Person in dem jeweiligen Projekt gearbeitet hat und wie viel Kosten die Person pro Projekt generiert hat. Zudem sehen Sie den Mitgliederbeitrag-Abzug, wie auch die Summe. Falls diese unter 0 CHF ist wird es einfach als 0 CHF angezeigt. Einen Minusbetrag ist nicht möglich. 

![Application](img/person.png)

**Auswertung pro Task**

In der Auswertung pro Task sehen sie die Aufgaben der Projekte, die Sie für die Auswertung selektiert haben. Sie gelangen über den Menüpunkt **Tasks** zu dieser Ansicht. In der Tabelle können Sie drei Informationen pro Task entnehmen. In der ersten Spalte sehen sie den Tasksnamen, in der zweiten Spalte sehen sie die Zeit die für diesen Task aufgezeichnet wurde und in der letzten Spalte können Sie die Kosten sehen die dieser Task verursacht. 

![Application](img/tasks.png)

**Export der Auswertung im CSV-Format**

Da nicht alle Vereinsmitglieder dieses Tool installieren können/wollen. Kann das Tool für die Lohnabrechnung einen Export machen im CSV Format machen. In diesem Format kann der/die Buchhalter/in sehen wer für welches Projekt wie lange gearbeitet hat und wie hoch die gesamte Entschädigung ist. 

![Application](img/export.png)
