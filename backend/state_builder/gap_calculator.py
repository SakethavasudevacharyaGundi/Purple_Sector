import pandas as pd

class GapCalculator:

    def calculate(self,lap_df:pd.DataFrame)->dict[str,dict]:
        lap_df=lap_df.sort_values("Position").copy()
        leader_time=lap_df.iloc[0]["Time"]
        result={}
        rows=lap_df.to_dict("records")
        for i,row in enumerate(rows):
            driver=str(row["Driver"])
            current_time=row["Time"]
            gap_to_leader=(current_time-leader_time).total_seconds() 
            gap_ahead=None
            if i>0:
                gap_ahead=(current_time-rows[i-1]["Time"]).total_seconds()    
            gap_behind=None
            if i<len(rows)-1:
                gap_behind=(rows[i+1]["Time"]-current_time).total_seconds()
            result[driver]={
                "gap_to_leader":round(gap_to_leader,3),
                "gap_ahead":round(gap_ahead,3) if gap_ahead is not None else None,
                "gap_behind":round(gap_behind,3) if gap_behind is not None else None,
            }  
        return result