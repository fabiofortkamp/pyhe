import pytest
import pyhe
import numpy as np

# for common combustion products, reaction is exotermix
# meaning, enthalpy of formation is negative
@pytest.mark.parametrize(
    "fluid",
   [
    "Steam",
    "Carbon monoxide",
    "Carbon dioxide",
    "Steam",
    "Sulfur dioxide",
   ] 
)
def test_enthalpy_of_formation_is_negative(fluid):

    h = pyhe.enthalpy_of_formation(fluid)

    assert h < 0

# for stable compounds, enthalpy of formation is zero
@pytest.mark.parametrize(
    "fluid",
   [
    "Carbon",
    "Oxygen gas",
    "Nitrogen gas",
    "Hydrogen gas",
   ] 
)
def test_enthalpy_of_formation_is_negative(fluid):

    h = pyhe.enthalpy_of_formation(fluid)

    assert h == 0

# molar mass is always positive
@pytest.mark.parametrize(
    "fluid",
   [          
"Carbon",              
"Sulfur",             
"Sulfur dioxide",       
"Hydrogen gas",         
"Nitrogen gas",         
"Oxygen gas",           
"Carbon dioxide",       
"Carbon monoxide",      
"Steam",                
"Water",                
"Hydrogen peroxide",    
"Ammonia",              
"Oxygen",               
"Hydrogen",             
"Nitrogen",             
"Hydroxyl",             
"Methane",              
"Acetylene",            
"Ethylene",             
"Ethane",               
"Propylene",            
"Propane",              
"Butane",               
"Pentane",              
"Octane vapor",         
"Octane liquid",        
"Benzene",              
"Methyl alcohol vapor", 
"Methyl alcohol liquid",
"Ethyl alcohol vapor",  
"Ethyl alcohol liquid", 
   ] 
)
def test_molar_mass_is_positive(fluid):

    MM = pyhe.molar_mass(fluid)

    assert MM > 0

@pytest.mark.parametrize(
    "fluid,T",
   [
    ("Carbon dioxide",455),
    ("Carbon monoxide",785),
    ("Steam",3000),
    ("Oxygen gas",200),
    ("Nitrogen gas",1029),
   ] 
)
def test_can_compute_enthalpy(fluid,T):
    h = pyhe.ideal_gas_enthalpy(fluid,T)
    assert np.isreal(h)

@pytest.mark.parametrize(
    "fluid,T",
   [
    ("Carbon dioxide",2038),
    ("Carbon monoxide",298),
    ("Steam",234),
    ("Oxygen gas",394),
    ("Nitrogen gas",1030),
   ] 
)
def test_can_compute_entropy(fluid,T):
    s = pyhe.ideal_gas_absolute_entropy(fluid,T)
    assert np.isreal(s)