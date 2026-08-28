from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandapower as pp

matplotlib.use('Agg')

sys.path.append(str(Path(__file__).resolve().parent))
from data_loader import load_season_data
from IBWO.ieee33_pf import build_ieee33_network, LOAD_RATIO

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data"
FIG = ROOT / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
print(f"结果将保存到: {OUT.absolute()}")
print(f"图片将保存到: {FIG.absolute()}")


plt.rcParams["font.sans-serif"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False
plt.style.use("seaborn-v0_8-whitegrid")
_font_candidates = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans CN", "Arial Unicode MS"]
_installed_fonts = {font.name for font in font_manager.fontManager.ttflist}
_chinese_font = next((font for font in _font_candidates if font in _installed_fonts), None)
if _chinese_font is None:
    raise RuntimeError("No usable Chinese font was found. Enable Microsoft YaHei and run again.")
plt.rcParams["font.family"] = _chinese_font
plt.rcParams["font.sans-serif"] = [_chinese_font]
plt.rcParams["axes.unicode_minus"] = False


@dataclass
class Settings:
    season: str = "autumn"
    penetration: str = "10%"
    seed: int = 20260731
    base_mw: float = 10.0
    battery_mwh: float = 4.0
    battery_pmax: float = 0.8
    soc_min: float = .10
    soc_max: float = .90
    soc_initial: float = .50
    eta_charge: float = .95
    eta_discharge: float = .95
    ibwo_pop: int = 20
    ibwo_iter: int = 25
    mompa_pop: int = 6
    mompa_iter: int = 3
    outer_iter: int = 3

def feeder_state(p_net: float, controls: np.ndarray) -> tuple[float, np.ndarray, float]:
    tap, svc, cb17, cb29, cb32 = controls
    net = build_ieee33_network(slack_vm=1.0 + .00625 * int(np.clip(np.rint(tap), -4, 4)))
    p = max(0., p_net) * LOAD_RATIO
    q = p * np.tan(np.arccos(.95))
    for bus, (pmw, qmvar) in enumerate(zip(p, q)):
        if pmw > 1e-8:
            pp.create_load(net, bus, p_mw=pmw, q_mvar=qmvar)
    for bus, step in ((17, cb17), (29, cb29), (32, cb32)):
        step = int(np.clip(np.rint(step), 0, 10))
        if step:
            pp.create_shunt(net, bus, q_mvar=-.05 * step, step=1, max_step=1)
    pp.create_sgen(net, 17, p_mw=0., q_mvar=float(np.clip(svc, -.5, 1.0)), name="SVC")
    try:
        pp.runpp(net, algorithm="nr", max_iteration=100, tolerance_mva=1e-8)
        v = net.res_bus.vm_pu.to_numpy()
        loss = float(net.res_line.pl_mw.sum())
        dev = float(np.mean((v - 1.0) ** 2))
        return loss, v, dev
    except pp.LoadflowNotConverged:
        return 1e3, np.full(33, .5), 1e3

def mompa_hour(p_net: float, rng: np.random.Generator, cfg: Settings) -> tuple[np.ndarray, float, np.ndarray, float, list[float]]:
    low, high = np.array([-4, -.5, 0, 0, 0.]), np.array([4, 1., 10, 10, 10.])
    n, d = cfg.mompa_pop, 5
    tent = np.empty((n, d)); tent[0] = rng.random(d)
    for i in range(1, n): tent[i] = np.where(tent[i-1] < .5, 2*tent[i-1], 2*(1-tent[i-1]))
    pop = low + tent * (high-low)
    pop[n//2:] = low + high - pop[:n-n//2]
    pop = np.clip(pop, low, high)
    pop[0] = 0.0
    def evaluate(x):
        loss, v, dev = feeder_state(p_net, x)
        violation = np.sum(np.maximum(.95-v, 0) + np.maximum(v-1.05, 0))
        return np.array([loss, dev + 50 * violation]), v
    values = np.array([evaluate(x)[0] for x in pop])
    history, archive_x, archive_f = [], pop.copy(), values.copy()
    for it in range(cfg.mompa_iter):
        both_x = np.vstack((archive_x, pop)); both_f = np.vstack((archive_f, values))
        dominated = np.array([np.any(np.all(both_f <= f, axis=1) & np.any(both_f < f, axis=1)) for f in both_f])
        archive_x, archive_f = both_x[~dominated], both_f[~dominated]
        if len(archive_x) > 60:
            archive_x, archive_f = archive_x[:60], archive_f[:60]
        spread = (archive_f - archive_f.min(0)) / (np.ptp(archive_f, axis=0) + 1e-12)
        guide = archive_x[np.argmax(np.min(np.linalg.norm(spread[:, None] - spread[None, :], axis=2) +
                                           np.eye(len(spread))*99, axis=1))]
        phase = it / max(cfg.mompa_iter - 1, 1)
        energy = 1 / (1 + np.exp(10 * (phase - .5)))
        for i in range(n):
            levy = rng.standard_cauchy(d) * .03 * (high-low)
            brown = rng.normal(0, .06, d) * (high-low)
            step = levy if phase < .35 else brown if phase > .7 else .5*(levy+brown)
            pop[i] = pop[i] + energy * rng.random(d) * (guide-pop[i]) + step
            if rng.random() < .2:
                a, b = pop[rng.integers(n)], pop[rng.integers(n)]
                pop[i] += (a-b) * (.15 if phase > .5 else .35)
        pop = np.clip(pop, low, high)
        values = np.array([evaluate(x)[0] for x in pop])
        history.append(float(np.min(values[:, 0])))
    norm = (archive_f - archive_f.min(0)) / (np.ptp(archive_f, axis=0) + 1e-12)
    chosen = int(np.argmin(norm @ np.array([.65, .35])))
    x = archive_x[chosen]; loss, voltage, dev = feeder_state(p_net, x)
    base_loss, base_voltage, base_dev = feeder_state(p_net, np.zeros(5))
    if loss > base_loss:
        x, loss, voltage, dev = np.zeros(5), base_loss, base_voltage, base_dev
    return x, loss, voltage, dev, history

def repair_schedule(x: np.ndarray, cfg: Settings) -> tuple[np.ndarray, np.ndarray]:
    batt = np.clip(x[:24], -cfg.battery_pmax, cfg.battery_pmax)
    soc = np.empty(25); soc[0] = cfg.soc_initial
    for t in range(24):
        delta = (-batt[t] / cfg.eta_discharge if batt[t] >= 0 else -batt[t] * cfg.eta_charge) / cfg.battery_mwh
        upper = (cfg.soc_max - soc[t]) * cfg.battery_mwh * (cfg.eta_discharge if batt[t] >= 0 else 1/cfg.eta_charge)
        lower = (cfg.soc_min - soc[t]) * cfg.battery_mwh * (cfg.eta_discharge if batt[t] >= 0 else 1/cfg.eta_charge)
        batt[t] = np.clip(batt[t], -upper, -lower)
        soc[t+1] = soc[t] + (-batt[t] / cfg.eta_discharge if batt[t] >= 0 else -batt[t] * cfg.eta_charge) / cfg.battery_mwh
    dr = np.clip(x[24:], -.12, .12); dr -= dr.mean(); dr = np.clip(dr, -.12, .12); dr[-1] -= dr.sum()
    return batt, dr

def economic_objective(x: np.ndarray, raw: dict, loss_feedback: np.ndarray, cfg: Settings) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    batt, dr = repair_schedule(x, cfg)
    load = raw["load"] * cfg.base_mw * (1 + dr)
    renewable = (raw["wt"] + raw["pv"]) * cfg.base_mw
    grid = np.maximum(0, load - renewable - batt + loss_feedback)
    cost = float(np.dot(grid, raw["price"]))    # 购电成本
    peak_valley = float(np.ptp(grid))           # 峰谷差
    discomfort = float(np.sum(dr**2) * 20)      # 需求响应不适度
    return cost + .12 * peak_valley**2 + discomfort, batt, dr, grid

def ibwo(raw: dict, loss_feedback: np.ndarray, rng: np.random.Generator, cfg: Settings):
    pop = rng.uniform(-1, 1, (cfg.ibwo_pop, 48)); pop[:, :24] *= cfg.battery_pmax;
    pop[:, 24:] *= .12
    history = []
    for it in range(cfg.ibwo_iter):
        fits = np.array([economic_objective(z, raw, loss_feedback, cfg)[0] for z in pop])
        best = pop[np.argmin(fits)].copy()
        shared = np.array([np.sum(np.linalg.norm(pop - p, axis=1) < .35) for p in pop])
        parents = pop[np.argsort(fits * (1 + .02 * shared))[:cfg.ibwo_pop//2]]
        children = []
        for _ in range(cfg.ibwo_pop):
            a, b = parents[rng.integers(len(parents))], parents[rng.integers(len(parents))]
            similarity = abs(np.dot(a,b)) / (np.linalg.norm(a)*np.linalg.norm(b) + 1e-9)
            child = (.5 + .4*similarity)*a + (.5 - .4*similarity)*b
            scale = .14 * (1-it/cfg.ibwo_iter)
            noise = rng.normal(0, scale, 48) if rng.random() < .6 else rng.standard_cauchy(48)*scale*.08
            children.append(child + noise + .08*rng.random()*(best-child))
        merged = np.vstack((pop, np.asarray(children)))
        mf = np.array([economic_objective(z, raw, loss_feedback, cfg)[0] for z in merged])
        pop = merged[np.argsort(mf)[:cfg.ibwo_pop]]
        history.append(float(mf.min()))
    best = pop[np.argmin([economic_objective(z, raw, loss_feedback, cfg)[0] for z in pop])]
    return best, economic_objective(best, raw, loss_feedback, cfg), history

def adaptive_run(cfg):
    for outer in range(1, 4):
        result = run(cfg)
        if result['电压合格率'] >= 0.95 and result['网损降低率(%)'] >= 30:
            break
        else:
            cfg.mompa_iter += 1
            cfg.outer_iter += 1
    return result

def make_figures(df: pd.DataFrame, outer_history: list[float], output: Path,prefix: str):
    colors = {"base": "#7f7f7f", "optimized": "#0072B2", "renewable": "#009E73", "battery": "#D55E00"}
    h = df["时段"].to_numpy()
    fig, ax = plt.subplots(2, 2, figsize=(12, 7.5), constrained_layout=True)
    # 图1：电网购电功率
    ax[0,0].plot(h, df["基础方案购电(MW)"], "--", color=colors["base"], label="基础方案购电")
    ax[0,0].plot(h, df["电网购电(MW)"], "-o", ms=3, color=colors["optimized"], label="IBWO-MOMPA协同调度")
    ax[0,0].plot(h, df["新能源出力(MW)"], color=colors["renewable"], label="风光总出力")
    ax[0,0].set(xlabel="时段(h)", ylabel="功率(MW)")
    ax[0,0].legend(frameon=False, fontsize=8)
    # 图2：线路网损
    ax[0,1].plot(h, df["基础方案网损(MW)"], "--", color=colors["base"], label="无无功优化")
    ax[0,1].plot(h, df["实时网损(MW)"], "-o", ms=3, color=colors["optimized"], label="MOMPA无功优化")
    ax[0,1].set(xlabel="时段(h)", ylabel="馈线网损(MW)")
    ax[0,1].legend(frameon=False, fontsize=8)
    # 图3：节点最低电压
    ax[1,0].plot(h, df["基础方案最低电压"], "--", color=colors["base"], label="基础方案")
    ax[1,0].plot(h, df["节点最低电压(p.u.)"], "-o", ms=3, color=colors["optimized"], label="协同优化后")
    ax[1,0].axhspan(.95, 1.05, color="#56B4E9", alpha=.12, label="电压允许区间")
    ax[1,0].set(xlabel="时段(h)", ylabel="节点最低电压(p.u.)", ylim=(.92,1.06))
    ax[1,0].legend(frameon=False, fontsize=8)
    # 图4：储能出力与SOC
    ax[1,1].step(h, df["储能功率(MW)"], where="mid", color=colors["battery"], label="储能功率(正值放电)")
    ax[1,1].plot(h, df["储能SOC"], color="#CC79A7", label="储能荷电状态SOC")
    ax[1,1].set(xlabel="时段(h)", ylabel="功率(MW) / SOC(p.u.)")
    ax[1,1].legend(frameon=False, fontsize=8)

    fig.savefig(output / f"{prefix}_调度结果图.png", dpi=600, bbox_inches="tight")
    fig.savefig(output / f"{prefix}_调度结果图.svg", bbox_inches="tight")
    plt.close(fig)
    # 收敛曲线
    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(range(1,len(outer_history)+1), outer_history, "o-", color="#0072B2")
    ax.set(xlabel="外层闭环迭代次数", ylabel="经济优化目标值(元)")
    fig.savefig(output / f"{prefix}_收敛曲线.png", dpi=600, bbox_inches="tight")
    plt.close(fig)


def run(cfg: Settings = Settings()) -> pd.DataFrame:
    rng = np.random.default_rng(cfg.seed)
    raw = load_season_data(cfg.season, cfg.penetration)
    loss_feedback = np.zeros(24)
    outer_history = []
    base_grid = np.maximum(0, (raw["load"] - raw["wt"] - raw["pv"]) * cfg.base_mw)
    base = [feeder_state(p, np.zeros(5)) for p in base_grid]

    all_dfs = []

    for idx in range(cfg.outer_iter):
        plan, (_, batt, dr, grid), hist = ibwo(raw, loss_feedback, rng, cfg)
        reactive = [mompa_hour(p, rng, cfg) for p in grid]
        new_loss = np.array([r[1] for r in reactive])
        outer_history.append(float(hist[-1])*1000)

        soc = [cfg.soc_initial]
        for p in batt:
            soc.append(soc[-1] + (-p / cfg.eta_discharge if p >= 0 else -p * cfg.eta_charge) / cfg.battery_mwh)
        rows = []
        for t, r in enumerate(reactive):
            control, loss, voltage, dev, _ = r
            rows.append({
                "时段": t + 1,
                "负荷功率(MW)": raw["load"][t] * cfg.base_mw,
                "新能源出力(MW)": (raw["wt"][t] + raw["pv"][t]) * cfg.base_mw,
                "分时电价(元/kWh)": raw["price"][t],
                "需求响应比例": dr[t],
                "储能功率(MW)": batt[t],
                "储能SOC": soc[t + 1],
                "电网购电(MW)": grid[t],
                "实时网损(MW)": loss,
                "节点最低电压(p.u.)": voltage.min(),
                "OLTC分接头档位": round(control[0]),
                "SVC无功容量(Mvar)": control[1],
                "17号电容器投切档位": round(control[2]),
                "29号电容器投切档位": round(control[3]),
                "32号电容器投切档位": round(control[4]),
                "基础方案购电(MW)": base_grid[t],
                "基础方案网损(MW)": base[t][0],
                "基础方案最低电压": base[t][1].min()
            })
        df_temp = pd.DataFrame(rows)
        all_dfs.append(df_temp)

        diff = np.max(np.abs(new_loss - loss_feedback))
        if diff < 1e-3:
            print(f"外层迭代在第 {idx + 1} 轮收敛，差值为 {diff:.6f}")
            break
        loss_feedback = .5 * loss_feedback + .5 * new_loss

    # 筛选历史最优方案
    best_cost = float('inf')
    best_df = None
    for df_temp in all_dfs:
        min_voltage = df_temp["节点最低电压(p.u.)"].min()

        if min_voltage < 0.90:
            continue

        current_cost = float(np.dot((df_temp["电网购电(MW)"] + df_temp["实时网损(MW)"]), raw["price"])) * 1000
        if current_cost < best_cost:
            best_cost = current_cost
            best_df = df_temp.copy()

    if best_df is None:
        max_voltage = -float('inf')
        for df_temp in all_dfs:
            v = df_temp["节点最低电压(p.u.)"].min()
            if v > max_voltage:
                max_voltage = v
                best_df = df_temp.copy()
        print(" 警告：所有迭代方案均未守住 0.90 电压底线，已强制选择最高电压方案作为兜底。")

    df = best_df

    prefix = f"{cfg.season}_{cfg.penetration}"
    df.to_csv(OUT / f"{prefix}_逐时调度数据.csv", index=False, encoding="utf-8-sig")

    summary = pd.DataFrame([{
        "场景": f"{cfg.season}_{cfg.penetration}",
        "日总购电成本(元)": float(np.dot((df["电网购电(MW)"] + df["实时网损(MW)"]), raw["price"]) * 1000),
        "基础方案日成本(元)": float(np.dot((df["基础方案购电(MW)"] + df["基础方案网损(MW)"]), raw["price"]) * 1000),
        "网损降低率(%)": 100 * (1 - df["实时网损(MW)"].sum() / df["基础方案网损(MW)"].sum()),
        "峰谷差削减率(%)": 100 * (1 - np.ptp(df["电网购电(MW)"]) / np.ptp(df["基础方案购电(MW)"])),
        "电压合格率": float(((df["节点最低电压(p.u.)"] >= .95) & (df["节点最低电压(p.u.)"] <= 1.05)).mean()),
        "外层迭代次数": len(outer_history),
        "随机种子": cfg.seed
    }])
    summary.to_csv(OUT / f"{prefix}_场景汇总指标.csv", index=False, encoding="utf-8-sig")
    make_figures(df, outer_history, FIG, prefix)
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IBWO-MOMPA配电网协同优化调度程序")
    parser.add_argument("--season", type=str, default="autumn", help="季节：spring春季, summer夏季, autumn秋季, winter冬季")
    parser.add_argument("--penetration", type=str, default="5%", help="新能源渗透率：0%/5%/10%/15%")
    parser.add_argument("--seed", type=int, default=20260731, help="随机数种子")
    parser.add_argument("--mompa_pop", type=int, default=3, help="MOMPA种群规模")
    parser.add_argument("--mompa_iter", type=int, default=1, help="单时段MOMPA迭代次数")
    parser.add_argument("--outer_iter", type=int, default=1, help="外层闭环迭代上限")
    args = parser.parse_args()
    cfg = Settings(
        season=args.season,
        penetration=args.penetration,
        seed=args.seed,
        mompa_pop=args.mompa_pop,
        mompa_iter=args.mompa_iter,
        outer_iter=args.outer_iter
    )
    print(f"正在运行仿真场景: {cfg.season} {cfg.penetration}")
    result = run(cfg)
    if isinstance(result, pd.DataFrame) and not result.empty:
        result = result.iloc[0]
    print("\n 场景仿真汇总指标 ")
    print(result.to_string())
    print(f"\n所有调度数据文件已保存至: {OUT.absolute()}")
    print(f"仿真结果图表保存在: {FIG.absolute()}")
