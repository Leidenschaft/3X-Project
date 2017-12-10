from typing import Dict
import terrain
import cls
import person
import ai_controller
class Main:
    def __init__(self):
        self.terrainBank={}                 #type:Dict[str,terrain.Terrain]
        self.clsBank={}                     #type:Dict[str,cls.Cls]
        self.personBank={}                  #type:Dict[str,person.Person]
        self.cls_clsgroup={}                #type:Dict[str,str]
        self.AIcontroller=None             #type:ai_controller.AI_Controller
    def __init__(self,data):
        self.terrainBank=terrain.Main(data).terrain_bank
        self.clsBank=cls.Main(data).cls_bank
        self.personBank=person.Main(data).person_bank
        self.cls_clsgroup=data.cls_clsgroup
        self.AIcontroller=ai_controller.AI_Controller()
