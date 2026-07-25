import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def fhzy(detaprd, a):
    """死区-线性-饱和转移率函数"""
    detaprs = abs(detaprd)
    fmax = 1.0
    K = 1.0
    if detaprs <= a:
        return 0.0
    elif detaprs <= a + fmax / K:
        return K * (detaprs - a)
    else:
        return fmax

def demand_response(load_pu, price, base_power=200, a=0.08,
                    ratio1=0.7, ratio2=0.2, ratio3=0.1):
    """
    需求侧响应预处理
    参数：
        load_pu: 长度24的数组，原始负荷标幺值
        price: 长度24的分时电价
        base_power: 基准功率（kW）
        a: 死区阈值
        ratio1~3: 三类负荷比例
    返回：
        load_after: 响应后负荷（标幺值，未乘基准）
    """
    pload = np.array(load_pu) * base_power  # 转为实际功率 kW
    pl1 = ratio1 * pload
    pl2 = ratio2 * pload
    pl3 = ratio3 * pload

    jz_pri = 0.9  # 基准电价
    detapr = price - jz_pri

    colz = np.where(detapr > 0)[0]  # 电价上升时段索引
    colf = np.where(detapr < 0)[0]  # 电价下降时段索引

    # ---- Ⅰ类负荷转移 ----
    linj = np.sum(np.abs(detapr[colf]))
    lini = np.sum(np.abs(detapr[colz]))
    lam_pl2 = pl2.copy()

    for t in range(24):
        if t in colz:
            fdetap = fhzy(detapr[t], a)
            linp = 0.0
            if linj > 0:
                for kj in colf:
                    linp += fdetap * np.abs(detapr[kj]) * pl2[t] / linj
            lam_pl2[t] = pl2[t] - linp
        elif t in colf:
            fdetap = fhzy(detapr[t], a)
            linp = 0.0
            if lini > 0:
                for ki in colz:
                    linp += fdetap * np.abs(detapr[ki]) * pl2[t] / lini
            lam_pl2[t] = pl2[t] + linp

    # ---- Ⅱ类负荷弹性 ----
    Est = np.zeros((24, 24))
    for i in range(24):
        for j in range(24):
            if i == j:
                Est[i, j] = -1.0
            elif i == j + 1:
                Est[i, j] = 0.4
            elif i + 1 == j:
                Est[i, j] = 0.2
            else:
                Est[i, j] = 0.05

    lam_pl3 = pl3.copy()
    for t in range(24):
        # 注意：原代码中计算时似乎未使用 e0/e1/e2，直接用了 Est 和 detapr/price
        # 这里保持原意
        lam_pl3[t] = pl3[t] + pl3[t] * np.dot(Est[t, :], detapr / price)

    # 响应后总负荷（实际功率）
    load_after = pl1 + lam_pl2 + lam_pl3
    # 返回标幺值（除以基准）
    return load_after / base_power

# 示例使用
if __name__ == '__main__':
    # 读取数据（例如春季典型日，渗透率0%）
    df = pd.read_excel('electric_zero.xlsx', sheet_name='0%')
    load_pu = df['春'].values[:24]  # 假设列名为'春'，取前24行
    price = pd.read_excel('electric_zero.xlsx', sheet_name='电价').values.flatten()

    load_new = demand_response(load_pu, price)
    # 绘图对比
    plt.plot(load_pu, label='Original')
    plt.plot(load_new, label='After DR')
    plt.legend()
    plt.show()