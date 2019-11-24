"""
1) Experiments on strategic voting risk depending on number of voters and number of candidates
2) Experiments on runtime limitatiosn
"""

from preference_creator import PreferenceCreator as PC
from voting_schemes_runner import VotingSchemesRunner as VSR
from tactical_voting import TacticalVoting as TV
from itertools import permutations
import integration_tests
import numpy as np
import pandas as pd
import seaborn as sns
import plotly_express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import time
import os
import matplotlib
from matplotlib import cm

TARGET_DIR = "experiments"
FIG_DIR = os.path.join(TARGET_DIR, "figs")
TARGET_FILE = "experiments/log.csv"

def experiment(max_n_candidates, max_n_voters):
    if not os.path.exists(TARGET_DIR):
        os.mkdir(TARGET_DIR)
    voting_schemes = ['1: Plurality Voting', '2: Voting for two', '3: Anti-Plurality Voting', '4: Borda Voting']
    vs_list = []
    v_list = []
    c_list = []
    strat_voting_list = []
    happiness_list = []
    run_time_list = []  # time needed to explore tactical voting options
    # TODO: fix error here!
    for vs in range(4):  # voting schemes:
        print(f"Starting voting scheme {vs}")
        for c in range(2, max_n_candidates+1):
            for v in range(2, max_n_voters+1):
                pc, vsr, tv = integration_tests.integration_MxN(c, v, vs, seed=42)
                avg_happiness = sum(vsr.get_happiness(pc.pref_mat, vsr.results))/v

                start_time = time.time()
                tv.bullet_voting()       
                tv.compromising_strategy()
                end_time = time.time()

                strat_voting_risk = sum([1 if len(i)>0 else 0 for i in tv.strategic_voting_options]) /pc.num_voters
                
                vs_list.append(voting_schemes[vs][3:])
                v_list.append(v)
                c_list.append(c)
                strat_voting_list.append(strat_voting_risk)
                happiness_list.append(avg_happiness)
                run_time_list.append(np.round(end_time-start_time, 2))

    df_new = pd.DataFrame({
            "voting_scheme": vs_list,
            "n_voters": v_list,
            "n_candidates": c_list,
            "strat_voting_risk": strat_voting_list,
            "avg_happiness": happiness_list,
            "run_time": run_time_list
        })
    df_new.to_csv(TARGET_FILE, index=True)

### Weird plotly magic
# import plotly
# plotly.io.orca.config.executable = "C:\\Users\\alexa\\AppData\\Roaming\\npm\\orca.cmd"
# plotly.io.orca.config.save()

viridis = [
    "#440154","#440558","#450a5c","#450e60","#451465","#461969",
    "#461d6d","#462372","#472775","#472c7a","#46307c","#45337d",
    "#433880","#423c81","#404224","#3f4686","#3d4a88","#3c4f8a",
    "#3b522b","#39558b","#37598c","#365c8c","#34608c","#33638d",
    "#31678d","#2f6b8d","#2d6e8e","#2c722e","#2b748e","#29788e",
    "#287c8e","#277f8e","#25848d","#24878d","#238b8d","#222f8d",
    "#21922d","#22958b","#23988a","#239b89","#249f87","#25a226",
    "#25a584","#26a883","#27ab82","#29ae80","#2eb17d","#35b479",
    "#3cb875","#42bb72","#49be6e","#4ec16b","#55c467","#5cc863",
    "#61c960","#6bcc5a","#72ce55","#7cd04f","#85d349","#8dd544",
    "#97d73e","#9ed93a","#a8db34","#b0dd31","#b8de30","#c3df2e",
    "#cbe02d","#d6e22b","#e1e329","#eae428","#f5e626","#fde725"
]

custom_viridis = [
    "#440154", # "#461969",
    "#461d6d", # "#45337d",
    "#433880","#3c4f8a",
    "#3b522b",# "#33638d",
    "#31678d",# "#29788e",
    "#287c8e","#222f8d",
    "#21922d",# "#25a226",
    "#25a584",# "#35b479",
    "#3cb875","#5cc863",
    "#61c960",# "#8dd544",
    "#97d73e",# "#c3df2e",
    "#cbe02d","#fde725"
]

def visualize():
    """Visualize experiment data per voting schme"""
    if not os.path.exists(FIG_DIR):
        os.mkdir(FIG_DIR)
    df = pd.read_csv(TARGET_FILE, index_col=0)
    for i in df["voting_scheme"].unique():
        df_plt = df.loc[df.voting_scheme==i, :]

        # strat_voting image
        fig = px.scatter(df_plt, x="n_candidates", y="n_voters", size="strat_voting_risk",
            color="strat_voting_risk", color_continuous_scale=px.colors.sequential.Viridis,
            width=800, height=800).update_layout(
            xaxis_title="Number of Candidates",
            yaxis_title="Number of Voters",
            font=dict(
                family="Courier New, monospace",
                size=22,
                color="#1f1f1f"))
        fig.write_image(os.path.join(FIG_DIR, str(i)).replace(" ", "_")+"_strat_voting.png")

        # run time image
        fig = px.histogram(df_plt, x="n_candidates", y="n_voters", color="run_time",
            color_discrete_sequence=custom_viridis, width=800, height=800).update_layout(
            xaxis_title="Number of Candidates",
            yaxis_title="Number of Voters",
            font=dict(
                family="Courier New, monospace",
                size=22,
                color="#1f1f1f"))
        # TODO: rename y axis
        fig.write_image(os.path.join(FIG_DIR, str(i)).replace(" ", "_")+"_runtime.png")

if __name__ == "__main__":
    experiment(10, 10)
    visualize()

