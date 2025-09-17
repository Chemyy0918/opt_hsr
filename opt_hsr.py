import f90nml
import autograd
import numpy
def normal_dmg(chara_level,white_hp,hp_percent,hp_mag,white_atk,atk_percent,atk_mag,white_def,def_percent,def_mag,special,special_mag,crit_rate,crit_dmg,boost,res_ignore,def_ignore,enermy_level,enermy_res,receive_boost,def_reduce,dmg_reduce):
    base_factor = white_hp*(1+hp_percent)*hp_mag+white_atk*(1+atk_percent)*atk_mag+white_def*(1+def_percent)*def_mag+special*special_mag
    if crit_rate>1:
        crit_rate = 1
    expect_crit_factor = crit_rate*(1+crit_dmg)+(1-crit_rate)*1
    boost_factor = 1+boost
    receive_boost_factor = 1+receive_boost
    def_factor = (chara_level+20)/((chara_level+20)+(enermy_level+20)*(1-def_reduce-def_ignore))
    res_factor = 1-enermy_res+res_ignore
    reduce_factor = 1-dmg_reduce
    return base_factor*expect_crit_factor*boost_factor*receive_boost_factor*def_factor*res_factor*reduce_factor
def normal_dmg_crit(chara_level,white_hp,hp_percent,hp_mag,white_atk,atk_percent,atk_mag,white_def,def_percent,def_mag,special,special_mag,crit_rate,crit_dmg,boost,res_ignore,def_ignore,enermy_level,enermy_res,receive_boost,def_reduce,dmg_reduce):
    base_factor = white_hp*(1+hp_percent)*hp_mag+white_atk*(1+atk_percent)*atk_mag+white_def*(1+def_percent)*def_mag+special*special_mag
    boost_factor = 1+boost
    receive_boost_factor = 1+receive_boost
    def_factor = (chara_level+20)/((chara_level+20)+(enermy_level+20)*(1-def_reduce-def_ignore))
    res_factor = 1-enermy_res+res_ignore
    reduce_factor = 1-dmg_reduce
    uncrit = base_factor*boost_factor*receive_boost_factor*def_factor*res_factor*reduce_factor
    docrit = base_factor*boost_factor*(1+crit_dmg)*receive_boost_factor*def_factor*res_factor*reduce_factor
    return [uncrit,docrit]
def dot_dmg():
    #TODO
    return 
def break_dmg(dmg_type,chara_level,break_effect,break_mag,boost,res_ignore,def_ignore,enermy_level,enermy_toughness,enermy_res,receive_boost,def_reduce,dmg_reduce):
    if dmg_type == "physical"or dmg_type== "fire":
        type_mag=2.0
    elif dmg_type=="wind":
        type_mag=1.5
    elif dmg_type=="ice" or dmg_type =="lightning":
        type_mag=1.0
    elif dmg_type=="quantum"or dmg_type=="imaginary":
        type_mag=0.5
    break_factor = 3767.55*(1+break_effect)*break_mag
    toughness_factor = enermy_toughness/40+0.5
    boost_factor = 1+boost
    def_factor = (chara_level+20)/((chara_level+20)+(enermy_level+20)*(1-def_reduce-def_ignore))
    receive_boost_factor = 1+receive_boost
    res_factor = 1-(enermy_res-res_ignore)
    reduce_factor = 1-dmg_reduce
    return type_mag*break_factor*toughness_factor*boost_factor*def_factor*receive_boost_factor*res_factor*reduce_factor
def superbreak_dmg(chara_level,break_effect,toughness_reduce,superbreak_mag,boost,res_ignore,def_ignore,enermy_level,enermy_res, receive_boost,def_reduce,dmg_reduce):
    break_factor = 3767.55*(1+break_effect)*superbreak_mag
    toughness_factor = toughness_reduce/10
    boost_factor = 1+boost
    def_factor = (chara_level+20)/((chara_level+20)+(enermy_level+20)*(1-def_reduce-def_ignore))
    receive_boost_factor = 1+receive_boost
    res_factor = 1-enermy_res+res_ignore
    reduce_factor = 1-dmg_reduce
    return break_factor*toughness_factor*boost_factor*def_factor*receive_boost_factor*res_factor*reduce_factor
#----数据读取----
config = f90nml.read("config.txt")
common = config['common']
chara = config['chara']
enermy = config['enermy']
##----通用区----
calculation = common['calculation']
dmg_type = common['dmg_type']
##----角色区----
###----基本数值区----
chara_level = float(chara['chara_level'])
white_hp = float(chara['white_hp'])+1e-8
blue_hp = float(chara['blue_hp'])
hp_percent = blue_hp / white_hp
white_atk = float(chara['white_atk'])+1e-8
blue_atk = float(chara['blue_atk'])
atk_percent = blue_atk / white_atk
white_def = float(chara['white_def'])+1e-8
blue_def = float(chara['blue_def'])
def_percent = blue_def / white_def
special = float(chara['special'])
###----倍率区----
hp_mag = float(chara['hp_mag'])
atk_mag = float(chara['atk_mag'])
def_mag = float(chara['def_mag'])
special_mag = float(chara['special_mag'])
###----双暴区----
crit_rate = float(chara['crit_rate'])
crit_dmg = float(chara['crit_dmg'])
###----增伤区----
universal_boost = float(chara['universal_boost'])
if calculation == 'break' or calculation == 'superbreak':
    universal_boost=0.0
special_boost = float(chara['special_boost'])
boost = universal_boost + special_boost
###----抗性区----
res_ignore = float(chara['res_ignore'])
###----防御区----
def_ignore = float(chara['def_ignore'])
###----击破区----
break_effect = float(chara['break_effect'])
toughness_reduce = float(chara['toughness_reduce'])
break_mag = float(chara['break_mag'])
superbreak_mag = float(chara['superbreak_mag'])
##----敌人区----
###----基本数值区----
enermy_level = float(enermy['enermy_level'])
enermy_toughness = float(enermy['enermy_toughness'])
###----易伤区----
dmg_receive_universal_boost = float(enermy['dmg_receive_universal_boost'])
dmg_receive_special_boost = float(enermy['dmg_receive_special_boost'])
receive_boost = dmg_receive_universal_boost + dmg_receive_special_boost
###----防御区----
def_reduce = float(enermy['def_reduce'])
###----抗性区----
enermy_res = float(enermy['enermy_res'])
###----减伤区----
dmg_reduce = float(enermy['dmg_reduce'])
#----处理区----
if calculation=="normal":
    dmg = normal_dmg(chara_level,white_hp,hp_percent,hp_mag,white_atk,atk_percent,atk_mag,white_def,def_percent,def_mag,special,special_mag,crit_rate,crit_dmg,boost,res_ignore,def_ignore,enermy_level,enermy_res,receive_boost,def_reduce,dmg_reduce)
    uncrit,docrit = normal_dmg_crit(chara_level,white_hp,hp_percent,hp_mag,white_atk,atk_percent,atk_mag,white_def,def_percent,def_mag,special,special_mag,crit_rate,crit_dmg,boost,res_ignore,def_ignore,enermy_level,enermy_res,receive_boost,def_reduce,dmg_reduce)
    grad_dmg = numpy.array(autograd.grad(normal_dmg,argnum=(2,5,8,12,13,14,15,16,19,20))(chara_level,white_hp,hp_percent,hp_mag,white_atk,atk_percent,atk_mag,white_def,def_percent,def_mag,special,special_mag,crit_rate,crit_dmg,boost,res_ignore,def_ignore,enermy_level,enermy_res,receive_boost,def_reduce,dmg_reduce))
    dkeyword=['大生命','大攻击','大防御','暴击率','暴击伤害','增伤百分比','抗性穿透百分比','无视防御百分比','易伤百分比','减防百分比']
    print(f"期望伤害值为{dmg:.2f}")
    print(f"未暴击伤害值为{uncrit:.2f}")
    print(f"暴击伤害值为{docrit:.2f}")
    for i in range(len(dkeyword)):
        print(f"伤害值对{dkeyword[i]}的偏导为{grad_dmg[i]:.2f},意味着该项再提高10%能带来约{0.1*grad_dmg[i]/dmg*100:.2f}%的收益")
if calculation=="break":
    dmg = break_dmg(dmg_type,chara_level,break_effect,break_mag,boost,res_ignore,def_ignore,enermy_level,enermy_toughness,enermy_res,receive_boost,def_reduce,dmg_reduce)
    grad_dmg = numpy.array(autograd.grad(break_dmg,argnum=(2,4,5,6,10,11))(dmg_type,chara_level,break_effect,break_mag,boost,res_ignore,def_ignore,enermy_level,enermy_toughness,enermy_res,receive_boost,def_reduce,dmg_reduce))
    dkeyword=['击破特攻百分比','击破增伤百分比','抗性穿透百分比','无视防御百分比','易伤百分比','减防百分比']
    print(f"击破伤害值为{dmg:.2f}")
    for i in range(len(dkeyword)):
        print(f"伤害值对{dkeyword[i]}的偏导为{grad_dmg[i]:.2f},意味着该项再提高10%能带来约{0.1*grad_dmg[i]/dmg*100:.2f}%的收益")
if calculation=="superbreak":
    dmg = superbreak_dmg(chara_level,break_effect,toughness_reduce,superbreak_mag,boost,res_ignore,def_ignore,enermy_level,enermy_res, receive_boost,def_reduce,dmg_reduce)
    grad_dmg = numpy.array(autograd.grad(superbreak_dmg,argnum=(1,4,5,6,9,10))(chara_level,break_effect,toughness_reduce,superbreak_mag,boost,res_ignore,def_ignore,enermy_level,enermy_res, receive_boost,def_reduce,dmg_reduce))
    dkeyword=['击破特攻百分比','击破增伤百分比','抗性穿透百分比','无视防御百分比','易伤百分比','减防百分比']
    print(f"超击破伤害值为{dmg:.2f}")
    for i in range(len(dkeyword)):
        print(f"伤害值对{dkeyword[i]}的偏导为{grad_dmg[i]:.2f},意味着该项再提高10%能带来约{0.1*grad_dmg[i]/dmg*100:.2f}%的收益")
input("输入任意键结束...")
