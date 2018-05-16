# Import modules
import pytest
import numpy as np

# Import from package
from pyswarms.single import LocalBestPSO
from pyswarms.utils.functions.single_obj import sphere_func

@pytest.mark.parametrize('options', [
    {'c2':0.7, 'w':0.5, 'k': 2, 'p': 2},
    {'c1':0.5, 'w':0.5, 'k': 2, 'p': 2},
    {'c1':0.5, 'c2':0.7, 'k': 2, 'p': 2},
    {'c1':0.5, 'c2':0.7, 'w':0.5, 'p': 2},
    {'c1':0.5, 'c2':0.7, 'w':0.5, 'k': 2}
])
def test_keyword_exception(options):
    """Tests if exceptions are thrown when keywords are missing"""
    with pytest.raises(KeyError):
        LocalBestPSO(5, 2, options)

@pytest.mark.parametrize('options', [
    {'c1':0.5, 'c2':0.7, 'w':0.5, 'k':-1, 'p':2},
    {'c1':0.5, 'c2':0.7, 'w':0.5, 'k':6, 'p':2},
    {'c1':0.5, 'c2':0.7, 'w':0.5, 'k':2, 'p':5}
])
def test_invalid_k_or_p_values(options):
    """Tests if exception is thrown when passing
    an invalid value for k or p"""
    with pytest.raises(ValueError):
        LocalBestPSO(5, 2, options)

@pytest.mark.parametrize('bounds', [
    tuple(np.array([-5,-5])),
    (np.array([-5,-5,-5]), np.array([5,5])),
    (np.array([-5,-5,-5]), np.array([5,5,5]))
])
def test_bounds_size_exception(bounds, options):
    """Tests if exceptions are raised when bound sizes are wrong"""
    with pytest.raises(IndexError):
        LocalBestPSO(5, 2, options=options, bounds=bounds)

@pytest.mark.parametrize('bounds', [
    (np.array([5,5]), np.array([-5,-5])),
    (np.array([5,-5]), np.array([-5,5]))
])
def test_bounds_maxmin_exception(bounds, options):
    """Tests if the max bounds is less than min bounds and vice-versa"""
    with pytest.raises(ValueError):
        LocalBestPSO(5, 2, options=options, bounds=bounds)

@pytest.mark.parametrize('bounds',[
    [np.array([-5, -5]), np.array([5,5])],
    np.array([np.array([-5, -5]), np.array([5, 5])])
])
def test_bound_type_exception(bounds, options):
    """Tests if exception is raised when bound type is not a tuple"""
    with pytest.raises(TypeError):
        LocalBestPSO(5,2, options=options, bounds=bounds)

@pytest.mark.parametrize('velocity_clamp', [[1, 3],np.array([1, 3])])
def test_vclamp_type_exception(velocity_clamp, options):
    """Tests if exception is raised when velocity_clamp type is not a
    tuple"""
    with pytest.raises(TypeError):
        LocalBestPSO(5, 2, velocity_clamp=velocity_clamp, options=options)

@pytest.mark.parametrize('velocity_clamp', [(1,1,1), (2,3,1)])
def test_vclamp_shape_exception(velocity_clamp, options):
    """Tests if exception is raised when velocity_clamp's size is not equal
    to 2"""
    with pytest.raises(IndexError):
        LocalBestPSO(5, 2, velocity_clamp=velocity_clamp, options=options)

@pytest.mark.parametrize('velocity_clamp', [(3,2),(10,8)])
def test_vclamp_maxmin_exception(velocity_clamp, options):
    """Tests if the max velocity_clamp is less than min velocity_clamp and
    vice-versa"""
    with pytest.raises(ValueError):
        LocalBestPSO(5, 2, velocity_clamp=velocity_clamp, options=options)

@pytest.mark.parametrize('err, init_pos',
    [(IndexError, [1.5, 3.2, 2.5]), (TypeError, (0.1, 1.5))])
def test_init_pos_exception(err, init_pos, options):
    """Tests if exception is thrown when init_pos is not a list or of different shape"""
    with pytest.raises(err):
        LocalBestPSO(5, 2, init_pos=init_pos, options=options)

def test_reset_default_values(lbest_reset):
    """Tests if best cost and best pos are set properly when the reset()
    method is called"""
    assert lbest_reset.best_cost == np.inf
    assert lbest_reset.best_pos == None

def test_training_history_shape(lbest_history):
    """Test if training histories are of expected shape"""
    assert lbest_history.get_cost_history.shape == (1000,)
    assert lbest_history.get_mean_pbest_history.shape == (1000,)
    assert lbest_history.get_mean_neighbor_history.shape == (1000,)
    assert lbest_history.get_pos_history.shape == (1000, 10, 2)
    assert lbest_history.get_velocity_history.shape == (1000, 10, 2)

def test_ftol_effect(options):
    """Test if setting the ftol breaks the optimization process accodingly"""
    pso = LocalBestPSO(10, 2, options=options, ftol=1e-1)
    pso.optimize(sphere_func, 2000, verbose=0)
    assert pso.get_cost_history.shape != (2000,)
