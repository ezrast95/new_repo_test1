# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyeds

######## 1. get datatypes ######## 
# added commant
result_file = "D:/ezra/compound_discoverer_analysis/pu_wild_emmer_ms2_with_acquireX/pos/pu_we_acquireX_pos.cdResult"
       

report = pyeds.Report(result_file)

# get all data types
for data_type in report.DataTypes:
    print(data_type)        


######## 2. get columns in datatypes ########   

# get specific data type
data_type = report.GetDataType("MassSpectrumItem")

# show all columns
for column in data_type.Columns:
    print(column.DisplayName)
    
# get column by name
print("")
print(data_type.GetColumn("Spectrum"))

# get columns by data purpose
print("")
for column in data_type.GetColumns("ResultItemDataPurpose/ElementalCompositionFormula"):
    print(column) 

######## 3. summary ########          
# open result file using the 'with' statement
with pyeds.Summary(result_file) as summary:
    
    # show full info
    summary.ShowAll()
    # show parametares in specific experiment per node in the workflow      
    summary.ShowWorkflows()  
        
######## 4. get specific information about data (that you got from sections 1-3) ########       
# open result file using the 'with' statement
with pyeds.EDS(result_file) as eds:

# count all items
    print(eds.Count("MassSpectrumItem"))
    
    # count filtered
    query = "MSOrder > 1"
    print(eds.Count("MassSpectrumItem", query=query))
    
# query = values defined by '[A-Za-z0-9-_\.%]+', single quotes,
# grouping by '()' and following operators
#     'AND | OR'
#     'IS NULL | IS NOT NULL'
#     'IN () | NOT IN ()'
#     '<= | >= | != | = | < | > | LIKE'.

######## 5. get specific data (that you got from sections 1-4) ######## 

# open result file using the 'with' statement
with pyeds.EDS(result_file) as eds:
    
    # read all items iterator
    items = eds.Read("MassSpectrumItem", query = "MSOrder > 1", limit = 1)
    MS2Spectrum = items.GetProperties("Spectrum")
    print(MS2Spectrum.RawValue)
  
# connect tandem-ms with mz,RT values from the compound table



######## 6. filter compounds table ######## 

eds = pyeds.EDS(result_file)
review = pyeds.Review(eds)

# open result file and review using the 'with' statement
with eds, review:
    
    # read scan info
    limits = 10
    path = ["ConsolidatedUnknownCompoundItem", "BestHitIonInstanceItem", "MassSpectrumInfoItem"]
    keep1 = ["ConsolidatedUnknownCompoundItem"]
    keep2 = ["MassSpectrumInfoItem"]
    properties = {"ConsolidatedUnknownCompoundItem":("ID", "RetentionTime", "MassOverCharge", "MolecularWeight", "Formula", "MaxArea"),"MassSpectrumInfoItem":("ID")}
    queries = {"ConsolidatedUnknownCompoundItem":"('RetentionTime' > 0.35 AND 'RetentionTime' < 17) AND ('MaxArea' >= 2E6)",
               "MassSpectrumInfoItem": "MSOrder > 1"}
    
    
    # filter spectra data
    filteredMSn = eds.ReadHierarchy(path, keep=keep2, queries=queries, properties=properties, limits=limits)
    
    # read msn spectra
    msnIds = [d.IDs for d in filteredMSn]
    spectraItems = eds.ReadMany("MassSpectrumItem", msnIds)
    msnCentroids = []
    for s in spectraItems:
        msnCentroids.append(s.Spectrum.Centroids)
    
    # filter compounds table    
    filteredCompounds = eds.ReadHierarchy(path, keep=keep1, queries=queries, properties=properties, limits=limits)
    for compound in filteredCompounds:
        # add custom values
        # item.AddValue(item.MolecularWeight+1.007276, "MZ [M+H]", align=3, template="{:.5f}")
        
        # insert item
        # review.InsertItem(item, hide=['ID'])
        review.InsertItem(compound)
        
# show review
review.Show() 
    











