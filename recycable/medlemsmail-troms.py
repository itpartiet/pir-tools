#!/usr/bin/python3
import json
import smtplib
from email.message import Message
from email.header import Header

## Skrevet av Tobias Brox for å sende ut skreddersydd epost til hver enkelt medlem

## medlemsdatabasen ble tatt ut i HTML-format fra Middelthuns system og massasjert om til json vha perl oneliners.

## MISTAKES: dårlig håndtering av komma i navn, en del mailservere klaget på non-ascii header.  Manglende content-type, tegnsettet i body ble også galt for noen.

with open("medlemmer.json","r") as medlemsfil:
    medlemmer=json.load(medlemsfil)

fylkeslagsledere={
'Akershus': ('Daniel Bjerkeli', 'daniel.bjerkeli@piratpartiet.no'),
'Aust-Agder': ('Targeir Attestog', 'targeir@piratpartiet.no'),
'Buskerud': ('Bjørn Gotheim', 'bjorn@piratpartiet.no'),
'Finnmark': ('Knut Schelvan', 'knut.schjelvan@gmail.com'),
'Hedmark': ('Dan-Olav Lynnes', 'dan@piratpartiet.no'),
'Hordaland': ('Øyvind A. Holm', 'oyvind@piratpartiet.no'),
'Møre og Romsdal': ('Stian Færøy', 'stian.faroy@piratpartiet.no'),
'Nordland': ('Kenneth Polden', 'kenneth@piratpartiet.no'),
'Nord-Trøndelag': ('Fredrik Weisethaunet', 'fredrik@piratpartiet.no'),
'Oppland': ('Lars Helge Finholt', 'finholt@piratpartiet.no'),
'Oslo': ('Manuel Lains', 'manuel@piratpartiet.no'),
'Rogaland': ('Olve A. Austlid', 'olve@piratpartiet.no'),
'Sogn og Fjordane': ('Øyvind Nondal', 'oyvind.nondal@piratpartiet.no'),
'Telemark': ('Simen Kvamme Hatlem', 'simen@piratpartiet.no'),
'Troms': ('Jørn Lomax', 'jorn@piratpartiet.no'),
'Vest-Agder': ('Tale Haukbjørk Østrådal', 'tale@piratpartiet.no'),
'Vestfold': ('Jørgen Wold', 'jorgen@piratpartiet.no'),
}

fylkeslagsstatus={
    'Akershus': 1,
    'Aust-Agder': 1,
    'Buskerud': 1,
    'Finnmark': 1,
    'Hedmark': 1,
    'Hordaland': 1,
    'Møre og Romsdal': 1,
    'Nordland': 2,
    'Nord-Trøndelag': 1,
    'Oppland': 1,
    'Oslo': 3,
    'Rogaland': 2,
    'Sogn og Fjordane': 1,
    'Telemark': 1,
    'Troms': 1,
    'Vest-Agder': 2,
    'Vestfold': 1
}

smtp = smtplib.SMTP('mail.piratpartiet.no')
smtp.starttls()
smtp.login('valglister@piratpartiet.no', 'hunter2')
mails = []
for medlem in medlemmer:
    #if medlem['fylke'] in ('Sør-Trønderlag', 'Rogaland', 'Sør-Trøndelag'):
        #continue
    if medlem['fylke'] != 'Troms':
        continue
    #if medlem['navn'] != 'Brox, Tobias':
        #continue
    import pdb ; pdb.set_trace()
    if not medlem['epost']:
        continue

    data = {}
    data.update({'FYLKESLAGSLEDEREPOST': fylkeslagsledere.get(medlem['fylke'], ['', 'styret@piratpartiet.no'])[1],
            'FYLKESLAGSLEDERNAVN': fylkeslagsledere.get(medlem['fylke'],[''])[0],
            'NAVN': medlem['navn'],
            'EPOST': medlem['epost'],
            'FYLKE': medlem['fylke'],
            'KOMMUNE': medlem['kommune']})

    mail = Message()
    mail['From'] = Header("""Piratpartiet <valglister@piratpartiet.no>""")
    #mail['To'] = Header(""""{NAVN}" <{EPOST}>""".format(**data))
    mail['To'] = """"{NAVN}" <{EPOST}>""".format(**data)
    #Subject: Subject: Du er nominert til å representere piratpartiet i lokalvalget!
    mail['Subject'] = Header("""Vi trenger ditt navn på lista for Troms!""")
    #Reply-To: valglister@piratpartiet.no,{FYLKESLAGSLEDEREPOST}
    mail['Reply-To'] = Header("""valglister@piratpartiet.no""")

    if medlem['kommune'] == 'Tromsø':
        mail.set_payload(
"""Hei,

Vi burde ha gode muligheter for å få i stand lister for Troms og Tromsø, men foreløbig har vi bare fem (fire) kandidater - vi trenger syv!  Vi trenger altså å "låne" navnet DITT!

Så lenge man ikke er på topp på lista er det for alle praktiske formål risikofritt å stå på lista - men blir man stemt inn, så forplikter man seg til å delta i lokalpolitikken de neste fire årene.

Send oss navn, fødselsdato og addresse dersom du har mulighet til å stille!

-- 
Mvh Piratpartiets spammaster - Tobias Brox - 91700050
""", 'utf-8')
    else:
        mail.set_payload(
"""Hei,            

Vi burde ha gode muligheter for å få i stand lister for Troms, men foreløbig har vi bare fem kandidater - vi trenger minst syv!  Vi trenger altså å "låne" navnet DITT!

Så lenge man ikke er på topp på lista er det for alle praktiske formål risikofritt å stå på lista - men blir man stemt inn, så forplikter man seg til å delta i lokalpolitikken de neste fire årene.

Send oss navn, fødselsdato og addresse dersom du har mulighet til å stille!

-- 
Mvh Piratpartiets spammaster - Tobias Brox - 91700050
""", 'utf-8')

    print("sending to %s" % medlem['epost'])
    ret = smtp.sendmail('valglister@piratpartiet.no', medlem['epost'], mail.as_string())
    print(ret)
    mails.append(mail.as_string())

print(repr(mails))




