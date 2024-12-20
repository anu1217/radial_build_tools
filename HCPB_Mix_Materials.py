import openmc
import json
import material_db_tools as mdbt

'''
This script specifies the composition of each HCPB component and its corresponding citation.
mdbt.mix_by_volume is called to mix individual materials and generate a new .json file.
'''

with open('PureFusionMaterials_libv1.json', 'r') as pure_mat_json:
    pure_mat = json.load(pure_mat_json)

mat_data = {}

#Volume fractions of constituent materials
material_comp = {
'fw_armor' : {"W": 1.00},
 'fw' : {"W": 0.1, "EUROFER97" : 0.9},
'breeder' : {"Li4SiO4Li60.0":0.65, "Li2TiO3Li60.0":0.35}, #need to convert mol% to vol%
'bw' : {"MF82H" : 0.8, "HeNIST" : 0.2},
'manifold_front_plate' : {"EUROFER97": 1.0},
'manifold' : {"HeT410P80": 1.00},
'manifold_back_plate' : {"HeT410P80": 1.00},
'hts_front_plate' : {"MF82H": 0.20, "HeNIST": 0.28, "BMF82H" : 0.52},
'hts': {"MF82H": 0.20, "HeNIST": 0.28, "BMF82H" : 0.52},
'hts_back_plate' : {"MF82H": 0.20, "HeNIST": 0.28, "BMF82H" : 0.52},
'vv_front_plate' : {"HeNIST" : 0.4, "Cr3FS" : 0.6}, #changed from SS316L in corresponding build_dict
'vv_fill' : {"HeNIST" : 0.4, "Cr3FS" : 0.6},
'vv_back_plate' : {"HeNIST" : 0.4, "Cr3FS" : 0.6}, #changed from SS316L in corresponding build_dict
'gap_2' : {"AirSTP": 1.0},
'lts_front_plate' : {"Cr3FS": 0.39, "BMF82H": 0.29, "Water": 0.32},
'lts' : {"Cr3FS": 0.39, "BMF82H": 0.29, "Water": 0.32},
'lts_back_plate' : {"Cr3FS": 0.39, "BMF82H": 0.29, "Water": 0.32},
'thermal_insulator' : {'AirSTP': 1.0},
'coil_pack_front_plate' : {"JK2LBSteel": 0.3, "Cu": 0.25, "TernaryNb3Sn" : 0.25, "Eins" : 0.1, "HeNIST" : 0.1},
'coil_pack' : {"JK2LBSteel": 0.3, "Cu": 0.25, "TernaryNb3Sn" : 0.25, "Eins" : 0.1, "HeNIST" : 0.1},
}

citation_list = {
    'fw_armor' : "ZhouEUDEMOHCPB_2023",
    'fw' : "ZhouEUDEMOHCPB_2023",
    'breeder' : "ZhouEUDEMOHCPB_2023",
    'bw' : "DavisFusEngDes_2018",
    'manifold_front_plate' : "DavisFusEngDes_2018",
    'manifold' : "DavisFusEngDes_2018",
    'manifold_back_plate' : "DavisFusEngDes_2018",
    'hts_front_plate' : "DavisFusEngDes_2018",
    'hts' : "DavisFusEngDes_2018",
    'hts_back_plate' : "DavisFusEngDes_2018",
    'vv_front_plate' : "DavisFusEngDes_2018",
    'vv_fill' : "DavisFusEngDes_2018",
    'vv_back_plate' : "DavisFusEngDes_2018",
    'gap_2' : "ZhouEUDEMOHCPB_2023" ,
    'lts_front_plate' : "DavisFusEngDes_2018",
    'lts' : "DavisFusEngDes_2018",
    'lts_back_plate' : "DavisFusEngDes_2018",
    'thermal_insulator' : "ZhouEUDEMOHCPB_2023",
    'coil_pack_front_plate' : "DavisFusEngDes_2018",
    'coil_pack' : "DavisFusEngDes_2018",
    }

for mat_name, comp in material_comp.items():
    mat_data[mat_name] = {
              "vol_fracs": comp,
              "mixture_citation" : citation_list[mat_name],
          } 

# Load material library
mat_lib = mdbt.MaterialLibrary()
mat_lib.from_json("PureFusionMaterials_libv1.json")

# create material library object
mixmat_lib = mdbt.MaterialLibrary()
for mat_name, mat_input in mat_data.items():
        mixmat_lib[mat_name] = mdbt.mix_by_volume(
            mat_lib, mat_input["vol_fracs"], mat_input["mixture_citation"]
        )

# write HCPB material library
mixmat_lib.write_json("mixedPureFusionMatsHCPB_libv1.json")
