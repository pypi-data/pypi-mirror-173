# -*- coding: utf-8 -*-
# !/usr/bin/env python
import datetime

import regex as re
import collections
from kolibri.preprocess.text.cleaning.cleaning_scripts import clean
from kolibri.preprocess.text.cleaning.__email_configs import *
from kolibri.preprocess.text.language_detection import detect_language
import dateparser
from kolibri.preprocess.text.cleaning.header_parser import HeaderParser

import glob
from os.path import join
from tqdm import tqdm
import os
import pytz
from kolibri.preprocess.text.cleaning.email_parser import parse_eml
class EmailMessage(object):
    """
    An email message represents a parsed email body.
    """

    def __init__(self, language='en', split_pattern=None, remove_html=True, escape_rejected_emails=True, detect_outof_office=True):
        self.date = None
        self.fragments = []
        self.fragment = None
        self.found_visible = False
        self.language = language
        self.salutations = salutation_opening_statements

        self.split_pattern = split_pattern
        self.regex_header = r"|".join(regex_headers)
        self.subject=None
        self.sender=None
        self.email_parser=None
        self.parsed_data={}
        self.remove_html=remove_html
        self.escape_rejected_emails=escape_rejected_emails
        self.detect_out_of_office=detect_outof_office
    def read(self, body_text, sender=None, date=None, title_text=None, collated_text=False, date_format="%Y-%m-%d %H:%M:%S"):
        """ Creates new fragment for each line
            and labels as a signature, quote, or hidden.
            Returns EmailMessage instance
        """
        self.fragments = []
        self.subject=title_text
        self.sender=sender
        try:
            date_ = dateparser.parse(date, date_formats=[date_format])
            self.date = date_


            if self.date.tzinfo is None:
                self.date = pytz.utc.localize(self.date)

        except Exception as e:
            self.date=date

        body_text=clean(str(body_text), remove_html=self.remove_html)


        self.source_text=body_text
        message=""
        if self.escape_rejected_emails:
            for rejection in rejected_emails_formulas:
                if re.findall(rejection.strip(), body_text):
                    message="[EMAIL_REJECTED]"
                    break

        if self.detect_out_of_office:
            for ooo in ooo_emails_formulas:
                if re.findall(ooo.strip(), body_text):
                    message = "[OOO]"
                    break
        self.text=body_text
        if message=="[EMAIL_REJECTED]":
            fragment=Fragment(body_text, self.salutations, self.regex_header)
            fragment.is_rejected=True
            self.fragments.append(fragment)
            return self
        elif message== "[OOO]":
            fragment=Fragment(body_text, self.salutations, self.regex_header)
            fragment.is_out_of_office=True
            self.fragments.append(fragment)
            return self
        self.subject = title_text
        #        regex_header = r"(From|To)\s*:[0-9A-Za-zöóìśćłńéáú⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎\s\/@\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+_-]+?((Subj(ect)?)|Sent at)\s?:|From\s*:[\w @\.:,;\&\(\)'\"\*[\]<>#\/\+-]+?(Sent|Date)\s?:(\s*\d+(\s|\/)(\w+|\d+)(\s|\/)\d+(\s|\/)?(\d+:\d+)?)?|From\s*:[\w @\.:,;\&\(\)'\"\*[\]<>#\/\+-]+?(Sent\s+at)\s?:(\s*\d+\s\w+\s\d+\s?\d+:\d+)?|From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(CC)\s?:|From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(To)\s?:|(De|Da)\s*:[0-9ÀA-Za-zéàçèêù\s\/@\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+(Objet|Oggetto)\s?:"
        if self.split_pattern:
            self.regex_header = r"" + self.split_pattern
        starts = [m.start(0) for m in re.finditer(self.regex_header, self.text, re.MULTILINE | re.UNICODE)]

        if len(starts) < 1:
            if collated_text:
                starts = [m.start(0) for m in re.finditer(pattern_salutation_colated, self.text, re.MULTILINE)]
            else:
                starts = [m.start(0) for m in re.finditer(pattern_salutation, self.text, re.MULTILINE)]

            starts = [s for s in starts if s > 150]
        if len(starts) < 1:
            fragment=Fragment(self.text, self.salutations, self.regex_header, collated_text)
            if fragment.date is None:
                fragment.date = self.date
            if fragment.sender is None:
                fragment.sender = self.sender
            self.fragments.append(fragment)

        else:
            if starts[0] > 0:
                starts.insert(0, 0)
            lines = [self.text[i:j] for i, j in zip(starts, starts[1:] + [None])]

            for line in lines:
                if self.split_pattern:
                    line = re.sub(self.split_pattern, '', line)
                if line.strip() != '':
                    fragment=Fragment(line, self.salutations, self.regex_header, collated_text)
                    if fragment.date is None:
                        fragment.date=self.date
                    if fragment.sender is None:
                        fragment.sender=self.sender

                    self.fragments.append(fragment)
        #sort by date
#        try:
#            self.fragments=sorted(self.fragments, key=lambda x: x.date)
#        except:
#            pass
        return self

    def read_eml(self, eml_file):
        self.parsed_data= parse_eml(eml_file)
        self.read(self.parsed_data['body'], self.parsed_data['title'])
        if self.fragments[0].date is None:
            self.fragments[0].date=self.parsed_data["date"]
        return self


    def detect_language(self):

        langs = [l.language for l in self.fragments]
        languages = collections.Counter()
        for d in langs:
            languages.update(d)
        if not languages:
            try:
                lang = detect_language(self.text, num_laguages=2)
            except Exception  as e:
                languages['und'] = 0.90
                print(e)
                return languages

            for l in lang:
                languages[l.language] = l.probability
        self.language=max(languages, key=languages.get)
        return self.language


class Fragment(object):
    """ A Fragment is a part of
        an Email Message, labeling each part.
    """

    def __init__(self, email_text, salutations, regex_header, collated_text=False):
        self.collated_text=collated_text
        self.salutations = salutations
        self.body = email_text.strip()
        self.regex_header = regex_header
        self.is_forwarded_message = self._get_forwarded()
        self.is_out_of_office=False
        self.is_rejected=False
        self.subject = None
        self.sender=None
        self.date=None
        self.headers = self._process_header()
        self.caution = self._get_caution_or_front_content()
        if self.subject is None and not self.collated_text:
            self.subject = self._get_title()
        self.attachement = self._get_attachement()
        self.salutation = self._get_salutation()
        self.disclaimer = self._get_disclaimer()
        self.signature = self._get_signature()
        self._content = email_text

    def _get_title(self):
        patterns = [
            "(R[Ee]|Antw\.:|F[Ww])\s?:\s?.+",
            ".*\s+(?=(Hi|Hello|Dear))"
        ]

        pattern = r'(?P<title>(' + '|'.join(patterns) + '))'
        groups = re.match(pattern, self.body)
        title = ""
        if groups is not None:
            if "title" in groups.groupdict().keys():
                title = groups.groupdict()["title"]
                self.body = self.body[len(title):].strip()
        return title

    def _get_caution_or_front_content(self):
        patterns =[c.strip() for c in email_caution_or_fron_content+sent_from_my_device if c.strip()]
#        pattern = r'(?P<caution>^\s*(' + r'|'.join(regexes) + '))'
        pattern=r'(?P<caution>^\s*(^\s*'+ r'|'.join(patterns)+'))'

        match = re.search(pattern, self.body)
        cautions = []
        while match:
            caution = match.group()
            cautions.append(caution)
            _span = match.span()
            self.body=self.body[_span[1]:]
            match = re.search(pattern, self.body)
#        start_with_closing=
        if len(cautions)==0:
            start_with_closing= re.match(signature_pattern_bis, self.body.strip())
            if start_with_closing:
                #we search for salution. if email start with closing, then form closing to salutation is to be removed
                match= re.search(pattern_salutation, self.body, re.MULTILINE)
                if match:
                    cautions = self.body[:match.start()]
                    self.body=self.body[match.start():]
            return cautions
        # groups = re.match(pattern, self.body, re.MULTILINE)
        # caution=""
        # if groups is not None:
        #     if "caution" in groups.groupdict().keys():
        #         caution = groups.groupdict()["caution"]
        #         self.body = self.body[len(caution):].strip()
        return '\n'.join(cautions)

    def _get_attachement(self):
        pattern = r'(?P<attachement>(^\s*[a-zA-Z0-9_,\. -]+\.(png|jpeg|docx|doc|xlsx|xls|pdf|pptx|ppt))|Attachments\s?:\s?([a-zA-Z0-9_,\. -]+\.(png|jpeg|docx|doc|xlsx|xls|pdf|pptx|ppt)))'
        groups = re.match(pattern, self.body, re.IGNORECASE)
        attachement = ''
        if not groups is None:
            if "attachement" in groups.groupdict().keys():
                attachement = groups.groupdict()["attachement"]
                self.body = self.body[len(attachement):].strip()
        return attachement

    def _get_salutation(self):
        # Notes on regex:
        # Max of 5 words succeeding first Hi/To etc, otherwise is probably an entire sentence

        groups = re.match(pattern_salutation, self.body)
        salutation = ''
        if groups is not None:
            if "salutation" in groups.groupdict().keys():
                salutation = groups.groupdict()["salutation"]
                self.body = self.body[len(salutation):].strip()
        return salutation

    @property
    def language(self):
        return_val = {}
        regx = "\*?-+\s+Sent\s+:.*\s+Received\s+:.*\s+Reply to\s:.*\s+Attachments\s+:.*\s+\*?-*|Dear Sender, thank you for your e-mail. I'll be out of office until.*|NO BODY.*|[^\w.,:\s]"
        text = self.body
        text = re.sub(regx, ' ', text.strip())



        return detect_language(text, num_languages=2, use_large_model=True)

    def _process_header(self):
        header_parser=HeaderParser()

        he=header_parser.parse(self.body)
        if he:
            self.body=header_parser.body
            self.date=he.get('Date_parsed', None)
            if self.date is not None:
                try:
                    self.date = pytz.utc.localize(self.date)
                except Exception as e:
                    pass
            self.date_str=str(he.get('Date', None))
            self.sender=he.get('From', None)
            self.reciever=he.get('To', None)
            self.subject=he.get("Subject", None)

#         print(self.body)
#         print('---------------------')
#
#
#         header_parser=HeaderParser()
#
#         he=header_parser.parse(self.body)
#         if he!={}:
#             print(he)
#         print('-----------------')
# #        print(header_parser.body)
#         #        regex = r"From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(Subj(ect)?)\s?:|From\s*:[\w @\.:,;\&\(\)'\"\*[\]<>#\/\+-]+?(Sent|Date)\s?:(\s*\d+(\s|\/)(\w+|\d+)(\s|\/)\d+(\s|\/)?(\d+:\d+)?)?|From\s*:[\w @\.:,;\&\(\)'\"\*[\]<>#\/\+-]+?(Sent\s+at)\s?:(\s*\d+\s\w+\s\d+\s?\d+:\d+)?|From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(CC)\s?:|From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(To)\s?:"
#
#         pattern = r"(?P<header_text>(" + self.regex_header + "))"
#
#         date_group = re.search(pattern, self.body)
#         header_text = None
#         if date_group is not None:
#             if "header_text" in date_group.groupdict().keys():
#                 header_text = date_group.groupdict()["header_text"]
#                 self.body = self.body[len(header_text):].strip()
#             if 'subject' in date_group.groupdict().keys():
#                 if not self.collated_text:
#                     self.title = date_group.groupdict()["subject"]
#                 elif date_group.groupdict()["subject"] is not None:
#                     self.body=date_group.groupdict()["subject"]+' '+self.body
#                     header_text=""
#
#         if header_text is not None:
#             date_group = re.search(header_date_regex, header_text, re.UNICODE | re.MULTILINE)
#             from_group = re.search(header_from_regex, header_text, re.UNICODE | re.MULTILINE)
#
#             if date_group:
#                 sent_text = date_group.groupdict()["date"]
# #                sent_text = re.sub(r'((?<=\s(\d{2})\:(\d{2})(\:\d{2}))|(?<=\s(\d{2})\:(\d{2}))|(?<=\s(\d{1})\:(\d{2}))).*|(,|\+\d)?\s*[<\w+:-_]+@[<\w+-_>]+.*', '', sent_text, re.IGNORECASE)
# #                 try:
# #                     date_=dateparser.parse(sent_text, date_formats=["%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M"])
# #                     if date_ is not None and date_.tzinfo is None:
# #                         date_=pytz.utc.localize(date_)
# #                     elif date_ is None:
# #                         print(header_text)
# #                 except:
# #                     raise
# #                 if date_ is not None:
# #                     self.date=date_
#
#             if from_group:
#                 from_text = from_group.groupdict()["from"]
#                 self.sender=from_text
#
#             # else:
#             #     print(header_text)
#         # else:
#         #     print("no_header")
#
#         return header_text

    def _get_disclaimer(self):

        groups = re.search(pattern_disclaimer, self.body, re.MULTILINE + re.DOTALL)
        disclaimer_text = None
        if groups is not None:
            if "disclaimer_text" in groups.groupdict().keys():
                found = groups.groupdict()["disclaimer_text"]
                disclaimer_text = self.body[self.body.find(found):]
                self.body = self.body[:self.body.find(disclaimer_text)].strip()

        return disclaimer_text

    def _get_signature(self):
        # note - these openinged statements *must* be in lower case for
        # sig within sig searching to work later in this func

        # TODO DRY
        self.signature = ''
        if self.collated_text:

            groups = re.search(signature_pattern_colated_text, self.body, re.IGNORECASE | re.MULTILINE)
        else:
            groups = re.search(signature_pattern, self.body, re.IGNORECASE | re.MULTILINE)
        signature = None
        if groups:
            if "signature" in groups.groupdict().keys():
                signature1 = groups.groupdict()["signature"]
                # search for a sig within current sig to lessen chance of accidentally stealing words from body
                sig_span = groups.span()
                if sig_span[0]<10:
                    return ""
                signature = self.body[sig_span[0]:]
                self.body = self.body[:sig_span[0]]
                groups = re.search(signature_pattern, signature[len(signature1):], re.IGNORECASE|re.MULTILINE)
                if groups:
                    signature2 = groups.groupdict()["signature"]
                    sig_span = groups.span()
                    if self.collated_text:
                        self.body = self.body + ' ' + signature[:len(signature1) + sig_span[0]]
                    else:
                        self.body = self.body + '\n' + signature[:len(signature1)+sig_span[0]]
                    signature = signature[len(signature1)+sig_span[0]:]

        self.body=re.sub(r"^\s*[\*,;.?!_=+-]+", "", self.body)
        return signature

    def _get_forwarded(self):

        pattern = '(?P<forward_text>([- ]* Forwarded Message [- ]*|[- ]* Forwarded By [- ]*|[- ]*Original Message[- ]*))'
        groups = re.search(pattern, self.body, re.DOTALL)
        forward = None
        if groups is not None:
            if "forward_text" in groups.groupdict().keys():
                forward = groups.groupdict()["forward_text"]

        if forward is not None:
            self.body = self.body.replace(forward, '')

        return forward is not None

    @property
    def content(self):
        return self._content.strip()

def get_input_files(dir_path, type):

    return glob.glob(join(dir_path, "*." + type))


def process_eml_from_folder():

    import xlsxwriter

    workbook = xlsxwriter.Workbook('/Users/mohamedmentis/Dropbox/My Mac (MacBook-Pro.local)/Documents/Mentis/Clients/Octa+/octaplus.xlsx')
    worksheet = workbook.add_worksheet()

    files=get_input_files("/Users/mohamedmentis/Dropbox/My Mac (MacBook-Pro.local)/Desktop/data", 'eml')

    worksheet.write(0, 0, "ContactId")
    worksheet.write(0, 1, "body")
    worksheet.write(0, 2, "title")
    worksheet.write(0, 3, "from")
    worksheet.write(0, 4, "to")
    worksheet.write(0, 5, "date")
    worksheet.write(0, 6, "from_name")
    worksheet.write(0, 7, "language")
    worksheet.write(0, 8, "references")
    worksheet.write(0, 9, "in_replay_to")
    worksheet.write(0, 10, "attachement_names")
    worksheet.write(0, 11, "clean_body_first")
    worksheet.write(0, 12, "lang_body_first")
    worksheet.write(0, 13, "clean_body_concatenated")
    worksheet.write(0, 14, "lang_body_concatenated")
    worksheet.write(0, 15, "clean_body_last")
    worksheet.write(0, 16, "lang_body_last")



    i=1

    with tqdm(total=len(files), position=0, leave=True) as pbar:
        for  file in tqdm(files, position=0, leave=True):
            email=EmailMessage().read_eml(file)
#            cleaned='\n'.join([f.title + '\n' + f.body for f in email.fragments])
#            print(cleaned)
#            print('-----------------------------------------------------------------------\n')
            parsed=email.parsed_data
            parsed["FileName"]=os.path.split(file)[1]
            worksheet.write(i, 0, parsed["FileName"])
            worksheet.write(i, 1, parsed["body"])
            worksheet.write(i, 2, parsed["title"])
            worksheet.write(i, 3, parsed["from"])
            worksheet.write(i, 4, ";".join([ p for p in parsed["to"]]))
            worksheet.write(i, 5, str(parsed["date"]))
            worksheet.write(i, 6, parsed["from_name"])
            worksheet.write(i, 7, parsed["language"])
            worksheet.write(i, 8, ";".join([r for r in parsed["message-id"]]))
            worksheet.write(i, 9, ";".join([r for r in parsed["in_replay_to"]]))
            worksheet.write(i, 10, ";".join([a for a in parsed["attachement_names"]]))
            worksheet.write(i, 11,  email.fragments[0].body)
            worksheet.write(i, 12,  next(iter(email.fragments[0].language)) if email.fragments[0].language else next(iter(email.detect_language())))
            worksheet.write(i, 13,  '\n'.join([f.subject + '\n' + f.body for f in email.fragments]))
            worksheet.write(i, 14, next(iter(email.detect_language())))
            worksheet.write(i, 15,  email.fragments[-1].body)
            worksheet.write(i, 16,  next(iter(email.fragments[-1].language)) if email.fragments[-1].language else next(iter(email.detect_language())))

            i+=1
            pbar.update()

    workbook.close()


def clean_email(text,no_newLines=False):
    if text is None or text.strip()=='':
        return ''
    parsed=EmailMessage().read(body_text=text, title_text=None, collated_text=no_newLines)

    if parsed is  not None:
        return '\n'.join([f.body for f in parsed.fragments])


if __name__ == "__main__":
    # import cProfile, pstats, io
    # from pstats import SortKey
    #
    # pr = cProfile.Profile()
    # pr.enable()

#    process_eml_from_folder()
    # pr.disable()
    # s = io.StringIO()
    # sortby = SortKey.CUMULATIVE
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())

    text="""
        Bonjour,
        J'entends bien que votre calcul est juste par rapport a ma consommation de l'année passée.
        Mais vu le prix en hausse du gaz je ne vais plus me chauffer au gaz, j'ai installé un pellet, donc je n'ai pas envie de m'étrangler financièrement tous les mois.
        Merci de votre compréhension, bien à vous.
        
        Vincent Daubry
        RC Maintenance / Wattiaux
        44 Rue de Douvres à 1070 Anderlecht
        66 / 3 Rue François Lebon à 1400 Nivelles
        Tel 02/523.63.55 ou 067/84.43.21
        vincent.daubry@rcm.be
        vincent.daubry@wattiauxgroup.be
        De : energie@octaplus.be 
        Envoyé : mercredi 28 septembre 2022 08:16
        À : Vincent Daubry 
        Objet : OCTA+: Votre montant d'acompte et solde - Client 221703
        
        Cher Monsieur Daubry,
        Votre demande m'est bien parvenue et je vous en remercie.
        Votre acompte de 480 € est adapté à votre consommation réelle et de la tarification actuelle. Je ne peux diminuer à 300 € comme souhaité.
        Votre facture de septembre avait un délai qui s'étendait jusqu'au 15/09/2022. Vous pouvez effectuer ce paiement de 480 € sur notre compte BE14 0963 0705 0083 avec en référence libre votre numéro de client CL221703.
        Pour toute éventuelle question, n'hésitez pas à réagir à ce message. Nous serons heureux de vous aider.
        Energiquement vôtre,
        Sandra P.
        Pour toutes nos modalités de contact, des questions-réponses et votre espace client personnalisé, cliquez ici.
        
        ________________________________
        From: Vincent Daubry [vd@wattiauxgroup.be]
        Sent: 21/09/2022 11:38:23
        To: OCTA+ Energie [energie@octaplus.be]
        Subject: RE: OCTA+ - Client 221703 - Rappel de paiement
        Bonjour,
        Est-il possible de modifier notre acompte ?
        Je souhaite verser 300,00 € mensuellement
        Merci, bien à vous.
        
        Vincent Daubry
        RC Maintenance / Wattiaux
        44 Rue de Douvres à 1070 Anderlecht
        66 / 3 Rue François Lebon à 1400 Nivelles
        Tel 02/523.63.55 ou 067/84.43.21
        vincent.daubry@rcm.be
        vincent.daubry@wattiauxgroup.be
        De : energie@octaplus.be 
        Envoyé : mardi 20 septembre 2022 15:22
        À : Vincent Daubry 
        Objet : OCTA+ - Client 221703 - Rappel de paiement
        
        [Image supprimée par l'expéditeur.]
        Cher Monsieur Daubry,
        A ce jour, votre compte client présente un solde ouvert de 956,77 €, dont un montant de 480,00 € est échu.
        Vous avez oublié de payer ? Cela peut arriver. Nous vous envoyons votre lettre de rappel en pièce-jointe, et vous invitons à effectuer le paiement avec les références suivantes : Solde ouvert : 956,77 €
        Notre numéro de compte : BE14 0963 0705 0083
        Communication : Client 221703
        Comme nous, vous avez un agenda très chargé et vous souhaitez simplifier votre vie administrative ? Avec une domiciliation bancaire, vous pouvez automatiser le paiement de vos factures et éviter des frais supplémentaires.
        Cliquez ici pour activer une domiciliation pour vos prochaines factures
        Nous espérons recevoir très prochainement votre paiement, et restons naturellement à votre disposition pour toute éventuelle question.
        Energiquement vôtre,
        L'équipe OCTA+
        [Image supprimée par l'expéditeur.]
        [Image supprimée par l'expéditeur.]
        [Image supprimée par l'expéditeur.]
        
        """
    em=EmailMessage().read(text)
    print(em.detect_language())
    print([e.body for e in em.fragments])







