from src.simcore.atmosphere import isa_density

def test_density_decreases_with_altitude():
    rho_sea_level = isa_density(0)
    rho_high = isa_density(5000)
    assert rho_high < rho_sea_level

def test_sea_level_density_is_realistic():
    rho = isa_density(0)
    assert 1.19 < rho < 1.23  # real sea-level air density ≈ 1.225 kg/m^3