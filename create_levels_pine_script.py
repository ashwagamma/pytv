import json
import numpy as np

jsonn_mancini = json.load(open('sr_levels/mancini_es.json'))
levels_support = jsonn_mancini['levels_support']
levels_resistance = jsonn_mancini['levels_resistance']
labels_levels_support = jsonn_mancini['labels_levels_support']
labels_levels_resistance = jsonn_mancini['labels_levels_resistance']
labels_levels_support_lvltxt = jsonn_mancini['labels_levels_support_lvltxt']
labels_levels_resistance_lvltxt = jsonn_mancini['labels_levels_resistance_lvltxt']
ranges_support = jsonn_mancini['ranges_support']
ranges_resistance = jsonn_mancini['ranges_resistance']
labels_ranges_support = jsonn_mancini['labels_ranges_support']
labels_ranges_resistance = jsonn_mancini['labels_ranges_resistance']
labels_ranges_support_lvltxt = jsonn_mancini['labels_ranges_support_lvltxt']
labels_ranges_resistance_lvltxt = jsonn_mancini['labels_ranges_resistance_lvltxt']

ranges_support_0, ranges_support_1 = map(list, zip(*ranges_support))
ranges_resistance_0, ranges_resistance_1 = map(list, zip(*ranges_resistance))
labels_levels_support_joined = np.char.add(np.char.add("\"", labels_levels_support_lvltxt), np.char.add(" ", np.char.add(labels_levels_support, "\"")))
labels_levels_resistance_joined = np.char.add(np.char.add("\"", labels_levels_resistance_lvltxt), np.char.add(" ", np.char.add(labels_levels_resistance, "\"")))
labels_ranges_support_joined = np.char.add(np.char.add("\"", labels_ranges_support_lvltxt), np.char.add(" ", np.char.add(labels_ranges_support, "\"")))
labels_ranges_resistance_joined = np.char.add(np.char.add("\"", labels_ranges_resistance_lvltxt), np.char.add(" ", np.char.add(labels_ranges_resistance, "\"")))

pine_script = ""
pine_script = pine_script +"""int[] levels_support = array.from("""+",".join(map(str, levels_support))+""")\n"""
pine_script = pine_script +"""int[] ranges_support_0 = array.from("""+",".join(map(str, ranges_support_0))+""")\n"""
pine_script = pine_script +"""int[] ranges_support_1 = array.from("""+",".join(map(str, ranges_support_1))+""")\n"""
pine_script = pine_script +"""int[] levels_resistance = array.from("""+",".join(map(str, levels_resistance))+""")\n"""
pine_script = pine_script +"""int[] ranges_resistance_0 = array.from("""+",".join(map(str, ranges_resistance_0))+""")\n"""
pine_script = pine_script +"""int[] ranges_resistance_1 = array.from("""+",".join(map(str, ranges_resistance_1))+""")\n"""
pine_script = pine_script +"""string[] labels_support = array.from("""+",".join(map(str, labels_levels_support_joined))+""")\n"""
pine_script = pine_script +"""string[] labels_resistance = array.from("""+",".join(map(str, labels_levels_resistance_joined))+""")\n"""
pine_script = pine_script +"""string[] labels_ranges_support = array.from("""+",".join(map(str, labels_ranges_support_joined))+""")\n"""
pine_script = pine_script +"""string[] labels_ranges_resistance = array.from("""+",".join(map(str, labels_ranges_resistance_joined))+""")\n"""

jsonn_va = json.load(open('sr_levels/value_area_levels_es.json'))

pine_script = pine_script +"""int[] levels_va = array.from("""+",".join(map(str, jsonn_va['levels']))+""")\n"""
pine_script = pine_script +"""string[] labels_va = array.from("""+",".join(map(str, np.char.add("\"", np.char.add(jsonn_va['labels_levels'],"\""))))+""")\n"""


print(pine_script)
