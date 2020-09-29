# User input parameters
number_of_estates = 100
households_per_estate = 150
blocks_per_estate = 5
binstores_per_block = 1
recycling_bins_per_binstore = 2
rubbish_bins_per_binstore = 3
preFRP_collections_per_week = 1
capacity_per_bin = 1100
FRP_collections_per_week = 1
material_collections = 1

# Cost assumptions
signage_manufacture = 5
signage_design = 20
recycling_bin_sticker_manufacture = 6.5
recycling_bin_sticker_design = 60
recycling_bin_aperture_sticker_manufacture = 3
recycling_bin_aperture_sticker_design = 20
recycling_binstore_sign_post = 50
recycling_binstore_sign_wall = 50
recycling_binstore_sign_design = 60
rubbish_bin_sticker_manufacture = 5
rubbish_bin_sticker_design = 60
rubbish_binstore_sign_post = 55
rubbish_binstore_sign_wall = 55
rubbish_binstore_sign_design = 60
chute_sign_manufacture = 3.5
chute_sign_design = 20
noticeboard = 1
recycling_poster = 0.27
annual_leaflet_manufacture = 0.35
annual_leaflet_design = 250

daily_salary = 25000/220
officer_visit = 13.43

recycling_collection_cost = 16.26

# User input cost scenarios
high_costs = {
        'new_bins':{240:18.9,360:31.86,660:231.08,1100:245.24,1280:308},
        'refurb_bins':{240:18.9,360:31.86,660:69,1100:69,1280:69},
        'bin_rental':{240:6.3,360:10.6,660:46.2,1100:49,1280:61.6},
        'reverse_lid':20,
        'aperture':16,
        'bin_cleaning':16.8,
        'painting':500,
        'lighting':237.625,
        'initial_deepclean':75.25,
        'site_assessment':0.75,
        'stakeholder_engagement':0.75,
        'improvement_plan':0.3,
        'implementation_plan':0.3,
        'delivery_preparation':0.75,
        'FRP_rollout':0.75,
       }

average_costs = {'new_bins':{240:18.9,360:31.86,660:231.08,1100:245.24,1280:308},
        'refurb_bins':{240:18.9,360:31.86,660:69,1100:69,1280:69},
        'bin_rental':{240:6.3,360:10.6,660:46.2,1100:49,1280:61.6},
        'reverse_lid':20,
        'aperture':16,
        'bin_cleaning':13.43,
        'painting':300,
        'lighting':121.5,
        'initial_deepclean':37.625,
        'site_assessment':0.5,
        'stakeholder_engagement':0.5,
        'improvement_plan':0.2,
        'implementation_plan':0.2,
        'delivery_preparation':0.5,
        'FRP_rollout':0.5,
       }

low_costs = {'new_bins':{240:18.9,360:31.9,660:69,1100:69,1280:69},
        'refurb_bins':{240:18.9,360:31.9,660:69,1100:69,1280:69},
        'bin_rental':{240:6.3,360:10.6,660:13.8,1100:13.8,1280:13.8},
        'reverse_lid':20,
        'aperture':10,
        'bin_cleaning':10.0725,
        'painting':0,
        'lighting':0,
        'initial_deepclean':0,
        'site_assessment':0.375,
        'stakeholder_engagement':0.375,
        'improvement_plan':0.15,
        'implementation_plan':0.15,
        'delivery_preparation':0.375,
        'FRP_rollout':0.375,
       }

# Intermediate outputs
total_households = number_of_estates * households_per_estate
total_blocks = blocks_per_estate * number_of_estates
total_binstores = binstores_per_block * blocks_per_estate * number_of_estates
total_recycling_bins = recycling_bins_per_binstore * total_binstores
total_rubbish_bins = rubbish_bins_per_binstore * total_binstores
total_weekly_capacity = capacity_per_bin * total_recycling_bins * FRP_collections_per_week
bin_capacity_per_household = total_weekly_capacity/total_households

# Block costs
total_initial_block_costs = total_blocks * (chute_sign_manufacture + noticeboard + recycling_poster)

# Council costs (one-off)
total_initial_council_costs = signage_design + recycling_bin_sticker_design + recycling_bin_aperture_sticker_design + rubbish_bin_sticker_design + recycling_binstore_sign_design + rubbish_binstore_sign_design + chute_sign_design

# Household costs
total_ongoing_leaflet_manufacture = total_households * annual_leaflet_manufacture
total_additional_recycling_collection = total_households * (FRP_collections_per_week - preFRP_collections_per_week) * recycling_collection_cost

# Rubbish bin ongoing costs
total_ongoing_recycling_bin_sticker_costs = total_recycling_bins * (recycling_bin_sticker_manufacture + recycling_bin_aperture_sticker_manufacture)
total_ongoing_rubbish_bin_sticker_costs = rubbish_bin_sticker_manufacture * total_rubbish_bins

def calculate_costs(scenario):
    if scenario == 'high':
        ### SET-UP COSTS ###
        # Recycling bin set-up costs
        user_initial_refurb_costs = high_costs['new_bins'][capacity_per_bin]
        user_reverse_lid = high_costs['reverse_lid']
        user_aperture = high_costs['aperture']
        total_initial_recycling_bin_costs = total_recycling_bins * (user_initial_refurb_costs + user_reverse_lid + user_aperture)

        # Bin store set-up costs
        user_painting = high_costs['painting']
        user_lighting = high_costs['lighting']
        user_initial_deepclean = high_costs['initial_deepclean']
        total_initial_binstore_costs = total_binstores * (
            user_painting +
            user_lighting +
            user_initial_deepclean +
            signage_manufacture +
            recycling_binstore_sign_post +
            recycling_binstore_sign_wall +
            rubbish_binstore_sign_post +
            rubbish_binstore_sign_wall)

        # Council costs set-up (project management)
        total_project_mgt_cost = number_of_estates * daily_salary * (
                high_costs['site_assessment'] +
                high_costs['stakeholder_engagement'] +
                high_costs['improvement_plan'] +
                high_costs['implementation_plan'] +
                high_costs['delivery_preparation'] +
                high_costs['FRP_rollout'])

        total_borough_setup_costs = total_initial_recycling_bin_costs + total_initial_council_costs
        total_housing_provider_setup_costs = total_initial_binstore_costs + total_initial_block_costs + total_project_mgt_cost
        total_setup_costs = total_borough_setup_costs + total_housing_provider_setup_costs

        ### ONGOING COSTS ###
        # Bin store ongoing costs
        user_cleaning = high_costs['bin_cleaning']
        total_ongoing_binstore_costs = total_binstores * (user_cleaning * 52 + officer_visit * 12)

        # Recycling bin ongoing costs
        user_ongoing_refurb_costs = high_costs['refurb_bins'][capacity_per_bin]
        total_ongoing_refurb_costs = user_ongoing_refurb_costs * total_recycling_bins
        total_bin_rental_costs = high_costs['bin_rental'][capacity_per_bin] * total_recycling_bins

        total_borough_ongoing_costs = total_ongoing_refurb_costs + annual_leaflet_design - total_bin_rental_costs
        total_housing_provider_ongoing_costs = total_ongoing_binstore_costs + total_ongoing_leaflet_manufacture + total_additional_recycling_collection + total_bin_rental_costs + total_ongoing_recycling_bin_sticker_costs + total_ongoing_rubbish_bin_sticker_costs
        total_ongoing_costs = total_borough_ongoing_costs + total_housing_provider_ongoing_costs
        return total_setup_costs, total_ongoing_costs

    elif scenario == 'average':
        ### SET-UP COSTS ###
        # Recycling bin set-up costs
        user_initial_refurb_costs = average_costs['new_bins'][capacity_per_bin]
        user_reverse_lid = average_costs['reverse_lid']
        user_aperture = average_costs['aperture']
        total_initial_recycling_bin_costs = total_recycling_bins * (user_initial_refurb_costs + user_reverse_lid + user_aperture)

        # Bin store set-up costs
        user_painting = average_costs['painting']
        user_lighting = average_costs['lighting']
        user_initial_deepclean = average_costs['initial_deepclean']
        total_initial_binstore_costs = total_binstores * (
            user_painting +
            user_lighting +
            user_initial_deepclean +
            signage_manufacture +
            recycling_binstore_sign_post +
            recycling_binstore_sign_wall +
            rubbish_binstore_sign_post +
            rubbish_binstore_sign_wall)

        # Council costs set-up (project management)
        total_project_mgt_cost = number_of_estates * daily_salary * (
                average_costs['site_assessment'] +
                average_costs['stakeholder_engagement'] +
                average_costs['improvement_plan'] +
                average_costs['implementation_plan'] +
                average_costs['delivery_preparation'] +
                average_costs['FRP_rollout'])

        total_borough_setup_costs = total_initial_recycling_bin_costs + total_initial_council_costs
        total_housing_provider_setup_costs = total_initial_binstore_costs + total_initial_block_costs + total_project_mgt_cost
        total_setup_costs = total_borough_setup_costs + total_housing_provider_setup_costs

        ### ONGOING COSTS ###
        # Bin store ongoing costs
        user_cleaning = average_costs['bin_cleaning']
        total_ongoing_binstore_costs = total_binstores * (user_cleaning * 52 + officer_visit * 12)

        # Recycling bin ongoing costs
        user_ongoing_refurb_costs = average_costs['refurb_bins'][capacity_per_bin]
        total_ongoing_refurb_costs = user_ongoing_refurb_costs * total_recycling_bins
        total_bin_rental_costs = average_costs['bin_rental'][capacity_per_bin] * total_recycling_bins

        total_borough_ongoing_costs = total_ongoing_refurb_costs + annual_leaflet_design - total_bin_rental_costs
        total_housing_provider_ongoing_costs = total_ongoing_binstore_costs + total_ongoing_leaflet_manufacture + total_additional_recycling_collection + total_bin_rental_costs + total_ongoing_recycling_bin_sticker_costs + total_ongoing_rubbish_bin_sticker_costs
        total_ongoing_costs = total_borough_ongoing_costs + total_housing_provider_ongoing_costs
        return total_setup_costs, total_ongoing_costs

    else:
        ### SET-UP COSTS ###
        # Recycling bin set-up costs
        user_initial_refurb_costs = low_costs['new_bins'][capacity_per_bin]
        user_reverse_lid = low_costs['reverse_lid']
        user_aperture = low_costs['aperture']
        total_initial_recycling_bin_costs = total_recycling_bins * (user_initial_refurb_costs + user_reverse_lid + user_aperture)

        # Bin store set-up costs
        user_painting = low_costs['painting']
        user_lighting = low_costs['lighting']
        user_initial_deepclean = low_costs['initial_deepclean']
        total_initial_binstore_costs = total_binstores * (
            user_painting +
            user_lighting +
            user_initial_deepclean +
            signage_manufacture +
            recycling_binstore_sign_post +
            recycling_binstore_sign_wall +
            rubbish_binstore_sign_post +
            rubbish_binstore_sign_wall)

        # Council costs set-up (project management)
        total_project_mgt_cost = number_of_estates * daily_salary * (
                low_costs['site_assessment'] +
                low_costs['stakeholder_engagement'] +
                low_costs['improvement_plan'] +
                low_costs['implementation_plan'] +
                low_costs['delivery_preparation'] +
                low_costs['FRP_rollout'])

        total_borough_setup_costs = total_initial_recycling_bin_costs + total_initial_council_costs
        total_housing_provider_setup_costs = total_initial_binstore_costs + total_initial_block_costs + total_project_mgt_cost
        total_setup_costs = total_borough_setup_costs + total_housing_provider_setup_costs

        ### ONGOING COSTS ###
        # Bin store ongoing costs
        user_cleaning = low_costs['bin_cleaning']
        total_ongoing_binstore_costs = total_binstores * (user_cleaning * 52 + officer_visit * 12)

        # Recycling bin ongoing costs
        user_ongoing_refurb_costs = low_costs['refurb_bins'][capacity_per_bin]
        total_ongoing_refurb_costs = user_ongoing_refurb_costs * total_recycling_bins
        total_bin_rental_costs = low_costs['bin_rental'][capacity_per_bin] * total_recycling_bins

        total_borough_ongoing_costs = total_ongoing_refurb_costs + annual_leaflet_design - total_bin_rental_costs
        total_housing_provider_ongoing_costs = total_ongoing_binstore_costs + total_ongoing_leaflet_manufacture + total_additional_recycling_collection + total_bin_rental_costs + total_ongoing_recycling_bin_sticker_costs + total_ongoing_rubbish_bin_sticker_costs
        total_ongoing_costs = total_borough_ongoing_costs + total_housing_provider_ongoing_costs
        return total_setup_costs, total_ongoing_costs

import pandas as pd
df = pd.read_excel('Borough data.xlsx',sheet_name = 'London Boroughs specific',index_col=1)
df = df.drop(columns=['ECODE','Check','Unnamed: 22'])
df = df.dropna(subset=['FLAT_MAIS'])
borough_data = df.to_dict()

borough = 'Hackney'
high_reduction_residual_waste = {
    'recyclable_waste_uplift':0.3
}
average_reduction_residual_waste = {
    'recyclable_waste_uplift':0.2
}
low_reduction_residual_waste = {
    'recyclable_waste_uplift':0.1
}

high_reduction_contamination = {
    'impact_contamination':0.242
}
average_reduction_contamination = {
    'impact_contamination':0.076
}
low_reduction_contamination = {
    'impact_contamination':0
}

# Assumptions
emissions_intensity_waste_disposal = 406.84592
emissions_intensity_recycling = 21.38
scc = 0.06927866

landfill_disposal_fee = 113
efw_fee = 89
mdf_disposal_fee = 27
living_wage = 10.75

wtp_improvement_odour = 11.772591006424
wtp_improvement_litter = 135.038543897216
FRP_uplift_resident_experience = 0.1
wtp_recycling = 10.1/60

waste = {
    'food_drink_cans':{'share':0.029,'price':385},
    'glass':{'share':0.224,'price':10.5},
    'cartons':{'share':0.009,'price':275},
    'paper':{'share':0.231,'price':10},
    'cardboard':{'share':0.17,'price':60},
    'plastics':{'share':0.076,'price':115},
}

baseline_dry_recyclable_waste = borough_data['Flats (t/hh)'][borough]*1000
FRP_avoided_residual_waste = baseline_dry_recyclable_waste * high_reduction_residual_waste['recyclable_waste_uplift'] * total_households/1000
FRP_avoided_contaminated_material = baseline_dry_recyclable_waste * high_reduction_contamination['impact_contamination'] * total_households/1000

emissions_preFRP = emissions_intensity_waste_disposal * (FRP_avoided_residual_waste + FRP_avoided_contaminated_material)
counterfactual_emissions = emissions_intensity_recycling * (FRP_avoided_residual_waste + FRP_avoided_contaminated_material)
scc_diverted = (emissions_preFRP - counterfactual_emissions) * scc

sent_to_landfill_share = 6.9/(6.9+59.3)
sent_to_efw_share = 59.3/(6.9+59.3)
sent_to_landfill = sent_to_landfill_share * (FRP_avoided_residual_waste + FRP_avoided_contaminated_material)
sent_to_efw = sent_to_efw_share * (FRP_avoided_residual_waste + FRP_avoided_contaminated_material)

counterfactual_disposal_cost = mdf_disposal_fee * (sent_to_landfill + sent_to_efw)
additional_waste_disposal_cost = sent_to_landfill * landfill_disposal_fee + sent_to_efw * efw_fee - counterfactual_disposal_cost

cost_diverted_food_drink_cans = (FRP_avoided_residual_waste + FRP_avoided_contaminated_material) * waste['food_drink_cans']['share'] * waste['food_drink_cans']['price']
cost_diverted_glass = (FRP_avoided_residual_waste + FRP_avoided_contaminated_material) * waste['glass']['share'] * waste['glass']['price']
cost_diverted_cartons = (FRP_avoided_residual_waste + FRP_avoided_contaminated_material) * waste['cartons']['share'] * waste['cartons']['price']
cost_diverted_paper = (FRP_avoided_residual_waste + FRP_avoided_contaminated_material) * waste['paper']['share'] * waste['paper']['price']
cost_diverted_cardboard = (FRP_avoided_residual_waste + FRP_avoided_contaminated_material) * waste['cardboard']['share'] * waste['cardboard']['price']
cost_diverted_plastics = (FRP_avoided_residual_waste + FRP_avoided_contaminated_material) * waste['plastics']['share'] * waste['plastics']['price']
total_cost_diverted_material = cost_diverted_food_drink_cans + cost_diverted_glass + cost_diverted_cartons + cost_diverted_paper + cost_diverted_cardboard + cost_diverted_plastics

value_improvement_odour = wtp_improvement_odour * total_households * FRP_uplift_resident_experience
value_improvement_litter = wtp_improvement_litter * total_households * FRP_uplift_resident_experience
value_improvement_resident = value_improvement_odour + value_improvement_litter

direct_benefit = 52 * wtp_recycling * living_wage * high_reduction_residual_waste['recyclable_waste_uplift'] * total_households
total_benefit = direct_benefit + value_improvement_resident + total_cost_diverted_material + additional_waste_disposal_cost + scc_diverted
