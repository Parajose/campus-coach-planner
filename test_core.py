import copy
import unittest
from core import analyse,DEMO

class PlanningTests(unittest.TestCase):
    def test_capacity_cost_and_revenue(self):
        r=analyse(DEMO)['rows'][0]
        self.assertEqual(r['coaches'],2)
        self.assertEqual(r['empty_seats'],7)
        self.assertEqual(r['revenue_ghs'],14940)
        self.assertEqual(r['cost_ghs'],14080)
        self.assertEqual(r['surplus_ghs'],860)
        self.assertEqual(r['break_even_students'],79)

    def test_allocations_conserve_demand(self):
        r=analyse(DEMO)
        for route in DEMO['routes']:
            rows=[b for b in r['allocation'] if b['route']==route['route']]
            self.assertEqual(sum(b['assigned_students'] for b in rows),route['students'])
            self.assertTrue(all(b['assigned_students']+b['available_seats']==route['capacity'] for b in rows))

    def test_zero_demand_no_cost(self):
        d=copy.deepcopy(DEMO);d['routes'][0]['students']=0
        r=analyse(d)['rows'][0]
        self.assertEqual((r['coaches'],r['cost_ghs'],r['occupancy_pct']),(0,0,0))

    def test_exact_capacity_one_bus(self):
        d=copy.deepcopy(DEMO);d['routes'][0]['students']=45
        self.assertEqual(analyse(d)['rows'][0]['coaches'],1)

    def test_zero_fare_no_finite_break_even(self):
        d=copy.deepcopy(DEMO);d['routes'][0]['fare']=0
        self.assertIsNone(analyse(d)['rows'][0]['break_even_students'])

    def test_fractional_students_rejected(self):
        d=copy.deepcopy(DEMO);d['routes'][0]['students']=4.5
        with self.assertRaises(ValueError):analyse(d)

    def test_invalid_capacity_rejected(self):
        d=copy.deepcopy(DEMO);d['routes'][0]['capacity']=0
        with self.assertRaises(ValueError):analyse(d)

    def test_nonfinite_rejected(self):
        d=copy.deepcopy(DEMO);d['routes'][0]['fare']=float('inf')
        with self.assertRaises(ValueError):analyse(d)

if __name__=='__main__':unittest.main()
