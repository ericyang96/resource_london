from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Row, Column, HTML, Reset, Button
from crispy_forms.bootstrap import Accordion, AccordionGroup

setup_cost_choices= [
    ('high', 'High'),
    ('med-high', 'Medium High'),
    ('average', 'Average'),
    ('med-low', 'Medium Low'),
    ('low', 'Low'),
    ]

ongoing_cost_choices= [
	('high', 'High'),
    ('med-high', 'Medium High'),
	('average', 'Average'),
    ('med-low', 'Medium Low'),
	('low', 'Low'),
	]

diverted_waste_choices= [
	('high', 'High'),
	('average', 'Average'),
	('low', 'Low'),
	]

reduced_contamination_choices= [
    ('high', 'High'),
    ('average', 'Average'),
    ('low', 'Low'),
    ]

user_type_choices= [
    ('london_borough', 'London Borough'),
    ('housing_provider', 'Housing Provider'),
    ]

borough_choices = [
	('Barking and Dagenham','Barking and Dagenham'),
	('Barnet','Barnet'),
	('Bexley','Bexley'),
	('Brent','Brent'),
	('Bromley','Bromley'),
	('Camden','Camden'),
	('Croydon','Croydon'),
	('Ealing','Ealing'),
	('Enfield','Enfield'),
	('Greenwich','Greenwich'),
	('Hackney','Hackney'),
	('Hammersmith and Fulham','Hammersmith and Fulham'),
	('Haringey','Haringey'),
	('Harrow','Harrow'),
	('Havering','Havering'),
	('Hillingdon','Hillingdon'),
	('Hounslow','Hounslow'),
	('Islington','Islington'),
	('Kensington and Chelsea','Kensington and Chelsea'),
	('Kingston upon Thames','Kingston upon Thames'),
	('Lambeth','Lambeth'),
	('Lewisham','Lewisham'),
	('Merton','Merton'),
	('Newham','Newham'),
	('Redbridge','Redbridge'),
	('Richmond upon Thames','Richmond upon Thames'),
	('Southwark','Southwark'),
	('Sutton','Sutton'),
	('Tower Hamlets','Tower Hamlets'),
	('Waltham Forest','Waltham Forest'),
	('Wandsworth','Wandsworth'),
	('Westminster','Westminster'),
]

residual_waste_disposal_choices = [
	('mixed','Mix (London average)'),
	('efw','Energy from Waste (EfW)'),
	('landfill','Landfill')
]

bin_capacity_choices = [
	(240,240),
	(360,360),
	(660,660),
	(1100,1100),
	(1280,1280),
]

agent_choices = [
	('london_borough','London Borough'),
	('housing_provider','Housing provider')
]

boolean_choices = [
    ('yes','Yes'),
    ('no','No')
]

#creating our forms
class CalculatorForm(forms.Form):

    borough = forms.CharField(label='Borough', widget=forms.Select(choices=borough_choices))
    user_type = forms.CharField(label='User Type',widget=forms.Select(choices=user_type_choices))
    setup_cost_scenario = forms.CharField(label='Setup cost scenario', widget=forms.Select(choices=setup_cost_choices))
    ongoing_cost_scenario = forms.CharField(label='Ongoing cost scenario', widget=forms.Select(choices=ongoing_cost_choices))
    diverted_waste_benefit_scenario = forms.CharField(label='Waste volume diverted from residual to recycling scenario', widget=forms.Select(choices=diverted_waste_choices))
    reduced_contamination_benefit_scenario = forms.CharField(label='Reduction in contamination rate scenario', widget=forms.Select(choices=reduced_contamination_choices))

    # Estate assumptions
    number_of_estates = forms.IntegerField(label='Number of estates')
    households_per_estate = forms.IntegerField(label='Households per estate')
    binstores_per_block = forms.IntegerField(label='Bin stores per block')
    blocks_per_estate = forms.IntegerField(label='Blocks per estate')
    recycling_bins_per_binstore = forms.IntegerField(label='Recycling bins per bin store')
    rubbish_bins_per_binstore = forms.IntegerField(label='Rubbish bins per bin store')

    # Collection assumptions
    capacity_per_bin = forms.IntegerField(label='Recycling capacity per bin',widget=forms.Select(choices=bin_capacity_choices))
    preFRP_collections_per_week = forms.IntegerField(label='Collections per week (pre-FRP)')
    FRP_collections_per_week = forms.IntegerField(label='Collections per week (FRP)')
    material_collections = forms.IntegerField(label='Material collections')
    preFRP_recycling_bins_per_binstore = forms.IntegerField(label='Recycling bins per binstore (pre-FRP)')
    residual_waste_disposal_method = forms.CharField(label='Residual waste disposal method', widget=forms.Select(choices=residual_waste_disposal_choices))

    # Cost allocations
    bin_purchase_maintenance_agent = forms.CharField(label='Bin purchase/maintenance', widget=forms.Select(choices=agent_choices))
    bin_rental_housing_provider = forms.CharField(label='Bin rental to housing provider?', widget=forms.Select(choices=boolean_choices))
    bin_rental_agent = forms.CharField(label='Bin rental', widget=forms.Select(choices=agent_choices))
    binstore_refurb_agent = forms.CharField(label='Bin store refurbishment', widget=forms.Select(choices=agent_choices))
    stickers_posters_signage_agent = forms.CharField(label='Stickers, posters, signage (product)', widget=forms.Select(choices=agent_choices))
    stickers_posters_signage_design_agent = forms.CharField(label='Stickers, posters, signage (design)', widget=forms.Select(choices=agent_choices))
    project_management_agent = forms.CharField(label='Project management', widget=forms.Select(choices=agent_choices))
    cleaning_inspections_agent = forms.CharField(label='Regular cleaning/inspections', widget=forms.Select(choices=agent_choices))
    additional_collections_agent = forms.CharField(label='Additional recycling waste collections', widget=forms.Select(choices=agent_choices))

    # Optional assumptions
    preFRP_dry_recycling_volume = forms.IntegerField(label='Dry recycling (pre-FRP)',required=False)
    preFRP_waste_volume = forms.IntegerField(label='Total waste (pre-FRP)',required=False)
    dry_recycling_per_household = forms.IntegerField(label='Dry recycling per household',required=False)
    residual_waste_disposal_costs = forms.IntegerField(label='Borough residual waste disposal costs',required=False)
    recycling_waste_disposal_costs = forms.IntegerField(label='Borough recycling waste disposal costs',required=False)
    contamination_waste_disposal_costs = forms.IntegerField(label='Borough contamination waste disposal costs',required=False)

    include_discount = forms.BooleanField(label='Apply discount factor?',required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            # https://stackoverflow.com/questions/27581394/django-crispy-forms-and-tooltip
            Field('borough'),
            Field('user_type'),
            HTML("<h4>Cost Scenarios</h4>"),
            Row(
                Column(
                    Field('setup_cost_scenario', template="help_text\setup_cost_scenario.html")
                ),
                Column(
                    Field('ongoing_cost_scenario', template="help_text\ongoing_cost_scenario.html")
                ),
                css_class='form-row'
            ),
            HTML("<h4>Benefit Scenarios</h4>"),
            Row(
                Column(
                    Field('diverted_waste_benefit_scenario', template="help_text\diverted_waste_benefit_scenario.html")
                ),
                Column(
                    Field('reduced_contamination_benefit_scenario', template="help_text/reduced_contamination_benefit_scenario.html")
                ),
                css_class='form-row'
            ),
            HTML("<h4>Estate Characteristics</h4>"),
            Row(
                Column(
                    Field('number_of_estates', template="help_text/number_of_estates.html")
                ),
                Column(
                    Field('households_per_estate', template="help_text\households_per_estate.html")
                ),
                Column(
                    Field('binstores_per_block', template="help_text/binstores_per_block.html")
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Field('blocks_per_estate', template="help_text/blocks_per_estate.html")
                ),
                Column(
                    Field('recycling_bins_per_binstore', template="help_text/recycling_bins_per_binstore.html")
                ),
                Column(
                    Field('rubbish_bins_per_binstore', template="help_text/rubbish_bins_per_binstore.html")
                ),
                css_class='form-row'
            ),
            HTML("<h4>Collection Assumptions</h4>"),
            Row(
                Column(
                    Field('capacity_per_bin', template="help_text\capacity_per_bin.html", css_class='form-group col-md-4 mb-0',)
                ),
                Column(
                    Field('preFRP_collections_per_week', template="help_text\preFRP_collections_per_week.html",css_class='form-group col-md-4 mb-0'),
                ),
                Column(
                    Field('FRP_collections_per_week', template="help_text\FRP_collections_per_week.html", css_class='form-group col-md-4 mb-0')
                    ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Field('material_collections', template="help_text\material_collections.html", css_class='form-group col-md-4 mb-0')
                ),
                Column(
                    Field('preFRP_recycling_bins_per_binstore', template="help_text\preFRP_recycling_bins_per_binstore.html", css_class='form-group col-md-4 mb-0')
                ),
                Column(
                    Field('residual_waste_disposal_method', template="help_text/residual_waste_disposal_method.html", css_class='form-group col-md-10 mb-0')
                ),
                css_class='form-row'
            ),
            HTML("<h4>Cost Allocations</h4>"),
            Row(
                Column(
                    Field('bin_purchase_maintenance_agent', template="help_text/bin_purchase_maintenance_agent.html"),
                ),
                Column(
                    Field('bin_rental_housing_provider', template="help_text/bin_rental_housing_provider.html")
                    ),
                Column(
                    Field('bin_rental_agent', template="help_text/bin_rental_agent.html")
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Field('binstore_refurb_agent', template="help_text/binstore_refurb_agent.html")
                ),
                Column(
                    Field('stickers_posters_signage_agent', template="help_text/stickers_posters_signage_agent.html")
                ),
                Column(
                    Field('stickers_posters_signage_design_agent', template="help_text/stickers_posters_signage_design_agent.html")
                ),
                css_class='form-row'
            ),
            Row(
                Column('project_management_agent', css_class='form-group col-md-4 mb-0'),
                Column('cleaning_inspections_agent', css_class='form-group col-md-4 mb-0'),
                Column('additional_collections_agent', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            HTML("<h4>Optional Assumptions</h4>"),
            Row(
                Column(
                    Field('preFRP_dry_recycling_volume', template="help_text/preFRP_dry_recycling_volume.html")
                ),
                Column(
                    Field('preFRP_waste_volume', template="help_text/preFRP_waste_volume.html")
                ),
                Column(
                    Field('dry_recycling_per_household', template="help_text/dry_recycling_per_household.html")
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Field('residual_waste_disposal_costs', template="help_text/residual_waste_disposal_costs.html")
                ),
                Column(
                    Field('recycling_waste_disposal_costs', template="help_text/recycling_waste_disposal_costs.html")
                ),
                Column(
                    Field('contamination_waste_disposal_costs', template="help_text/contamination_waste_disposal_costs.html")
                ),
                css_class='form-row'
            ),
            Row(

                css_class='form-row'
            ),
            'include_discount',
            Submit('submit', 'Submit')
        )

class DownloadForm(forms.Form):
    borough = forms.CharField(widget=forms.HiddenInput)
    user_type = forms.CharField(widget=forms.HiddenInput)
    number_of_estates = forms.IntegerField(widget=forms.HiddenInput)
    households_per_estate = forms.IntegerField(widget=forms.HiddenInput)
    blocks_per_estate = forms.IntegerField(widget=forms.HiddenInput)
    setup_cost_scenario = forms.CharField(widget=forms.HiddenInput)
    ongoing_cost_scenario = forms.CharField(widget=forms.HiddenInput)
    diverted_waste_benefit_scenario = forms.CharField(widget=forms.HiddenInput)
    reduced_contamination_benefit_scenario = forms.CharField(widget=forms.HiddenInput)

    # Estate assumptions
    number_of_estates = forms.IntegerField(widget=forms.HiddenInput)
    households_per_estate = forms.IntegerField(widget=forms.HiddenInput)
    binstores_per_block = forms.IntegerField(widget=forms.HiddenInput)
    blocks_per_estate = forms.IntegerField(widget=forms.HiddenInput)
    recycling_bins_per_binstore = forms.IntegerField(widget=forms.HiddenInput)
    rubbish_bins_per_binstore = forms.IntegerField(widget=forms.HiddenInput)

    # Collection assumptions
    capacity_per_bin = forms.IntegerField(widget=forms.HiddenInput)
    preFRP_collections_per_week = forms.IntegerField(widget=forms.HiddenInput)
    FRP_collections_per_week = forms.IntegerField(widget=forms.HiddenInput)
    material_collections = forms.IntegerField(widget=forms.HiddenInput)
    preFRP_recycling_bins_per_binstore = forms.IntegerField(widget=forms.HiddenInput)
    residual_waste_disposal_method = forms.CharField(widget=forms.HiddenInput)

    # Cost allocations
    bin_purchase_maintenance_agent = forms.CharField(widget=forms.HiddenInput)
    bin_rental_housing_provider = forms.CharField(widget=forms.HiddenInput)
    bin_rental_agent = forms.CharField(widget=forms.HiddenInput)
    binstore_refurb_agent = forms.CharField(widget=forms.HiddenInput)
    stickers_posters_signage_agent = forms.CharField(widget=forms.HiddenInput)
    stickers_posters_signage_design_agent = forms.CharField(widget=forms.HiddenInput)
    project_management_agent = forms.CharField(widget=forms.HiddenInput)
    cleaning_inspections_agent = forms.CharField(widget=forms.HiddenInput)
    additional_collections_agent = forms.CharField(widget=forms.HiddenInput)

    # Optional assumptions
    preFRP_dry_recycling_volume = forms.IntegerField(widget=forms.HiddenInput)
    preFRP_waste_volume = forms.IntegerField(widget=forms.HiddenInput)
    dry_recycling_per_household = forms.IntegerField(widget=forms.HiddenInput)
    residual_waste_disposal_costs = forms.IntegerField(widget=forms.HiddenInput)
    recycling_waste_disposal_costs = forms.IntegerField(widget=forms.HiddenInput)
    contamination_waste_disposal_costs = forms.IntegerField(widget=forms.HiddenInput)
