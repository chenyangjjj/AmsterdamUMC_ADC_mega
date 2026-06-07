import pandas as pd 
import numpy as np 
from neuroCombat import neuroCombat
from colorama import Fore, Style
from datetime import datetime


# Note: This is a harmonization technique suitable only for cross-sectional data
# If there are follow-up measurements, please use longComBat R library for harmonization

# Get input:
# file path to xlsx file with clinical data. XLSX file should contain participant age (M_age), sex (Sex), and diagnosis (D_diagnosis).
clindata_path = '/Users/jiangxiaofan/Desktop/projects/project_ADC_copathology/data/MRI_scanner/clindata_path_data.xlsx'
# file path to xlsx file with mri data. XLSX file should contain all the regions to be harmonized
mridata_path = '/Users/jiangxiaofan/Desktop/projects/project_ADC_copathology/data/MRI_scanner/mridata_path_data.xlsx'

# output file path
today = datetime.now()
output_path = mridata_path[:-5] + '_harmonized_' + today.strftime('%Y%m%d') + '.xlsx'

# Load clinical data
clindata = pd.read_excel(clindata_path)
clindata_select = clindata[['MRI_ID', 'Sex', 'D_diagnosis', 'M_age','Edu']]  # select only data that is needed for harmonization

# Load MRI data
mridata = pd.read_excel(mridata_path)

# Merge clindata and mridata, based on MRI_ID
Dbl = clindata_select.merge(mridata, how='right')
print(Dbl)
Dbl = Dbl.rename({'Sex': 'Sex',
                  'D_diagnosis': 'Diagnosis',
                  'M_age': 'Age',
                  'Edu': 'Edu',
                  'Scanner': 'scanner',
                  'Field_Strength': 'field_strength',
                  'eTIV': 'eTIV'},
                 axis='columns')


# Harmonization is only needed for cortical thickness (aparc_thickness), areas (aparc_area) and subcortical volumes (aparc_stats)
# Lists with all columns that need harmonization, so all columns except for covariates.
list_biomarkers_cortthick_all = [
    'lh_bankssts_thickness','lh_caudalanteriorcingulate_thickness','lh_caudalmiddlefrontal_thickness',
    'lh_cuneus_thickness','lh_entorhinal_thickness','lh_fusiform_thickness','lh_inferiorparietal_thickness',
    'lh_inferiortemporal_thickness','lh_isthmuscingulate_thickness','lh_lateraloccipital_thickness',
    'lh_lateralorbitofrontal_thickness','lh_lingual_thickness','lh_medialorbitofrontal_thickness',
    'lh_middletemporal_thickness','lh_parahippocampal_thickness','lh_paracentral_thickness',
    'lh_parsopercularis_thickness','lh_parsorbitalis_thickness','lh_parstriangularis_thickness',
    'lh_pericalcarine_thickness','lh_postcentral_thickness','lh_posteriorcingulate_thickness','lh_precentral_thickness',
    'lh_precuneus_thickness','lh_rostralanteriorcingulate_thickness','lh_rostralmiddlefrontal_thickness',
    'lh_superiorfrontal_thickness','lh_superiorparietal_thickness','lh_superiortemporal_thickness',
    'lh_supramarginal_thickness','lh_frontalpole_thickness','lh_temporalpole_thickness',
    'lh_transversetemporal_thickness','lh_insula_thickness','lh_MeanThickness_thickness','rh_bankssts_thickness',
    'rh_caudalanteriorcingulate_thickness','rh_caudalmiddlefrontal_thickness','rh_cuneus_thickness',
    'rh_entorhinal_thickness','rh_fusiform_thickness','rh_inferiorparietal_thickness','rh_inferiortemporal_thickness',
    'rh_isthmuscingulate_thickness','rh_lateraloccipital_thickness','rh_lateralorbitofrontal_thickness',
    'rh_lingual_thickness','rh_medialorbitofrontal_thickness','rh_middletemporal_thickness',
    'rh_parahippocampal_thickness','rh_paracentral_thickness','rh_parsopercularis_thickness',
    'rh_parsorbitalis_thickness','rh_parstriangularis_thickness','rh_pericalcarine_thickness','rh_postcentral_thickness',
    'rh_posteriorcingulate_thickness','rh_precentral_thickness','rh_precuneus_thickness',
    'rh_rostralanteriorcingulate_thickness','rh_rostralmiddlefrontal_thickness','rh_superiorfrontal_thickness',
    'rh_superiorparietal_thickness','rh_superiortemporal_thickness','rh_supramarginal_thickness',
    'rh_frontalpole_thickness','rh_temporalpole_thickness','rh_transversetemporal_thickness','rh_insula_thickness','rh_MeanThickness_thickness']

list_biomarkers_grey_matter_all = [
    'lh_bankssts_volume','lh_caudalanteriorcingulate_volume','lh_caudalmiddlefrontal_volume',
    'lh_cuneus_volume','lh_entorhinal_volume','lh_fusiform_volume','lh_inferiorparietal_volume',
    'lh_inferiortemporal_volume','lh_isthmuscingulate_volume','lh_lateraloccipital_volume',
    'lh_lateralorbitofrontal_volume','lh_lingual_volume','lh_medialorbitofrontal_volume',
    'lh_middletemporal_volume','lh_parahippocampal_volume','lh_paracentral_volume',
    'lh_parsopercularis_volume','lh_parsorbitalis_volume','lh_parstriangularis_volume',
    'lh_pericalcarine_volume','lh_postcentral_volume','lh_posteriorcingulate_volume','lh_precentral_volume',
    'lh_precuneus_volume','lh_rostralanteriorcingulate_volume','lh_rostralmiddlefrontal_volume',
    'lh_superiorfrontal_volume','lh_superiorparietal_volume','lh_superiortemporal_volume',
    'lh_supramarginal_volume','lh_frontalpole_volume','lh_temporalpole_volume',
    'lh_transversetemporal_volume','lh_insula_volume','rh_bankssts_volume',
    'rh_caudalanteriorcingulate_volume','rh_caudalmiddlefrontal_volume','rh_cuneus_volume',
    'rh_entorhinal_volume','rh_fusiform_volume','rh_inferiorparietal_volume','rh_inferiortemporal_volume',
    'rh_isthmuscingulate_volume','rh_lateraloccipital_volume','rh_lateralorbitofrontal_volume',
    'rh_lingual_volume','rh_medialorbitofrontal_volume','rh_middletemporal_volume',
    'rh_parahippocampal_volume','rh_paracentral_volume','rh_parsopercularis_volume',
    'rh_parsorbitalis_volume','rh_parstriangularis_volume','rh_pericalcarine_volume','rh_postcentral_volume',
    'rh_posteriorcingulate_volume','rh_precentral_volume','rh_precuneus_volume',
    'rh_rostralanteriorcingulate_volume','rh_rostralmiddlefrontal_volume','rh_superiorfrontal_volume',
    'rh_superiorparietal_volume','rh_superiortemporal_volume','rh_supramarginal_volume',
    'rh_frontalpole_volume','rh_temporalpole_volume','rh_transversetemporal_volume','rh_insula_volume']

list_biomarkers_areas_all = [
    'lh_bankssts_area','lh_caudalanteriorcingulate_area','lh_caudalmiddlefrontal_area','lh_cuneus_area',
    'lh_entorhinal_area','lh_fusiform_area','lh_inferiorparietal_area','lh_inferiortemporal_area',
    'lh_isthmuscingulate_area','lh_lateraloccipital_area','lh_lateralorbitofrontal_area','lh_lingual_area','lh_medialorbitofrontal_area','lh_middletemporal_area','lh_parahippocampal_area','lh_paracentral_area','lh_parsopercularis_area','lh_parsorbitalis_area',
    'lh_parstriangularis_area','lh_pericalcarine_area','lh_postcentral_area','lh_posteriorcingulate_area','lh_precentral_area','lh_precuneus_area','lh_rostralanteriorcingulate_area','lh_rostralmiddlefrontal_area',
    'lh_superiorfrontal_area','lh_superiorparietal_area','lh_superiortemporal_area','lh_supramarginal_area','lh_frontalpole_area','lh_temporalpole_area','lh_transversetemporal_area','lh_insula_area',
    'rh_bankssts_area','rh_caudalanteriorcingulate_area','rh_caudalmiddlefrontal_area','rh_cuneus_area','rh_entorhinal_area','rh_fusiform_area','rh_inferiorparietal_area','rh_inferiortemporal_area','rh_isthmuscingulate_area',
    'rh_lateraloccipital_area','rh_lateralorbitofrontal_area','rh_lingual_area','rh_medialorbitofrontal_area','rh_middletemporal_area','rh_parahippocampal_area','rh_paracentral_area','rh_parsopercularis_area','rh_parsorbitalis_area',
    'rh_parstriangularis_area','rh_pericalcarine_area','rh_postcentral_area','rh_posteriorcingulate_area','rh_precentral_area','rh_precuneus_area','rh_rostralanteriorcingulate_area','rh_rostralmiddlefrontal_area','rh_superiorfrontal_area',
    'rh_superiorparietal_area','rh_superiortemporal_area','rh_supramarginal_area','rh_frontalpole_area','rh_temporalpole_area','rh_transversetemporal_area','rh_insula_area'
]

list_biomarkers_subcortvol_all_old = [
    'Left-Lateral-Ventricle','Left-Inf-Lat-Vent','Left-Cerebellum-White-Matter','Left-Cerebellum-Cortex','Left-Thalamus','Left-Caudate','Left-Putamen','Left-Pallidum',
    '3rd-Ventricle','4th-Ventricle','Brain-Stem','Left-Hippocampus','Left-Amygdala','CSF','Left-Accumbens-area','Left-VentralDC','Left-vessel','Left-choroid-plexus',
    'Right-Lateral-Ventricle','Right-Inf-Lat-Vent','Right-Cerebellum-White-Matter','Right-Cerebellum-Cortex','Right-Thalamus','Right-Caudate','Right-Putamen','Right-Pallidum',
    'Right-Hippocampus','Right-Amygdala','Right-Accumbens-area','Right-VentralDC','Right-vessel','Right-choroid-plexus','lhCerebralWhiteMatterVol','rhCerebralWhiteMatterVol',
    'SubCortGrayVol','TotalGrayVol','SupraTentorialVol','SupraTentorialVolNotVent']

list_biomarkers_subcortvol_all = [
    "Left.Thalamus_volume","Left.Caudate_volume","Left.Putamen_volume","Left.Pallidum_volume","Left.Hippocampus_volume", 
    "Left.Amygdala_volume","Left.Accumbens.area_volume","Left.choroid.plexus_volume","Left.WM.hypointensities_volume","Right.Thalamus_volume","Right.Caudate_volume",
    "Right.Putamen_volume","Right.Pallidum_volume","Right.Hippocampus_volume","Right.Amygdala_volume","Right.Accumbens.area_volume","Right.choroid.plexus_volume","Right.WM.hypointensities_volume"]

list_biomarkers_subcortvol_all = ["Left-Thalamus","Left-Caudate","Left-Putamen","Left-Pallidum","Left-Hippocampus","Left-Amygdala",
              "Left-Accumbens-area","Left-choroid-plexus",
              "Right-Thalamus","Right-Caudate","Right-Putamen","Right-Pallidum","Right-Hippocampus","Right-Amygdala","Right-Accumbens-area","Right-choroid-plexus"]


# Adjust the lists if your data only contains a subset of the variables. If your data contains all columns, no adjustment is needed and you can use the following:
list_biomarkers_cortthick = list_biomarkers_cortthick_all[:]
list_biomarkers_volume = list_biomarkers_grey_matter_all[:]
list_biomarkers_areas = list_biomarkers_areas_all[:]
list_biomarkers_subcortvol = list_biomarkers_subcortvol_all[:]


def harmonization(Dbl, list_biomarkers, categorical_cols, batch_col, continuous_cols):
    # Removes all participants with even 1 region where the segmentation has failed.
    # If it removes too many, consider imputation (not data team's problem!)
    idx_na= Dbl[list_biomarkers].isna().any(axis=1)
    Dqa = Dbl[~idx_na].reset_index(drop=True)

    # Combines field strength and scanner into a single variable
    idx_remove= Dqa[['field_strength','scanner']].isna().any(axis=1)
    Dqa= Dqa[~idx_remove].reset_index(drop=True)
    Dqa['field_strength'] = np.round(Dqa['field_strength']*10)/10
    for i in range(Dqa.shape[0]):
        Dqa.loc[i, 'scanner'] = Dqa.loc[i, 'scanner'] + ' (' + str(Dqa.loc[i, 'field_strength']) + ')'

    # Prints the list of scanners and the number of participants in each scanner.
    # If there are any scanner with < 5 participants, removing them would be easier
    remove_scanners = []
    for s in list(set(Dqa['scanner'])):
        print(s,np.sum(Dqa['scanner'] == s))  # print list with scanners and number of participants
        if np.sum(Dqa['scanner'] == s) < 5:  # scanner with less than 5 participants
            remove_scanners.append(s)  # add scanner with <5 participants to list remove_scanners

    print(Fore.RED+ 'Scanners removed because of <5 participants: ')
    print(remove_scanners)
    print(Style.RESET_ALL)
    for scan in remove_scanners:
        Dqa = Dqa[Dqa['scanner'] != scan]  # remove participants with scanner in remove_scanners list

    # Dqa_select = Dqa[list_biomarkers]
    # check nans: print(Dqa_select.columns[Dqa_select.isna().any()].tolist())

    covar_cols = categorical_cols + [batch_col] + continuous_cols  # covariate columns

    covars = Dqa[covar_cols]  # covariates

    # Harmonization using neuroCombat function:
    data = np.transpose(Dqa[list_biomarkers].values)
    data_combat = neuroCombat(dat=data,
        covars = covars,
        batch_col = batch_col,
        categorical_cols = categorical_cols,
        continuous_cols = continuous_cols,
        eb = False,
        parametric = True)['data']

    Dqa[list_biomarkers] = np.transpose(data_combat)
    return Dqa  # return matrix with harmonized variables


# Standard covariates for harmonization: sex, diagnosis, scanner, age and intracranial volume
categorical_cols = ['Sex', 'Diagnosis']
batch_col = 'scanner'
continuous_cols_CT = ['Age','Edu']

# use function harmonization to harmonize cortical thickness, areas and subcortical volumes separately
print('\n' + Fore.YELLOW + 'Cortical thickness:' + Style.RESET_ALL)
Dqa_cortthick = harmonization(Dbl, list_biomarkers_cortthick, categorical_cols, batch_col, continuous_cols_CT)   # harmonize cortical thickness
# print('\n' + Fore.YELLOW + 'Areas:' + Style.RESET_ALL)
#Dqa_areas = harmonization(Dbl, list_biomarkers_areas, categorical_cols, batch_col, continuous_cols)  # harmonize areas

continuous_cols = ['Age','Edu',"eTIV"]  # in aseg_stats, intracranial volume is called EstimatedTotalIntraCranialVol instead of eTIV or eTIV_x
print('\n' + Fore.YELLOW + 'Subcortical volumes:' + Style.RESET_ALL)
Dqa_cortvol = harmonization(Dbl, list_biomarkers_volume, categorical_cols,batch_col,continuous_cols)  # harmonize subcortical volumes
Dqa_subcortvol = harmonization(Dbl, list_biomarkers_subcortvol, categorical_cols,batch_col,continuous_cols)  # harmonize subcortical volumes

# combine all
Dqa_tmp2 = Dqa_cortthick[['MRI_ID','Sex','Diagnosis','Age','scanner',"Edu"] + list_biomarkers_cortthick]
Dqa_temp = Dqa_tmp2.merge(Dqa_subcortvol[['MRI_ID','eTIV']+list_biomarkers_subcortvol],on='MRI_ID',how='outer')
Dqa_temp = Dqa_temp.merge(Dqa_cortvol[['MRI_ID'] + list_biomarkers_volume], on='MRI_ID', how='outer')  # NEW LINE

# if there were columns that didn't need to be harmonized (from aparc_meancurve, aparc_volume of wmparc_stats), add those columns again:
# list_biomarkers_other = [s for s in mridata.columns if ('_meancurve' in s or '_volume' in s or 'wm-' in s)] # columns that need to be added
# if len(list_biomarkers_other)==0:
#     Dqa = Dqa_temp
# else:
#     Dqa = Dqa_temp.merge(mridata[['MRI_ID']+list_biomarkers_other],on='MRI_ID',how='outer')

Dqa = Dqa_temp

# write to excel
Dqa.to_excel("/Users/jiangxiaofan/Desktop/projects/project_ADC_copathology/data/MRI_scanner/final_23_June2025.xlsx", index=False)
#print(Fore.YELLOW + 'Data saved in ' + output_path + Style.RESET_ALL)
