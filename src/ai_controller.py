from typing import List,Tuple
import random
from . import map_controller
from .utility import *
from .battle import Battle
class AI_Controller:
    def __init__(self):
        pass
    def enemy_single_movement(self,_valid,_invalid,_ally,_enemy,mapcontroller):
        valid=_valid   #type:Dict[str,Dict[Tuple[int,int],Tuple[float,List[Tuple[int,int]]]]]
        invalid=_invalid #type:Dict[str,Dict[Tuple[int,int],Tuple[float,List[Tuple[int,int]]]]]
        ally=_ally    #type:Dict[str,Dict[Tuple[int,int],Tuple[float,List[Tuple[int,int]]]]]
        enemy=_enemy   #type:Dict[str,Dict[Tuple[int,int],Tuple[float,List[Tuple[int,int]]]]]
        map=mapcontroller #type:map_controller.Main
        if len(valid)==0:
            return ["E",]
        ring=65536
        candidates=[]   #type:List[str]
        for p in valid:
            if map.person_container.AItype[p][0]<ring:
                ring=map.person_container.AItype[p][0]
                candidates.clear()
                candidates.append(p)
            elif map.person_container.AItype[p][0]==ring:
                candidates.append(p)
        person_to_move=random.choice(candidates)
        return self.individual_movement(valid,invalid,ally,enemy,map,person_to_move)

    def choose_attack_obj(self,strategy,attack_candidate):
        obj=None
        for ao in strategy["Attack_Selection"]:
            if ao=="Fatal":
                for candidate in attack_candidate:
                    if candidate[1].pid in strategy["Not_Attack"]:
                        continue
                    if candidate[3][5]*(1+candidate[3][2])>=candidate[1].ability["HP"]:
                        if candidate[3][3]>0:
                            if obj is None:
                                obj=candidate
                            else:
                                if candidate[3][3]>=obj[3][3]:
                                    obj=candidate
                if not (obj==None):
                    break
            if ao=="Object":
                rank=9999
                for candidate in attack_candidate:
                    if candidate[1].pid in strategy["Not_Attack"]:
                        continue
                    if candidate[1].pid in strategy["Attack_Obj"]:
                        if (candidate[3][5]>0)and(candidate[3][3]>0):
                            if strategy["Attack_Obj"].index(candidate[1].pid)<rank:
                                rank=strategy["Attack_Obj"].index(candidate[1].pid)
                                obj=candidate
                            elif strategy["Attack_Obj"].index(candidate[1].pid)==rank:
                                if candidate[3][0]==1:
                                    obj=candidate
                if not(obj==None):
                    break
            if ao=="Uncountered":
                for candidate in attack_candidate:
                    if candidate[1].pid in strategy["Not_Attack"]:
                        continue
                    if candidate[3][0]==1:
                        if candidate[3][3]>0 and candidate[3][5]>0:
                            if obj is None:
                                obj=candidate
                            else:
                                if candidate[3][5]*(1+candidate[3][2])>=obj[3][5]*(1+obj[3][2]):
                                    obj=candidate
                if not(obj==None):
                    break
            if ao=="Any":
                minhp=9999
                for candidate in attack_candidate:
                    if candidate[1].pid in strategy["Not_Attack"]:
                        continue
                    if candidate[1].ability["HP"]-candidate[3][5]*(1+candidate[3][2])<minhp:
                        if candidate[3][3]>0 and candidate[3][5]>0:
                            minhp=candidate[1].ability["HP"]-candidate[3][5]*(1+candidate[3][2])
                            obj=candidate
                if obj is None:
                    obj=random.choice(attack_candidate)
                if obj[1].pid in strategy["Not_Attack"]:
                    return None
        return obj

    def find_geographical_shortest(self,p,_map,tarpos):
        wait = {}
        dst = {}
        pos = _map.person_container.position[p.pid]
        mov = float(p.ability["MOV"])
        wait[pos] = (mov, [pos, ])
        M = _map.terrain_container.M
        N = _map.terrain_container.N
        while not tarpos in dst:
            (tpos, movtuple) = max(wait.items(), key=lambda x: x[1][0])
            r = movtuple[0]
            track = movtuple[1]
            dst[tpos] = (r, track)
            wait.pop(tpos)
            if tpos[0] > 0:
                npos = (tpos[0] - 1, tpos[1])
                if not (npos in dst):
                    tr = r - _map.terrain_container.map[npos[0]][npos[1]].decay[
                        _map.global_vars.data.cls_clsgroup[p.cls]]
                    newtrack = track.copy()
                    newtrack.append(npos)
                    if True:
                        if npos in wait:
                            r0 = wait[npos][0]
                            if tr > r0:
                                wait[npos] = (tr, newtrack)
                        else:
                            wait[npos] = (tr, newtrack)
            if tpos[0] < M - 1:
                npos = (tpos[0] + 1, tpos[1])
                if not (npos in dst):
                    tr = r - _map.terrain_container.map[npos[0]][npos[1]].decay[
                        _map.global_vars.data.cls_clsgroup[p.cls]]
                    newtrack = track.copy()
                    newtrack.append(npos)
                    if True:
                        if npos in wait:
                            r0 = wait[npos][0]
                            if tr > r0:
                                wait[npos] = (tr, newtrack)
                        else:
                            wait[npos] = (tr, newtrack)
            if tpos[1] > 0:
                npos = (tpos[0], tpos[1] - 1)
                if not (npos in dst):
                    tr = r - _map.terrain_container.map[npos[0]][npos[1]].decay[
                        _map.global_vars.data.cls_clsgroup[p.cls]]
                    newtrack = track.copy()
                    newtrack.append(npos)
                    if True:
                        if npos in wait:
                            r0 = wait[npos][0]
                            if tr > r0:
                                wait[npos] = (tr, newtrack)
                        else:
                            wait[npos] = (tr, newtrack)
            if tpos[1] < N - 1:
                npos = (tpos[0], tpos[1] + 1)
                if not (npos in dst):
                    tr = r - _map.terrain_container.map[npos[0]][npos[1]].decay[
                        _map.global_vars.data.cls_clsgroup[p.cls]]
                    newtrack = track.copy()
                    newtrack.append(npos)
                    if True:
                        if npos in wait:
                            r0 = wait[npos][0]
                            if tr > r0:
                                wait[npos] = (tr, newtrack)
                        else:
                            wait[npos] = (tr, newtrack)
        track = dst[tarpos][1]
        rem_mov = dst[tarpos][0]
        moveto = tarpos
        occupied = 0
        for _p in _map.person_container.position:
            if not (_p == p.pid):
                if _map.person_container.position[_p] == moveto:
                    occupied = 1
                    break
        return (dst,track,rem_mov,moveto,occupied)

    def find_relative_shortest(self,p,_map,tarpos):
        wait = {}
        dst = {}
        pos = _map.person_container.position[p.pid]
        mov = float(p.ability["MOV"])
        wait[pos] = (mov, [pos, ])
        M = _map.terrain_container.M
        N = _map.terrain_container.N
        while not tarpos in dst:
            (tpos, movtuple) = max(wait.items(), key=lambda x: x[1][0])
            r = movtuple[0]
            track = movtuple[1]
            dst[tpos] = (r, track)
            wait.pop(tpos)
            if tpos[0] > 0:
                npos = (tpos[0] - 1, tpos[1])
                if not (npos in dst):
                    occ=0
                    for _p in _map.person_container.position:
                        if not (_map.person_container.controller[_p]%2==_map.person_container.controller[p.pid]%2):
                            if _map.person_container.position[_p] == npos:
                                occ = 1
                                break
                    if occ==0:
                        tr = r - _map.terrain_container.map[npos[0]][npos[1]].decay[_map.global_vars.data.cls_clsgroup[p.cls]]
                    else:
                        tr=r-255
                    newtrack = track.copy()
                    newtrack.append(npos)
                    if True:
                        if npos in wait:
                            r0 = wait[npos][0]
                            if tr > r0:
                                wait[npos] = (tr, newtrack)
                        else:
                            wait[npos] = (tr, newtrack)
            if tpos[0] < M - 1:
                npos = (tpos[0] + 1, tpos[1])
                if not (npos in dst):
                    occ=0
                    for _p in _map.person_container.position:
                        if not (_map.person_container.controller[_p]%2==_map.person_container.controller[p.pid]%2):
                            if _map.person_container.position[_p] == npos:
                                occ = 1
                                break
                    if occ==0:
                        tr = r - _map.terrain_container.map[npos[0]][npos[1]].decay[_map.global_vars.data.cls_clsgroup[p.cls]]
                    else:
                        tr=r-255
                    newtrack = track.copy()
                    newtrack.append(npos)
                    if True:
                        if npos in wait:
                            r0 = wait[npos][0]
                            if tr > r0:
                                wait[npos] = (tr, newtrack)
                        else:
                            wait[npos] = (tr, newtrack)
            if tpos[1] > 0:
                npos = (tpos[0], tpos[1] - 1)
                if not (npos in dst):
                    occ=0
                    for _p in _map.person_container.position:
                        if not (_map.person_container.controller[_p]%2==_map.person_container.controller[p.pid]%2):
                            if _map.person_container.position[_p] == npos:
                                occ = 1
                                break
                    if occ==0:
                        tr = r - _map.terrain_container.map[npos[0]][npos[1]].decay[_map.global_vars.data.cls_clsgroup[p.cls]]
                    else:
                        tr=r-255
                    newtrack = track.copy()
                    newtrack.append(npos)
                    if True:
                        if npos in wait:
                            r0 = wait[npos][0]
                            if tr > r0:
                                wait[npos] = (tr, newtrack)
                        else:
                            wait[npos] = (tr, newtrack)
            if tpos[1] < N - 1:
                npos = (tpos[0], tpos[1] + 1)
                if not (npos in dst):
                    occ=0
                    for _p in _map.person_container.position:
                        if not (_map.person_container.controller[_p]%2==_map.person_container.controller[p.pid]%2):
                            if _map.person_container.position[_p] == npos:
                                occ = 1
                                break
                    if occ==0:
                        tr = r - _map.terrain_container.map[npos[0]][npos[1]].decay[_map.global_vars.data.cls_clsgroup[p.cls]]
                    else:
                        tr=r-255
                    newtrack = track.copy()
                    newtrack.append(npos)
                    if True:
                        if npos in wait:
                            r0 = wait[npos][0]
                            if tr > r0:
                                wait[npos] = (tr, newtrack)
                        else:
                            wait[npos] = (tr, newtrack)
        track = dst[tarpos][1]
        rem_mov = dst[tarpos][0]
        moveto = tarpos
        occupied = 0
        for _p in _map.person_container.position:
            if not (_p == p.pid):
                if _map.person_container.position[_p] == moveto:
                    occupied = 1
                    break
        return (dst,track,rem_mov,moveto,occupied)

    def find_push_action(self,p,_map,tar):
        tarpos=_map.person_container.position[tar]
        dst,track,rem_mov,moveto,occupied=self.find_geographical_shortest(p,_map,tarpos)
        if rem_mov<-100:
            return (None,None)
        while not ((rem_mov>=float(0)) and occupied==0):
            moveto=track[-2]
            rem_mov=dst[moveto][0]
            track=dst[moveto][1]
            occupied=0
            for _p in _map.person_container.position:
                if not (_p == p.pid):
                    if _map.person_container.position[_p] == moveto:
                        occupied = 1
                        break
        return moveto,track

    def individual_movement(self,_valid,_invalid,_ally,_enemy,_map,_person_to_move):
        p=_person_to_move
        strategy=_map.person_container.AItype[p][1]
        person=_map.global_vars.personBank[p]
        pos = _map.person_container.position[p]
        if strategy["Strategy"]=="PURSUE":
            for tar in strategy["Push"]:
                tartp = tar.split(",")
                if len(tartp) == 1:
                    push_pid = tartp[0]
                    if push_pid in _map.person_container.position:
                        (move_to, track) = self.find_push_action(person, _map, push_pid)
                        if not move_to == None:
                            attack_candidate = []
                            if len(person.item) > 0:
                                for weap in person.item:
                                    if _map.can_equip(p,weap):
                                        minrange = weap.itemtype.min_range
                                        maxrange = weap.itemtype.max_range
                                        for enm in _enemy:
                                            pose = _map.person_container.position[enm]
                                            if (calc_dist(pose, move_to) >= minrange) and (
                                                calc_dist(pose, move_to) <= maxrange):
                                                enemy_person = _map.global_vars.personBank[enm]
                                                bat = Battle(person, enemy_person, weap, enemy_person.get_equip(), _map,
                                                             move_to)
                                                sim = bat.simulate()
                                                del (bat)
                                                attack_candidate.append((move_to, enemy_person, weap, sim))
                            if len(attack_candidate) > 0:
                                attack_object = self.choose_attack_obj(strategy, attack_candidate)
                                if not (attack_object == None):
                                    return ["A",person,move_to,track,attack_object[1],attack_object[2]]
                            return ["M", person, move_to, track]
                else:
                    tarpos = (int(tartp[0]), int(tartp[1]))
                    dst_g, track_g, rem_mov_g, moveto_g, occupied_g = self.find_geographical_shortest(person, _map,
                                                                                                      tarpos)
                    dst_r, track_r, rem_mov_r, moveto_r, occupied_r = self.find_relative_shortest(person, _map, tarpos)
                    # print(tarpos,rem_mov_g,rem_mov_r)
                    if (rem_mov_r - rem_mov_g <= person.ability["MOV"]) and (rem_mov_r >= -100):
                        while not ((rem_mov_r >= float(0)) and occupied_r == 0):
                            moveto_r = track_r[-2]
                            rem_mov_r = dst_r[moveto_r][0]
                            track_r = dst_r[moveto_r][1]
                            occupied_r = 0
                            for _p in _map.person_container.position:
                                if not (_p == person.pid):
                                    if _map.person_container.position[_p] == moveto_r:
                                        occupied_r = 1
                                        break
                        attack_candidate = []
                        if len(person.item) > 0:
                            for weap in person.item:
                                if _map.can_equip(p, weap):
                                    minrange = weap.itemtype.min_range
                                    maxrange = weap.itemtype.max_range
                                    for enm in _enemy:
                                        pose = _map.person_container.position[enm]
                                        if (calc_dist(pose, moveto_r) >= minrange) and (
                                                    calc_dist(pose, moveto_r) <= maxrange):
                                            enemy_person = _map.global_vars.personBank[enm]
                                            bat = Battle(person, enemy_person, weap, enemy_person.get_equip(), _map,
                                                         moveto_r)
                                            sim = bat.simulate()
                                            del (bat)
                                            attack_candidate.append((moveto_r, enemy_person, weap, sim))
                        if len(attack_candidate) > 0:
                            attack_object = self.choose_attack_obj(strategy, attack_candidate)
                            if not (attack_object == None):
                                return ["A", person, moveto_r, track_r, attack_object[1], attack_object[2]]
                        return ["M", person, moveto_r, track_r]
                        # find way on relative best route
                    else:
                        step = 0
                        direction = 0
                        while True:
                            moveto_g = track_g[step]
                            rem_mov_g = dst_g[moveto_g][0]
                            if rem_mov_g < 0:
                                direction = 1
                                step -= 1
                                continue
                            for _p in _map.person_container.position:
                                if not (_p == person.pid):
                                    if _map.person_container.position[_p] == moveto_g:
                                        if _map.person_container.controller[_p] % 2 == _map.person_container.controller[
                                            person.pid] % 2:
                                            if direction == 0:
                                                step += 1
                                            else:
                                                step -= 1
                                            break
                                        else:
                                            movement_candidate = []
                                            dst_to_move_list = _valid[p]
                                            for dst in dst_to_move_list:
                                                if len(person.item) > 0:
                                                    for weap in person.item:
                                                        if _map.can_equip(p,
                                                                          weap):  # attackable(weap.itemtype.weapontype):
                                                            minrange = weap.itemtype.min_range
                                                            maxrange = weap.itemtype.max_range
                                                            for enm in _enemy:
                                                                if not enm == _p:
                                                                    continue
                                                                pose = _map.person_container.position[enm]
                                                                if (calc_dist(pose, dst) >= minrange) and (
                                                                            calc_dist(pose, dst) <= maxrange):
                                                                    enemy_person = _map.global_vars.personBank[enm]
                                                                    bat = Battle(person, enemy_person, weap,
                                                                                 enemy_person.get_equip(), _map, dst)
                                                                    sim = bat.simulate()
                                                                    del (bat)
                                                                    movement_candidate.append(
                                                                        (dst, enemy_person, weap, sim))
                                            if len(movement_candidate) > 0:
                                                attack_object = self.choose_attack_obj(strategy, movement_candidate)
                                                if not (attack_object == None):
                                                    dst = attack_object[0]
                                                    track = dst_to_move_list[dst][1]
                                                    return ["A", person, dst, track, attack_object[1], attack_object[2]]
                                            while not ((rem_mov_r >= float(0)) and occupied_r == 0):
                                                moveto_r = track_r[-2]
                                                rem_mov_r = dst_r[moveto_r][0]
                                                track_r = dst_r[moveto_r][1]
                                                occupied_r = 0
                                                for _p in _map.person_container.position:
                                                    if not (_p == person.pid):
                                                        if _map.person_container.position[_p] == moveto_r:
                                                            occupied_r = 1
                                                            break
                                            attack_candidate = []
                                            if len(person.item) > 0:
                                                for weap in person.item:
                                                    if _map.can_equip(p, weap):
                                                        minrange = weap.itemtype.min_range
                                                        maxrange = weap.itemtype.max_range
                                                        for enm in _enemy:
                                                            pose = _map.person_container.position[enm]
                                                            if (calc_dist(pose, moveto_r) >= minrange) and (
                                                                        calc_dist(pose, moveto_r) <= maxrange):
                                                                enemy_person = _map.global_vars.personBank[enm]
                                                                bat = Battle(person, enemy_person, weap,
                                                                             enemy_person.get_equip(), _map,
                                                                             moveto_r)
                                                                sim = bat.simulate()
                                                                del (bat)
                                                                attack_candidate.append(
                                                                    (moveto_r, enemy_person, weap, sim))
                                            if len(attack_candidate) > 0:
                                                attack_object = self.choose_attack_obj(strategy, attack_candidate)
                                                if not (attack_object == None):
                                                    return ["A", person, moveto_r, track_r, attack_object[1],
                                                            attack_object[2]]
                                            return ["M", person, moveto_r, track_r]
                                            # push the enemy
                            if step == len(track_g) - 1:
                                return ["M", person, moveto_g, dst_g[moveto_g][1]]
                            if direction == 1:
                                return ["M", person, moveto_g, dst_g[moveto_g][1]]
                            step += 1
                            # go maximum at geographical best route and attack blocker
            return ["M", person, pos, [pos]]
        if strategy["Strategy"]=="ACTIVE":
            movement_candidate = []
            dst_to_move_list = _valid[p]
            for dst in dst_to_move_list:
                if len(person.item) > 0:
                    for weap in person.item:
                        if _map.can_equip(p, weap):  # attackable(weap.itemtype.weapontype):
                            minrange = weap.itemtype.min_range
                            maxrange = weap.itemtype.max_range
                            for enm in _enemy:
                                pose = _map.person_container.position[enm]
                                if (calc_dist(pose, dst) >= minrange) and (calc_dist(pose, dst) <= maxrange):
                                    enemy_person = _map.global_vars.personBank[enm]
                                    bat = Battle(person, enemy_person, weap, enemy_person.get_equip(), _map, dst)
                                    sim = bat.simulate()
                                    del (bat)
                                    movement_candidate.append((dst, enemy_person, weap, sim))
            if len(movement_candidate) > 0:
                attack_object = self.choose_attack_obj(strategy, movement_candidate)
                if not (attack_object == None):
                    dst = attack_object[0]
                    track = dst_to_move_list[dst][1]
                    return ["A", person, dst, track, attack_object[1], attack_object[2]]
            for tar in strategy["Push"]:
                tartp=tar.split(",")
                if len(tartp)==1:
                    push_pid=tartp[0]
                    if push_pid in _map.person_container.position:
                        (move_to,track)=self.find_push_action(person,_map,push_pid)
                        if not move_to==None:
                            return ["M",person,move_to,track]
                else:
                    tarpos=(int(tartp[0]),int(tartp[1]))
                    dst_g, track_g, rem_mov_g, moveto_g, occupied_g=self.find_geographical_shortest(person,_map,tarpos)
                    dst_r,track_r,rem_mov_r,moveto_r,occupied_r=self.find_relative_shortest(person,_map,tarpos)
                    #print(tarpos,rem_mov_g,rem_mov_r)
                    if (rem_mov_r-rem_mov_g<=person.ability["MOV"])and(rem_mov_r>=-100):
                        while not ((rem_mov_r >= float(0)) and occupied_r == 0):
                            moveto_r = track_r[-2]
                            rem_mov_r = dst_r[moveto_r][0]
                            track_r = dst_r[moveto_r][1]
                            occupied_r = 0
                            for _p in _map.person_container.position:
                                if not (_p == person.pid):
                                    if _map.person_container.position[_p] == moveto_r:
                                        occupied_r = 1
                                        break
                        return ["M",person,moveto_r,track_r]
                        #find way on relative best route
                    else:
                        step=0
                        direction=0
                        while True:
                            moveto_g=track_g[step]
                            rem_mov_g=dst_g[moveto_g][0]
                            if rem_mov_g<0:
                                direction=1
                                step-=1
                                continue
                            for _p in _map.person_container.position:
                                if not (_p == person.pid):
                                    if _map.person_container.position[_p] == moveto_g:
                                        if _map.person_container.controller[_p] %2 == _map.person_container.controller[person.pid]%2:
                                            if direction==0:
                                                step+=1
                                            else:
                                                step-=1
                                            break
                                        else:
                                            movement_candidate = []
                                            dst_to_move_list = _valid[p]
                                            for dst in dst_to_move_list:
                                                if len(person.item) > 0:
                                                    for weap in person.item:
                                                        if _map.can_equip(p,
                                                                          weap):  # attackable(weap.itemtype.weapontype):
                                                            minrange = weap.itemtype.min_range
                                                            maxrange = weap.itemtype.max_range
                                                            for enm in _enemy:
                                                                if not enm==_p:
                                                                    continue
                                                                pose = _map.person_container.position[enm]
                                                                if (calc_dist(pose, dst) >= minrange) and (
                                                                    calc_dist(pose, dst) <= maxrange):
                                                                    enemy_person = _map.global_vars.personBank[enm]
                                                                    bat = Battle(person, enemy_person, weap,
                                                                                 enemy_person.get_equip(), _map, dst)
                                                                    sim = bat.simulate()
                                                                    del (bat)
                                                                    movement_candidate.append(
                                                                        (dst, enemy_person, weap, sim))
                                            if len(movement_candidate) > 0:
                                                attack_object = self.choose_attack_obj(strategy, movement_candidate)
                                                if not (attack_object == None):
                                                    dst = attack_object[0]
                                                    track = dst_to_move_list[dst][1]
                                                    return ["A", person, dst, track, attack_object[1], attack_object[2]]
                                            while not ((rem_mov_r >= float(0)) and occupied_r == 0):
                                                moveto_r = track_r[-2]
                                                rem_mov_r = dst_r[moveto_r][0]
                                                track_r = dst_r[moveto_r][1]
                                                occupied_r = 0
                                                for _p in _map.person_container.position:
                                                    if not (_p == person.pid):
                                                        if _map.person_container.position[_p] == moveto_r:
                                                            occupied_r = 1
                                                            break
                                            attack_candidate = []
                                            if len(person.item) > 0:
                                                for weap in person.item:
                                                    if _map.can_equip(p, weap):
                                                        minrange = weap.itemtype.min_range
                                                        maxrange = weap.itemtype.max_range
                                                        for enm in _enemy:
                                                            pose = _map.person_container.position[enm]
                                                            if (calc_dist(pose, moveto_r) >= minrange) and (
                                                                        calc_dist(pose, moveto_r) <= maxrange):
                                                                enemy_person = _map.global_vars.personBank[enm]
                                                                bat = Battle(person, enemy_person, weap,
                                                                             enemy_person.get_equip(), _map,
                                                                             moveto_r)
                                                                sim = bat.simulate()
                                                                del (bat)
                                                                attack_candidate.append(
                                                                    (moveto_r, enemy_person, weap, sim))
                                            if len(attack_candidate) > 0:
                                                attack_object = self.choose_attack_obj(strategy, attack_candidate)
                                                if not (attack_object == None):
                                                    return ["A", person, moveto_r, track_r, attack_object[1],
                                                            attack_object[2]]
                                            return ["M", person, moveto_r, track_r]
                                            #push the enemy
                            if step==len(track_g)-1:
                                return ["M",person,moveto_g,dst_g[moveto_g][1]]
                            if direction==1:
                                return ["M",person,moveto_g,dst_g[moveto_g][1]]
                            step+=1
                            #go maximum at geographical best route and attack blocker
            return ["M",person,pos,[pos]]
        if strategy["Strategy"]=="STAY":
            return ["M",person,pos,[pos]]
        if strategy["Strategy"]=="DEFENSIVE":
            attack_candidate=[]
            if len(person.item)>0:
                for weap in person.item:
                    if _map.can_equip(p,weap):
                        minrange=weap.itemtype.min_range
                        maxrange=weap.itemtype.max_range
                        for enm in _enemy:
                            pose=_map.person_container.position[enm]
                            if (calc_dist(pose,pos)>=minrange)and(calc_dist(pose,pos)<=maxrange):
                                enemy_person=_map.global_vars.personBank[enm]
                                bat=Battle(person,enemy_person,weap,enemy_person.get_equip(),_map,pos)
                                sim=bat.simulate()
                                del(bat)
                                attack_candidate.append((pos,enemy_person,weap,sim))
            if len(attack_candidate)>0:
                attack_object=self.choose_attack_obj(strategy,attack_candidate)
                if not (attack_object==None):
                    return ["A",person,pos,[pos],attack_object[1],attack_object[2]]
                else:
                    return ["M",person,pos,[pos]]
            else:
                return ["M",person,pos,[pos]]
        if strategy["Strategy"]=="PASSIVE":
            movement_candidate=[]
            dst_to_move_list=_valid[p]
            for dst in dst_to_move_list:
                if len(person.item) > 0:
                    for weap in person.item:
                        if _map.can_equip(p,weap):#attackable(weap.itemtype.weapontype):
                            minrange = weap.itemtype.min_range
                            maxrange = weap.itemtype.max_range
                            for enm in _enemy:
                                pose = _map.person_container.position[enm]
                                if (calc_dist(pose, dst) >= minrange) and (calc_dist(pose, dst) <= maxrange):
                                    enemy_person = _map.global_vars.personBank[enm]
                                    bat = Battle(person, enemy_person, weap, enemy_person.get_equip(), _map, dst)
                                    sim = bat.simulate()
                                    del(bat)
                                    movement_candidate.append((dst,enemy_person, weap, sim))
            if len(movement_candidate)>0:
                attack_object=self.choose_attack_obj(strategy,movement_candidate)
                if not (attack_object==None):
                    dst=attack_object[0]
                    track=dst_to_move_list[dst][1]
                    return ["A",person,dst,track,attack_object[1],attack_object[2]]
                else:
                    return ["M",person,pos,[pos]]
            else:
                return ["M",person,pos,[pos]]
        if strategy["Strategy"]=="NULL":
            dst_to_move_list=_valid[p]
            dst_to_move=random.choice(list(dst_to_move_list.keys()))
            track=dst_to_move_list[dst_to_move][1]
            return ["M",person,dst_to_move,track]
        return ["E"]