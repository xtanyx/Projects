import pandas as pd

def make_csv(frame, disaster_name):

    fr_dis = frame[frame["Disaster Type"] == disaster_name]
    fr_dis = fr_dis[["ISO","Start Year","Start Month", "End Month"]]
    fr_dis["month_diff"] = fr_dis["End Month"] - fr_dis["Start Month"] + 1 # The plus 1 is to include the "Start Month"
    fr_dis.loc[fr_dis["month_diff"] <= 0, "month_diff"] += 12

    # What is the number of floods per country per month of every year 
    fr_dis_grp = pd.DataFrame({'Count': fr_dis.groupby(["Start Year", "Start Month","ISO"]).size()}).reset_index()
    dis_csv = fr_dis_grp.pivot(values="Count",columns="ISO", 
                               index=["Start Year","Start Month"]).reset_index().fillna(0)
    dis_csv.to_csv(f"./{disaster_name}.csv", index=False)

frame = pd.read_excel("./natural_disasters.xlsx",sheet_name=["EM-DAT Data"])
print(type(frame))
frame = frame["EM-DAT Data"]

# Remove uneccesary columns
frame_rem = frame[["DisNo.","Disaster Type","Disaster Subtype","ISO",
                   "Country","Start Year","Start Month", "End Month"]]

# Remove NaN values w.r.t the "Start Month" and "End Month" columns
frame_nan = frame_rem[(frame_rem["Start Month"].notna()) & 
                      (frame_rem["End Month"].notna())]

# Remove rows that have year > 2020 
#   and unnecessary disaster types
frame_fil = frame_nan[frame_nan["Start Year"] <= 2020]
frame_fil = frame_fil[(frame_fil["Disaster Type"] != "Impact") & 
                      (frame_fil["Disaster Type"] != "Infestation") &
                      (frame_fil["Disaster Type"] != "Animal incident")]
# print(frame_fil[frame_fil["Disaster Type"] == "Flood"].shape)
# print(frame_fil[abs((frame_fil["End Month"] - frame_fil["Start Month"]) + 1) >= 2]["Disaster Type"].shape[0])
# # print(frame_fil[abs((frame_fil["End Month"] - frame_fil["Start Month"]) + 1) >= 4]["Disaster Type"].mode())
# print(abs(frame_fil["End Month"] - frame_fil["Start Month"]+1).sum()/frame_fil.shape[0])
# print("fuck")
for dis in frame_fil["Disaster Type"]:
    make_csv(frame_fil, dis)

