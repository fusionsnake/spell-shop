#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import re
from pathlib import Path

def extract_spell_info_from_filename(filename):
    """从文件名提取法术名称"""
    # 去掉.docx后缀
    name = filename.replace('.docx', '')
    # 去掉常见前缀
    prefixes = ['福利一：', '福利二：', '福利三：', '福利四：', '福利五：', '福利六：', '福利七：',
                '福利：', '小福利：', '特别福利', '端午福利：', '01、', '02、', '03、', '04、', '05、', '06、']
    for prefix in prefixes:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    return name.strip()

def categorize_spell(name):
    """根据法术名称分类"""
    name_lower = name.lower()
    
    # 财运类
    if any(k in name for k in ['财', '金', '银', '运', '富', '进库', '地库', '招财']):
        return '财运'
    # 雷法类
    if any(k in name for k in ['雷', '电', '霆', '震']):
        return '雷法'
    # 祈福类
    if any(k in name for k in ['福', '祈', '祝', '祭', '愿', '祷', '福旺', '新春']):
        return '祈福'
    # 驱邪类
    if any(k in name for k in ['禁', '驱', '除', '破', '收', '煞', '鬼', '邪', '退', '镇']):
        return '驱邪'
    # 护身类
    if any(k in name for k in ['护', '身', '挡', '封', '解', '赦', '压']):
        return '护身'
    # 五行类
    if any(k in name for k in ['五行', '八卦', '阴阳', '水', '火', '木', '金', '土']):
        return '五行'
    # 斗君/北斗类
    if any(k in name for k in ['斗', '星', '北斗', '南斗']):
        return '星斗'
    # 巫术类
    if '巫' in name:
        return '巫术'
    
    return '综合'

def determine_price(category):
    """根据分类定价"""
    prices = {
        '财运': 888,
        '雷法': 1288,
        '祈福': 666,
        '驱邪': 999,
        '护身': 777,
        '五行': 888,
        '星斗': 999,
        '巫术': 666,
        '综合': 666
    }
    return prices.get(category, 666)

def main():
    base_dir = Path("/Users/yuandianhui/Desktop/🗂️ 归档文件夹/松韵")
    output_file = "/Users/yuandianhui/Desktop/法术超市/spells_data.json"
    
    spells = []
    spell_id = 1
    
    # 遍历所有docx文件
    for docx_file in base_dir.rglob("*.docx"):
        # 跳过群聊记录和转写文件
        if "群聊记录" in docx_file.name or "转写" in docx_file.name:
            continue
            
        filename = docx_file.name
        spell_name = extract_spell_info_from_filename(filename)
        category = categorize_spell(spell_name)
        
        # 获取相对路径作为课程信息
        rel_path = docx_file.relative_to(base_dir)
        course = str(rel_path.parent).split('/')[0] if '/' in str(rel_path) else '其他'
        
        spell = {
            "id": spell_id,
            "name": spell_name,
            "category": category,
            "course": course,
            "price": determine_price(category),
            "file_path": str(docx_file),
            "description": f"{spell_name}，源自{course}，属于{category}类秘法。",
            "effects": get_effects_by_category(category),
            "difficulty": "中级" if category in ['雷法', '禁法'] else "初级"
        }
        
        spells.append(spell)
        spell_id += 1
    
    # 按分类排序
    spells.sort(key=lambda x: (x['category'], x['name']))
    
    # 保存JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(spells, f, ensure_ascii=False, indent=2)
    
    print(f"共提取 {len(spells)} 个法术")
    
    # 统计分类
    categories = {}
    for spell in spells:
        cat = spell['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n分类统计:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}个")
    
    return spells

def get_effects_by_category(category):
    """根据分类返回效果描述"""
    effects = {
        '财运': ['招财进宝', '开库纳财', '五鬼运财', '生意兴隆'],
        '雷法': ['驱邪镇煞', '护身辟邪', '治病消灾', '斩妖除魔'],
        '祈福': ['祈福纳祥', '增运旺宅', '平安顺遂', '心想事成'],
        '驱邪': ['驱邪避凶', '镇宅安神', '化解煞气', '清除晦气'],
        '护身': ['护身保命', '化解灾难', '逢凶化吉', '平安吉祥'],
        '五行': ['调和五行', '平衡阴阳', '改善运势', '趋吉避凶'],
        '星斗': ['星宿护佑', '改运转运', '化解灾厄', '增福延寿'],
        '巫术': ['通灵问事', '化解疑难', '增强灵力', '通达天地'],
        '综合': ['综合功效', '多效合一', '平衡调理', '趋福避祸']
    }
    return effects.get(category, effects['综合'])

if __name__ == "__main__":
    main()
