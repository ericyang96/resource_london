import pandas as pd
import csv
import os
import xlsxwriter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CalculatorForm, DownloadForm
from django.http import HttpResponse


df = pd.read_excel('Borough data.xlsx',sheet_name = 'London Boroughs specific',index_col=1)
df = df.drop(columns=['ECODE','Check','Unnamed: 22'])
df = df.dropna(subset=['FLAT_MAIS'])
borough_data = df.to_dict()

scenario_benefits = {
	'high':{
		'recyclable_waste_uplift':0.39,
		'impact_contamination':0.46
	},
	'average':{
		'recyclable_waste_uplift':0.26,
		'impact_contamination':0.24
	},
	'low':{
		'recyclable_waste_uplift':0.16,
		'impact_contamination':0
	}
}

sent_to_landfill_share = 6.9/(6.9+59.3)
sent_to_efw_share = 59.3/(6.9+59.3)

residual_waste_disposal = {
 	'mixed':{'emissions_intensity':407,'cost':130},
	'landfill':{'emissions_intensity':586,'cost':175},
	'efw':{'emissions_intensity':386,'cost':125}
}

landfill_disposal_fee = 113
efw_fee = 89

CO2_emissions_recycling = 21.38

# Cost assumptions
signage_manufacture = 5
signage_design = 20
recycling_bin_sticker_manufacture = 6.5
recycling_bin_sticker_design = 60
recycling_bin_aperture_sticker_manufacture = 3
recycling_bin_aperture_sticker_design = 20
recycling_binstore_sign_post = 100
recycling_binstore_sign_wall = 50
recycling_binstore_sign_design = 105
rubbish_bin_sticker_manufacture = 5
rubbish_bin_sticker_design = 60
rubbish_binstore_sign_post = 105
rubbish_binstore_sign_wall = 55
rubbish_binstore_sign_design = 60
chute_sign_manufacture = 3.5
chute_sign_design = 20
noticeboard = 50
recycling_poster = 0.27
annual_leaflet_manufacture = 0.35
annual_leaflet_design = 250
daily_salary = 25000/220
rubbish_collection_cost = 16.26
recycling_collection_cost = 16.26

scenario_costs = {
		'high':{
		        'new_bins':{240:21.09,360:34,660:254.98,1100:274.52,1280:336.68},
		        'refurb_bins':{240:21.09,360:34,660:69,1100:69,1280:69},
		        'bin_rental':{240:100*240/1100,360:100*360/1100,660:100*660/1100.2,1100:100,1280:100*1280/1100},
		        'reverse_lid':20,
		        'aperture':16,
		        'bin_cleaning':13.9,
		        'painting':500,
		        'lighting':237.625,
		        'initial_deepclean':75.25,
		        'site_assessment':0.75,
		        'stakeholder_engagement':0.75,
		        'improvement_plan':0.3,
		        'implementation_plan':0.3,
		        'delivery_preparation':0.75,
		        'FRP_rollout':0.75,
				'installation':1,
				'officer_visit':17.3745
		},
		'med-high':{
		        'new_bins':{240:21.09,360:34,660:254.98,1100:274.52,1280:336.68},
		        'refurb_bins':{240:21.09,360:34,660:69,1100:69,1280:69},
		        'bin_rental':{240:100*240/1100,360:100*360/1100,660:100*660/1100.2,1100:100,1280:100*1280/1100},
		        'reverse_lid':20,
		        'aperture':16,
		        'bin_cleaning':13.9,
		        'painting':400,
		        'lighting':180,
		        'initial_deepclean':56,
		        'site_assessment':0.625,
		        'stakeholder_engagement':0.625,
		        'improvement_plan':0.25,
		        'implementation_plan':0.25,
		        'delivery_preparation':0.625,
		        'FRP_rollout':0.625,
				'installation':0.75,
				'officer_visit':15.63705
		},
		'average': {
				'new_bins':{240:21.09,360:34,660:254.98,1100:274.52,1280:336.68},
		        'refurb_bins':{240:21.09,360:34,660:69,1100:69,1280:69},
		        'bin_rental':{240:100*240/1100,360:100*360/1100,660:100*660/1100.2,1100:100,1280:100*1280/1100},
		        'reverse_lid':20,
		        'aperture':16,
		        'bin_cleaning':13.9,
		        'painting':300,
		        'lighting':121.5,
		        'initial_deepclean':37.625,
		        'site_assessment':0.5,
		        'stakeholder_engagement':0.5,
		        'improvement_plan':0.2,
		        'implementation_plan':0.2,
		        'delivery_preparation':0.5,
		        'FRP_rollout':0.5,
				'installation':0.5,
				'officer_visit':13.8996
		},
		'med-low':{
		        'new_bins':{240:21.09,360:34,660:69,1100:69,1280:69},
		        'refurb_bins':{240:21.09,360:34,660:69,1100:69,1280:69},
		        'bin_rental':{240:100*240/1100,360:100*360/1100,660:100*660/1100.2,1100:100,1280:100*1280/1100},
		        'reverse_lid':20,
		        'aperture':16,
		        'bin_cleaning':13.9,
		        'painting':500,
		        'lighting':237.625,
		        'initial_deepclean':75.25,
		        'site_assessment':0.375,
		        'stakeholder_engagement':0.375,
		        'improvement_plan':0.15,
		        'implementation_plan':0.15,
		        'delivery_preparation':0.375,
		        'FRP_rollout':0.375,
				'installation':0.375,
				'officer_visit':12.16215
		},
		'low':{
				'new_bins':{240:21.09,360:34,660:69,1100:69,1280:69},
		        'refurb_bins':{240:21.09,360:34,660:69,1100:69,1280:69},
		        'bin_rental':{240:100*240/1100,360:100*360/1100,660:100*660/1100.2,1100:100,1280:100*1280/1100},
		        'reverse_lid':20,
		        'aperture':10,
		        'bin_cleaning':13.9,
		        'painting':0,
		        'lighting':0,
		        'initial_deepclean':0,
		        'site_assessment':0.375,
		        'stakeholder_engagement':0.375,
		        'improvement_plan':0.15,
		        'implementation_plan':0.15,
		        'delivery_preparation':0.375,
		        'FRP_rollout':0.375,
				'installation':0.25,
				'officer_visit':10.4247
		}

}

# Assumptions (Benefits)
emissions_intensity_waste_disposal = 406.84592
emissions_intensity_recycling = 21.38
scc = 0.06927866


living_wage = 10.75

wtp_improvement_odour = 11.772591006424
wtp_improvement_litter = 135.038543897216
FRP_uplift_resident_experience = 0.1
wtp_recycling = 10.1/60

waste = {
    'food_drink_cans':{'share':0.029,'price':100},
    'glass':{'share':0.224,'price':10},
    'cartons':{'share':0.009,'price':275},
    'paper':{'share':0.231,'price':20},
    'cardboard':{'share':0.17,'price':60},
    'plastics':{'share':0.076,'price':100},
}


def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('../accounts/login')

    else:
        f = UserCreationForm()

    return render(request, 'register.html', {'form': f})

def calculatorform(request):
	#if form is submitted
	if request.method == 'POST':
		form = CalculatorForm(request.POST)

		#checking the form is valid or not
		if form.is_valid():
			borough = form.cleaned_data.get('borough')
			user_type = form.cleaned_data.get('user_type')
			number_of_estates = form.cleaned_data['number_of_estates']
			households_per_estate = form.cleaned_data['households_per_estate']
			setup_cost_scenario = form.cleaned_data['setup_cost_scenario']
			ongoing_cost_scenario = form.cleaned_data['ongoing_cost_scenario']
			diverted_waste_benefit_scenario = form.cleaned_data['diverted_waste_benefit_scenario']
			reduced_contamination_benefit_scenario = form.cleaned_data['reduced_contamination_benefit_scenario']
			number_of_estates = form.cleaned_data['number_of_estates']
			households_per_estate = form.cleaned_data['households_per_estate']
			binstores_per_block = form.cleaned_data['binstores_per_block']
			blocks_per_estate = form.cleaned_data['blocks_per_estate']
			recycling_bins_per_binstore = form.cleaned_data['recycling_bins_per_binstore']
			rubbish_bins_per_binstore = form.cleaned_data['rubbish_bins_per_binstore']
			capacity_per_bin = form.cleaned_data['capacity_per_bin']
			preFRP_collections_per_week = form.cleaned_data['preFRP_collections_per_week']
			FRP_collections_per_week = form.cleaned_data['FRP_collections_per_week']
			material_collections = form.cleaned_data['material_collections']
			preFRP_recycling_bins_per_binstore = form.cleaned_data['preFRP_recycling_bins_per_binstore']
			residual_waste_disposal_method = form.cleaned_data['residual_waste_disposal_method']
			bin_purchase_maintenance_agent = form.cleaned_data['bin_purchase_maintenance_agent']
			bin_rental_housing_provider = form.cleaned_data['bin_rental_housing_provider']
			binstore_refurb_agent = form.cleaned_data['binstore_refurb_agent']
			stickers_posters_signage_agent = form.cleaned_data['stickers_posters_signage_agent']
			stickers_posters_signage_design_agent = form.cleaned_data['stickers_posters_signage_agent']
			project_management_agent = form.cleaned_data['project_management_agent']
			cleaning_agent = form.cleaned_data['cleaning_agent']
			inspections_agent = form.cleaned_data['inspections_agent']
			additional_collections_agent = form.cleaned_data['additional_collections_agent']

			# Optional assumptions
			preFRP_dry_recycling_volume = form.cleaned_data.get('preFRP_dry_recycling_volume')
			if preFRP_dry_recycling_volume is None:
				preFRP_recycling_waste = borough_data['Household - waste sent for recycling-composting-reuse (tonnes)'][form.cleaned_data['borough']]
			else:
				preFRP_recycling_waste = preFRP_dry_recycling_volume

			preFRP_waste_volume = form.cleaned_data.get('preFRP_waste_volume')
			if preFRP_waste_volume is None:
				preFRP_total_waste = borough_data['Household - total waste (tonnes)'][form.cleaned_data['borough']]
			else:
				preFRP_total_waste = preFRP_waste_volume


			baseline_dry_recyclable_waste = borough_data['Flats (t/hh)'][form.cleaned_data['borough']] * 1000

			residual_waste_disposal_costs = form.cleaned_data.get('residual_waste_disposal')
			if residual_waste_disposal_costs is None:
				borough_residual_waste_disposal_costs = residual_waste_disposal[form.cleaned_data['residual_waste_disposal_method']]['cost']
			else:
				borough_residual_waste_disposal_costs = residual_waste_disposal_costs

			recycling_waste_disposal_costs = form.cleaned_data.get('recycling_waste_disposal_costs')
			if recycling_waste_disposal_costs is None:
				mdf_disposal_fee = 18
			else:
				mdf_disposal_fee = recycling_waste_disposal_costs
			contamination_waste_disposal_costs = form.cleaned_data.get('contamination_waste_disposal_costs')
			if contamination_waste_disposal_costs is None:
				contamination_cost = 176
			else:
				contamination_cost = contamination_waste_disposal_costs

			# Intermediate calculations
			total_households = form.cleaned_data['number_of_estates'] * form.cleaned_data['households_per_estate']
			total_blocks = form.cleaned_data['blocks_per_estate'] * form.cleaned_data['number_of_estates']
			total_binstores = form.cleaned_data['binstores_per_block'] * form.cleaned_data['blocks_per_estate'] * form.cleaned_data['number_of_estates']
			total_recycling_bins = form.cleaned_data['recycling_bins_per_binstore'] * total_binstores
			total_rubbish_bins = form.cleaned_data['rubbish_bins_per_binstore'] * total_binstores
			total_weekly_capacity = form.cleaned_data['capacity_per_bin'] * total_recycling_bins * form.cleaned_data['FRP_collections_per_week']
			bin_capacity_per_household = total_weekly_capacity/total_households

			### SETUP COSTS ###

			# Setup costs per recycling bin
			user_initial_refurb_costs = scenario_costs[form.cleaned_data['setup_cost_scenario']]['new_bins'][form.cleaned_data['capacity_per_bin']]
			user_reverse_lid = scenario_costs[form.cleaned_data['setup_cost_scenario']]['reverse_lid']
			user_aperture = scenario_costs[form.cleaned_data['setup_cost_scenario']]['aperture']

	        # Setup costs per bin store
			user_painting = scenario_costs[form.cleaned_data['setup_cost_scenario']]['painting']
			user_lighting = scenario_costs[form.cleaned_data['setup_cost_scenario']]['lighting']
			user_initial_deepclean = scenario_costs[form.cleaned_data['setup_cost_scenario']]['initial_deepclean']

        	# Council costs set-up (project management)
			total_project_mgt_cost = form.cleaned_data['number_of_estates'] * daily_salary * (
                scenario_costs[form.cleaned_data['setup_cost_scenario']]['site_assessment'] +
                scenario_costs[form.cleaned_data['setup_cost_scenario']]['stakeholder_engagement'] +
                scenario_costs[form.cleaned_data['setup_cost_scenario']]['improvement_plan'] +
                scenario_costs[form.cleaned_data['setup_cost_scenario']]['implementation_plan'] +
                scenario_costs[form.cleaned_data['setup_cost_scenario']]['delivery_preparation'] +
                scenario_costs[form.cleaned_data['setup_cost_scenario']]['FRP_rollout'] + scenario_costs[form.cleaned_data['setup_cost_scenario']]['installation'])

			setup_cost_assignment = {
				'total_setup_recycling_bin':{
					'agent':form.cleaned_data['bin_purchase_maintenance_agent'],
					'value':user_initial_refurb_costs * total_recycling_bins
				},
				'total_setup_reverse_lid':{
					'agent':form.cleaned_data['bin_purchase_maintenance_agent'],
					'value': user_reverse_lid * total_recycling_bins
				},
				'total_setup_aperture':{
					'agent':form.cleaned_data['bin_purchase_maintenance_agent'],
					'value':user_aperture * total_recycling_bins
				},
				'total_setup_painting':{
					'agent':form.cleaned_data['binstore_refurb_agent'],
					'value':user_painting * total_binstores
				},
				'total_setup_lighting':{
					'agent':form.cleaned_data['binstore_refurb_agent'],
					'value':user_lighting * total_binstores
				},
				'total_setup_initial_deepclean':{
					'agent':form.cleaned_data['binstore_refurb_agent'],
					'value':user_initial_deepclean * total_binstores
				},
				'total_setup_binstore_signage':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':signage_manufacture * total_binstores
				},
				'total_setup_recycling_binstore_sign_post':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':recycling_binstore_sign_post * total_binstores
				},
				'total_setup_recycling_binstore_sign_wall':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':recycling_binstore_sign_wall * total_binstores
				},
				'total_setup_rubbish_binstore_sign_post':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':rubbish_binstore_sign_post * total_binstores
				},
				'total_setup_rubbish_binstore_sign_wall':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':rubbish_binstore_sign_wall * total_binstores
				},
				'total_setup_block_costs':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':total_blocks * (chute_sign_manufacture + noticeboard + recycling_poster)
				},
				'total_setup_communications_design':{
					'agent':form.cleaned_data['stickers_posters_signage_design_agent'],
					'value':signage_design + recycling_bin_sticker_design + recycling_bin_aperture_sticker_design + rubbish_bin_sticker_design + recycling_binstore_sign_design + rubbish_binstore_sign_design + chute_sign_design
				},
				'total_project_mgt':{
					'agent':form.cleaned_data['project_management_agent'],
					'value':total_project_mgt_cost
				},
			}

			total_borough_setup_costs = sum(d['value'] for d in setup_cost_assignment.values() if d['agent'] == 'london_borough')
			total_housing_provider_setup_costs = sum(d['value'] for d in setup_cost_assignment.values() if d['agent'] == 'housing_provider')
			total_setup_costs = total_borough_setup_costs + total_housing_provider_setup_costs

			### ONGOING COSTS ###
			user_cleaning = scenario_costs[form.cleaned_data['ongoing_cost_scenario']]['bin_cleaning']
			total_bin_rental_costs = scenario_costs[form.cleaned_data['ongoing_cost_scenario']]['bin_rental'][form.cleaned_data['capacity_per_bin']] * total_binstores * (form.cleaned_data['recycling_bins_per_binstore'] - form.cleaned_data['preFRP_recycling_bins_per_binstore'])
			if form.cleaned_data['bin_rental_housing_provider'] == 'yes':
				borough_bin_rental_costs = -total_bin_rental_costs
				housing_provider_bin_rental_costs = total_bin_rental_costs
			else:
				borough_bin_rental_costs = total_bin_rental_costs
				housing_provider_bin_rental_costs = -total_bin_rental_costs

			ongoing_cost_assignment = {
				'total_ongoing_cleaning_costs':{
					'agent':form.cleaned_data['cleaning_agent'],
					'value':total_binstores * user_cleaning * 52,
					'year':1
				},
				'total_ongoing_inspection_costs':{
					'agent':form.cleaned_data['inspections_agent'],
					'value':total_binstores * scenario_costs[form.cleaned_data['ongoing_cost_scenario']]['officer_visit'] * 12,
					'year':1
				},
				'total_ongoing_leaflet_manufacture':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':total_households * annual_leaflet_manufacture,
					'year':1
				},
				'total_additional_recycling_collection':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':total_households * (form.cleaned_data['FRP_collections_per_week'] - form.cleaned_data['preFRP_collections_per_week']) * recycling_collection_cost,
					'year':1
				},
				'total_ongoing_refurb_costs':{
					'agent':form.cleaned_data['bin_purchase_maintenance_agent'],
					'value':total_recycling_bins * scenario_costs[form.cleaned_data['ongoing_cost_scenario']]['refurb_bins'][form.cleaned_data['capacity_per_bin']],
					'year':5
				},
				'total_ongoing_recycling_bin_sticker_costs':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':total_recycling_bins * (recycling_bin_sticker_manufacture + recycling_bin_aperture_sticker_manufacture),
					'year':1
				},
				'total_ongoing_rubbish_bin_sticker_costs':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':rubbish_bin_sticker_manufacture * total_rubbish_bins,
					'year':1
				},
				'total_annual_leaflet_design':{
					'agent':form.cleaned_data['stickers_posters_signage_design_agent'],
					'value':annual_leaflet_design,
					'year':1
				},
				'total_bin_rental_costs_borough':{
					'agent':'london_borough',
					'value':borough_bin_rental_costs,
					'year':1
				},
				'total_bin_rental_costs_housing_provider':{
					'agent':'housing_provider',
					'value':housing_provider_bin_rental_costs,
					'year':1
				},
			}

			year1_total_ongoing_costs_london_borough = sum(d['value'] for d in ongoing_cost_assignment.values() if (d['agent'] == 'london_borough' and d['year'] == 1))
			year1_total_ongoing_costs_housing_provider = sum(d['value'] for d in ongoing_cost_assignment.values() if (d['agent'] == 'housing_provider' and d['year'] == 1))
			year5_total_ongoing_costs_london_borough = sum(d['value'] for d in ongoing_cost_assignment.values() if (d['agent'] == 'london_borough' and d['year'] == 5)) + year1_total_ongoing_costs_london_borough
			year5_total_ongoing_costs_housing_provider = sum(d['value'] for d in ongoing_cost_assignment.values() if (d['agent'] == 'housing_provider' and d['year'] == 5)) + year1_total_ongoing_costs_housing_provider

			year0_total_ongoing_costs_london_borough = year5_total_ongoing_costs_london_borough - ongoing_cost_assignment['total_bin_rental_costs_borough']['value']
			year0_total_ongoing_costs_housing_provider = year5_total_ongoing_costs_housing_provider - ongoing_cost_assignment['total_bin_rental_costs_housing_provider']['value']
			year1_total_ongoing_costs = year1_total_ongoing_costs_london_borough + year1_total_ongoing_costs_housing_provider
			year5_total_ongoing_costs = year5_total_ongoing_costs_london_borough + year5_total_ongoing_costs_housing_provider

			### BENEFITS ###
			recyclable_waste_uplift_parameter = scenario_benefits[form.cleaned_data['diverted_waste_benefit_scenario']]['recyclable_waste_uplift']
			contamination_reduction_parameter = scenario_benefits[form.cleaned_data['reduced_contamination_benefit_scenario']]['impact_contamination']

			FRP_avoided_residual_waste = baseline_dry_recyclable_waste * recyclable_waste_uplift_parameter * total_households/1000
			FRP_avoided_contaminated_material = baseline_dry_recyclable_waste * contamination_reduction_parameter * total_households/1000

			emissions_preFRP = emissions_intensity_waste_disposal * (FRP_avoided_residual_waste + FRP_avoided_contaminated_material)
			counterfactual_emissions = emissions_intensity_recycling * (FRP_avoided_residual_waste + FRP_avoided_contaminated_material)
			scc_diverted = (emissions_preFRP - counterfactual_emissions) * scc

			additional_waste_disposal_cost = total_households * ((borough_residual_waste_disposal_costs - mdf_disposal_fee) * recyclable_waste_uplift_parameter * borough_data['Flats (t/hh)'][form.cleaned_data['borough']] + (contamination_cost - mdf_disposal_fee) * contamination_reduction_parameter * borough_data['Flats (t/hh)'][form.cleaned_data['borough']])

			reduced_residual_waste_collection_costs = (form.cleaned_data['preFRP_collections_per_week'] - form.cleaned_data['FRP_collections_per_week'])*rubbish_collection_cost*total_households

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

			direct_benefit = 52 * wtp_recycling * living_wage * scenario_benefits[form.cleaned_data['diverted_waste_benefit_scenario']]['recyclable_waste_uplift'] * total_households
			value_improvement_resident_total = value_improvement_resident + direct_benefit
			total_benefit = value_improvement_resident_total + total_cost_diverted_material + reduced_residual_waste_collection_costs  + additional_waste_disposal_cost + scc_diverted


			if form.cleaned_data['material_collections'] > 1:
				total_cost_diverted_material_adjustment = 1
			else:
				total_cost_diverted_material_adjustment = 0

			year0_netbenefit_london_borough = -total_borough_setup_costs - year0_total_ongoing_costs_london_borough + additional_waste_disposal_cost + total_cost_diverted_material * total_cost_diverted_material_adjustment
			year0_netbenefit_housing_provider = -total_housing_provider_setup_costs - year0_total_ongoing_costs_housing_provider
			year0_social_benefit = year0_netbenefit_london_borough + year0_netbenefit_housing_provider + total_cost_diverted_material + scc_diverted + value_improvement_resident_total

			year1_netbenefit_london_borough = -year1_total_ongoing_costs_london_borough + additional_waste_disposal_cost + total_cost_diverted_material * total_cost_diverted_material_adjustment
			year1_netbenefit_housing_provider = -year1_total_ongoing_costs_housing_provider
			year1_social_benefit = year1_netbenefit_london_borough + year1_netbenefit_housing_provider + total_cost_diverted_material + scc_diverted + value_improvement_resident_total

			year5_netbenefit_london_borough = -year5_total_ongoing_costs_london_borough + additional_waste_disposal_cost + total_cost_diverted_material * total_cost_diverted_material_adjustment
			year5_netbenefit_housing_provider = -year5_total_ongoing_costs_housing_provider
			year5_social_benefit = year5_netbenefit_london_borough + year5_netbenefit_housing_provider + total_cost_diverted_material + scc_diverted + value_improvement_resident_total

			total_netbenefit_london_borough = year0_netbenefit_london_borough + 8*year1_netbenefit_london_borough + 2*year5_netbenefit_london_borough
			total_netbenefit_housing_provider = year0_netbenefit_housing_provider + 8*year1_netbenefit_housing_provider + 2*year5_netbenefit_housing_provider
			total_netbenefit_society = year0_social_benefit + 8*year1_social_benefit + 2*year5_social_benefit

			test_cost = ongoing_cost_assignment['total_ongoing_refurb_costs']['value']

			# Key Performance Indicators
			preFRP_household_dry_recycling_rate = preFRP_recycling_waste/preFRP_total_waste
			FRP_household_dry_recycling_rate = (preFRP_recycling_waste + borough_data['Flats (t/hh)'][form.cleaned_data['borough']]*1000* scenario_benefits[form.cleaned_data['diverted_waste_benefit_scenario']]['recyclable_waste_uplift']*total_households/1000)/preFRP_total_waste
			dry_recycling_uplift = FRP_household_dry_recycling_rate - preFRP_household_dry_recycling_rate
			CO2_abated = (((borough_data['Flats (t/hh)'][form.cleaned_data['borough']]*1000)*(recyclable_waste_uplift_parameter+contamination_reduction_parameter))*total_households/1000)*(residual_waste_disposal[form.cleaned_data['residual_waste_disposal_method']]['emissions_intensity']-CO2_emissions_recycling)/1000
			dry_recycling_bin_capacity_treated_flats = form.cleaned_data['capacity_per_bin']*form.cleaned_data['FRP_collections_per_week']*total_recycling_bins/total_households

			borough_additional_net_benefit_per_householdyear = total_netbenefit_london_borough/(total_households * 10)
			housing_provider_additional_net_benefit_per_householdyear = total_netbenefit_housing_provider/(total_households * 10)
			society_net_benefit_per_householdyear = total_netbenefit_society/(total_households * 10)

			download_form = DownloadForm(initial={
                'borough': borough,
                'user_type': user_type,
				'households_per_estate':households_per_estate,
				'number_of_estates':number_of_estates,
				'blocks_per_estate':blocks_per_estate,
				'setup_cost_scenario':setup_cost_scenario,
				'ongoing_cost_scenario':ongoing_cost_scenario,
				'diverted_waste_benefit_scenario':diverted_waste_benefit_scenario,
				'reduced_contamination_benefit_scenario':reduced_contamination_benefit_scenario,
				'number_of_estates':number_of_estates,
				'households_per_estate':households_per_estate,
				'binstores_per_block':binstores_per_block,
				'blocks_per_estate':blocks_per_estate,
				'recycling_bins_per_binstore':recycling_bins_per_binstore,
				'rubbish_bins_per_binstore':rubbish_bins_per_binstore,
				'capacity_per_bin':capacity_per_bin,
				'preFRP_collections_per_week':preFRP_collections_per_week,
				'FRP_collections_per_week':FRP_collections_per_week,
				'material_collections':material_collections,
				'preFRP_recycling_bins_per_binstore':preFRP_recycling_bins_per_binstore,
				'residual_waste_disposal_method':residual_waste_disposal_method,
				'bin_purchase_maintenance_agent':bin_purchase_maintenance_agent,
				'bin_rental_housing_provider':bin_rental_housing_provider,
				'binstore_refurb_agent':binstore_refurb_agent,
				'stickers_posters_signage_agent':stickers_posters_signage_agent,
				'stickers_posters_signage_design_agent':stickers_posters_signage_agent,
				'project_management_agent':project_management_agent,
				'cleaning_agent':cleaning_agent,
				'inspections_agent':inspections_agent,
				'additional_collections_agent':additional_collections_agent,
				'preFRP_dry_recycling_volume': preFRP_dry_recycling_volume,
				'preFRP_waste_volume': preFRP_waste_volume,
				'residual_waste_disposal_costs': residual_waste_disposal_costs,
				'recycling_waste_disposal_costs': recycling_waste_disposal_costs,
				'contamination_waste_disposal_costs': contamination_waste_disposal_costs

            })
			context = {
				'baseline_dry_recyclable_waste':baseline_dry_recyclable_waste,
				'preFRP_dry_recycling_volume':preFRP_dry_recycling_volume,
				'preFRP_household_dry_recycling_rate':preFRP_household_dry_recycling_rate,
				'FRP_household_dry_recycling_rate':FRP_household_dry_recycling_rate,
				'dry_recycling_uplift':dry_recycling_uplift,
				'recyclable_waste_uplift_parameter':recyclable_waste_uplift_parameter,
				'contamination_reduction_parameter':contamination_reduction_parameter,
				'CO2_abated':CO2_abated,
				'reduced_residual_waste_collection_costs':reduced_residual_waste_collection_costs,
				'dry_recycling_bin_capacity_treated_flats':dry_recycling_bin_capacity_treated_flats,
				'scc_diverted':scc_diverted,
				'additional_waste_disposal_cost':additional_waste_disposal_cost,
				'total_cost_diverted_material':total_cost_diverted_material,
				'value_improvement_resident_total':value_improvement_resident_total,
				'total_benefit':total_benefit,
				'total_borough_setup_costs':total_borough_setup_costs,
				'total_housing_provider_setup_costs':total_housing_provider_setup_costs,
				'year0_total_ongoing_costs_london_borough':year0_total_ongoing_costs_london_borough,
				'year1_total_ongoing_costs_london_borough':year1_total_ongoing_costs_london_borough,
				'year5_total_ongoing_costs_london_borough':year5_total_ongoing_costs_london_borough,
				'year0_total_ongoing_costs_housing_provider':year0_total_ongoing_costs_housing_provider,
				'year1_total_ongoing_costs_housing_provider':year1_total_ongoing_costs_housing_provider,
				'year5_total_ongoing_costs_housing_provider':year5_total_ongoing_costs_housing_provider,
				'year0_netbenefit_london_borough':year0_netbenefit_london_borough,
				'year0_netbenefit_housing_provider':year0_netbenefit_housing_provider,
				'year0_social_benefit':year0_social_benefit,
				'year1_netbenefit_london_borough':year1_netbenefit_london_borough,
				'year1_netbenefit_housing_provider':year1_netbenefit_housing_provider,
				'year1_social_benefit':year1_social_benefit,
				'year5_netbenefit_london_borough':year5_netbenefit_london_borough,
				'year5_netbenefit_housing_provider':year5_netbenefit_housing_provider,
				'year5_social_benefit':year5_social_benefit,
				'total_netbenefit_london_borough':total_netbenefit_london_borough,
				'total_netbenefit_housing_provider':total_netbenefit_housing_provider,
				'total_netbenefit_society':total_netbenefit_society,
				'borough_additional_net_benefit_per_householdyear':borough_additional_net_benefit_per_householdyear,
				'housing_provider_additional_net_benefit_per_householdyear':housing_provider_additional_net_benefit_per_householdyear,
				'society_net_benefit_per_householdyear':society_net_benefit_per_householdyear,
				'download_form': download_form
				}
			return render(request, 'result.html/', context)

	else:
		#creating a new form
		form = CalculatorForm(
			initial={
				'households_per_estate':150,
				'blocks_per_estate':5,
				'binstores_per_block':1,
				'recycling_bins_per_binstore':2,
				'rubbish_bins_per_binstore':3,
			}
		)

	#returning form
	return render(request, 'calculator.html', {'form':form});

def download_data(request):
	try:
		assert request.method == 'POST'
		form = DownloadForm(request.POST)
		assert form.is_valid()
		# Optional assumptions
	except AssertionError:
	    error = 'Your request has some problems.'
	    contracts = error

	borough = form.cleaned_data.get('borough')
	user_type = form.cleaned_data.get('user_type')
	number_of_estates = form.cleaned_data['number_of_estates']
	households_per_estate = form.cleaned_data['households_per_estate']
	setup_cost_scenario = form.cleaned_data['setup_cost_scenario']
	ongoing_cost_scenario = form.cleaned_data['ongoing_cost_scenario']
	diverted_waste_benefit_scenario = form.cleaned_data['diverted_waste_benefit_scenario']
	reduced_contamination_benefit_scenario = form.cleaned_data['reduced_contamination_benefit_scenario']
	number_of_estates = form.cleaned_data['number_of_estates']
	households_per_estate = form.cleaned_data['households_per_estate']
	binstores_per_block = form.cleaned_data['binstores_per_block']
	blocks_per_estate = form.cleaned_data['blocks_per_estate']
	recycling_bins_per_binstore = form.cleaned_data['recycling_bins_per_binstore']
	rubbish_bins_per_binstore = form.cleaned_data['rubbish_bins_per_binstore']
	capacity_per_bin = form.cleaned_data['capacity_per_bin']
	preFRP_collections_per_week = form.cleaned_data['preFRP_collections_per_week']
	FRP_collections_per_week = form.cleaned_data['FRP_collections_per_week']
	material_collections = form.cleaned_data['material_collections']
	preFRP_recycling_bins_per_binstore = form.cleaned_data['preFRP_recycling_bins_per_binstore']
	residual_waste_disposal_method = form.cleaned_data['residual_waste_disposal_method']
	bin_purchase_maintenance_agent = form.cleaned_data['bin_purchase_maintenance_agent']
	bin_rental_housing_provider = form.cleaned_data['bin_rental_housing_provider']
	binstore_refurb_agent = form.cleaned_data['binstore_refurb_agent']
	stickers_posters_signage_agent = form.cleaned_data['stickers_posters_signage_agent']
	stickers_posters_signage_design_agent = form.cleaned_data['stickers_posters_signage_agent']
	project_management_agent = form.cleaned_data['project_management_agent']
	cleaning_agent = form.cleaned_data['cleaning_agent']
	inspections_agent = form.cleaned_data['inspections_agent']
	additional_collections_agent = form.cleaned_data['additional_collections_agent']

	# Optional assumptions
	preFRP_dry_recycling_volume = form.cleaned_data.get('preFRP_dry_recycling_volume')
	if preFRP_dry_recycling_volume is None:
		preFRP_recycling_waste = borough_data['Household - waste sent for recycling-composting-reuse (tonnes)'][form.cleaned_data['borough']]
	else:
		preFRP_recycling_waste = preFRP_dry_recycling_volume

	preFRP_waste_volume = form.cleaned_data.get('preFRP_waste_volume')
	if preFRP_waste_volume is None:
		preFRP_total_waste = borough_data['Household - total waste (tonnes)'][form.cleaned_data['borough']]
	else:
		preFRP_total_waste = preFRP_waste_volume


	baseline_dry_recyclable_waste = borough_data['Flats (t/hh)'][form.cleaned_data['borough']] * 1000

	residual_waste_disposal_costs = form.cleaned_data.get('residual_waste_disposal')
	if residual_waste_disposal_costs is None:
		borough_residual_waste_disposal_costs = residual_waste_disposal[form.cleaned_data['residual_waste_disposal_method']]['cost']
	else:
		borough_residual_waste_disposal_costs = residual_waste_disposal_costs

	recycling_waste_disposal_costs = form.cleaned_data.get('recycling_waste_disposal_costs')
	if recycling_waste_disposal_costs is None:
		mdf_disposal_fee = 18
	else:
		mdf_disposal_fee = recycling_waste_disposal_costs
	contamination_waste_disposal_costs = form.cleaned_data.get('contamination_waste_disposal_costs')
	if contamination_waste_disposal_costs is None:
		contamination_cost = 176
	else:
		contamination_cost = contamination_waste_disposal_costs

	# Intermediate calculations
	total_households = form.cleaned_data['number_of_estates'] * form.cleaned_data['households_per_estate']
	total_blocks = form.cleaned_data['blocks_per_estate'] * form.cleaned_data['number_of_estates']
	total_binstores = form.cleaned_data['binstores_per_block'] * form.cleaned_data['blocks_per_estate'] * form.cleaned_data['number_of_estates']
	total_recycling_bins = form.cleaned_data['recycling_bins_per_binstore'] * total_binstores
	total_rubbish_bins = form.cleaned_data['rubbish_bins_per_binstore'] * total_binstores
	total_weekly_capacity = form.cleaned_data['capacity_per_bin'] * total_recycling_bins * form.cleaned_data['FRP_collections_per_week']
	bin_capacity_per_household = total_weekly_capacity/total_households

	### SETUP COSTS ###

	# Setup costs per recycling bin
	user_initial_refurb_costs = scenario_costs[form.cleaned_data['setup_cost_scenario']]['new_bins'][form.cleaned_data['capacity_per_bin']]
	user_reverse_lid = scenario_costs[form.cleaned_data['setup_cost_scenario']]['reverse_lid']
	user_aperture = scenario_costs[form.cleaned_data['setup_cost_scenario']]['aperture']

    # Setup costs per bin store
	user_painting = scenario_costs[form.cleaned_data['setup_cost_scenario']]['painting']
	user_lighting = scenario_costs[form.cleaned_data['setup_cost_scenario']]['lighting']
	user_initial_deepclean = scenario_costs[form.cleaned_data['setup_cost_scenario']]['initial_deepclean']

	# Council costs set-up (project management)
	total_project_mgt_cost = form.cleaned_data['number_of_estates'] * daily_salary * (
        scenario_costs[form.cleaned_data['setup_cost_scenario']]['site_assessment'] +
        scenario_costs[form.cleaned_data['setup_cost_scenario']]['stakeholder_engagement'] +
        scenario_costs[form.cleaned_data['setup_cost_scenario']]['improvement_plan'] +
        scenario_costs[form.cleaned_data['setup_cost_scenario']]['implementation_plan'] +
        scenario_costs[form.cleaned_data['setup_cost_scenario']]['delivery_preparation'] +
        scenario_costs[form.cleaned_data['setup_cost_scenario']]['FRP_rollout'] + scenario_costs[form.cleaned_data['setup_cost_scenario']]['installation'])

	setup_cost_assignment = {
		'total_setup_recycling_bin':{
			'agent':form.cleaned_data['bin_purchase_maintenance_agent'],
			'value':user_initial_refurb_costs * total_recycling_bins
		},
		'total_setup_reverse_lid':{
			'agent':form.cleaned_data['bin_purchase_maintenance_agent'],
			'value': user_reverse_lid * total_recycling_bins
		},
		'total_setup_aperture':{
			'agent':form.cleaned_data['bin_purchase_maintenance_agent'],
			'value':user_aperture * total_recycling_bins
		},
		'total_setup_painting':{
			'agent':form.cleaned_data['binstore_refurb_agent'],
			'value':user_painting * total_binstores
		},
		'total_setup_lighting':{
			'agent':form.cleaned_data['binstore_refurb_agent'],
			'value':user_lighting * total_binstores
		},
		'total_setup_initial_deepclean':{
			'agent':form.cleaned_data['binstore_refurb_agent'],
			'value':user_initial_deepclean * total_binstores
		},
		'total_setup_binstore_signage':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':signage_manufacture * total_binstores
		},
		'total_setup_recycling_binstore_sign_post':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':recycling_binstore_sign_post * total_binstores
		},
		'total_setup_recycling_binstore_sign_wall':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':recycling_binstore_sign_wall * total_binstores
		},
		'total_setup_rubbish_binstore_sign_post':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':rubbish_binstore_sign_post * total_binstores
		},
		'total_setup_rubbish_binstore_sign_wall':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':rubbish_binstore_sign_wall * total_binstores
		},
		'total_setup_block_costs':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':total_blocks * (chute_sign_manufacture + noticeboard + recycling_poster)
		},
		'total_setup_communications_design':{
			'agent':form.cleaned_data['stickers_posters_signage_design_agent'],
			'value':signage_design + recycling_bin_sticker_design + recycling_bin_aperture_sticker_design + rubbish_bin_sticker_design + recycling_binstore_sign_design + rubbish_binstore_sign_design + chute_sign_design
		},
		'total_project_mgt':{
			'agent':form.cleaned_data['project_management_agent'],
			'value':total_project_mgt_cost
		},
	}

	total_borough_setup_costs = sum(d['value'] for d in setup_cost_assignment.values() if d['agent'] == 'london_borough')
	total_housing_provider_setup_costs = sum(d['value'] for d in setup_cost_assignment.values() if d['agent'] == 'housing_provider')
	total_setup_costs = total_borough_setup_costs + total_housing_provider_setup_costs

	### ONGOING COSTS ###
	user_cleaning = scenario_costs[form.cleaned_data['ongoing_cost_scenario']]['bin_cleaning']
	total_bin_rental_costs = scenario_costs[form.cleaned_data['ongoing_cost_scenario']]['bin_rental'][form.cleaned_data['capacity_per_bin']] * total_binstores * (form.cleaned_data['recycling_bins_per_binstore'] - form.cleaned_data['preFRP_recycling_bins_per_binstore'])
	if form.cleaned_data['bin_rental_housing_provider'] == 'yes':
		borough_bin_rental_costs = -total_bin_rental_costs
		housing_provider_bin_rental_costs = total_bin_rental_costs
	else:
		borough_bin_rental_costs = total_bin_rental_costs
		housing_provider_bin_rental_costs = -total_bin_rental_costs

	ongoing_cost_assignment = {
		'total_ongoing_cleaning_costs':{
			'agent':form.cleaned_data['cleaning_agent'],
			'value':total_binstores * user_cleaning * 52,
			'year':1
		},
		'total_ongoing_inspection_costs':{
			'agent':form.cleaned_data['inspections_agent'],
			'value':total_binstores * scenario_costs[form.cleaned_data['ongoing_cost_scenario']]['officer_visit'] * 12,
			'year':1
		},
		'total_ongoing_leaflet_manufacture':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':total_households * annual_leaflet_manufacture,
			'year':1
		},
		'total_additional_recycling_collection':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':total_households * (form.cleaned_data['FRP_collections_per_week'] - form.cleaned_data['preFRP_collections_per_week']) * recycling_collection_cost,
			'year':1
		},
		'total_ongoing_refurb_costs':{
			'agent':form.cleaned_data['bin_purchase_maintenance_agent'],
			'value':total_recycling_bins * scenario_costs[form.cleaned_data['ongoing_cost_scenario']]['refurb_bins'][form.cleaned_data['capacity_per_bin']],
			'year':5
		},
		'total_ongoing_recycling_bin_sticker_costs':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':total_recycling_bins * (recycling_bin_sticker_manufacture + recycling_bin_aperture_sticker_manufacture),
			'year':1
		},
		'total_ongoing_rubbish_bin_sticker_costs':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':rubbish_bin_sticker_manufacture * total_rubbish_bins,
			'year':1
		},
		'total_annual_leaflet_design':{
			'agent':form.cleaned_data['stickers_posters_signage_design_agent'],
			'value':annual_leaflet_design,
			'year':1
		},
		'total_bin_rental_costs_borough':{
			'agent':'london_borough',
			'value':borough_bin_rental_costs,
			'year':1
		},
		'total_bin_rental_costs_housing_provider':{
			'agent':'housing_provider',
			'value':housing_provider_bin_rental_costs,
			'year':1
		},
	}

	year1_total_ongoing_costs_london_borough = sum(d['value'] for d in ongoing_cost_assignment.values() if (d['agent'] == 'london_borough' and d['year'] == 1))
	year1_total_ongoing_costs_housing_provider = sum(d['value'] for d in ongoing_cost_assignment.values() if (d['agent'] == 'housing_provider' and d['year'] == 1))
	year5_total_ongoing_costs_london_borough = sum(d['value'] for d in ongoing_cost_assignment.values() if (d['agent'] == 'london_borough' and d['year'] == 5)) + year1_total_ongoing_costs_london_borough
	year5_total_ongoing_costs_housing_provider = sum(d['value'] for d in ongoing_cost_assignment.values() if (d['agent'] == 'housing_provider' and d['year'] == 5)) + year1_total_ongoing_costs_housing_provider

	year0_total_ongoing_costs_london_borough = year5_total_ongoing_costs_london_borough - ongoing_cost_assignment['total_bin_rental_costs_borough']['value']
	year0_total_ongoing_costs_housing_provider = year5_total_ongoing_costs_housing_provider - ongoing_cost_assignment['total_bin_rental_costs_housing_provider']['value']
	year1_total_ongoing_costs = year1_total_ongoing_costs_london_borough + year1_total_ongoing_costs_housing_provider
	year5_total_ongoing_costs = year5_total_ongoing_costs_london_borough + year5_total_ongoing_costs_housing_provider

	### BENEFITS ###
	recyclable_waste_uplift_parameter = scenario_benefits[form.cleaned_data['diverted_waste_benefit_scenario']]['recyclable_waste_uplift']
	contamination_reduction_parameter = scenario_benefits[form.cleaned_data['reduced_contamination_benefit_scenario']]['impact_contamination']

	FRP_avoided_residual_waste = baseline_dry_recyclable_waste * recyclable_waste_uplift_parameter * total_households/1000
	FRP_avoided_contaminated_material = baseline_dry_recyclable_waste * contamination_reduction_parameter * total_households/1000

	emissions_preFRP = emissions_intensity_waste_disposal * (FRP_avoided_residual_waste + FRP_avoided_contaminated_material)
	counterfactual_emissions = emissions_intensity_recycling * (FRP_avoided_residual_waste + FRP_avoided_contaminated_material)
	scc_diverted = (emissions_preFRP - counterfactual_emissions) * scc

	additional_waste_disposal_cost = total_households * ((borough_residual_waste_disposal_costs - mdf_disposal_fee) * recyclable_waste_uplift_parameter * borough_data['Flats (t/hh)'][form.cleaned_data['borough']] + (contamination_cost - mdf_disposal_fee) * contamination_reduction_parameter * borough_data['Flats (t/hh)'][form.cleaned_data['borough']])

	reduced_residual_waste_collection_costs = (form.cleaned_data['preFRP_collections_per_week'] - form.cleaned_data['FRP_collections_per_week'])*rubbish_collection_cost*total_households

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

	direct_benefit = 52 * wtp_recycling * living_wage * scenario_benefits[form.cleaned_data['diverted_waste_benefit_scenario']]['recyclable_waste_uplift'] * total_households
	value_improvement_resident_total = value_improvement_resident + direct_benefit
	total_benefit = value_improvement_resident_total + total_cost_diverted_material + reduced_residual_waste_collection_costs + additional_waste_disposal_cost + scc_diverted


	if form.cleaned_data['material_collections'] > 1:
		total_cost_diverted_material_adjustment = 1
	else:
		total_cost_diverted_material_adjustment = 0

	year0_netbenefit_london_borough = -total_borough_setup_costs - year0_total_ongoing_costs_london_borough + additional_waste_disposal_cost + total_cost_diverted_material * total_cost_diverted_material_adjustment
	year0_netbenefit_housing_provider = -total_housing_provider_setup_costs - year0_total_ongoing_costs_housing_provider
	year0_social_benefit = year0_netbenefit_london_borough + year0_netbenefit_housing_provider + total_cost_diverted_material + scc_diverted + value_improvement_resident_total

	year1_netbenefit_london_borough = -year1_total_ongoing_costs_london_borough + additional_waste_disposal_cost + total_cost_diverted_material * total_cost_diverted_material_adjustment
	year1_netbenefit_housing_provider = -year1_total_ongoing_costs_housing_provider
	year1_social_benefit = year1_netbenefit_london_borough + year1_netbenefit_housing_provider + total_cost_diverted_material + scc_diverted + value_improvement_resident_total

	year5_netbenefit_london_borough = -year5_total_ongoing_costs_london_borough + additional_waste_disposal_cost + total_cost_diverted_material * total_cost_diverted_material_adjustment
	year5_netbenefit_housing_provider = -year5_total_ongoing_costs_housing_provider
	year5_social_benefit = year5_netbenefit_london_borough + year5_netbenefit_housing_provider + total_cost_diverted_material + scc_diverted + value_improvement_resident_total

	total_netbenefit_london_borough = year0_netbenefit_london_borough + 8*year1_netbenefit_london_borough + 2*year5_netbenefit_london_borough
	total_netbenefit_housing_provider = year0_netbenefit_housing_provider + 8*year1_netbenefit_housing_provider + 2*year5_netbenefit_housing_provider
	total_netbenefit_society = year0_social_benefit + 8*year1_social_benefit + 2*year5_social_benefit

	test_cost = ongoing_cost_assignment['total_ongoing_refurb_costs']['value']

	# Key Performance Indicators
	preFRP_household_dry_recycling_rate = preFRP_recycling_waste/preFRP_total_waste
	FRP_household_dry_recycling_rate = (preFRP_recycling_waste + borough_data['Flats (t/hh)'][form.cleaned_data['borough']]*1000* scenario_benefits[form.cleaned_data['diverted_waste_benefit_scenario']]['recyclable_waste_uplift']*total_households/1000)/preFRP_total_waste
	dry_recycling_uplift = FRP_household_dry_recycling_rate - preFRP_household_dry_recycling_rate
	CO2_abated = (((borough_data['Flats (t/hh)'][form.cleaned_data['borough']]*1000)*(recyclable_waste_uplift_parameter+contamination_reduction_parameter))*total_households/1000)*(residual_waste_disposal[form.cleaned_data['residual_waste_disposal_method']]['emissions_intensity']-CO2_emissions_recycling)/1000
	dry_recycling_bin_capacity_treated_flats = form.cleaned_data['capacity_per_bin']*form.cleaned_data['FRP_collections_per_week']*total_recycling_bins/total_households

	borough_additional_net_benefit_per_householdyear = total_netbenefit_london_borough/(total_households * 10)
	housing_provider_additional_net_benefit_per_householdyear = total_netbenefit_housing_provider/(total_households * 10)
	society_net_benefit_per_householdyear = total_netbenefit_society/(total_households * 10)

	attachment = 'model_outputs.xlsx'
	response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	response['Content-Disposition'] = 'attachment;filename="{}"'.format(attachment)

	workbook = xlsxwriter.Workbook(response)
	pct = workbook.add_format({'num_format': '0.0%'})
	money = workbook.add_format({'num_format': '£0'})
	bold = workbook.add_format({'bold': True})

	# Inputs table
	worksheet_inputs = workbook.add_worksheet('Inputs')
	worksheet_inputs.write('A1', 'Input parameter', bold)
	worksheet_inputs.write('B1', 'Value', bold)

	detailed_inputs = (
	    ['Borough',borough],
		['User Type',user_type],
		['Setup cost scenario',setup_cost_scenario],
		['Ongoing cost scenario',ongoing_cost_scenario],
		['Waste volume diverted from residual to recycling scenario',diverted_waste_benefit_scenario],
		['Reduction in contamination rate scenario',reduced_contamination_benefit_scenario],
		['Number of estates',number_of_estates],
		['Households per estate',households_per_estate],
		['Blocks per estate',blocks_per_estate],
		['Bin areas per block',binstores_per_block],
		['Recycling bins per bin area',recycling_bins_per_binstore],
		['Rubbish bins per bin area',rubbish_bins_per_binstore],
		['Recycling capacity per bin',capacity_per_bin],
		['Pre-FRP frequency of recycling collections per week',preFRP_collections_per_week],
		['FRP frequency of recycling collections per week',FRP_collections_per_week],
		['Material collections',material_collections],
		['Recycling bins per bin area (pre-FRP)',preFRP_recycling_bins_per_binstore],
		['Residual waste disposal method',residual_waste_disposal_method],
		['Dry recycling tonnage (pre-FRP)',preFRP_dry_recycling_volume],
		['Total household waste tonnage (pre-FRP)',preFRP_waste_volume],
		['Borough residual waste disposal costs',residual_waste_disposal_costs],
		['Borough recycling treatment costs',recycling_waste_disposal_costs],
		['Cost of contamination',contamination_waste_disposal_costs],
		['New bin purchase/maintenance',bin_purchase_maintenance_agent],
		['Recycling bin rental to housing provider?',bin_rental_housing_provider],
		['Bin area refurbishment',binstore_refurb_agent],
		['Stickers, posters, signage, leaflet (product)',stickers_posters_signage_agent],
		['Stickers, posters, signage, leaflet (design)',stickers_posters_signage_design_agent],
		['Project management',project_management_agent],
		['Regular cleaning', cleaning_agent],
		['Monthly officer inspections',inspections_agent],
		['Additional recycling waste collections',additional_collections_agent]
	)
	row = 1
	col = 0
	output_col_width = 10
	for item, val in (detailed_inputs):
		worksheet_inputs.write(row, col, item)
		worksheet_inputs.write(row, col + 1, val)
		if len(item) > output_col_width:
			output_col_width = len(item)
		row += 1

	worksheet_inputs.set_column(0, 0, output_col_width)

	# Key Performance Indicators tab
	worksheet1 = workbook.add_worksheet('Key Performance Indicators')
	worksheet1.write('A1', 'Output', bold)
	worksheet1.write('B1', 'Value', bold)
	worksheet1.write('C1', 'Output Definition', bold)

	key_performance_indicators_pct = (
	    ['Pre-intervention household dry recycling rate (%)', round(preFRP_household_dry_recycling_rate, 3),'Estimated dry recycling rate before implementation of the FRP for either the London borough or for the treated estates if volumes user inputted'],
	  	['Post-intervention household dry recycling rate (%)',round(FRP_household_dry_recycling_rate,3),'Estimated dry recycling rate after implementation of the FRP for either the London borough or for the treated estates if volumes user inputted'],
	  	['Improvement in dry recycling rate from FRP (percentage points)',round(dry_recycling_uplift,3),'Estimated uplift (in percentage points) in the dry recycling rate as a result of implementing FRP (difference between pre and post-intervention dry recycling rate)'],
	  	['Uplift in dry recycled waste volumes in treated flats from FRP (%)',round(recyclable_waste_uplift_parameter,3),'Estimated percentage increase in the volume of household waste sent to dry recycling as a result of implementing the FRP (driven by benefit scenario selected)'],
		['Reduction in contamination rate of dry recycling in treated flats (percentage points)',round(contamination_reduction_parameter,3),'Estimated percentage point reduction in the contamination rate of household dry recycling volumes as a result of implementing the FRP (driven by benefit scenario selected)'],
	)

	row = 1
	col = 0
	output_col_width = 10
	for item, cost, definition in (key_performance_indicators_pct):
		worksheet1.write(row, col,item,pct)
		worksheet1.write(row, col + 1, cost,pct)
		worksheet1.write(row, col + 2, definition,pct)
		if len(item) > output_col_width:
			output_col_width = len(item)
		row += 1

	key_performance_indicators_numeric = (
		['CO2 emissions abated (tonnes/year)',round(CO2_abated),'Estimated annual CO2e emissions abated (tonnes/yr) as a result of waste being diverted from final disposal i.e. EFW/Landfill'],
		['Dry recycling bin capacity per household in treated flats (litres/hh/pw)',round(dry_recycling_bin_capacity_treated_flats),'FRP includes a recommended minimum dry recycling bin capacity of 60 litres/hh/week. If this output is below then consider increasing the frequency of collections or number of bins'],
	)
	for item, cost, definition in (key_performance_indicators_numeric):
		worksheet1.write(row, col, item, pct)
		worksheet1.write(row, col + 1, cost)
		worksheet1.write(row, col + 2, definition, pct)
		if len(item) > output_col_width:
			output_col_width = len(item)
		row += 1

	key_performance_indicators_money = (
		['Additional London borough net benefit per household of FRP (£ average/year)',round(borough_additional_net_benefit_per_householdyear),'Additional London borough net benefit/cost per household of FRP (average annual £ net benefit/cost across 10-year time horizon)'],
		['Additional housing provider net benefit per household of FRP (£ average/year)',round(housing_provider_additional_net_benefit_per_householdyear),'Additional housing provider net benefit/cost per household of FRP (average annual £ net benefit/cost across 10-year time horizon)'],
		['Net benefit to society per household from FRP (£/year)',round(society_net_benefit_per_householdyear),'Estimated annual net benefit/(cost) to society per household from implementing the FRP on the treated estates. Societal benefits/costs include not only costs/benefits that accrue directly to Boroughs/Housing providers but also those that accrue to residents and other members of society (e.g. through improved resident experience and reduced carbon emissions)'],
	)
	for item, cost, definition in (key_performance_indicators_money):
		worksheet1.write(row, col,item)
		worksheet1.write(row, col + 1, cost,money)
		worksheet1.write(row, col + 2, definition, pct)
		if len(item) > output_col_width:
			output_col_width = len(item)
		row += 1

	worksheet1.set_column(0, 0, output_col_width)

	# Detailed costs
	worksheet2 = workbook.add_worksheet('Costs by Year')
	worksheet2.write('A1', 'Output', bold)
	worksheet2.write('B1', 'London borough', bold)
	worksheet2.write('C1', 'Housing provider', bold)
	worksheet2.write('D1', 'Output definition', bold)

	costs_by_year = (
	    ['Total setup costs', round(total_borough_setup_costs/100)*100, round(total_housing_provider_setup_costs/100)*100,'Setup costs included one-off costs associated with implementing the FRP in designated estates, including: bringing bin provision up to the specified standard, improvements to bin stores, project management to implement measures, and the initial cost of signage/communications'],
		['Year 0 ongoing costs',round(year0_total_ongoing_costs_london_borough/100)*100,round(year0_total_ongoing_costs_housing_provider/100)*100,'Ongoing costs included recurring costs associated with implementing the Flats Recycling Package in designated estates, including: additional costs of waste collection, regular cleaning of bin areas, monthly inspections, refurbishing bins and replacing signage/communications.'],
		['Year 1 ongoing costs',round(year1_total_ongoing_costs_london_borough/100)*100,round(year1_total_ongoing_costs_housing_provider/100)*100,'Ongoing costs included recurring costs associated with implementing the Flats Recycling Package in designated estates, including: additional costs of waste collection, regular cleaning of bin areas, monthly inspections, refurbishing bins and replacing signage/communications.'],
		['Year 2 ongoing costs',round(year1_total_ongoing_costs_london_borough/100)*100,round(year1_total_ongoing_costs_housing_provider/100)*100,'Ongoing costs included recurring costs associated with implementing the Flats Recycling Package in designated estates, including: additional costs of waste collection, regular cleaning of bin areas, monthly inspections, refurbishing bins and replacing signage/communications.'],
		['Year 3 ongoing costs',round(year1_total_ongoing_costs_london_borough/100)*100,round(year1_total_ongoing_costs_housing_provider/100)*100,'Ongoing costs included recurring costs associated with implementing the Flats Recycling Package in designated estates, including: additional costs of waste collection, regular cleaning of bin areas, monthly inspections, refurbishing bins and replacing signage/communications.'],
		['Year 4 ongoing costs',round(year1_total_ongoing_costs_london_borough/100)*100,round(year1_total_ongoing_costs_housing_provider/100)*100,'Ongoing costs included recurring costs associated with implementing the Flats Recycling Package in designated estates, including: additional costs of waste collection, regular cleaning of bin areas, monthly inspections, refurbishing bins and replacing signage/communications.'],
		['Year 5 ongoing costs',round(year5_total_ongoing_costs_london_borough/100)*100,round(year5_total_ongoing_costs_housing_provider/100)*100,'Ongoing costs included recurring costs associated with implementing the Flats Recycling Package in designated estates, including: additional costs of waste collection, regular cleaning of bin areas, monthly inspections, refurbishing bins and replacing signage/communications.'],
		['Year 6 ongoing costs',round(year1_total_ongoing_costs_london_borough/100)*100,round(year1_total_ongoing_costs_housing_provider/100)*100,'Ongoing costs included recurring costs associated with implementing the Flats Recycling Package in designated estates, including: additional costs of waste collection, regular cleaning of bin areas, monthly inspections, refurbishing bins and replacing signage/communications.'],
		['Year 7 ongoing costs',round(year1_total_ongoing_costs_london_borough/100)*100,round(year1_total_ongoing_costs_housing_provider/100)*100,'Ongoing costs included recurring costs associated with implementing the Flats Recycling Package in designated estates, including: additional costs of waste collection, regular cleaning of bin areas, monthly inspections, refurbishing bins and replacing signage/communications.'],
		['Year 8 ongoing costs',round(year1_total_ongoing_costs_london_borough/100)*100,round(year1_total_ongoing_costs_housing_provider/100)*100,'Ongoing costs included recurring costs associated with implementing the Flats Recycling Package in designated estates, including: additional costs of waste collection, regular cleaning of bin areas, monthly inspections, refurbishing bins and replacing signage/communications.'],
		['Year 9 ongoing costs',round(year1_total_ongoing_costs_london_borough/100)*100,round(year1_total_ongoing_costs_housing_provider/100)*100,'Ongoing costs included recurring costs associated with implementing the Flats Recycling Package in designated estates, including: additional costs of waste collection, regular cleaning of bin areas, monthly inspections, refurbishing bins and replacing signage/communications.'],
		['Year 10 ongoing costs',round(year5_total_ongoing_costs_london_borough/100)*100,round(year5_total_ongoing_costs_housing_provider/100)*100,'Ongoing costs included recurring costs associated with implementing the Flats Recycling Package in designated estates, including: additional costs of waste collection, regular cleaning of bin areas, monthly inspections, refurbishing bins and replacing signage/communications.'],
	)

	row = 1
	col = 0
	output_col_width = 10
	for item, lb, hp, definition in (costs_by_year):
		worksheet2.write(row, col, item)
		worksheet2.write(row, col + 1, lb, money)
		worksheet2.write(row, col + 2, hp, money)
		worksheet2.write(row, col + 3, definition)
		if len(item) > output_col_width:
			output_col_width = len(item)
		row += 1

	worksheet2.set_column(0, 0, output_col_width)
	worksheet2.set_column(1, 0, len('London borough'))
	worksheet2.set_column(2, 0, len('Housing provider'))

	# Intermediate costs table
	worksheet_detailed_costs = workbook.add_worksheet('Detailed Costs')
	worksheet_detailed_costs.write('A1', 'Cost parameter', bold)
	worksheet_detailed_costs.write('B1', 'Value', bold)
	worksheet_detailed_costs.write('A2', 'Setup costs', bold)
	worksheet_detailed_costs.write('A3', 'Per recycling bin', bold)
	worksheet_detailed_costs.write('A4','Recycling bins'),
	worksheet_detailed_costs.write('B4',setup_cost_assignment['total_setup_recycling_bin']['value'],money),
	worksheet_detailed_costs.write('A5','Reverse lid'),
	worksheet_detailed_costs.write('B5',setup_cost_assignment['total_setup_reverse_lid']['value'],money),
	worksheet_detailed_costs.write('A6','New paper aperture'),
	worksheet_detailed_costs.write('B6',setup_cost_assignment['total_setup_aperture']['value'],money),
	worksheet_detailed_costs.write('A7','Per bin area costs',bold),
	worksheet_detailed_costs.write('A8','Painting'),
	worksheet_detailed_costs.write('B8',setup_cost_assignment['total_setup_painting']['value'],money),
	worksheet_detailed_costs.write('A9','Lighting'),
	worksheet_detailed_costs.write('B9',setup_cost_assignment['total_setup_lighting']['value'],money),
	worksheet_detailed_costs.write('A10','Initial deep clean'),
	worksheet_detailed_costs.write('B10',setup_cost_assignment['total_setup_initial_deepclean']['value'],money),
	worksheet_detailed_costs.write('A11','Bin store signage'),
	worksheet_detailed_costs.write('B11',setup_cost_assignment['total_setup_binstore_signage']['value'],money),
	worksheet_detailed_costs.write('A12','Signage: Bin area on post (recycling)'),
	worksheet_detailed_costs.write('B12',setup_cost_assignment['total_setup_recycling_binstore_sign_post']['value'],money),
	worksheet_detailed_costs.write('A13','Signage: Bin area on wall (recycling)'),
	worksheet_detailed_costs.write('B13',setup_cost_assignment['total_setup_recycling_binstore_sign_wall']['value'],money),
	worksheet_detailed_costs.write('A14','Signage: Bin area on post (rubbish)'),
	worksheet_detailed_costs.write('B14',setup_cost_assignment['total_setup_rubbish_binstore_sign_post']['value'],money),
	worksheet_detailed_costs.write('A15','Signage: Bin area on wall (rubbish)'),
	worksheet_detailed_costs.write('B15',setup_cost_assignment['total_setup_rubbish_binstore_sign_wall']['value'],money),
	worksheet_detailed_costs.write('A16','Per block costs',bold),
	worksheet_detailed_costs.write('A17','Noticeboard A3'),
	worksheet_detailed_costs.write('B17',total_blocks * noticeboard,money),
	worksheet_detailed_costs.write('A18','Recycling poster'),
	worksheet_detailed_costs.write('B18',total_blocks * recycling_poster,money),
	worksheet_detailed_costs.write('A19','Chute signage'),
	worksheet_detailed_costs.write('B19',total_blocks * chute_sign_manufacture,money),
	worksheet_detailed_costs.write('A20','Per council costs'),
	worksheet_detailed_costs.write('A21','Bin store signage - design (one-off)'),
	worksheet_detailed_costs.write('B21',signage_design,money),
	worksheet_detailed_costs.write('A22','Recycling bin sticker - design cost (one-off)'),
	worksheet_detailed_costs.write('B22',recycling_bin_sticker_design,money),
	worksheet_detailed_costs.write('A23','Recycling bin aperture sticker - design cost (one-off)'),
	worksheet_detailed_costs.write('B23',recycling_bin_aperture_sticker_design,money),
	worksheet_detailed_costs.write('A24','Rubbish bin sticker - design cost (one-off)'),
	worksheet_detailed_costs.write('B24',rubbish_bin_sticker_design,money),
	worksheet_detailed_costs.write('A25','Recycling - bin area signage'),
	worksheet_detailed_costs.write('B25',recycling_binstore_sign_design,money),
	worksheet_detailed_costs.write('A26','Rubbish - bin area signage'),
	worksheet_detailed_costs.write('B26',rubbish_binstore_sign_design,money),
	worksheet_detailed_costs.write('A27','Chute sign - design cost (one-off)'),
	worksheet_detailed_costs.write('B27',chute_sign_design,money),
	worksheet_detailed_costs.write('A28','Project management costs',bold),
	worksheet_detailed_costs.write('A29','Conduct site assessment'),
	worksheet_detailed_costs.write('B29',form.cleaned_data['number_of_estates'] * daily_salary * scenario_costs[form.cleaned_data['setup_cost_scenario']]['site_assessment'],money),
	worksheet_detailed_costs.write('A30','Stakeholder engagement'),
	worksheet_detailed_costs.write('B30',form.cleaned_data['number_of_estates'] * daily_salary * scenario_costs[form.cleaned_data['setup_cost_scenario']]['stakeholder_engagement'],money),
	worksheet_detailed_costs.write('A31','Produce improvement plan'),
	worksheet_detailed_costs.write('B31',form.cleaned_data['number_of_estates'] * daily_salary * scenario_costs[form.cleaned_data['setup_cost_scenario']]['improvement_plan'],money),
	worksheet_detailed_costs.write('A32','Produce implementation plan'),
	worksheet_detailed_costs.write('B32',form.cleaned_data['number_of_estates'] * daily_salary * scenario_costs[form.cleaned_data['setup_cost_scenario']]['implementation_plan'],money),
	worksheet_detailed_costs.write('A33','Preparing for delivery (procurement, etc.)'),
	worksheet_detailed_costs.write('B33',form.cleaned_data['number_of_estates'] * daily_salary * scenario_costs[form.cleaned_data['setup_cost_scenario']]['delivery_preparation'],money),
	worksheet_detailed_costs.write('A34','Roll out of FRP (officer time to oversee)'),
	worksheet_detailed_costs.write('B34',form.cleaned_data['number_of_estates'] * daily_salary * scenario_costs[form.cleaned_data['setup_cost_scenario']]['FRP_rollout'],money),
	worksheet_detailed_costs.write('A35','Installation of FRP measures'),
	worksheet_detailed_costs.write('B35',form.cleaned_data['number_of_estates'] * daily_salary * scenario_costs[form.cleaned_data['setup_cost_scenario']]['installation'],money),
	worksheet_detailed_costs.write('A37', 'Ongoing costs', bold)
	worksheet_detailed_costs.write('A38', 'Per bin area costs', bold)
	worksheet_detailed_costs.write('A39', 'Regular cleaning of bins, bin rooms and signage'),
	worksheet_detailed_costs.write('B39', total_binstores * user_cleaning * 52,money),
	worksheet_detailed_costs.write('A40', 'Monthly visit by officer'),
	worksheet_detailed_costs.write('B40', total_binstores * scenario_costs[form.cleaned_data['ongoing_cost_scenario']]['officer_visit'] * 12,money),
	worksheet_detailed_costs.write('A41', 'Per household costs', bold),
	worksheet_detailed_costs.write('A42', 'Annual leaflet - manufacture'),
	worksheet_detailed_costs.write('B42', total_households * annual_leaflet_manufacture,money),
	worksheet_detailed_costs.write('A43', 'Additional recycling collection cost'),
	worksheet_detailed_costs.write('B43', ongoing_cost_assignment['total_additional_recycling_collection']['value'],money),
	worksheet_detailed_costs.write('A44', 'Per recycling bin costs', bold),
	worksheet_detailed_costs.write('A45', 'Bin refurbishment'),
	worksheet_detailed_costs.write('B45', ongoing_cost_assignment['total_ongoing_refurb_costs']['value'],money),
	worksheet_detailed_costs.write('A46', 'Bin rental'),
	worksheet_detailed_costs.write('B46', housing_provider_bin_rental_costs,money),
	worksheet_detailed_costs.write('A47', 'Recycling bin sticker - manufacture cost'),
	worksheet_detailed_costs.write('B47', total_recycling_bins * recycling_bin_sticker_manufacture,money),
	worksheet_detailed_costs.write('A48', 'Recycling bin aperture sticker - manufacture cost'),
	worksheet_detailed_costs.write('B48', total_recycling_bins * recycling_bin_aperture_sticker_manufacture,money),
	worksheet_detailed_costs.write('A49', 'Per rubbish bin costs', bold),
	worksheet_detailed_costs.write('A50', 'Rubbish bin sticker - manufacture cost'),
	worksheet_detailed_costs.write('B50', rubbish_bin_sticker_manufacture * total_rubbish_bins,money),
	worksheet_detailed_costs.write('A51', 'Per council costs', bold),
	worksheet_detailed_costs.write('A52', 'Annual leaflet - design'),
	worksheet_detailed_costs.write('B52', annual_leaflet_design,money),
	worksheet_detailed_costs.write('A54', 'Note: Not all ongoing costs are incurred on a yearly basis.'),
	worksheet_detailed_costs.set_column(0, 0, len('Recycling bin aperture sticker - design cost (one-off)'))

	# Detailed benefits
	worksheet3 = workbook.add_worksheet('Detailed Benefits')
	worksheet3.write('A1', 'Output', bold)
	worksheet3.write('B1', 'Value', bold)
	worksheet3.write('C1', 'Output definition', bold)

	detailed_benefits = (
		['Social cost of carbon diverted',round(scc_diverted/100)*100,'Estimated monetary value of CO2e emissions abated (tonnes/yr) as a result of waste being diverted from alternative waste disposal methods. Emission reductions are valued at a social cost of carbon of £69.30/tonne'],
		['Cost reduction of waste disposal (reduced gate fees and landfill tax)',round(additional_waste_disposal_cost/100)*100,'Estimated reduction in waste disposal costs (including gate fees, landfill and other taxes) for London boroughs as a result of waste being diverted from alternative methods to recycling'],
		['Reduced residual waste collection costs',round(reduced_residual_waste_collection_costs/100)*100,'Estimated monetary benefit of reduced residual waste collection frequency following the implementation of the FRP'],
		['Value of material diverted from landfill/efw/contamination',round(total_cost_diverted_material/100)*100,'Estimated value of additional materials collected through increased recycled waste volumes. This benefit is assumed to accrue to Boroughs if multisource collections are selected'],
		['Value of improved resident experience',round(value_improvement_resident_total/100)*100,'Estimated monetary value to residents of improved recycling service and estate cleanliness (improved visual and reduced odours) as a result of implementing the FRP. These results have been calculated using survey evidence from the economic literature concerning the value people place on both improved recycling facilities and improvements to their local environment'],
		['Total social benefit of FRP',round(total_benefit/100)*100,''],
	)

	row = 1
	col = 0
	for item, cost, definition in (detailed_benefits):
		worksheet3.write(row, col,item,pct)
		worksheet3.write(row, col + 1, cost,money)
		worksheet3.write(row, col + 2, definition)
		if len(item) > output_col_width:
			output_col_width = len(item)
		row += 1
	worksheet3.write(row + 1, col, 'Note: Total social benefit of FRP may not equal the sum of the value of individual benefits due to rounding.')

	worksheet3.set_column(0, 0, output_col_width)

	# Overall net costs/benefits
	worksheet4 = workbook.add_worksheet('Overall Net Costs and Benefits')
	worksheet4.write('A1', 'Output', bold)
	worksheet4.write('B1', 'London borough', bold)
	worksheet4.write('C1', 'Housing provider', bold)
	worksheet4.write('D1', 'Society', bold)

	net_costs = (
	    ['Total net benefit', round(total_netbenefit_london_borough/100)*100, round(total_netbenefit_housing_provider/100)*100, round(total_netbenefit_society/100)*100],
		['Year 0 net benefit',round(year0_netbenefit_london_borough/100)*100,round(year0_netbenefit_housing_provider/100)*100,round(year0_social_benefit/100)*100],
		['Year 1 net benefit',round(year1_netbenefit_london_borough/100)*100,round(year1_netbenefit_housing_provider/100)*100,round(year1_social_benefit/100)*100],
		['Year 2 net benefit',round(year1_netbenefit_london_borough/100)*100,round(year1_netbenefit_housing_provider/100)*100,round(year1_social_benefit/100)*100],
		['Year 3 net benefit',round(year1_netbenefit_london_borough/100)*100,round(year1_netbenefit_housing_provider/100)*100,round(year1_social_benefit/100)*100],
		['Year 4 net benefit',round(year1_netbenefit_london_borough/100)*100,round(year1_netbenefit_housing_provider/100)*100,round(year1_social_benefit/100)*100],
		['Year 5 net benefit',round(year5_netbenefit_london_borough/100)*100,round(year5_netbenefit_housing_provider/100)*100,round(year5_social_benefit/100)*100],
		['Year 6 net benefit',round(year1_netbenefit_london_borough/100)*100,round(year1_netbenefit_housing_provider/100)*100,round(year1_social_benefit/100)*100],
		['Year 7 net benefit',round(year1_netbenefit_london_borough/100)*100,round(year1_netbenefit_housing_provider/100)*100,round(year1_social_benefit/100)*100],
		['Year 8 net benefit',round(year1_netbenefit_london_borough/100)*100,round(year1_netbenefit_housing_provider/100)*100,round(year1_social_benefit/100)*100],
		['Year 9 net benefit',round(year1_netbenefit_london_borough/100)*100,round(year1_netbenefit_housing_provider/100)*100,round(year1_social_benefit/100)*100],
		['Year 10 net benefit',round(year5_netbenefit_london_borough/100)*100,round(year5_netbenefit_housing_provider/100)*100,round(year5_social_benefit/100)*100],
	)

	row = 1
	col = 0
	output_col_width = 10
	lb_col_width = 10
	hp_col_width = 10
	soc_col_width = 10
	for item, lb, hp, soc in (net_costs):
		worksheet4.write(row, col, item)
		worksheet4.write(row, col + 1, lb, money)
		worksheet4.write(row, col + 2, hp, money)
		worksheet4.write(row, col + 3, soc, money)
		if len(item) > output_col_width:
			output_col_width = len(item)
		if len(str(lb)) > lb_col_width:
			lb_col_width = len(str(lb))
		if len(str(hp)) > hp_col_width:
			hp_col_width = len(str(hp))
		if len(str(soc)) > soc_col_width:
			soc_col_width = len(str(soc))
		row += 1

	worksheet4.write(row + 1, col, 'Note: Total net benefit may not equal the sum of the value of the benefit derived in each year due to rounding.')

	worksheet4.set_column(0, 0, output_col_width)
	worksheet4.set_column(1, 0, lb_col_width)
	worksheet4.set_column(2, 0, hp_col_width)
	worksheet4.set_column(3, 0, soc_col_width)

	workbook.close()

	return response
