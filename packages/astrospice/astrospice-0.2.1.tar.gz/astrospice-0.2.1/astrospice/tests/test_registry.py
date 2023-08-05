import pytest
from astropy.table import Table

from astrospice import Body, SPKKernel, registry

# Ignore dubious year warnings for years a while in the future
pytestmark = pytest.mark.filterwarnings(r'ignore:ERFA function.*dubious year')


@pytest.mark.parametrize('body', registry.bodies)
def test_search(body):
    kernels = registry.get_available_kernels(body)
    assert isinstance(kernels, Table)


def test_get_kernels():
    k = registry.get_kernels('psp', 'predict', version=35)
    assert isinstance(k, list)
    assert len(k) == 1
    assert isinstance(k[0], SPKKernel)


def test_errors():
    with pytest.raises(ValueError, match='not a body not in list'):
        registry.get_kernels('not a body', 'recon')

    msg = 'blah is not one of the known kernel types for psp'
    with pytest.raises(ValueError, match=msg):
        registry.get_kernels('psp', 'blah')

    msg = 'No kernels available for psp, type=predict, version=1'
    with pytest.raises(ValueError, match=msg):
        registry.get_kernels('psp', 'predict', version=1)


def test_get_latest():
    kernel = registry.get_latest_kernel('psp', 'predict')
    assert isinstance(kernel, SPKKernel)
    assert kernel.bodies == [Body('SOLAR PROBE PLUS')]
