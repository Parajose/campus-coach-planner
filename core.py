"""Route-level coach planning with transparent integer capacity and cost rules."""
import math
DEMO={"routes":[{"route":"Essikado → Accra","students":83,"capacity":45,"fare":180,"coach_cost":6200,"other_cost":400},{"route":"Essikado → Kumasi","students":57,"capacity":45,"fare":200,"coach_cost":6800,"other_cost":450}],"contingency_pct":10}

def number(value,name,whole=False):
    if isinstance(value,bool): raise ValueError(name+" must be numeric.")
    x=float(value)
    if not math.isfinite(x) or x<0 or x>10000000: raise ValueError(name+" must be finite and non-negative.")
    if whole and not x.is_integer(): raise ValueError(name+" must be a whole number.")
    return int(x) if whole else x

def analyse(data):
    routes=data["routes"]
    if not isinstance(routes,list) or not 1<=len(routes)<=100: raise ValueError("Provide 1–100 routes.")
    contingency=number(data.get("contingency_pct",0),"Contingency")
    if contingency>100: raise ValueError("Contingency must be between 0 and 100 percent.")
    rows=[]; allocation=[]; names=set()
    for route in routes:
        name=str(route["route"]).strip()
        if not name or name in names: raise ValueError("Route names must be non-empty and unique.")
        names.add(name)
        demand=number(route["students"],"Students",True); cap=number(route["capacity"],"Capacity",True)
        if cap<1: raise ValueError("Coach capacity must be at least one.")
        if demand>10000: raise ValueError("Demo planner supports up to 10,000 students per route.")
        fare=number(route["fare"],"Fare"); coach=number(route["coach_cost"],"Coach cost"); extra=number(route["other_cost"],"Other cost")
        buses=math.ceil(demand/cap); seats=buses*cap
        # Other cost applies once per active route, never to a route with zero demand.
        cost=(buses*coach+(extra if demand else 0))*(1+contingency/100)
        revenue=demand*fare
        break_even=math.ceil(cost/fare) if fare else (None if cost else 0)
        rows.append({"route":name,"students":demand,"coaches":buses,"seats":seats,"empty_seats":seats-demand,"occupancy_pct":round(100*demand/seats,2) if seats else 0,"revenue_ghs":round(revenue,2),"cost_ghs":round(cost,2),"surplus_ghs":round(revenue-cost,2),"break_even_students":break_even,"break_even_fits_capacity":break_even is not None and break_even<=seats})
        remaining=demand
        for i in range(buses):
            assigned=min(cap,remaining); remaining-=assigned
            allocation.append({"route":name,"coach":i+1,"assigned_students":assigned,"available_seats":cap-assigned})
    revenue=sum(r["revenue_ghs"] for r in rows); cost=sum(r["cost_ghs"] for r in rows)
    return {"summary":[["Students",str(sum(r["students"] for r in rows))],["Coaches needed",str(sum(r["coaches"] for r in rows))],["Estimated revenue","GHS "+format(revenue,",.2f")],["Estimated surplus","GHS "+format(revenue-cost,",.2f")]],"rows":rows,"allocation":allocation,"chart":{"labels":[r["route"] for r in rows],"values":[r["occupancy_pct"] for r in rows],"label":"Seat occupancy (%)","reference":None},"notes":["All demo fares and coach costs are fictional planning inputs, not operator quotes.","Coaches are calculated independently per route using ceiling(demand / capacity). This is not a timetable, payment system or confirmed booking service.","Cost = (coaches × coach cost + one active-route other cost) × (1 + contingency%). Break-even uses the planned fleet and full cost; changing demand may change fleet size."]}
