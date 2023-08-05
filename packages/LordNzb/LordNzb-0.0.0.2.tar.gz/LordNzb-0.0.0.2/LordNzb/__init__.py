
import os
import regex as re
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import quote as link_encode
from dataclasses import dataclass
from LordNzb.helper.reg import multi_regex_matching


regPas = re.compile("{{(.+)?}}")
m_reg_Head = multi_regex_matching(
    '\"(?P<val>[A-Za-z0-9]*)\.(?:par|7z|vol|nfo)(?:.+?)\"',
    '(?P<val>[A-Za-z0-9]*)\.(?:par|7z|vol|nfo)(?:.+?)'
)
regXMLNS = re.compile('{(.+?)}')


def _find_in_xml(root, str):
    for e in root:
        if str in e.tag:
            return e
    return None


@dataclass
class NZB:
    filename: str

    header: str
    password: str

    groups: list
    size: str
    date_time_utc: float

    @property
    def name(self):
        _nzb = self.filename.replace(".nzb", "")
        _nzb = regPas.sub("", _nzb)
        return _nzb

    def get_date_string(self, dateformat='%Y-%m-%d %H:%M:%S') -> str:
        if self.date_time_utc is not None:
            return datetime.utcfromtimestamp(self.date_time_utc).strftime(dateformat)
        return ""

    def get_meta_dict(self) -> dict:
        """
        return Dictionary with significant values
        """
        date = self.get_date_string()

        link_name = link_encode(self.name)
        link_header = link_encode(self.header)
        link_pass = link_encode(self.password)
        link_one_group = link_encode(self.groups[0] if self.groups else '')

        return {
            "filename": self.filename,
            "name": self.name,
            "header": self.header,
            "password": self.password,
            "group": self.groups,
            "size": self.size,
            "date": date,
            "nzbindex": f"https://nzbindex.nl/?q={link_header}",
            "nzbking": f"https://nzbking.com/?q={link_header}",
            "binsearch": f"https://binsearch.info/?q={link_header}",
            "nzblnk": f"nzblnk://?t={link_name}&h={link_header}&p={link_pass}&g={link_one_group}"
        }

    @staticmethod
    def get_dict_keys() -> list:
        return ["filename", "name", "header", "password", "group", "size", "date", "nzbindex", "nzbking", "binsearch",
                "nzblnk"]


def parser(file_path):
    file_name = os.path.basename(file_path)

    # open XML
    tree = ET.parse(file_path)
    root = tree.getroot()

    # get Passwort
    passw = ""
    _passw = regPas.search(file_name)
    if not _passw is None:
        passw = _passw.group(1)
    else:
        _ele = root.find(".//*[@type='password']")
        if not _ele is None:
           passw = _ele.text

    # get Header

    ele = _find_in_xml(root, 'file')

    header = ""
    _th = ele.attrib['subject']
    _th = m_reg_Head(_th)
    if not _th is None:
        header = _th['val']

    # get Group

    group = []

    ns = regXMLNS.search(root.tag)
    if ns is not None:
        ns = ns.group(0)
    else:
        ns = ""
    groups = ele.findall(".//" + ns + "group")

    for g in groups:
        group.append(g.text)

    # Date

    dateTime = None
    _eleDate = root.find(".//*[@date]")
    if _eleDate is not None:
        dateTime = int(_eleDate.attrib['date'])

    # Size

    size = 0
    _segments = root.findall(".//" + ns + "segment")
    for segm in _segments:
        size += int(segm.attrib['bytes'])
    for size_name in ['bytes', 'kb', 'mb', 'gb', 'tb']:
        if size >= 1024:
            size = size / 1024
        else:
            size = f"{size:.2f} {size_name}"
            break

    r_nzb = NZB(
        filename=file_name,
        password=passw,
        header=header,
        date_time_utc=dateTime,
        groups=group,
        size=size,
    )
    return r_nzb