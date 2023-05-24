import os
import re
import traceback
import xml.etree.ElementTree as ET
from pathlib import Path


class GameXml():

    def __init__(self, reg_lines=None, ud_lines=None, game_xml_path=None):
        self.reg_lines = reg_lines
        self.ud_lines = ud_lines
        self.game_xml_path = game_xml_path

    def return_formatted_line_for_gamexml(self, ud_line):
        ret = r'        <File Name="' + os.path.basename(ud_line) + r'" GameRelativePath="' + os.path.dirname(ud_line) + r'" ReadOnly="0" ForceCopy="1" />'
        ret=re.sub("c:", r".\\c1", ret, flags=re.I)
        return ret

    def create_reg_file(self, path_to_game_exe, reg_for_origin):
        ret = True
        try:
            # path_to_game_exe = os.path.dirname(self.game_xml_path)
            if not re.search(r'\[', reg_for_origin, flags=re.I):
                reg_for_origin = '[' + reg_for_origin + ']'
            if not re.search(r'\"', path_to_game_exe, flags=re.I):
                path_to_game_exe = '\"' + path_to_game_exe + '\"'
            reg_for_origin_with_WOW = self.return_formatted_reg_line_with_WOW6432Node(reg_for_origin)
            #creates C:\GameConfig\gameconfig\gameeee\registry\game.reg
            path_to_new_registry = os.path.join(os.path.dirname(self.game_xml_path), 'registry')
            os.makedirs(path_to_new_registry, exist_ok=True)
            with open(os.path.join(path_to_new_registry, r'game.reg'), 'w', encoding = 'utf-8') as f:
                f.writelines(r'Windows Registry Editor Version 5.00' + '\n\n')
                f.writelines(reg_for_origin + '\n')
                f.writelines(r'"Install Dir"=' + path_to_game_exe + '\n')
                f.writelines(reg_for_origin_with_WOW + '\n')
                f.writelines(r'"Install Dir"=' + path_to_game_exe + '\n')
        except Exception as e:
            print(traceback.format_exc())
            ret = False
        return ret

    def add_lines_to_gamexml(self):
        print(self.game_xml_path)
        with open(self.game_xml_path, "r") as f:
                lines = f.readlines()
        with open(self.game_xml_path, "w") as f:
            for line in lines:
                f.write(line)
                if line.strip().startswith("<Files>"):
                    for l in self.ud_lines:
                        f.write(self.return_formatted_line_for_gamexml(l) + '\n')
                if line.strip().startswith("<Registry>"):
                    for l in self.reg_lines:
                        formated = self.return_formatted_reg_line(l)
                        f.write(formated + '\n')
                        f.write(self.return_formatted_reg_line_with_WOW6432Node(formated) + '\n')

    def return_formatted_reg_line(self, reg_line):
        ret=re.sub(r"\[", r'"', reg_line, flags=re.I)
        ret=re.sub(r"\]", r'" />', ret, flags=re.I)
        ret = r'      <ReflectedKey Name=' + ret
        return ret

    def return_formatted_reg_line_with_WOW6432Node(self, reg_line):
        if not r'WOW6432Node' in reg_line:
            reg_line=re.sub(r"\\SOFTWARE\\", r'\\SOFTWARE\\WOW6432Node\\', reg_line, flags=re.I)
        return reg_line

if __name__ == '__main__':
    gx = GameXml(ud_lines=[r'c:\\Games\\Origin Games\\Unravel\\Unravel.exe', r'c:\\Games\\Origin Games\\Unravel\\Unrav3el.exe'], game_xml_path=r'C:\playcast\GameStreamServer\Config\GameConfig\Unravel\Unravel.xml', reg_lines=[r'[HKEY_LOCAL_MACHINE\SOFTWARE\Playdead\INSIDE]', r'[HKEY_LOCAL_MACHINE\SOFTWARE\Playdead\INSID3E]'])
    gx.create_reg_file(path_to_game_exe=r'c:\Games\Origin Games\Unravel', reg_for_origin=r'HKEY_LOCAL_MACHINE\SOFTWARE\Coldwood Interactive\Unravel')