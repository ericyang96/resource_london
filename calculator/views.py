from django.shortcuts import render
import pandas as pd
from .forms import CalculatorForm, DownloadForm
from django.http import HttpResponse
import csv

#https://stackoverflow.com/questions/4142151/how-to-import-the-class-within-the-same-directory-or-sub-directory
#https://stackoverflow.com/questions/45710477/importing-variables-from-another-file-in-python
#https://www.imagescape.com/blog/2019/10/09/multipage-forms-django/
#https://docs.djangoproject.com/en/dev/howto/static-files/
#https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
#http://jsfiddle.net/TLBvx/252/
#https://stackoverflow.com/questions/6164507/change-the-content-of-a-div-based-on-selection-from-dropdown-menu
#https://django-crispy-forms.readthedocs.io/en/latest/layouts.html
#https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
#https://data-flair.training/blogs/python-project-calorie-calculator-django/
#https://learndjango.com/tutorials/django-login-and-logout-tutorial
#https://django-formtools.readthedocs.io/en/latest/wizard.html
# https://herewecode.io/blog/a-beginners-guide-to-git-how-to-start-and-create-your-first-repository/

df = pd.read_excel('Borough data.xlsx',sheet_name = 'London Boroughs specific',index_col=1)
df = df.drop(columns=['ECODE','Check','Unnamed: 22'])
df = df.dropna(subset=['FLAT_MAIS'])
borough_data = df.to_dict()

scenario_benefits = {
	'high':{
		'recyclable_waste_uplift':0.39,
		'impact_contamination':0.46
	},
	'medium':{
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
 	'mixed':{'emissions_intensity':407,'cost':113*sent_to_landfill_share+89*sent_to_efw_share},
	'landfill':{'emissions_intensity':586,'cost':113},
	'efw':{'emissions_intensity':386,'cost':89}
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
officer_visit = 13.43
rubbish_collection_cost = 16.26
recycling_collection_cost = 16.26

scenario_costs = {
		'high':{
		        'new_bins':{240:21.09,360:34,660:254.98,1100:274.52,1280:336.68},
		        'refurb_bins':{240:21,360:34,660:69,1100:69,1280:69},
		        'bin_rental':{240:100*240/1100,360:100*360/1100,660:100*660/1100.2,1100:100,1280:100*1280/1100},
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
				'installation':1
		},
		'med-high':{
		        'new_bins':{240:21.09,360:34,660:254.98,1100:274.52,1280:336.68},
		        'refurb_bins':{240:21,360:34,660:69,1100:69,1280:69},
		        'bin_rental':{240:100*240/1100,360:100*360/1100,660:100*660/1100.2,1100:100,1280:100*1280/1100},
		        'reverse_lid':20,
		        'aperture':16,
		        'bin_cleaning':15,
		        'painting':400,
		        'lighting':180,
		        'initial_deepclean':56,
		        'site_assessment':0.625,
		        'stakeholder_engagement':0.625,
		        'improvement_plan':0.25,
		        'implementation_plan':0.25,
		        'delivery_preparation':0.625,
		        'FRP_rollout':0.625,
				'installation':0.75
		},
		'average': {
				'new_bins':{240:21.09,360:34,660:254.98,1100:274.52,1280:336.68},
		        'refurb_bins':{240:21,360:34,660:69,1100:69,1280:69},
		        'bin_rental':{240:100*240/1100,360:100*360/1100,660:100*660/1100.2,1100:100,1280:100*1280/1100},
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
				'installation':0.5
		},
		'med-low':{
		        'new_bins':{240:21.09,360:34,660:69,1100:69,1280:69},
		        'refurb_bins':{240:21,360:34,660:69,1100:69,1280:69},
		        'bin_rental':{240:100*240/1100,360:100*360/1100,660:100*660/1100.2,1100:100,1280:100*1280/1100},
		        'reverse_lid':20,
		        'aperture':16,
		        'bin_cleaning':12,
		        'painting':500,
		        'lighting':237.625,
		        'initial_deepclean':75.25,
		        'site_assessment':0.375,
		        'stakeholder_engagement':0.375,
		        'improvement_plan':0.15,
		        'implementation_plan':0.15,
		        'delivery_preparation':0.375,
		        'FRP_rollout':0.375,
				'installation':0.375
		},
		'low':{
				'new_bins':{240:21.09,360:34,660:69,1100:69,1280:69},
		        'refurb_bins':{240:21,360:34,660:69,1100:69,1280:69},
		        'bin_rental':{240:100*240/1100,360:100*360/1100,660:100*660/1100.2,1100:100,1280:100*1280/1100},
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
				'installation':0.25
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
    'food_drink_cans':{'share':0.029,'price':385},
    'glass':{'share':0.224,'price':10.5},
    'cartons':{'share':0.009,'price':275},
    'paper':{'share':0.231,'price':10},
    'cardboard':{'share':0.17,'price':60},
    'plastics':{'share':0.076,'price':115},
}

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
			bin_rental_agent = form.cleaned_data['bin_rental_agent']
			binstore_refurb_agent = form.cleaned_data['binstore_refurb_agent']
			stickers_posters_signage_agent = form.cleaned_data['stickers_posters_signage_agent']
			stickers_posters_signage_design_agent = form.cleaned_data['stickers_posters_signage_agent']
			project_management_agent = form.cleaned_data['project_management_agent']
			cleaning_inspections_agent = form.cleaned_data['cleaning_inspections_agent']
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

			dry_recycling_per_household = form.cleaned_data['dry_recycling_per_household']
			if dry_recycling_per_household is None:
				baseline_dry_recyclable_waste = borough_data['Flats (t/hh)'][form.cleaned_data['borough']] * 1000
			else:
				baseline_dry_recyclable_waste = dry_recycling_per_household * 1000

			residual_waste_disposal_costs = form.cleaned_data.get('residual_waste_disposal')
			if residual_waste_disposal_costs is None:
				borough_residual_waste_disposal_costs = residual_waste_disposal[form.cleaned_data['residual_waste_disposal_method']]['cost']
			else:
				borough_residual_waste_disposal_costs = residual_waste_disposal_costs

			recycling_waste_disposal_costs = form.cleaned_data.get('recycling_waste_disposal_costs')
			if recycling_waste_disposal_costs is None:
				mdf_disposal_fee = 27
			else:
				mdf_disposal_fee = recycling_waste_disposal_costs
			contamination_waste_disposal_costs = form.cleaned_data.get('contamination_waste_disposal_costs')
			if contamination_waste_disposal_costs is None:
				contamination_cost = 92
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
				'total_ongoing_binstore_costs':{
					'agent':form.cleaned_data['cleaning_inspections_agent'],
					'value':total_binstores * (user_cleaning * 52 + officer_visit * 12),
					'year':1
				},
				'total_ongoing_leaflet_manufacture':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':total_households * annual_leaflet_manufacture,
					'year':1
				},
				'total_additional_recycling_collection ':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':total_households * (form.cleaned_data['FRP_collections_per_week'] - form.cleaned_data['preFRP_collections_per_week']) * recycling_collection_cost,
					'year':1
				},
				'total_ongoing_refurb_costs':{
					'agent':form.cleaned_data['bin_purchase_maintenance_agent'],
					'value':total_recycling_bins * scenario_costs[form.cleaned_data['ongoing_cost_scenario']]['refurb_bins'][form.cleaned_data['capacity_per_bin']],
					'year':8
				},
				'total_ongoing_recycling_bin_sticker_costs':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':total_recycling_bins * (recycling_bin_sticker_manufacture + recycling_bin_aperture_sticker_manufacture),
					'year':5
				},
				'total_ongoing_rubbish_bin_sticker_costs':{
					'agent':form.cleaned_data['stickers_posters_signage_agent'],
					'value':rubbish_bin_sticker_manufacture * total_rubbish_bins,
					'year':5
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
			year8_total_ongoing_costs_london_borough = sum(d['value'] for d in ongoing_cost_assignment.values() if (d['agent'] == 'london_borough' and d['year'] == 8)) + year1_total_ongoing_costs_london_borough
			year8_total_ongoing_costs_housing_provider = sum(d['value'] for d in ongoing_cost_assignment.values() if (d['agent'] == 'housing_provider' and d['year'] == 8)) + year1_total_ongoing_costs_housing_provider

			year0_total_ongoing_costs_london_borough = year5_total_ongoing_costs_london_borough - ongoing_cost_assignment['total_bin_rental_costs_borough']['value']
			year0_total_ongoing_costs_housing_provider = year5_total_ongoing_costs_housing_provider - ongoing_cost_assignment['total_bin_rental_costs_housing_provider']['value']
			year1_total_ongoing_costs = year1_total_ongoing_costs_london_borough + year1_total_ongoing_costs_housing_provider
			year5_total_ongoing_costs = year5_total_ongoing_costs_london_borough + year5_total_ongoing_costs_housing_provider
			year8_total_ongoing_costs = year8_total_ongoing_costs_london_borough + year8_total_ongoing_costs_housing_provider

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
			total_benefit = value_improvement_resident_total + total_cost_diverted_material + additional_waste_disposal_cost + scc_diverted


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

			year8_netbenefit_london_borough = -year8_total_ongoing_costs_london_borough + additional_waste_disposal_cost + total_cost_diverted_material * total_cost_diverted_material_adjustment
			year8_netbenefit_housing_provider= -year8_total_ongoing_costs_housing_provider
			year8_social_benefit = year8_netbenefit_london_borough + year8_netbenefit_housing_provider + total_cost_diverted_material + scc_diverted + value_improvement_resident_total

			total_netbenefit_london_borough = year0_netbenefit_london_borough + 7*year1_netbenefit_london_borough + 2*year5_netbenefit_london_borough + year8_netbenefit_london_borough
			total_netbenefit_housing_provider = year0_netbenefit_housing_provider + 7*year1_netbenefit_housing_provider + 2*year5_netbenefit_housing_provider + year8_netbenefit_housing_provider
			total_netbenefit_society = year0_social_benefit + 7*year1_social_benefit + 2*year5_social_benefit + year8_social_benefit

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
				'bin_rental_agent':bin_rental_agent,
				'binstore_refurb_agent':binstore_refurb_agent,
				'stickers_posters_signage_agent':stickers_posters_signage_agent,
				'stickers_posters_signage_design_agent':stickers_posters_signage_agent,
				'project_management_agent':project_management_agent,
				'cleaning_inspections_agent':cleaning_inspections_agent,
				'additional_collections_agent':additional_collections_agent,
				'preFRP_dry_recycling_volume': preFRP_dry_recycling_volume,
				'preFRP_waste_volume': preFRP_waste_volume,
				'dry_recycling_per_household': dry_recycling_per_household,
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
				'year8_total_ongoing_costs_london_borough':year8_total_ongoing_costs_london_borough,
				'year0_total_ongoing_costs_housing_provider':year0_total_ongoing_costs_housing_provider,
				'year1_total_ongoing_costs_housing_provider':year1_total_ongoing_costs_housing_provider,
				'year5_total_ongoing_costs_housing_provider':year5_total_ongoing_costs_housing_provider,
				'year8_total_ongoing_costs_housing_provider':year8_total_ongoing_costs_housing_provider,
				'year0_netbenefit_london_borough':year0_netbenefit_london_borough,
				'year0_netbenefit_housing_provider':year0_netbenefit_housing_provider,
				'year0_social_benefit':year0_social_benefit,
				'year1_netbenefit_london_borough':year1_netbenefit_london_borough,
				'year1_netbenefit_housing_provider':year1_netbenefit_housing_provider,
				'year1_social_benefit':year1_social_benefit,
				'year5_netbenefit_london_borough':year5_netbenefit_london_borough,
				'year5_netbenefit_housing_provider':year5_netbenefit_housing_provider,
				'year5_social_benefit':year5_social_benefit,
				'year8_netbenefit_london_borough':year8_netbenefit_london_borough,
				'year8_netbenefit_housing_provider':year8_netbenefit_housing_provider,
				'year8_social_benefit':year8_social_benefit,
				'total_netbenefit_london_borough':total_netbenefit_london_borough,
				'total_netbenefit_housing_provider':total_netbenefit_housing_provider,
				'total_netbenefit_society':total_netbenefit_society,
				'borough_additional_net_benefit_per_householdyear':borough_additional_net_benefit_per_householdyear,
				'housing_provider_additional_net_benefit_per_householdyear':housing_provider_additional_net_benefit_per_householdyear,
				'society_net_benefit_per_householdyear':society_net_benefit_per_householdyear,
				'download_form': download_form
				}
			return render(request, 'result.html', context)

	else:
		#creating a new form
		form = CalculatorForm(
			initial={
				'households_per_estate':150,
				'blocks_per_estate':5,
				'binstores_per_block':1,
				'recycling_bins_per_binstore':2,
				'rubbish_bins_per_binstore':3
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
	bin_rental_agent = form.cleaned_data['bin_rental_agent']
	binstore_refurb_agent = form.cleaned_data['binstore_refurb_agent']
	stickers_posters_signage_agent = form.cleaned_data['stickers_posters_signage_agent']
	stickers_posters_signage_design_agent = form.cleaned_data['stickers_posters_signage_agent']
	project_management_agent = form.cleaned_data['project_management_agent']
	cleaning_inspections_agent = form.cleaned_data['cleaning_inspections_agent']
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

	dry_recycling_per_household = form.cleaned_data.get('dry_recycling_per_household')
	if dry_recycling_per_household is None:
		baseline_dry_recyclable_waste = borough_data['Flats (t/hh)'][form.cleaned_data['borough']] * 1000
	else:
		baseline_dry_recyclable_waste = dry_recycling_per_household * 1000

	residual_waste_disposal_costs = form.cleaned_data.get('residual_waste_disposal')
	if residual_waste_disposal_costs is None:
		borough_residual_waste_disposal_costs = residual_waste_disposal[form.cleaned_data['residual_waste_disposal_method']]['cost']
	else:
		borough_residual_waste_disposal_costs = residual_waste_disposal_costs

	recycling_waste_disposal_costs = form.cleaned_data.get('recycling_waste_disposal_costs')
	if recycling_waste_disposal_costs is None:
		mdf_disposal_fee = 27
	else:
		mdf_disposal_fee = recycling_waste_disposal_costs
	contamination_waste_disposal_costs = form.cleaned_data.get('contamination_waste_disposal_costs')
	if contamination_waste_disposal_costs is None:
		contamination_cost = 92
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
		'total_ongoing_binstore_costs':{
			'agent':form.cleaned_data['cleaning_inspections_agent'],
			'value':total_binstores * (user_cleaning * 52 + officer_visit * 12),
			'year':1
		},
		'total_ongoing_leaflet_manufacture':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':total_households * annual_leaflet_manufacture,
			'year':1
		},
		'total_additional_recycling_collection ':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':total_households * (form.cleaned_data['FRP_collections_per_week'] - form.cleaned_data['preFRP_collections_per_week']) * recycling_collection_cost,
			'year':1
		},
		'total_ongoing_refurb_costs':{
			'agent':form.cleaned_data['bin_purchase_maintenance_agent'],
			'value':total_recycling_bins * scenario_costs[form.cleaned_data['ongoing_cost_scenario']]['refurb_bins'][form.cleaned_data['capacity_per_bin']],
			'year':8
		},
		'total_ongoing_recycling_bin_sticker_costs':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':total_recycling_bins * (recycling_bin_sticker_manufacture + recycling_bin_aperture_sticker_manufacture),
			'year':5
		},
		'total_ongoing_rubbish_bin_sticker_costs':{
			'agent':form.cleaned_data['stickers_posters_signage_agent'],
			'value':rubbish_bin_sticker_manufacture * total_rubbish_bins,
			'year':5
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
	year8_total_ongoing_costs_london_borough = sum(d['value'] for d in ongoing_cost_assignment.values() if (d['agent'] == 'london_borough' and d['year'] == 8)) + year1_total_ongoing_costs_london_borough
	year8_total_ongoing_costs_housing_provider = sum(d['value'] for d in ongoing_cost_assignment.values() if (d['agent'] == 'housing_provider' and d['year'] == 8)) + year1_total_ongoing_costs_housing_provider

	year0_total_ongoing_costs_london_borough = year5_total_ongoing_costs_london_borough - ongoing_cost_assignment['total_bin_rental_costs_borough']['value']
	year0_total_ongoing_costs_housing_provider = year5_total_ongoing_costs_housing_provider - ongoing_cost_assignment['total_bin_rental_costs_housing_provider']['value']
	year1_total_ongoing_costs = year1_total_ongoing_costs_london_borough + year1_total_ongoing_costs_housing_provider
	year5_total_ongoing_costs = year5_total_ongoing_costs_london_borough + year5_total_ongoing_costs_housing_provider
	year8_total_ongoing_costs = year8_total_ongoing_costs_london_borough + year8_total_ongoing_costs_housing_provider

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
	total_benefit = value_improvement_resident_total + total_cost_diverted_material + additional_waste_disposal_cost + scc_diverted


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

	year8_netbenefit_london_borough = -year8_total_ongoing_costs_london_borough + additional_waste_disposal_cost + total_cost_diverted_material * total_cost_diverted_material_adjustment
	year8_netbenefit_housing_provider= -year8_total_ongoing_costs_housing_provider
	year8_social_benefit = year8_netbenefit_london_borough + year8_netbenefit_housing_provider + total_cost_diverted_material + scc_diverted + value_improvement_resident_total

	total_netbenefit_london_borough = year0_netbenefit_london_borough + 7*year1_netbenefit_london_borough + 2*year5_netbenefit_london_borough + year8_netbenefit_london_borough
	total_netbenefit_housing_provider = year0_netbenefit_housing_provider + 7*year1_netbenefit_housing_provider + 2*year5_netbenefit_housing_provider + year8_netbenefit_housing_provider
	total_netbenefit_society = year0_social_benefit + 7*year1_social_benefit + 2*year5_social_benefit + year8_social_benefit

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

	attachment = 'model_outputs.csv'
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment;filename="{}"'.format(attachment)

	writer = csv.writer(response)
	writer.writerow(['Key performance indicators'])
	writer.writerow(['Pre-intervention household dry recycling rate (%)',preFRP_household_dry_recycling_rate])
	writer.writerow(['Post-intervention household dry recycling rate (%)',FRP_household_dry_recycling_rate])
	writer.writerow(['Dry recycling rate uplift (pp)',dry_recycling_uplift])
	writer.writerow(['Uplift in dry recycled waste volumes in treated flats from FRP (%)',recyclable_waste_uplift_parameter])
	writer.writerow(['Reduction in contamination rate of dry recycling in treated flats (pp)',contamination_reduction_parameter])
	writer.writerow(['CO2 emissions abated (tons/year)',CO2_abated])
	writer.writerow(['Dry recycling bin capacity per household in treated flats (litres/hh/pw)',dry_recycling_bin_capacity_treated_flats])
	writer.writerow(['Additional London Borough net benefit per household of FRP (£ average/year)',borough_additional_net_benefit_per_householdyear])
	writer.writerow(['Additional housing provider net benefit per household of FRP (£ average/year)',housing_provider_additional_net_benefit_per_householdyear])
	writer.writerow(['Net benefit to society per household from FRP (£/year)',society_net_benefit_per_householdyear])
	writer.writerow([])
	writer.writerow(['Total setup costs'])
	writer.writerow(['Total setup costs (London Borough)',total_borough_setup_costs])
	writer.writerow(['Total setup costs (Housing provider)',total_housing_provider_setup_costs])
	writer.writerow(['Ongoing costs by year'])
	writer.writerow(['Value','Year 0','Year 1','Year 2','Year 3','Year 4','Year 5','Year 6','Year 7','Year 8','Year 9','Year 10'])
	writer.writerow(['Ongoing costs (London Borough)',year0_total_ongoing_costs_london_borough,year1_total_ongoing_costs_london_borough,year1_total_ongoing_costs_london_borough,year1_total_ongoing_costs_london_borough,year1_total_ongoing_costs_london_borough,year5_total_ongoing_costs_london_borough,year1_total_ongoing_costs_london_borough,year1_total_ongoing_costs_london_borough,year8_total_ongoing_costs_london_borough,year1_total_ongoing_costs_london_borough,year5_total_ongoing_costs_london_borough,])
	writer.writerow([])
	writer.writerow(['Ongoing costs (Housing provider)',year0_total_ongoing_costs_housing_provider,year1_total_ongoing_costs_housing_provider,year1_total_ongoing_costs_housing_provider,year1_total_ongoing_costs_housing_provider,year1_total_ongoing_costs_housing_provider,year5_total_ongoing_costs_housing_provider,year1_total_ongoing_costs_housing_provider,year1_total_ongoing_costs_housing_provider,year8_total_ongoing_costs_housing_provider,year1_total_ongoing_costs_housing_provider,year5_total_ongoing_costs_housing_provider,])
	writer.writerow([])
	writer.writerow(['Benefits'])
	writer.writerow(['Social cost of carbon diverted',scc_diverted])
	writer.writerow(['Cost reduction of waste disposal (reduced gate fees and landfill tax) (£)',additional_waste_disposal_cost])
	writer.writerow(['Reduced residual waste collection costs (£)',reduced_residual_waste_collection_costs])
	writer.writerow(['Value of material diverted from landfill/efw/contamination (£)',total_cost_diverted_material])
	writer.writerow(['Value of improved resident experience (£)',value_improvement_resident_total])
	writer.writerow(['Total social benefit of FRP (£)',total_benefit])
	writer.writerow([])
	writer.writerow(['Overall net benefits/costs'])
	writer.writerow(['Total net benefit (London Borough)',total_netbenefit_london_borough])
	writer.writerow(['Total net benefit (Housing provider)',total_netbenefit_housing_provider])
	writer.writerow(['Total net benefit (society)',total_netbenefit_society])
	writer.writerow([])
	writer.writerow(['Net benefits/costs by year'])
	writer.writerow(['Value','Year 0','Year 1','Year 2','Year 3','Year 4','Year 5','Year 6','Year 7','Year 8','Year 9','Year 10'])
	writer.writerow(['Net benefit (London Borough)',year0_netbenefit_london_borough,year1_netbenefit_london_borough,year1_netbenefit_london_borough,year1_netbenefit_london_borough,year1_netbenefit_london_borough,year5_netbenefit_london_borough,year1_netbenefit_london_borough,year1_netbenefit_london_borough,year8_netbenefit_london_borough,year1_netbenefit_london_borough,year5_netbenefit_london_borough])
	writer.writerow(['Net benefit (Housing provider)',year0_netbenefit_housing_provider,year1_netbenefit_housing_provider,year1_netbenefit_housing_provider,year1_netbenefit_housing_provider,year1_netbenefit_housing_provider,year5_netbenefit_housing_provider,year1_netbenefit_housing_provider,year1_netbenefit_housing_provider,year8_netbenefit_housing_provider,year1_netbenefit_housing_provider,year5_netbenefit_housing_provider])
	writer.writerow(['Net benefit (society)',year0_social_benefit,year1_social_benefit,year1_social_benefit,year1_social_benefit,year1_social_benefit,year5_social_benefit,year1_social_benefit,year1_social_benefit,year8_social_benefit,year1_social_benefit,year5_social_benefit])

	return response
