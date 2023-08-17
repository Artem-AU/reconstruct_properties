import json
import csv

# Open the JSON file
with open('82fc28f3cb6a9693151e6531e249d791.props_unzipped.json', 'r') as f:
    # Load the JSON data into a dictionary
    prop_dict = json.load(f)


# print(prop_dict.keys())

# print(type(prop_dict['Hierarchy']))


# PRINT HIERARCHY
# for attribute in prop_dict['Hierarchy']:
#     print(attribute)
#     if attribute == "objects":
#         for dict in prop_dict['Hierarchy'][attribute]:
#             for key, value in dict.items():
#                 if key == "objects":
#                     for item in value:
#                         print(type(item))
#                     # print(type(value))
#                 # print(key)
#             # print(type(dict))
#         # print(type(prop_dict['Hierarchy'][attribute]))
#         # print(prop_dict['Hierarchy'][attribute])  


# # PRINT PROPERTIES CATEGORIES
# for attribute in prop_dict['Attributes']:
#     if "category" in attribute.keys():
#         print(attribute["category"])


# PRINT PROPERTIES CATEGORIES + PROPERTY NAMES
def all_prop_list(prop_dict):
    # print('prop_dict:', prop_dict)
    prop_list = []
    if "Attributes" in prop_dict.keys():
        for attribute in prop_dict['Attributes']:
            if "displayName" in attribute.keys():
                prop_list.append(attribute["category"] + "." + attribute["displayName"])
    # print('props:', prop_list)
    return prop_list

# for item in all_prop_list(prop_dict):
#     print(item)


def get_attribute_id(selected_properties):
    attr_ids = []
    for attr in selected_properties:
        category, displayName = attr.split(".")
        for i, attribute in enumerate(prop_dict['Attributes']):
            if "category" in attribute.keys() and attribute["category"] == category and attribute["displayName"] == displayName:
                attr_ids.append(i)
                break
    return attr_ids


# print(get_attribute_id(["Element.IfcClass", "Element.IfcGUID"]))


def reconstruct_prop_dict(prop_dict, selected_properties):
    reconstruct_dict = {}
    for entity in prop_dict['Entities']:
        if isinstance(entity, dict):
            current_dict = reconstruct_dict
            for i, attr_id in enumerate(get_attribute_id(selected_properties)):
                if attr_id in entity["attributeIds"]:
                    index = entity["attributeIds"].index(attr_id)
                    value_id = entity["valueIds"][index]
                    value = prop_dict['Values'][value_id]
                    parent_key = value
                    if i == len(get_attribute_id(selected_properties)) - 1:
                        if parent_key in current_dict:
                            current_dict[parent_key].append(entity["id"])
                        else:
                            current_dict[parent_key] = [entity["id"]]
                    else:
                        if parent_key not in current_dict:
                            current_dict[parent_key] = {}
                        current_dict = current_dict[parent_key]
                else:
                    parent_key = "zz_NotFound"
                    if i == len(get_attribute_id(selected_properties)) - 1:
                        if parent_key in current_dict:
                            current_dict[parent_key].append(entity["id"])
                        else:
                            current_dict[parent_key] = [entity["id"]]
                    else:
                        if parent_key not in current_dict:
                            current_dict[parent_key] = {}
                        current_dict = current_dict[parent_key]
    return reconstruct_dict




reconstruct_hierarchy = ["Contractor_Attributes.C_PDS_SubzoneCode",
    "Contractor_Attributes.C_PDS_Subdiscipline", "IFC Type.IfcName [Type]"]
reconstruct_prop = reconstruct_prop_dict(
    prop_dict, reconstruct_hierarchy)

# # for key, item in reconstruct_prop.items():
# #     print(key)
# #     print(str(key) + ":" + str(item) + "\n\n")

import csv

def write_dict_to_csv(prop_dict, filename, headers):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header line to the CSV file
        writer.writerow(headers)
        # Call the recursive function to write the dictionary to the CSV file
        write_dict_recursive(prop_dict, writer)

def write_dict_recursive(data_dict, writer, keys=[], level=0):
    for key, value in data_dict.items():
        # Append the current key to the list of keys
        keys.append(key)
        # Write the keys to the CSV file with the appropriate level of indentation
        writer.writerow([''] * level + [key])
        # Check if the value is a dictionary
        if isinstance(value, dict):
            # If the value is a dictionary, call the recursive function with the value, the CSV writer object, the list of keys, and the incremented level parameter
            write_dict_recursive(value, writer, keys, level + 1)
        # Remove the current key from the list of keys
        keys.pop()

# headers = reconstruct_hierarchy
# write_dict_to_csv(reconstruct_prop, 'reconstruct_prop.csv', headers)