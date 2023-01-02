from connector import ClassConnector

import os.path
from xml.etree.ElementTree import parse

import pygame
# python3 -m pip install -U pygame


def rotate_compass(basis_direction, rotate_steps):
    compass = "NESW"
    return compass[(compass.index(basis_direction) + int(rotate_steps)) % 4]


class ClassPart:
    def set_banns(self, part_list):
        for part in part_list:
            if self.ConnectorN != part.ConnectorS:
                self.bannsN.add(part)
            if self.ConnectorE != part.ConnectorW:
                self.bannsE.add(part)
            if self.ConnectorS != part.ConnectorN:
                self.bannsS.add(part)
            if self.ConnectorW != part.ConnectorE:
                self.bannsW.add(part)

    def __init__(self, size, folder_offset, part, rotate=0):
        self.bannsW = set()
        self.bannsS = set()
        self.bannsE = set()
        self.bannsN = set()

        self.image = \
            pygame.transform.rotate(  # rotates counterclockwise
                pygame.transform.smoothscale(
                    pygame.image.load(os.path.join("Designes", folder_offset, part.attrib["File"])),
                    (size + 1, size + 1)
                ),
                rotate * 90
            )
        self.ConnectorN = ClassConnector(part.attrib[rotate_compass("N", rotate)])
        self.ConnectorE = ClassConnector(part.attrib[rotate_compass("E", rotate)])
        self.ConnectorS = ClassConnector(part.attrib[rotate_compass("S", rotate)])
        self.ConnectorW = ClassConnector(part.attrib[rotate_compass("W", rotate)])

        self.Name = f'{part.attrib["File"].split(".")[0]:<10} - R {rotate}'

    def __str__(self):
        return f"ClassPart : {self.Name:<20} {self.ConnectorN} {self.ConnectorE} {self.ConnectorS} {self.ConnectorW}"

    def __repr__(self):
        return self.Name


class ClassParts:
    def __init__(self, design, part_size, ):
        self.PartList = []
        xml_part_list = parse(os.path.join("Designes", design, "PartList.xml"))
        for Part in xml_part_list.findall('Part'):

            if "turns" in Part.attrib.keys():
                turn_string = Part.attrib["turns"]
                for i in range(len(turn_string)):
                    self.PartList.append(ClassPart(part_size, design, Part, int(turn_string[i])))
            else:
                self.PartList.append(ClassPart(part_size, design, Part))

        for Part in self.PartList:
            Part.set_banns(self.PartList)

    def __str__(self):
        result = "Loaded Parts\n"
        for Part in self.PartList:
            result = result + str(Part) + "\n"
        return result
