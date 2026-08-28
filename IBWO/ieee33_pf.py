from pathlib import Path
import numpy as np
import pandapower as pp

CURRENT_DIR = Path(__file__).parent
PROJECT_ROOT = CURRENT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"

BASE_P_MW = np.array([
    0, .010, .009, .012, .006, .006, .020, .020, .060, .060, .0045,
    .0045, .006, .006, .012, .012, .006, .006, .009, .009, .009, .009,
    .009, .009, .042, .042, .006, .006, .006, .012, .012, .006, .006])

#计算负荷比例
LOAD_RATIO = BASE_P_MW / BASE_P_MW.sum()


def build_ieee33_network(slack_vm=1.0):
    net = pp.create_empty_network(sn_mva=10, name="IEEE 33 bus radial feeder")
    for bus in range(33):
        pp.create_bus(net, vn_kv=12.66, name=f"Bus {bus}")
    pp.create_ext_grid(net, bus=0, vm_pu=slack_vm, va_degree=0, name="Slack")
    lines = [(0,1,.0922,.0470),(1,2,.4930,.2511),(2,3,.3660,.1864),(3,4,.3811,.1941),(4,5,.8190,.7070),(5,6,.1872,.6188),(6,7,.7114,.2351),(7,8,1.03,.74),(8,9,1.044,.74),(9,10,.1966,.065),(10,11,.3744,.1238),(11,12,1.468,1.155),(12,13,.5416,.7129),(13,14,.591,.526),(14,15,.7463,.545),(15,16,1.289,1.721),(16,17,.372,.574),(1,18,.164,.1565),(18,19,1.5042,1.3554),(19,20,.4095,.4784),(20,21,.7089,.9373),(2,22,.4512,.3083),(22,23,.898,.7091),(23,24,.896,.7011),(5,25,.203,.1034),(25,26,.2842,.1447),(26,27,1.059,.9337),(27,28,.8042,.7006),(28,29,.5075,.2585),(29,30,.9744,.963),(30,31,.3105,.3619),(31,32,.341,.5362)]
    for f, t, r, x in lines:
        pp.create_line_from_parameters(net, f, t, 1, r, x, 0, .4, name=f"Line {f}-{t}")
    return net

__all__ = ['build_ieee33_network', 'LOAD_RATIO']