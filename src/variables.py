"""全專案變數定義：插件卡的 read/write 名單與地圖條件對照。"""

VARS = {
    'phase': ('string', 'start', '進度階段'),
    'note_read': ('boolean', False, '已讀便條'),
    'flavor_deduced': ('boolean', False, '已推理出初遇風味'),
    'spoon_taken': ('boolean', False, '已取得調酒匙'),
    'storage_pried': ('boolean', False, '已撬開儲藏室百葉窗'),
    'box_unlocked': ('boolean', False, '已解鎖臥室木盒'),
    'box_pass': ('string', '', '木盒輸入密碼'),
    'truth_known': ('boolean', False, '已得知病歷單真相'),
    'cocktail_mixed': ('boolean', False, '已調製晚霞'),
    'ending_choice': ('string', '', '終局抉擇'),
    'mem1': ('string', '', '回憶一進度'),
    'mem2': ('string', '', '回憶二進度'),
    'mem3': ('string', '', '回憶三進度'),
}

RPG_VARS = [
    ('hp', 'rpgHp', 'number', 100),
    ('bag', 'inventory', 'string', '[]'),
    ('equipment', 'rpgEquipment', 'string', '{}'),
    ('state', 'rpgState', 'string', ''),
    ('used', 'inventoryLastUsed', 'string', ''),
    ('count', 'inventoryCount', 'number', 0)
]


def project_variables():
    return ([{'id': k, 'name': k, 'label': lab, 'type': t, 'defaultValue': d} for k, (t, d, lab) in VARS.items()]
            + [{'id': i, 'name': n, 'label': n, 'type': t, 'defaultValue': d} for i, n, t, d in RPG_VARS])
