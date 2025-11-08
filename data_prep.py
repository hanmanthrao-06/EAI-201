# data_prep.py (robust version)
import pandas as pd
import numpy as np
import os
import sys

RAW_COMBINED = "data/raw/combined_raw.csv"
RAW_DIR = "data/raw"
OUT_CLEAN = "data/clean/dataset_clean.csv"

def find_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

def safe_load(path):
    if not os.path.exists(path):
        print(f"ERROR: file not found -> {path}")
        return None
    print(f"Loading: {path}")
    try:
        df = pd.read_csv(path)
        print(f"  Loaded {len(df)} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        print("ERROR reading CSV:", e)
        return None

def build_combined():
    # If combined_raw exists, use it. Otherwise try to build minimal combined from team_appearances.
    if os.path.exists(RAW_COMBINED):
        return safe_load(RAW_COMBINED)

    print("combined_raw.csv not found — attempting to create from team_appearances.csv + tournaments.csv + teams.csv")
    ta = safe_load(os.path.join(RAW_DIR, "team_appearances.csv"))
    t = safe_load(os.path.join(RAW_DIR, "tournaments.csv"))
    teams = safe_load(os.path.join(RAW_DIR, "teams.csv"))

    if ta is None or t is None or teams is None:
        print("Could not build combined dataset automatically. Please ensure data/raw contains team_appearances.csv, tournaments.csv and teams.csv or a combined_raw.csv")
        return None

    # attempt to merge sensible columns
    # ensure id columns exist
    id_team = find_column(ta, ["team_id","teamId","team"])
    id_tourn = find_column(ta, ["tournament_id","tournamentId","tournament_id_x","tournament"])
    if id_team is None or id_tourn is None:
        print("Missing team / tournament id columns in team_appearances.csv. Columns present:", ta.columns.tolist())
        return None

    # minimal keep columns (take what exists)
    keep = [id_team, id_tourn]
    for cand in ["goals_for","goals_scored","goals_for_count","goals"]:
        if cand in ta.columns:
            keep.append(cand)
            break
    for cand in ["goals_against","goals_conceded","goals_against_count"]:
        if cand in ta.columns:
            keep.append(cand)
            break
    for cand in ["wins","wins_count","win_count"]:
        if cand in ta.columns:
            keep.append(cand)
            break
    for cand in ["losses","losses_count","loss_count"]:
        if cand in ta.columns:
            keep.append(cand)
            break
    for cand in ["draws","draws_count","tie_count"]:
        if cand in ta.columns:
            keep.append(cand)
            break
    for cand in ["matches_played","matches_played_count","matches"]:
        if cand in ta.columns:
            keep.append(cand)
            break

    keep = list(dict.fromkeys(keep))  # dedupe
    ta_small = ta.loc[:, [c for c in keep if c in ta.columns]]

    # merge names/years
    t_id = find_column(t, ["tournament_id","tournamentId","tournament_id_x","id"])
    t_name = find_column(t, ["tournament_name","name","tournament","edition"])
    teams_id = find_column(teams, ["team_id","id","teamId"])
    team_name = find_column(teams, ["team_name","team","name","teamName"])

    # rename for consistency before merge
    ta_small = ta_small.rename(columns={id_team: "team_id", id_tourn: "tournament_id"})
    if teams_id is not None and team_name is not None:
        teams_small = teams[[teams_id, team_name]].rename(columns={teams_id:"team_id", team_name:"team"})
    else:
        teams_small = None

    if t_id is not None and t_name is not None:
        t_small = t[[t_id, t_name]].rename(columns={t_id:"tournament_id", t_name:"tournament"})
    else:
        t_small = None

    df = ta_small.copy()
    if teams_small is not None:
        df = df.merge(teams_small, on="team_id", how="left")
    if t_small is not None:
        df = df.merge(t_small, on="tournament_id", how="left")

    # attempt to standardize numeric columns' names
    rename_map = {}
    if "goals_for" not in df.columns:
        g1 = find_column(df, ["goals_for","goals_scored","goals_for_count","goals"])
        if g1: rename_map[g1] = "goals_for"
    if "goals_against" not in df.columns:
        g2 = find_column(df, ["goals_against","goals_conceded","goals_against_count"])
        if g2: rename_map[g2] = "goals_against"
    if "wins" not in df.columns:
        w = find_column(df, ["wins","wins_count","win_count"])
        if w: rename_map[w] = "wins"
    if "losses" not in df.columns:
        l = find_column(df, ["losses","losses_count","loss_count"])
        if l: rename_map[l] = "losses"
    if "draws" not in df.columns:
        d = find_column(df, ["draws","draws_count","tie_count"])
        if d: rename_map[d] = "draws"
    if "matches_played" not in df.columns:
        m = find_column(df, ["matches_played","matches_played_count","matches"])
        if m: rename_map[m] = "matches_played"

    if rename_map:
        df = df.rename(columns=rename_map)
        print("Renamed columns:", rename_map)

    # save combined for inspection
    os.makedirs(RAW_DIR, exist_ok=True)
    df.to_csv(RAW_COMBINED, index=False)
    print("Saved combined raw to", RAW_COMBINED)
    return df

def compute_is_finalist(df):
    # if is_finalist present return df
    if "is_finalist" in df.columns:
        print("is_finalist already present.")
        df["is_finalist"] = df["is_finalist"].fillna(0).astype(int)
        return df

    # try to build from tournament_standings.csv
    standings_path = os.path.join(RAW_DIR, "tournament_standings.csv")
    if not os.path.exists(standings_path):
        print("tournament_standings.csv not found; cannot create is_finalist automatically.")
        df["is_finalist"] = 0
        return df

    st = safe_load(standings_path)
    # try to detect id columns
    st_tid = find_column(st, ["tournament_id","tournamentId","tournament_id_x","tournament"])
    st_team = find_column(st, ["team_id","teamId","team"])

    if st_tid is None or st_team is None or "position" not in st.columns:
        print("Cannot detect required columns in tournament_standings.csv; columns:", st.columns.tolist())
        df["is_finalist"] = 0
        return df

    st_small = st[[st_tid, st_team, "position"]].rename(columns={st_tid:"tournament_id", st_team:"team_id"})
    st_small["is_finalist"] = st_small["position"].apply(lambda x: 1 if int(x) in (1,2) else 0)

    # if our df has numeric tournament_id and team_id join on them; otherwise try to join on team name + tournament
    if "tournament_id" in df.columns and "team_id" in df.columns:
        merged = df.merge(st_small[["tournament_id","team_id","is_finalist"]], on=["tournament_id","team_id"], how="left")
        merged["is_finalist"] = merged["is_finalist"].fillna(0).astype(int)
        return merged
    else:
        # fallback: try by team name + tournament if names exist
        if "team" in df.columns and "tournament" in df.columns and "team" in st.columns:
            print("Falling back to merging by team name + tournament (may be imperfect).")
            # ensure st has team names (might not)
            st_names = st.copy()
            if "team" not in st_names.columns:
                # try to get team name from teams.csv
                teams = safe_load(os.path.join(RAW_DIR, "teams.csv"))
                if teams is not None:
                    tname_col = find_column(teams, ["team_name","team","name"])
                    tid_col = find_column(teams, ["team_id","id"])
                    if tname_col and tid_col:
                        teams_small = teams[[tid_col,tname_col]].rename(columns={tid_col:"team_id", tname_col:"team"})
                        st_names = st.merge(teams_small, on="team_id", how="left")
            # merge
            st_names_small = st_names[[find_column(st_names, ["team","team_name","name"]), find_column(st_names, ["tournament_id","tournamentId","tournament_id_x","tournament"]), "position"]]
            # normalize column names
            st_names_small = st_names_small.rename(columns={st_names_small.columns[0]:"team", st_names_small.columns[1]:"tournament", "position":"position"})
            st_names_small["is_finalist"] = st_names_small["position"].apply(lambda x: 1 if int(x) in (1,2) else 0)
            merged = df.merge(st_names_small[["team","tournament","is_finalist"]], on=["team","tournament"], how="left")
            merged["is_finalist"] = merged["is_finalist"].fillna(0).astype(int)
            return merged
        else:
            print("No suitable join keys to create is_finalist. Filling with zeros.")
            df["is_finalist"] = 0
            return df

def basic_clean(df):
    print("Basic cleaning...")
    df = df.drop_duplicates()
    df = df.dropna(axis=1, how="all")
    # fill numeric with median, strings with Unknown
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("Unknown")
    return df

def engineer_features(df):
    print("Feature engineering...")
    # ensure goals exist
    if "goals_for" in df.columns and "goals_against" in df.columns:
        df["goal_diff"] = df["goals_for"] - df["goals_against"]
    # win/loss/draw column detection
    wins_col = find_column(df, ["wins","wins_count","win_count"])
    losses_col = find_column(df, ["losses","losses_count","loss_count"])
    draws_col = find_column(df, ["draws","draws_count","tie_count"])
    matches_col = find_column(df, ["matches_played","matches_played_count","matches"])

    # set zero-safe denominator
    if matches_col:
        denom = df[matches_col].replace(0, np.nan)
    else:
        denom = None

    if wins_col and denom is not None:
        df["win_rate"] = df[wins_col] / denom
    else:
        df["win_rate"] = 0.0

    if losses_col and denom is not None:
        df["loss_rate"] = df[losses_col] / denom
    else:
        df["loss_rate"] = 0.0

    if draws_col and denom is not None:
        df["draw_rate"] = df[draws_col] / denom
    else:
        df["draw_rate"] = 0.0

    # fill any remaining NaNs with 0
    df["win_rate"] = df["win_rate"].fillna(0.0)
    df["loss_rate"] = df["loss_rate"].fillna(0.0)
    df["draw_rate"] = df["draw_rate"].fillna(0.0)

    return df

def keep_and_save(df):
    # choose a compact set of columns to keep if they exist
    keep_candidates = ["team","team_id","season","year","tournament","tournament_id",
                       "goals_for","goals_against","goal_diff","wins","losses","draws",
                       "matches_played","win_rate","loss_rate","draw_rate","is_finalist"]
    keep = [c for c in keep_candidates if c in df.columns]
    if "team" not in keep and "team_id" in keep:
        # try to get team name from teams.csv
        teams = safe_load(os.path.join(RAW_DIR,"teams.csv"))
        if teams is not None:
            name_col = find_column(teams, ["team_name","team","name"])
            id_col = find_column(teams, ["team_id","id"])
            if id_col and name_col:
                teams_small = teams[[id_col,name_col]].rename(columns={id_col:"team_id", name_col:"team"})
                df = df.merge(teams_small, on="team_id", how="left")
                if "team" in df.columns:
                    keep.insert(0,"team")

    # prefer season over year
    if "year" in df.columns and "season" not in df.columns:
        df = df.rename(columns={"year":"season"})
    if "season" in df.columns:
        if "season" not in keep:
            keep.append("season")

    os.makedirs(os.path.dirname(OUT_CLEAN), exist_ok=True)
    df.to_csv(OUT_CLEAN, index=False)
    print("Saved cleaned dataset to:", OUT_CLEAN)
    print("Final columns:", df.columns.tolist())
    print("Rows:", len(df))

def main():
    df = build_combined()
    if df is None:
        print("No combined data available. Exiting.")
        sys.exit(1)

    df = basic_clean(df)
    df = compute_is_finalist(df)
    df = engineer_features(df)
    keep_and_save(df)

if __name__ == "__main__":
    main()
