from recommendation.constraints.stint_segment import StintSegment

class SegmentBuilder:
    def build(self,race_state,driver_state,candidate,)->list[StintSegment]:
        segments=[]
        current_lap=race_state.lap_number
        total_laps=race_state.total_laps
        pit_stops=candidate.pit_stops
        
        if not pit_stops:
            length=(driver_state.current_tyre_age)+ (total_laps-current_lap)
            segments.append(StintSegment(compound=driver_state.current_compound,length=length))
            return segments
        first_stop=pit_stops[0]
        first_length=(driver_state.current_tyre_age)+(first_stop.lap-current_lap)
        segments.append(StintSegment(compound=driver_state.current_compound,length=first_length))

        for i,stop in enumerate(pit_stops):
            if i==len(pit_stops)-1:
                length=(total_laps-stop.lap)+1
            else:
                next_stop=pit_stops[i+1]
                length=(next_stop.lap-stop.lap)
            segments.append(StintSegment(compound=stop.compound,length=length))
        
        return segments