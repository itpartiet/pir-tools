#!/usr/bin/python3
import json
import smtplib

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
    if medlem['fylke'] in ('Sør-Trønderlag', 'Rogaland', 'Sør-Trøndelag'):
        continue
    if not medlem['epost']:
        continue
    else:
        data = {}
        data.update({'FYLKESLAGSLEDEREPOST': fylkeslagsledere.get(medlem['fylke'], ['', 'styret@piratpartiet.no'])[1],
                'FYLKESLAGSLEDERNAVN': fylkeslagsledere.get(medlem['fylke'],[''])[0],
                'NAVN': medlem['navn'],
                'EPOST': medlem['epost'],
                'FYLKE': medlem['fylke'],
                'KOMMUNE': medlem['kommune']})
        if medlem['fylke'] in fylkeslagsledere:
            data['FYLKESLAGSLEDER'] = "fylkeslagsleder {FYLKESLAGSLEDERNAVN} <{FYLKESLAGSLEDEREPOST}>".format(**data)
        else:
            data['FYLKESLAGSLEDER'] = "sentralstyret, styret@piratpartiet.no"
                
        mail = [
"""From: Piratpartiet <valglister@piratpartiet.no>
To: {NAVN} <{EPOST}>
Subject: Subject: Du er nominert til å representere piratpartiet i lokalvalget!
Reply-To: valglister@piratpartiet.no,{FYLKESLAGSLEDEREPOST}

""".format(**data)]
        fs = fylkeslagsstatus.get(medlem['fylke'], 0)
        if fs<2:
            mail.append("""Vi trenger ditt navn på valglista for {FYLKE}!""".format(**data))
        else:
            mail.append("""Du er invitert til å stå på valglista for {FYLKE}.""".format(**data))
        if fs == 0:
            mail.append(""" Dessuten, fylkeslaget mangler for tiden fungerende styre.  Dersom du kunne tenke deg å være med på å gjenopplive  {FYLKE} fylkeslag, så send en epost til sentralstyret, styret@piratpartiet.no.""".format(**data))
        mail.append("\n\n")
        if medlem['kommune'] == 'Bergen':
            mail.append("Du er også velkommen til å stå på valglista for {KOMMUNE} kommune.".format(**data))
        elif medlem['kommune'] == 'Oslo':
            mail.append('For å stille liste til bydelsvalg må man ha minst 7 kandidater på lista.  For å få stilt liste i din bydel kan det være nødvendig å rekruttere flere medlemmer - har du noen venner som enda ikke er med i piratpartiet, som kunne tenke seg å stå på liste?')
        elif medlem['kommune'] in ('Tromsø', 'Stavanger', 'Kristiansand'):
            mail.append('Vi har store muligheter til å få i stand en liste for {KOMMUNE} - men vi trenger ditt navn der også!'.format(**data))
        else:
            mail.append('Generelt er kravet at man må ha minst 7 kandidater for å stille med liste, men tallet kan variere for enkelte kommuner. For å få stilt liste i {KOMMUNE} kan det være nødvendig å rekruttere flere medlemmer - har du noen venner som enda ikke er med i piratpartiet, men som kunne tenke seg å stå på liste?'.format(**data))
        mail.append('\n\nDet er et krav at man har folkeregistrert addresse i fylket/kommunen man ønsker å representere ved innleveringsfrist for listene, 31. mars klokken 12.  Det er IKKE et krav at man er medlem i partiet!\n\nDersom du aksepterer nominasjonen, send en epost med fullt navn, addresse, fødselsdato og evt annen relevant informasjon (f.eks., om man ønsker å stå langt oppe eller langt nede på lista) på epost valglister@piratpartiet.no pluss {FYLKESLAGSLEDER}. Vi har ingen tid å miste, svar på denne mailen med det samme!\n'.format(**data))

        print("sending to %s" % medlem['epost'])
        smtp.sendmail('valglister@piratpartiet.no', medlem['epost'], "".join(mail).encode('utf-8'))
        mails.append(mail)

print(repr(mails))




